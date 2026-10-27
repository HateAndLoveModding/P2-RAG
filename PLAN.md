# P2 plan: RAG over 30 CFR and a KJV Bible corpus

## Context

P2 is due **Tue Oct 27, 11:59 pm** (README, SCHEDULE.md; Canvas is the record).
Decisions already made:

- Own corpus: the **KJV** (public domain in the US), from `https://raw.githubusercontent.com/javascripture/javascripture/gh-pages/bibles/KJV.json` (the ESV is Crossway's copyright and is not used).
- Books: Genesis, Exodus, Deuteronomy, Joshua, Judges, Ruth, 1-2 Samuel, 1-2 Kings, Esther, Job, Psalms, Proverbs, Ecclesiastes, Song of Solomon, Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel, plus the whole New Testament.
- One document per chapter, with the reference written inline on every verse (`Isaiah 5:10 And ten acres...`), so every chunk carries book, chapter and verse.
- `p2-raw/extract_kjv.py` stays committed: it is how the corpus was made (run it from inside `p2-raw/`; `KJV.json` and `kjv-chapters/` are gitignored).
- Relevance: parallel passages count as relevant (the Synoptic Gospels, Psalm 18 and 2 Samuel 22, Psalms 14 and 53, Isaiah 36-39 and 2 Kings 18-20, Jeremiah 52 and 2 Kings 25, Exodus 20 and Deuteronomy 5, Old Testament verses quoted in the New Testament).
- Core ablation: `bm25_ref`, the tokenizer kind (`5:10` as one token).
- Stretch (graded): **option 4, a second ablation**, as two committed variants: an embedding model and a chunking change.
- Extra stretch goal: **option 6** (hand vs claude queries), for no points, after the rest; if it runs past the submission, it goes on a branch (Step 8).
- `dense` stays fixed from Step 1 (bge-small, p2.toml's 300/50); the sweep in Step 5 never replaces it.

Rules for every step:
- The student directs, Claude builds one step at a time and narrates.
- The student writes the `hand` queries, all relevance judgments, the hypotheses, the tie rule, the prose of `EVAL.md`, and `DECISIONS.md`.
- Before any command with Claude calls: say the count, try 2, ask before the full run.
- Every step ends with `uv run p2 check`, a commit and a push, and CI green.

Order follows points and dependencies: stage 1 is 55 points and needs no corpus work.

## Status (Mon Oct 26, afternoon)

- Done: ESV clone removed; KJV ingested, 971 documents, 697,338 words, about 976,273 tokens (`p2 check` warns above 800,000 and fails above 1,000,000, so no more books fit); `p2 license` 971 ok, 0 flagged. The one ingest flag is `psalms_117`, "very short (37 words)", which is the real length of that psalm.
- Corpus, manifest, `INGEST.md`, `LICENSES.md` and `p2-raw/extract_kjv.py` committed in `7ac43a7` and pushed; Step 0 done, `p2-check` green on that push.
- Step 1, items 1-3 done (not committed yet): `dense`, `hybrid` and `rerank` written, and all four systems run on the 20 shared practice queries; `rrf_k = 10` added in `[hybrid]` of `p2.toml`. `uv run p2 check` has no FAIL; its TODOs start with the shared test runs.
- Practice scores (MRR@10): bm25 0.507, dense 0.562, hybrid 0.587, rerank 0.900. Rerank minus hybrid +0.313 [+0.160, +0.478], and rerank is also higher than bm25 and dense; the other pairs are not distinguishable. By class, rerank is 1.000 on identifier and mixed, 0.714 on paraphrase.
- Hybrid's k: 60 gave MRR@10 0.471 (below both inputs: with 2,484 documents, a document ranked moderately by both systems beat one ranked first by one of them), 20 gave 0.534, 10 gave 0.587; 10 minus 60 is +0.116 [+0.036, +0.217]. Chosen on the practice queries, so the test queries are the unbiased check.
- Rerank: Claude sees each candidate's best chunk under hybrid (not the first 600 characters, as in lab 13); about 12,000 input tokens and 5.6 s per call in the 2-query trial.
- Next: item 4, `uv run p2 run --all --with-claude`: 40 new rerank calls on the shared test queries (the 20 practice replies are cached; the own corpus is skipped until `eval/own/queries.tsv` has queries), about 580,000 input tokens (the practice run averaged 14,450 per call, 10,660 to 26,833).
- `uv run pytest`: 5 tests fail because they expect the unfilled template (`dense` still a stub, `EVAL.md` placeholders); they run only in the course's template CI, never in this repo's `p2-check`.

## Step 0 - Get CI green (about 20 min) - done

`uv run p2 check`, push, and check that the Actions run `p2-check` goes green.
This run only checks the corpus format, size and licenses; nothing is encoded until a `dense` run on the corpus is committed (Step 4).

## Step 1 - Stage 1 on the shared corpus (55 points, about 4-5 h) - items 1-3 done, item 4 next

1. **dense** in `p2/retrievers/dense.py`: a `ChunkScorer` subclass, as in `p2/retrievers/bm25.py`; vectors from `p2/embed.py` (`embed.load(embed.BGE)`, `embed.doc_vectors(model, texts, cfg.root)`, `model.encode([query])`), idea from `class/12-embeddings-and-retrieval/lab/starter/retrieve.py`. Write it so the model name and a query prefix are arguments, because the Step 5 variants and the sweep reuse the class with other models. Run `uv run p2 run --corpus shared --queries practice --system dense`.
2. **hybrid** in `p2/retrievers/hybrid.py`: RRF with k = 10, read from `rrf_k` in the `[hybrid]` table of `p2.toml` (k = 60 and 20 were tried first on the practice queries; 10 was best, so it was picked on the practice set and the test queries are the unbiased check; say so in EVAL.md section 1 and DECISIONS.md), of `retrievers.build("bm25", ...)` and `build("dense", ...)` over full rankings, ordered with `p2.runfile.order()`, plus `search_chunks` with the same fusion over chunks (idea: `rrf()` in `class/13-rag-pipeline/lab/starter/pipeline.py`).
3. **rerank** in `p2/retrievers/rerank.py`: hybrid's top 20 to `p2.claude.call(...)` with the lab 13 schema plus `minimum: 1, maximum: 20`, `NEEDS_CLAUDE = True`, plus `search_chunks`. Trial: 2 lines in `.cache/two.tsv`, `uv run p2 run --corpus shared --queries .cache/two.tsv --system rerank`.
4. **Run everything**: `uv run p2 run --all --with-claude` (60 rerank calls on shared, 20 of them already cached from the practice run, so 40 new; ask first), then `uv run p2 score`. Commit `runs/`, `traces/`, `results/`, `EVAL.md`.
5. **Answers**: the student picks the system (hybrid 12 calls, rerank 24). Trial `--only a01,a09`, then all 12; `uv run p2 verify answers/shared/<label>.json`.
6. `uv run p2 check`, commit, push, CI green; the first CI run with `dense` encodes the shared corpus, about 3-7 min.

While the 60 rerank calls and the first encode run, the student writes the 10 `hand` queries for Step 3.

EVAL.md for this step (the student writes):
- Section 1, "What you built": `dense`, `hybrid`, `rerank` in one or two sentences each, with the embedder choice and why.
- Section 1, "What the intervals let you claim": the practice-query intervals.
- Section 2: which system answered and why, and the audit of 3 answers read by hand.

## Step 2 - The KJV corpus (10 points)

Ingested, license-clean and committed (see Status).

EVAL.md section 3, "The corpus" (the student writes): what it is, the source URL, 971 documents and the size in MB, the license basis (US public domain, one of the brief's allowed sources; note the Crown patent in the UK, the way the brief asks about the USGS reservation), and the document least sure about (`psalms_117`, short but real).

## Step 3 - Gold set (15 points, about 2-3 h, mostly the student)

- `eval/own/queries.tsv`: at least 30 queries, at least 10 `hand` (written by the student), the rest drafted by Claude as `claude`. Suggested classes: `reference` (Isaiah 5:10), `quote` (a remembered phrase), `topic` (paraphrase, different words).
- Claude finds candidates from bm25, dense, hybrid and grep; the student reads and judges into `eval/own/qrels.txt`, including the parallel passages.
- Commit.

EVAL.md section 3, "The gold set" (the student writes): the counts by origin and class, the relevance rule in two or three sentences (with the parallel-passage decision), how candidates were found, and that every document was read before it was labeled.

## Step 4 - Four systems on the own corpus (10 points, about 30 min)

Trial first: 2 own queries in `.cache/two-own.tsv`, `uv run p2 run --corpus own --queries .cache/two-own.tsv --system rerank`, and look at the input tokens per call (KJV chapters are longer than CFR sections).
Then `uv run p2 run --all --with-claude` (one rerank call per own query, 30 or more, ask first), `uv run p2 score`, commit, push.
This is the push whose CI run encodes the own corpus with bge-small for the first time, about 6-14 min.

EVAL.md section 4 (the student writes): what the own-corpus intervals let you claim.

## Step 5 - Core ablation, stretch 4, and the embedding sweep (10 + 25 points)

### 5a. Hypotheses first (the student writes, then commit and push)

- Section 5: the core hypothesis for `bm25_ref` against `bm25`, one sentence with a direction.
- Section 8: the stretch-4 hypotheses, one per variant, each naming its variant: which model the model variant uses (against `dense`), and which chunk size and overlap the chunking variant uses (against the model variant).
- The tie rule for the sweep, for example "if the interval includes zero, keep the smaller or faster setting".

All of this is committed before any variant or sweep runs, so the history shows it came first.
The committed variants are the ones the hypotheses name, whether or not they win.

### 5b. Core ablation: `bm25_ref` (tokenizer)

- `p2/retrievers/bm25_ref.py`, `BASE = "bm25"`: BM25 with a tokenizer that keeps `5:10` as one token (no `5` and `10` parts) and treats everything else as `codes` does.
- `BM25.__init__` and `score_chunks` call `textproc.tokens(text, self.tokenizer)`, which knows only `codes` and `lab`, so the subclass overrides both with its own tokenizer; `bm25.py` and `textproc.py` stay untouched.
- Side effect to watch: a chapter-only query such as "Isaiah 5" no longer matches `5` in the verse labels.
- `uv run p2 run --corpus own --system bm25_ref --ablation`, `uv run p2 score`, commit, push.

### 5c. Stretch 4: the two committed variants

- Model variant: `p2/retrievers/dense_<model>.py`, `BASE = "dense"`, the model named in 5a at dense's 300/50, so the one change is the model.
- Chunking variant: `p2/retrievers/dense_<model>_c<size>o<overlap>.py`, `BASE = "dense_<model>"`, the same model with the size and overlap named in 5a.
- Each: `uv run p2 run --corpus own --system <name> --ablation`, `uv run p2 score`, commit, push.
- CI encodes the own corpus once per committed variant. bge-large and Qwen3 can take longer than CI's 45-minute job; the cache keeps the progress, so CI then goes green only after one or more further runs. The timing in 5d tells which models are safe before 5a names one.

### 5d. The embedding sweep (exploration, no Claude calls)

- A script outside `p2/`, `scripts/sweep.py`, never a file in `p2/retrievers/`, because CI re-runs every system there.
- It builds the `dense` class with each setting on the own corpus, scores the own gold set (MRR@10, nDCG@10, recall@10, paired intervals against the stage's reference), and writes `sweep/results.tsv`, which is committed with the script.
- Timing first: encode about 200 chunks with each model and extrapolate to the whole corpus, before the full encodes and before 5a names a model.
- Stage A, the model, at 256 words and overlap 45: `BAAI/bge-small-en-v1.5`, `BAAI/bge-base-en-v1.5`, `BAAI/bge-large-en-v1.5`, `Qwen/Qwen3-Embedding-0.6B` (needs an instruction line before each query), `minishlab/potion-retrieval-32M`. 5 encodes.
- Stage B, the chunk size, with the stage A winner at overlap 45: 128, 256 (reused), 384. 2 new encodes. The bge models read only the first 512 tokens, about 380 words of KJV with verse labels, so 384 is partly truncated for them.
- Stage C, the overlap, with the stage B winner: 15, 30, 45, 60. 3 new encodes.
- Each stage picks its winner by the tie rule from 5a.
- Reported as exploration: the best of about 10 settings on the same 30 or more queries looks better than it is.

EVAL.md (the student writes):
- Section 5: the core ablation's change, hypothesis, result and claim against the interval, and the two queries it helped most and the two it hurt most.
- Section 8, "Your stretch": the five things for option 4 (name; what was done and the files; the `own-ablation` and `own-ablation-queries` tables in section 5; what the intervals let you claim; what to do next), with the two helped and two hurt queries read for each variant.
- Section 8: the sweep, its table from `sweep/results.tsv`, and the best combination as the "what to do next".

## Step 6 - Analysis and writing (25 points, the student, about 2-3 h)

Claude pulls the evidence and explains numbers; the student writes:
- Section 6: the failure analysis, at least 5 queries where the best own-corpus system fell short, sorted by cause, with what to try and what evidence would show it worked.
- Section 7: the cross-corpus comparison, whether the winner changed and why, with tested explanations kept apart from guesses.
- `DECISIONS.md`: the 5 prompts, and the notes at the bottom of the file cleaned up.

## Step 7 - Submit

`uv run p2 check --final`, commit, push, CI green, then the student records the 5-10 minute video and posts the repo URL and video in the Canvas Project 2 discussion.

## Step 8 - Option 6, the extra stretch goal (no points)

- 10 more `hand` queries (20 in all) and at least 20 `claude` ones, judged by the same relevance rule.
- The prediction in `EVAL.md` section 8, committed before scoring: is bm25's lead over dense larger on the claude queries, and by about how much?
- `uv run p2 run --all --with-claude` (rerank calls only for the new queries; the rest are cached), `uv run p2 score`; the `own-origins` table fills in section 4.
- More queries change every own-corpus number, including sections 4 to 7. If this runs past the submission, do it on a branch (`option-6`) and leave `main` as submitted, so no commit on `main` is dated after the deadline.

## Claude-call budget

About 60 (shared rerank) + 12-24 (answers) + 30-40 (own rerank) = 100-125 `claude -p` calls, roughly 1.3-1.5 million input tokens on the student's plan; the Step 4 trial gives the real per-call number for the own corpus. Option 6 adds one rerank call per new query. The ablations and the sweep make none.

## Verification

- `uv run pytest` and `uv run p2 check` after every step; `uv run p2 check --final` at the end.
- GitHub Actions `p2-check` green after each push.
- `p2 run` prints MRR@10 on the practice queries for each new system as a sanity check (bm25 finds none of the 7 paraphrase queries; dense should).
- `bm25_ref` on the query `Isaiah 5:10` ranks `isaiah_05` first, and its top chunk holds verse 5:10.
