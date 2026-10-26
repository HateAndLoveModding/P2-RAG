# P2 plan: RAG over 30 CFR and a KJV Bible corpus

## Context

P2 is due **Tue Oct 27, 11:59 pm** (README, SCHEDULE.md; Canvas is the record).
Decisions already made:

- Own corpus: the **KJV** (public domain in the US), from `https://raw.githubusercontent.com/javascripture/javascripture/gh-pages/bibles/KJV.json` (the ESV is Crossway's copyright and is not used).
- Books: Genesis, Exodus, Deuteronomy, Joshua, Judges, Ruth, 1-2 Samuel, 1-2 Kings, Esther, Job, Psalms, Proverbs, Ecclesiastes, Song of Solomon, Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel, plus the whole New Testament.
- One document per chapter, with the reference written inline on every verse (`Isaiah 5:10 And ten acres...`), so every chunk carries book, chapter and verse.
- Stretch: **option 4, a second ablation**; option 6 only if time is left.

Rule for every step: the student directs, Claude builds one step at a time and narrates.
The student writes the `hand` queries, all relevance judgments, the hypotheses, the prose of `EVAL.md`, and `DECISIONS.md`.
Before any command with Claude calls: say the count, try 2, ask before the full run.

Order follows points and dependencies: stage 1 is 55 points and needs no corpus work.

## Status (Mon Oct 26)

- Done: ESV clone removed; KJV ingested, 971 documents, 701,789 words, about 982,504 tokens; `p2 license` 971 ok, 0 flagged; `p2 check` 11 passed, 0 failed. The one ingest flag is `psalms_117`, "very short (38 words)", which is the real length of that psalm.
- Not committed yet.

## Step 0 - Get CI green (about 20 min)

`uv sync`, `uv run p2 check`, commit, push, and check that the Actions run `p2-check` goes green.

## Step 1 - Stage 1 on the shared corpus (55 points, about 4-5 h)

1. **dense** in `p2/retrievers/dense.py`: a `ChunkScorer` subclass, as in `p2/retrievers/bm25.py`; vectors from `p2/embed.py` (`embed.load(embed.BGE)`, `embed.doc_vectors(model, texts, cfg.root)`, `model.encode([query])`), idea from `class/12-embeddings-and-retrieval/lab/starter/retrieve.py`. Run `uv run p2 run --corpus shared --queries practice --system dense`.
2. **hybrid** in `p2/retrievers/hybrid.py`: RRF with k = 60 of `retrievers.build("bm25", ...)` and `build("dense", ...)` over full rankings, ordered with `p2.runfile.order()`, plus `search_chunks` with the same fusion over chunks (idea: `rrf()` in `class/13-rag-pipeline/lab/starter/pipeline.py`).
3. **rerank** in `p2/retrievers/rerank.py`: hybrid's top 20 to `p2.claude.call(...)` with the lab 13 schema plus `minimum: 1, maximum: 20`, `NEEDS_CLAUDE = True`, plus `search_chunks`. Trial: 2 lines in `.cache/two.tsv`, `uv run p2 run --corpus shared --queries .cache/two.tsv --system rerank`.
4. **Run everything**: `uv run p2 run --all --with-claude` (60 rerank calls on shared, ask first), then `uv run p2 score`. Commit `runs/`, `traces/`, `results/`, `EVAL.md`. The student writes `EVAL.md` section 1.
5. **Answers**: the student picks the system (hybrid 12 calls, rerank 24). Trial `--only a01,a09`, then all 12; `uv run p2 verify answers/shared/<label>.json`; the student reads 3 answers and writes about them.
6. `uv run p2 check`, commit, push, CI green.

## Step 2 - The KJV corpus (10 points)

Ingested and license-clean (see Status). Left: settle the open corpus questions, commit `corpora/own/`, `LICENSES.md`, and push; the first CI encode takes up to about 15 min.

## Step 3 - Gold set (15 points, about 2-3 h, mostly the student)

- `eval/own/queries.tsv`: at least 30 queries, at least 10 `hand` (written by the student; 20 if option 6 stays possible), the rest drafted by Claude as `claude`. Suggested classes: `reference` (Isaiah 5:10), `quote` (a remembered phrase), `topic` (paraphrase, different words).
- Claude finds candidates from bm25, dense, hybrid and grep; the student reads and judges into `eval/own/qrels.txt`, and writes the relevance rule in `EVAL.md`.

## Step 4 - Four systems on the own corpus (10 points, about 30 min)

`uv run p2 run --all --with-claude` (one rerank call per own query, 30 or more, ask first), `uv run p2 score`, commit.

## Step 5 - Core ablation and stretch 4 (10 + 25 points, about 1.5 h)

Two variants of different kinds, each its own file in `p2/retrievers/` with `BASE = ...`:
- Tokenizer: `bm25_ref.py`, a BM25 subclass that keeps `5:10` whole (the default `codes` tokenizer splits it into `5` and `10`), `BASE = "bm25"`.
- Chunking: `dense_c150.py` (or similar) built with `cfg.replace(chunk_words=150, chunk_overlap=25)`, `BASE = "dense"`.

For each: the student writes the hypothesis in `EVAL.md` (the stretch one in section 8) and it is **committed before the run**; then `uv run p2 run --corpus own --system <name> --ablation`, `uv run p2 score`, and the student reads the helped and hurt queries and writes the claim against the interval.

## Step 6 - Analysis and writing (25 points, the student, about 2-3 h)

Failure analysis (at least 5 queries, sorted by cause, `EVAL.md` section 6), cross-corpus comparison, `DECISIONS.md` (5 prompts), stretch write-up (section 8, the five items). Claude pulls the evidence and explains numbers; the student writes.

## Step 7 - Submit

`uv run p2 check --final`, commit, push, CI green, then the student records the 5-10 minute video and posts the repo URL and video in the Canvas Project 2 discussion.

## Claude-call budget

About 60 (shared rerank) + 12-24 (answers) + 30-40 (own rerank) = 100-125 `claude -p` calls, roughly 1.3-1.5 million input tokens on the student's plan. Stretch 4 makes none.

## Verification

- `uv run pytest` and `uv run p2 check` after every step; `uv run p2 check --final` at the end.
- GitHub Actions `p2-check` green after each push.
- `p2 run` prints MRR@10 on the practice queries for each new system as a sanity check (bm25 finds none of the 7 paraphrase queries; dense should).
