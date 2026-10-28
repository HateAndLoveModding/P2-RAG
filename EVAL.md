# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

dense embeds 300-word chunks with 50 words overlap using the bge-small-en-v1.5 model
hybrid fuses bm25 and dense using a k of 10 and 1 / (k + bm25_rank) + 1 / (k + dense_rank)
rerank asks claude to rerank hybrid's results based on what it thinks is most relevant

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.817 | 0.587 | 0.588 |
| rerank | 0.833 | 0.900 | 0.850 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 1.000 | 0.548 | 0.917 |
| hybrid | MRR@10 | 0.559 | 0.440 | 0.792 |
| hybrid | nDCG@10 | 0.599 | 0.413 | 0.779 |
| rerank | Recall@10 | 1.000 | 0.595 | 0.917 |
| rerank | MRR@10 | 1.000 | 0.714 | 1.000 |
| rerank | nDCG@10 | 1.000 | 0.626 | 0.936 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.192 | [+0.050, +0.358] | 0.223 | hybrid higher |
| hybrid minus bm25 | MRR@10 | +0.080 | [-0.099, +0.267] | 0.265 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | +0.070 | [-0.084, +0.233] | 0.229 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.258 | [+0.083, +0.450] | 0.270 | hybrid higher |
| hybrid minus dense | MRR@10 | +0.025 | [-0.137, +0.182] | 0.231 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.108 | [-0.028, +0.242] | 0.193 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.208 | [+0.050, +0.383] | 0.242 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.393 | [+0.200, +0.595] | 0.287 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.331 | [+0.167, +0.506] | 0.248 | rerank higher |
| rerank minus dense | Recall@10 | +0.275 | [+0.100, +0.450] | 0.259 | rerank higher |
| rerank minus dense | MRR@10 | +0.338 | [+0.150, +0.533] | 0.273 | rerank higher |
| rerank minus dense | nDCG@10 | +0.370 | [+0.205, +0.544] | 0.246 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.017 | [+0.000, +0.050] | 0.047 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.313 | [+0.160, +0.478] | 0.232 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.262 | [+0.156, +0.376] | 0.158 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

Rerank is distinguishably higher in MRR and nDCG and hybrid is only better in recall. Dense and bm25 are not distinguishable. The minimum detectable differences go from 0.05 to .4 and gaps smaller than about 0.25 do not show up with only 20 queries. My numbers support the claim from lecture 12.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 13 of 13 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

I used system rerank because the MRR evaluation metric was significantly higher which is important especially when using Claude because the first documents returned are viewed as more important and reduces the likelyhood of hallucination. I did not change anything `prompts/answer.txt` because I felt like the prompt was direct and specific and did not need any updating. `uv run p2 verify` passed with flying colors so I am only checking whether the document supports the claim that Claude made. 

a01: FAIL
I said that a01 failed because I think Claude misinterpreted the document. The document says, "The operator shall immediately contact MSHA at once without delay." The first line of Claude's response is "Within 15 minutes." The second sentence is a very close copy of the actual document but the wording changed a little bit and I think it changes the meaning a little bit. I Interpreted "The operator shall immediately contact MSHA at once without delay and within 15 minutes at the toll-free number" to mean that the operator must contact MSHA immediately, without delay, but they must also contact the toll-free number within 15 minutes. I am thinking that there may be some sort of local MSHA which the operator must contact immediately but there is also a remote MSHA which the operator must contact via phone within 15 minutes (don't quote me on that).

a04: PASS
The document was very clear and Claude interpreted it correctly that.

a08: PASS
Claude correctly recognized that breatable air must sustain each person for 96 hours. 

Claude does well if there is a specific direct answer but not if there is an ambiguous answer. Claude may not recognize an ambiguous answer though which seems like the main problem. Claude ideally should ask for clarification for ambiguous texts. 

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

My corpus is the King James Verion of the Bible. I sourced a JSON file of it from GitHub (https://github.com/javascripture/javascripture/tree/gh-pages). It has 971 documents (one for each chapter) totaling 3.9MB. The KJV Bible has a public domain license. I could not fit the entire KJV Bible though because it is more than 1 million tokens. I decided to keep the entire new testament and just cut a few books from the old testament. So, the corpus has Genesis, Exodus, Deuteronomy, Joshua through 2 Kings, Esther, Job through Daniel, and the whole New Testament. The KJV was published in 1611 and so the US copyright has run out and so it falls in the US public-domain books category of allowed sources. Though in the UK, it is still under the Crown patent. I was a little unsure about Psalms 117 because there was a message saying that it was very short, but I kept it as I originally had it because that is actually how should the Psalm is. Originally I was going to use the ESV Bible because that is my go to translation but Crossway holds a copyright for it.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

I wrote 10 queries by hand based on things I might want to look up. I had claude write 20 queries. I used topic, reference, and quote classes. I felt like those are the classes of queries I would actually use in my day to day life. For example, I often was to look up a Bible verse given the reference. So I want to just be able to input the reference and get the Bible verse out. The topic class is used for more general things like finding out where in the Bible a story or passages on a specific topic are. The quote query is used for finding where a specific verse is found in the Bible based on a rough paraphrase of the verse from memory. 

Relevant for a reference passage means that it returns the chapter with the exact verse referenced. For example, "What does Daniel 2:28 say?" should return whatever chapter has Daniel 2:28 in it. The verse does not have to be specified but the RAG should still return the exact verse alluded to. For example, "The Bible says that there is no God in Psalm 14." should return whatever chapter has Psalm 14:1 in it. The chapter does not even have to be specified but the RAG should still return the exact verse alluded to. For example, "Where exactly in Job does it talk about why he can't gaze at a virgin?" should return Job 31:1.

Relevant for a quote passage also means that the RAG should return the chapter with the exact verse alluded to. The difference between a "reference" and a "quote" query is that a quote query does not give any book or chapter "hints" to the RAG.

Relevant for a topic passage means that the RAG should return a wider set of passages related to some topic. For example, "Baptism" should return passages all throughout the Bible about people getting baptized either physically or spiritually. Possible passages include Acts 2, Acts 8, John 1, and 1 Peter 3. 

I already had an idea of what the correct passage should be for my own queries that I wrote and some of the ones that Claude wrote. I also did a few Google searches if I didn't know where the correct passage was and then I read that specific document to make sure that I thought the document answered the query. I at least skimmed each document that I deemed relevant. The labels are binary. 

h02, h04, and c09 have two relevant chapters defined because they are nearly identical passages or phrases in the Bible. c17 has two relevant chapters because there is a new testament reference to the passage in the old testament. The story in Esther is partially split across two chapters which is why both are relevant. I did not look at the relevant passages that claude defined for the test queries that Claude wrote. I wrote them first and then had Claude evaluate the set and Claude recognized a typo, a reference to a book not in the corpus, the continuation of the story in the next chapter, and a very similar passage later in the book. I read each chapter before changing the set. 

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.808 | 0.658 | 0.688 |
| dense | 0.650 | 0.488 | 0.511 |
| hybrid | 0.825 | 0.575 | 0.635 |
| rerank | 0.858 | 0.878 | 0.860 |
| ablation/dense_bge_base | 0.617 | 0.558 | 0.563 |
| ablation/dense_w100 | 0.650 | 0.507 | 0.528 |
| ablation/dense_w150 | 0.683 | 0.484 | 0.522 |
| ablation/dense_w200 | 0.642 | 0.466 | 0.491 |
| ablation/dense_w250 | 0.586 | 0.499 | 0.489 |
| ablation/dense_w350 | 0.650 | 0.509 | 0.528 |
| ablation/rerank_dense_w150 | 0.761 | 0.778 | 0.761 |

30 judged queries; nDCG uses binary labels; a random ranking of the 971 documents would get recall@10 near 0.010.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | reference (n=10) | quote (n=10) | topic (n=10) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 0.900 | 1.000 | 0.525 |
| bm25 | MRR@10 | 0.800 | 0.912 | 0.262 |
| bm25 | nDCG@10 | 0.811 | 0.932 | 0.321 |
| dense | Recall@10 | 1.000 | 0.400 | 0.550 |
| dense | MRR@10 | 0.783 | 0.320 | 0.361 |
| dense | nDCG@10 | 0.821 | 0.339 | 0.374 |
| hybrid | Recall@10 | 1.000 | 0.900 | 0.575 |
| hybrid | MRR@10 | 0.812 | 0.543 | 0.370 |
| hybrid | nDCG@10 | 0.850 | 0.640 | 0.416 |
| rerank | Recall@10 | 1.000 | 1.000 | 0.575 |
| rerank | MRR@10 | 1.000 | 1.000 | 0.633 |
| rerank | nDCG@10 | 1.000 | 1.000 | 0.581 |
| ablation/dense_bge_base | Recall@10 | 1.000 | 0.350 | 0.500 |
| ablation/dense_bge_base | MRR@10 | 0.883 | 0.325 | 0.464 |
| ablation/dense_bge_base | nDCG@10 | 0.913 | 0.326 | 0.449 |
| ablation/dense_w100 | Recall@10 | 0.950 | 0.500 | 0.500 |
| ablation/dense_w100 | MRR@10 | 0.775 | 0.500 | 0.245 |
| ablation/dense_w100 | nDCG@10 | 0.794 | 0.500 | 0.289 |
| ablation/dense_w150 | Recall@10 | 0.900 | 0.600 | 0.550 |
| ablation/dense_w150 | MRR@10 | 0.700 | 0.453 | 0.298 |
| ablation/dense_w150 | nDCG@10 | 0.734 | 0.481 | 0.351 |
| ablation/dense_w200 | Recall@10 | 1.000 | 0.550 | 0.375 |
| ablation/dense_w200 | MRR@10 | 0.761 | 0.460 | 0.176 |
| ablation/dense_w200 | nDCG@10 | 0.801 | 0.453 | 0.217 |
| ablation/dense_w250 | Recall@10 | 0.900 | 0.450 | 0.408 |
| ablation/dense_w250 | MRR@10 | 0.725 | 0.364 | 0.408 |
| ablation/dense_w250 | nDCG@10 | 0.749 | 0.384 | 0.334 |
| ablation/dense_w350 | Recall@10 | 0.900 | 0.450 | 0.600 |
| ablation/dense_w350 | MRR@10 | 0.770 | 0.500 | 0.258 |
| ablation/dense_w350 | nDCG@10 | 0.782 | 0.461 | 0.339 |
| ablation/rerank_dense_w150 | Recall@10 | 1.000 | 0.700 | 0.583 |
| ablation/rerank_dense_w150 | MRR@10 | 1.000 | 0.700 | 0.633 |
| ablation/rerank_dense_w150 | nDCG@10 | 1.000 | 0.700 | 0.582 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=20) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.525 | 0.950 | -0.425 | [-0.725, -0.100] | claude higher |
| bm25 | MRR@10 | 0.432 | 0.771 | -0.339 | [-0.658, +0.001] | not distinguishable |
| bm25 | nDCG@10 | 0.432 | 0.816 | -0.384 | [-0.682, -0.069] | claude higher |
| dense | Recall@10 | 0.400 | 0.775 | -0.375 | [-0.700, -0.025] | claude higher |
| dense | MRR@10 | 0.300 | 0.582 | -0.282 | [-0.572, +0.033] | not distinguishable |
| dense | nDCG@10 | 0.308 | 0.613 | -0.305 | [-0.583, -0.006] | claude higher |
| hybrid | Recall@10 | 0.525 | 0.975 | -0.450 | [-0.750, -0.150] | claude higher |
| hybrid | MRR@10 | 0.349 | 0.688 | -0.339 | [-0.624, -0.023] | claude higher |
| hybrid | nDCG@10 | 0.382 | 0.762 | -0.381 | [-0.643, -0.093] | claude higher |
| rerank | Recall@10 | 0.625 | 0.975 | -0.350 | [-0.650, -0.075] | claude higher |
| rerank | MRR@10 | 0.633 | 1.000 | -0.367 | [-0.667, -0.100] | claude higher |
| rerank | nDCG@10 | 0.620 | 0.981 | -0.361 | [-0.661, -0.081] | claude higher |
| ablation/dense_bge_base | Recall@10 | 0.450 | 0.700 | -0.250 | [-0.576, +0.100] | not distinguishable |
| ablation/dense_bge_base | MRR@10 | 0.414 | 0.629 | -0.215 | [-0.557, +0.148] | not distinguishable |
| ablation/dense_bge_base | nDCG@10 | 0.425 | 0.632 | -0.207 | [-0.544, +0.149] | not distinguishable |
| ablation/dense_w100 | Recall@10 | 0.500 | 0.725 | -0.225 | [-0.550, +0.125] | not distinguishable |
| ablation/dense_w100 | MRR@10 | 0.425 | 0.547 | -0.122 | [-0.425, +0.203] | not distinguishable |
| ablation/dense_w100 | nDCG@10 | 0.405 | 0.589 | -0.184 | [-0.466, +0.117] | not distinguishable |
| ablation/dense_w150 | Recall@10 | 0.500 | 0.775 | -0.275 | [-0.600, +0.050] | not distinguishable |
| ablation/dense_w150 | MRR@10 | 0.403 | 0.524 | -0.120 | [-0.415, +0.195] | not distinguishable |
| ablation/dense_w150 | nDCG@10 | 0.399 | 0.583 | -0.184 | [-0.469, +0.118] | not distinguishable |
| ablation/dense_w200 | Recall@10 | 0.425 | 0.750 | -0.325 | [-0.650, +0.025] | not distinguishable |
| ablation/dense_w200 | MRR@10 | 0.322 | 0.537 | -0.215 | [-0.531, +0.122] | not distinguishable |
| ablation/dense_w200 | nDCG@10 | 0.324 | 0.574 | -0.250 | [-0.540, +0.064] | not distinguishable |
| ablation/dense_w250 | Recall@10 | 0.358 | 0.700 | -0.342 | [-0.650, +0.000] | not distinguishable |
| ablation/dense_w250 | MRR@10 | 0.425 | 0.536 | -0.111 | [-0.445, +0.239] | not distinguishable |
| ablation/dense_w250 | nDCG@10 | 0.339 | 0.564 | -0.225 | [-0.516, +0.092] | not distinguishable |
| ablation/dense_w350 | Recall@10 | 0.350 | 0.800 | -0.450 | [-0.750, -0.125] | claude higher |
| ablation/dense_w350 | MRR@10 | 0.320 | 0.604 | -0.284 | [-0.602, +0.062] | not distinguishable |
| ablation/dense_w350 | nDCG@10 | 0.307 | 0.638 | -0.331 | [-0.622, -0.011] | claude higher |
| ablation/rerank_dense_w150 | Recall@10 | 0.683 | 0.800 | -0.117 | [-0.417, +0.183] | not distinguishable |
| ablation/rerank_dense_w150 | MRR@10 | 0.733 | 0.800 | -0.067 | [-0.383, +0.233] | not distinguishable |
| ablation/rerank_dense_w150 | nDCG@10 | 0.682 | 0.800 | -0.118 | [-0.422, +0.185] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | +0.175 | +0.125 | +0.050 | [-0.325, +0.450] | not distinguishable |
| MRR@10 | +0.189 | +0.133 | +0.056 | [-0.285, +0.399] | not distinguishable |
| nDCG@10 | +0.203 | +0.124 | +0.079 | [-0.246, +0.406] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.56 (10 queries), claude 0.85 (20 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 20 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.158 | [-0.325, +0.000] | 0.243 | not distinguishable |
| dense minus bm25 | MRR@10 | -0.170 | [-0.360, +0.013] | 0.272 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.177 | [-0.346, -0.014] | 0.243 | bm25 higher |
| hybrid minus bm25 | Recall@10 | +0.017 | [-0.083, +0.117] | 0.142 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.083 | [-0.207, +0.030] | 0.172 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.052 | [-0.148, +0.038] | 0.136 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.175 | [+0.058, +0.317] | 0.193 | hybrid higher |
| hybrid minus dense | MRR@10 | +0.087 | [-0.021, +0.197] | 0.159 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.124 | [+0.037, +0.219] | 0.135 | hybrid higher |
| rerank minus bm25 | Recall@10 | +0.050 | [+0.000, +0.133] | 0.103 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.220 | [+0.094, +0.354] | 0.191 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.172 | [+0.075, +0.280] | 0.151 | rerank higher |
| rerank minus dense | Recall@10 | +0.208 | [+0.075, +0.358] | 0.207 | rerank higher |
| rerank minus dense | MRR@10 | +0.390 | [+0.249, +0.537] | 0.211 | rerank higher |
| rerank minus dense | nDCG@10 | +0.349 | [+0.217, +0.489] | 0.199 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.033 | [+0.000, +0.100] | 0.093 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.303 | [+0.177, +0.432] | 0.184 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.225 | [+0.130, +0.325] | 0.143 | rerank higher |
| ablation/dense_bge_base minus bm25 | Recall@10 | -0.192 | [-0.367, -0.017] | 0.259 | bm25 higher |
| ablation/dense_bge_base minus bm25 | MRR@10 | -0.101 | [-0.295, +0.093] | 0.283 | not distinguishable |
| ablation/dense_bge_base minus bm25 | nDCG@10 | -0.125 | [-0.306, +0.054] | 0.263 | not distinguishable |
| ablation/dense_bge_base minus dense | Recall@10 | -0.033 | [-0.150, +0.050] | 0.149 | not distinguishable |
| ablation/dense_bge_base minus dense | MRR@10 | +0.069 | [-0.010, +0.159] | 0.126 | not distinguishable |
| ablation/dense_bge_base minus dense | nDCG@10 | +0.052 | [-0.024, +0.129] | 0.114 | not distinguishable |
| ablation/dense_bge_base minus hybrid | Recall@10 | -0.208 | [-0.358, -0.075] | 0.213 | hybrid higher |
| ablation/dense_bge_base minus hybrid | MRR@10 | -0.018 | [-0.133, +0.101] | 0.172 | not distinguishable |
| ablation/dense_bge_base minus hybrid | nDCG@10 | -0.072 | [-0.186, +0.036] | 0.163 | not distinguishable |
| ablation/dense_bge_base minus rerank | Recall@10 | -0.242 | [-0.400, -0.092] | 0.224 | rerank higher |
| ablation/dense_bge_base minus rerank | MRR@10 | -0.320 | [-0.476, -0.170] | 0.222 | rerank higher |
| ablation/dense_bge_base minus rerank | nDCG@10 | -0.297 | [-0.454, -0.149] | 0.221 | rerank higher |
| ablation/dense_w100 minus bm25 | Recall@10 | -0.158 | [-0.317, -0.008] | 0.229 | bm25 higher |
| ablation/dense_w100 minus bm25 | MRR@10 | -0.152 | [-0.294, -0.027] | 0.197 | bm25 higher |
| ablation/dense_w100 minus bm25 | nDCG@10 | -0.160 | [-0.299, -0.036] | 0.193 | bm25 higher |
| ablation/dense_w100 minus dense | Recall@10 | +0.000 | [-0.083, +0.100] | 0.134 | not distinguishable |
| ablation/dense_w100 minus dense | MRR@10 | +0.019 | [-0.108, +0.147] | 0.187 | not distinguishable |
| ablation/dense_w100 minus dense | nDCG@10 | +0.016 | [-0.083, +0.124] | 0.152 | not distinguishable |
| ablation/dense_w100 minus hybrid | Recall@10 | -0.175 | [-0.308, -0.050] | 0.187 | hybrid higher |
| ablation/dense_w100 minus hybrid | MRR@10 | -0.068 | [-0.173, +0.038] | 0.153 | not distinguishable |
| ablation/dense_w100 minus hybrid | nDCG@10 | -0.108 | [-0.202, -0.014] | 0.137 | hybrid higher |
| ablation/dense_w100 minus rerank | Recall@10 | -0.208 | [-0.350, -0.075] | 0.202 | rerank higher |
| ablation/dense_w100 minus rerank | MRR@10 | -0.371 | [-0.528, -0.222] | 0.223 | rerank higher |
| ablation/dense_w100 minus rerank | nDCG@10 | -0.333 | [-0.476, -0.199] | 0.202 | rerank higher |
| ablation/dense_w100 minus ablation/dense_bge_base | Recall@10 | +0.033 | [-0.067, +0.150] | 0.164 | not distinguishable |
| ablation/dense_w100 minus ablation/dense_bge_base | MRR@10 | -0.051 | [-0.207, +0.106] | 0.232 | not distinguishable |
| ablation/dense_w100 minus ablation/dense_bge_base | nDCG@10 | -0.035 | [-0.164, +0.102] | 0.195 | not distinguishable |
| ablation/dense_w150 minus bm25 | Recall@10 | -0.125 | [-0.250, -0.025] | 0.167 | bm25 higher |
| ablation/dense_w150 minus bm25 | MRR@10 | -0.175 | [-0.324, -0.034] | 0.212 | bm25 higher |
| ablation/dense_w150 minus bm25 | nDCG@10 | -0.166 | [-0.307, -0.038] | 0.197 | bm25 higher |
| ablation/dense_w150 minus dense | Recall@10 | +0.033 | [-0.083, +0.150] | 0.164 | not distinguishable |
| ablation/dense_w150 minus dense | MRR@10 | -0.004 | [-0.137, +0.133] | 0.194 | not distinguishable |
| ablation/dense_w150 minus dense | nDCG@10 | +0.011 | [-0.099, +0.130] | 0.165 | not distinguishable |
| ablation/dense_w150 minus hybrid | Recall@10 | -0.142 | [-0.300, +0.000] | 0.217 | not distinguishable |
| ablation/dense_w150 minus hybrid | MRR@10 | -0.091 | [-0.189, +0.019] | 0.151 | not distinguishable |
| ablation/dense_w150 minus hybrid | nDCG@10 | -0.114 | [-0.208, -0.004] | 0.147 | hybrid higher |
| ablation/dense_w150 minus rerank | Recall@10 | -0.175 | [-0.308, -0.058] | 0.187 | rerank higher |
| ablation/dense_w150 minus rerank | MRR@10 | -0.394 | [-0.540, -0.254] | 0.208 | rerank higher |
| ablation/dense_w150 minus rerank | nDCG@10 | -0.338 | [-0.472, -0.213] | 0.189 | rerank higher |
| ablation/dense_w150 minus ablation/dense_bge_base | Recall@10 | +0.067 | [-0.067, +0.200] | 0.198 | not distinguishable |
| ablation/dense_w150 minus ablation/dense_bge_base | MRR@10 | -0.074 | [-0.222, +0.070] | 0.210 | not distinguishable |
| ablation/dense_w150 minus ablation/dense_bge_base | nDCG@10 | -0.041 | [-0.172, +0.091] | 0.190 | not distinguishable |
| ablation/dense_w150 minus ablation/dense_w100 | Recall@10 | +0.033 | [-0.083, +0.150] | 0.164 | not distinguishable |
| ablation/dense_w150 minus ablation/dense_w100 | MRR@10 | -0.023 | [-0.135, +0.097] | 0.169 | not distinguishable |
| ablation/dense_w150 minus ablation/dense_w100 | nDCG@10 | -0.006 | [-0.110, +0.104] | 0.156 | not distinguishable |
| ablation/dense_w200 minus bm25 | Recall@10 | -0.167 | [-0.317, -0.017] | 0.226 | bm25 higher |
| ablation/dense_w200 minus bm25 | MRR@10 | -0.192 | [-0.329, -0.076] | 0.185 | bm25 higher |
| ablation/dense_w200 minus bm25 | nDCG@10 | -0.197 | [-0.324, -0.084] | 0.175 | bm25 higher |
| ablation/dense_w200 minus dense | Recall@10 | -0.008 | [-0.117, +0.100] | 0.159 | not distinguishable |
| ablation/dense_w200 minus dense | MRR@10 | -0.022 | [-0.162, +0.118] | 0.206 | not distinguishable |
| ablation/dense_w200 minus dense | nDCG@10 | -0.021 | [-0.126, +0.085] | 0.156 | not distinguishable |
| ablation/dense_w200 minus hybrid | Recall@10 | -0.183 | [-0.317, -0.067] | 0.184 | hybrid higher |
| ablation/dense_w200 minus hybrid | MRR@10 | -0.109 | [-0.215, -0.001] | 0.158 | hybrid higher |
| ablation/dense_w200 minus hybrid | nDCG@10 | -0.145 | [-0.233, -0.060] | 0.126 | hybrid higher |
| ablation/dense_w200 minus rerank | Recall@10 | -0.217 | [-0.367, -0.083] | 0.198 | rerank higher |
| ablation/dense_w200 minus rerank | MRR@10 | -0.412 | [-0.563, -0.264] | 0.221 | rerank higher |
| ablation/dense_w200 minus rerank | nDCG@10 | -0.370 | [-0.508, -0.237] | 0.197 | rerank higher |
| ablation/dense_w200 minus ablation/dense_bge_base | Recall@10 | +0.025 | [-0.092, +0.150] | 0.179 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_bge_base | MRR@10 | -0.092 | [-0.252, +0.066] | 0.233 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_bge_base | nDCG@10 | -0.072 | [-0.203, +0.059] | 0.191 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_w100 | Recall@10 | -0.008 | [-0.133, +0.108] | 0.179 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_w100 | MRR@10 | -0.041 | [-0.154, +0.070] | 0.162 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_w100 | nDCG@10 | -0.037 | [-0.137, +0.051] | 0.138 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_w150 | Recall@10 | -0.042 | [-0.175, +0.100] | 0.202 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_w150 | MRR@10 | -0.018 | [-0.139, +0.096] | 0.169 | not distinguishable |
| ablation/dense_w200 minus ablation/dense_w150 | nDCG@10 | -0.031 | [-0.139, +0.065] | 0.147 | not distinguishable |
| ablation/dense_w250 minus bm25 | Recall@10 | -0.222 | [-0.372, -0.078] | 0.215 | bm25 higher |
| ablation/dense_w250 minus bm25 | MRR@10 | -0.159 | [-0.329, +0.002] | 0.243 | not distinguishable |
| ablation/dense_w250 minus bm25 | nDCG@10 | -0.199 | [-0.344, -0.071] | 0.199 | bm25 higher |
| ablation/dense_w250 minus dense | Recall@10 | -0.064 | [-0.183, +0.036] | 0.159 | not distinguishable |
| ablation/dense_w250 minus dense | MRR@10 | +0.011 | [-0.114, +0.131] | 0.180 | not distinguishable |
| ablation/dense_w250 minus dense | nDCG@10 | -0.023 | [-0.115, +0.063] | 0.129 | not distinguishable |
| ablation/dense_w250 minus hybrid | Recall@10 | -0.239 | [-0.400, -0.100] | 0.216 | hybrid higher |
| ablation/dense_w250 minus hybrid | MRR@10 | -0.076 | [-0.179, +0.032] | 0.154 | not distinguishable |
| ablation/dense_w250 minus hybrid | nDCG@10 | -0.147 | [-0.232, -0.068] | 0.119 | hybrid higher |
| ablation/dense_w250 minus rerank | Recall@10 | -0.272 | [-0.433, -0.122] | 0.226 | rerank higher |
| ablation/dense_w250 minus rerank | MRR@10 | -0.379 | [-0.551, -0.209] | 0.250 | rerank higher |
| ablation/dense_w250 minus rerank | nDCG@10 | -0.372 | [-0.523, -0.225] | 0.218 | rerank higher |
| ablation/dense_w250 minus ablation/dense_bge_base | Recall@10 | -0.031 | [-0.156, +0.089] | 0.181 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_bge_base | MRR@10 | -0.058 | [-0.215, +0.091] | 0.223 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_bge_base | nDCG@10 | -0.074 | [-0.199, +0.039] | 0.175 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w100 | Recall@10 | -0.064 | [-0.192, +0.050] | 0.179 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w100 | MRR@10 | -0.007 | [-0.129, +0.102] | 0.168 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w100 | nDCG@10 | -0.039 | [-0.141, +0.050] | 0.140 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w150 | Recall@10 | -0.097 | [-0.206, -0.006] | 0.147 | ablation/dense_w150 higher |
| ablation/dense_w250 minus ablation/dense_w150 | MRR@10 | +0.016 | [-0.098, +0.122] | 0.162 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w150 | nDCG@10 | -0.033 | [-0.127, +0.044] | 0.124 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w200 | Recall@10 | -0.056 | [-0.167, +0.022] | 0.135 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w200 | MRR@10 | +0.033 | [-0.089, +0.155] | 0.180 | not distinguishable |
| ablation/dense_w250 minus ablation/dense_w200 | nDCG@10 | -0.002 | [-0.079, +0.071] | 0.112 | not distinguishable |
| ablation/dense_w350 minus bm25 | Recall@10 | -0.158 | [-0.308, -0.025] | 0.208 | bm25 higher |
| ablation/dense_w350 minus bm25 | MRR@10 | -0.149 | [-0.301, -0.016] | 0.209 | bm25 higher |
| ablation/dense_w350 minus bm25 | nDCG@10 | -0.160 | [-0.306, -0.034] | 0.199 | bm25 higher |
| ablation/dense_w350 minus dense | Recall@10 | +0.000 | [-0.083, +0.067] | 0.116 | not distinguishable |
| ablation/dense_w350 minus dense | MRR@10 | +0.021 | [-0.093, +0.138] | 0.169 | not distinguishable |
| ablation/dense_w350 minus dense | nDCG@10 | +0.016 | [-0.067, +0.100] | 0.123 | not distinguishable |
| ablation/dense_w350 minus hybrid | Recall@10 | -0.175 | [-0.317, -0.050] | 0.199 | hybrid higher |
| ablation/dense_w350 minus hybrid | MRR@10 | -0.066 | [-0.151, +0.022] | 0.125 | not distinguishable |
| ablation/dense_w350 minus hybrid | nDCG@10 | -0.108 | [-0.186, -0.040] | 0.106 | hybrid higher |
| ablation/dense_w350 minus rerank | Recall@10 | -0.208 | [-0.367, -0.067] | 0.213 | rerank higher |
| ablation/dense_w350 minus rerank | MRR@10 | -0.369 | [-0.521, -0.217] | 0.224 | rerank higher |
| ablation/dense_w350 minus rerank | nDCG@10 | -0.333 | [-0.477, -0.196] | 0.205 | rerank higher |
| ablation/dense_w350 minus ablation/dense_bge_base | Recall@10 | +0.033 | [-0.067, +0.133] | 0.164 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_bge_base | MRR@10 | -0.048 | [-0.189, +0.085] | 0.201 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_bge_base | nDCG@10 | -0.035 | [-0.152, +0.078] | 0.169 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w100 | Recall@10 | +0.000 | [-0.117, +0.100] | 0.165 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w100 | MRR@10 | +0.003 | [-0.122, +0.122] | 0.175 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w100 | nDCG@10 | +0.0002 | [-0.107, +0.095] | 0.146 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w150 | Recall@10 | -0.033 | [-0.117, +0.033] | 0.115 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w150 | MRR@10 | +0.026 | [-0.096, +0.138] | 0.169 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w150 | nDCG@10 | +0.006 | [-0.097, +0.094] | 0.139 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w200 | Recall@10 | +0.008 | [-0.117, +0.125] | 0.179 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w200 | MRR@10 | +0.043 | [-0.040, +0.120] | 0.117 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w200 | nDCG@10 | +0.037 | [-0.037, +0.105] | 0.105 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w250 | Recall@10 | +0.064 | [-0.006, +0.153] | 0.118 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w250 | MRR@10 | +0.010 | [-0.094, +0.114] | 0.153 | not distinguishable |
| ablation/dense_w350 minus ablation/dense_w250 | nDCG@10 | +0.039 | [-0.010, +0.095] | 0.078 | not distinguishable |
| ablation/rerank_dense_w150 minus bm25 | Recall@10 | -0.047 | [-0.183, +0.081] | 0.192 | not distinguishable |
| ablation/rerank_dense_w150 minus bm25 | MRR@10 | +0.120 | [-0.070, +0.302] | 0.270 | not distinguishable |
| ablation/rerank_dense_w150 minus bm25 | nDCG@10 | +0.073 | [-0.095, +0.229] | 0.235 | not distinguishable |
| ablation/rerank_dense_w150 minus dense | Recall@10 | +0.111 | [+0.000, +0.233] | 0.171 | not distinguishable |
| ablation/rerank_dense_w150 minus dense | MRR@10 | +0.290 | [+0.124, +0.444] | 0.232 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus dense | nDCG@10 | +0.249 | [+0.120, +0.379] | 0.187 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus hybrid | Recall@10 | -0.064 | [-0.206, +0.067] | 0.197 | not distinguishable |
| ablation/rerank_dense_w150 minus hybrid | MRR@10 | +0.203 | [+0.061, +0.347] | 0.209 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus hybrid | nDCG@10 | +0.125 | [+0.002, +0.249] | 0.180 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus rerank | Recall@10 | -0.097 | [-0.222, +0.006] | 0.168 | not distinguishable |
| ablation/rerank_dense_w150 minus rerank | MRR@10 | -0.100 | [-0.233, +0.033] | 0.206 | not distinguishable |
| ablation/rerank_dense_w150 minus rerank | nDCG@10 | -0.100 | [-0.228, +0.008] | 0.173 | not distinguishable |
| ablation/rerank_dense_w150 minus ablation/dense_bge_base | Recall@10 | +0.144 | [+0.022, +0.278] | 0.190 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_bge_base | MRR@10 | +0.220 | [+0.058, +0.380] | 0.234 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_bge_base | nDCG@10 | +0.198 | [+0.064, +0.340] | 0.201 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w100 | Recall@10 | +0.111 | [+0.028, +0.217] | 0.142 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w100 | MRR@10 | +0.271 | [+0.136, +0.413] | 0.201 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w100 | nDCG@10 | +0.233 | [+0.123, +0.349] | 0.166 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w150 | Recall@10 | +0.078 | [+0.011, +0.167] | 0.114 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w150 | MRR@10 | +0.294 | [+0.167, +0.427] | 0.187 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w150 | nDCG@10 | +0.239 | [+0.139, +0.347] | 0.151 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w200 | Recall@10 | +0.119 | [-0.014, +0.253] | 0.196 | not distinguishable |
| ablation/rerank_dense_w150 minus ablation/dense_w200 | MRR@10 | +0.312 | [+0.173, +0.457] | 0.207 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w200 | nDCG@10 | +0.270 | [+0.148, +0.397] | 0.182 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w250 | Recall@10 | +0.175 | [+0.058, +0.308] | 0.181 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w250 | MRR@10 | +0.279 | [+0.128, +0.429] | 0.221 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w250 | nDCG@10 | +0.272 | [+0.150, +0.401] | 0.185 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w350 | Recall@10 | +0.111 | [+0.000, +0.233] | 0.171 | not distinguishable |
| ablation/rerank_dense_w150 minus ablation/dense_w350 | MRR@10 | +0.269 | [+0.129, +0.416] | 0.206 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus ablation/dense_w350 | nDCG@10 | +0.233 | [+0.116, +0.360] | 0.176 | ablation/rerank_dense_w150 higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

The hybrid and rerank recall is not much higher than bm25 but the biggest jump was the rerank MRR score. That shows that the retrievers are returning the right information but the standard hybrid combining metric is not actually helping. Having the agent though rank the documents does make a big difference because Claude actually has some logic and not just a deterministic math weight. 

No the hand and claude queries do not tell the same story. The Claude queries were higher in every evaluation metric by what I would say is a significant margin. 

I was surprised. I did not do the prediction before. 

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/dense_bge_base minus bm25 | Recall@10 | -0.192 | [-0.367, -0.017] | 0.259 | bm25 higher |
| ablation/dense_bge_base minus bm25 | MRR@10 | -0.101 | [-0.295, +0.093] | 0.283 | not distinguishable |
| ablation/dense_bge_base minus bm25 | nDCG@10 | -0.125 | [-0.306, +0.054] | 0.263 | not distinguishable |
| ablation/dense_bge_base minus dense | Recall@10 | -0.033 | [-0.150, +0.050] | 0.149 | not distinguishable |
| ablation/dense_bge_base minus dense | MRR@10 | +0.069 | [-0.010, +0.159] | 0.126 | not distinguishable |
| ablation/dense_bge_base minus dense | nDCG@10 | +0.052 | [-0.024, +0.129] | 0.114 | not distinguishable |
| ablation/dense_bge_base minus hybrid | Recall@10 | -0.208 | [-0.358, -0.075] | 0.213 | hybrid higher |
| ablation/dense_bge_base minus hybrid | MRR@10 | -0.018 | [-0.133, +0.101] | 0.172 | not distinguishable |
| ablation/dense_bge_base minus hybrid | nDCG@10 | -0.072 | [-0.186, +0.036] | 0.163 | not distinguishable |
| ablation/dense_bge_base minus rerank | Recall@10 | -0.242 | [-0.400, -0.092] | 0.224 | rerank higher |
| ablation/dense_bge_base minus rerank | MRR@10 | -0.320 | [-0.476, -0.170] | 0.222 | rerank higher |
| ablation/dense_bge_base minus rerank | nDCG@10 | -0.297 | [-0.454, -0.149] | 0.221 | rerank higher |
| ablation/dense_w100 minus bm25 | Recall@10 | -0.158 | [-0.317, -0.008] | 0.229 | bm25 higher |
| ablation/dense_w100 minus bm25 | MRR@10 | -0.152 | [-0.294, -0.027] | 0.197 | bm25 higher |
| ablation/dense_w100 minus bm25 | nDCG@10 | -0.160 | [-0.299, -0.036] | 0.193 | bm25 higher |
| ablation/dense_w100 minus dense | Recall@10 | +0.000 | [-0.083, +0.100] | 0.134 | not distinguishable |
| ablation/dense_w100 minus dense | MRR@10 | +0.019 | [-0.108, +0.147] | 0.187 | not distinguishable |
| ablation/dense_w100 minus dense | nDCG@10 | +0.016 | [-0.083, +0.124] | 0.152 | not distinguishable |
| ablation/dense_w100 minus hybrid | Recall@10 | -0.175 | [-0.308, -0.050] | 0.187 | hybrid higher |
| ablation/dense_w100 minus hybrid | MRR@10 | -0.068 | [-0.173, +0.038] | 0.153 | not distinguishable |
| ablation/dense_w100 minus hybrid | nDCG@10 | -0.108 | [-0.202, -0.014] | 0.137 | hybrid higher |
| ablation/dense_w100 minus rerank | Recall@10 | -0.208 | [-0.350, -0.075] | 0.202 | rerank higher |
| ablation/dense_w100 minus rerank | MRR@10 | -0.371 | [-0.528, -0.222] | 0.223 | rerank higher |
| ablation/dense_w100 minus rerank | nDCG@10 | -0.333 | [-0.476, -0.199] | 0.202 | rerank higher |
| ablation/dense_w150 minus bm25 | Recall@10 | -0.125 | [-0.250, -0.025] | 0.167 | bm25 higher |
| ablation/dense_w150 minus bm25 | MRR@10 | -0.175 | [-0.324, -0.034] | 0.212 | bm25 higher |
| ablation/dense_w150 minus bm25 | nDCG@10 | -0.166 | [-0.307, -0.038] | 0.197 | bm25 higher |
| ablation/dense_w150 minus dense | Recall@10 | +0.033 | [-0.083, +0.150] | 0.164 | not distinguishable |
| ablation/dense_w150 minus dense | MRR@10 | -0.004 | [-0.137, +0.133] | 0.194 | not distinguishable |
| ablation/dense_w150 minus dense | nDCG@10 | +0.011 | [-0.099, +0.130] | 0.165 | not distinguishable |
| ablation/dense_w150 minus hybrid | Recall@10 | -0.142 | [-0.300, +0.000] | 0.217 | not distinguishable |
| ablation/dense_w150 minus hybrid | MRR@10 | -0.091 | [-0.189, +0.019] | 0.151 | not distinguishable |
| ablation/dense_w150 minus hybrid | nDCG@10 | -0.114 | [-0.208, -0.004] | 0.147 | hybrid higher |
| ablation/dense_w150 minus rerank | Recall@10 | -0.175 | [-0.308, -0.058] | 0.187 | rerank higher |
| ablation/dense_w150 minus rerank | MRR@10 | -0.394 | [-0.540, -0.254] | 0.208 | rerank higher |
| ablation/dense_w150 minus rerank | nDCG@10 | -0.338 | [-0.472, -0.213] | 0.189 | rerank higher |
| ablation/dense_w200 minus bm25 | Recall@10 | -0.167 | [-0.317, -0.017] | 0.226 | bm25 higher |
| ablation/dense_w200 minus bm25 | MRR@10 | -0.192 | [-0.329, -0.076] | 0.185 | bm25 higher |
| ablation/dense_w200 minus bm25 | nDCG@10 | -0.197 | [-0.324, -0.084] | 0.175 | bm25 higher |
| ablation/dense_w200 minus dense | Recall@10 | -0.008 | [-0.117, +0.100] | 0.159 | not distinguishable |
| ablation/dense_w200 minus dense | MRR@10 | -0.022 | [-0.162, +0.118] | 0.206 | not distinguishable |
| ablation/dense_w200 minus dense | nDCG@10 | -0.021 | [-0.126, +0.085] | 0.156 | not distinguishable |
| ablation/dense_w200 minus hybrid | Recall@10 | -0.183 | [-0.317, -0.067] | 0.184 | hybrid higher |
| ablation/dense_w200 minus hybrid | MRR@10 | -0.109 | [-0.215, -0.001] | 0.158 | hybrid higher |
| ablation/dense_w200 minus hybrid | nDCG@10 | -0.145 | [-0.233, -0.060] | 0.126 | hybrid higher |
| ablation/dense_w200 minus rerank | Recall@10 | -0.217 | [-0.367, -0.083] | 0.198 | rerank higher |
| ablation/dense_w200 minus rerank | MRR@10 | -0.412 | [-0.563, -0.264] | 0.221 | rerank higher |
| ablation/dense_w200 minus rerank | nDCG@10 | -0.370 | [-0.508, -0.237] | 0.197 | rerank higher |
| ablation/dense_w250 minus bm25 | Recall@10 | -0.222 | [-0.372, -0.078] | 0.215 | bm25 higher |
| ablation/dense_w250 minus bm25 | MRR@10 | -0.159 | [-0.329, +0.002] | 0.243 | not distinguishable |
| ablation/dense_w250 minus bm25 | nDCG@10 | -0.199 | [-0.344, -0.071] | 0.199 | bm25 higher |
| ablation/dense_w250 minus dense | Recall@10 | -0.064 | [-0.183, +0.036] | 0.159 | not distinguishable |
| ablation/dense_w250 minus dense | MRR@10 | +0.011 | [-0.114, +0.131] | 0.180 | not distinguishable |
| ablation/dense_w250 minus dense | nDCG@10 | -0.023 | [-0.115, +0.063] | 0.129 | not distinguishable |
| ablation/dense_w250 minus hybrid | Recall@10 | -0.239 | [-0.400, -0.100] | 0.216 | hybrid higher |
| ablation/dense_w250 minus hybrid | MRR@10 | -0.076 | [-0.179, +0.032] | 0.154 | not distinguishable |
| ablation/dense_w250 minus hybrid | nDCG@10 | -0.147 | [-0.232, -0.068] | 0.119 | hybrid higher |
| ablation/dense_w250 minus rerank | Recall@10 | -0.272 | [-0.433, -0.122] | 0.226 | rerank higher |
| ablation/dense_w250 minus rerank | MRR@10 | -0.379 | [-0.551, -0.209] | 0.250 | rerank higher |
| ablation/dense_w250 minus rerank | nDCG@10 | -0.372 | [-0.523, -0.225] | 0.218 | rerank higher |
| ablation/dense_w350 minus bm25 | Recall@10 | -0.158 | [-0.308, -0.025] | 0.208 | bm25 higher |
| ablation/dense_w350 minus bm25 | MRR@10 | -0.149 | [-0.301, -0.016] | 0.209 | bm25 higher |
| ablation/dense_w350 minus bm25 | nDCG@10 | -0.160 | [-0.306, -0.034] | 0.199 | bm25 higher |
| ablation/dense_w350 minus dense | Recall@10 | +0.000 | [-0.083, +0.067] | 0.116 | not distinguishable |
| ablation/dense_w350 minus dense | MRR@10 | +0.021 | [-0.093, +0.138] | 0.169 | not distinguishable |
| ablation/dense_w350 minus dense | nDCG@10 | +0.016 | [-0.067, +0.100] | 0.123 | not distinguishable |
| ablation/dense_w350 minus hybrid | Recall@10 | -0.175 | [-0.317, -0.050] | 0.199 | hybrid higher |
| ablation/dense_w350 minus hybrid | MRR@10 | -0.066 | [-0.151, +0.022] | 0.125 | not distinguishable |
| ablation/dense_w350 minus hybrid | nDCG@10 | -0.108 | [-0.186, -0.040] | 0.106 | hybrid higher |
| ablation/dense_w350 minus rerank | Recall@10 | -0.208 | [-0.367, -0.067] | 0.213 | rerank higher |
| ablation/dense_w350 minus rerank | MRR@10 | -0.369 | [-0.521, -0.217] | 0.224 | rerank higher |
| ablation/dense_w350 minus rerank | nDCG@10 | -0.333 | [-0.477, -0.196] | 0.205 | rerank higher |
| ablation/rerank_dense_w150 minus bm25 | Recall@10 | -0.047 | [-0.183, +0.081] | 0.192 | not distinguishable |
| ablation/rerank_dense_w150 minus bm25 | MRR@10 | +0.120 | [-0.070, +0.302] | 0.270 | not distinguishable |
| ablation/rerank_dense_w150 minus bm25 | nDCG@10 | +0.073 | [-0.095, +0.229] | 0.235 | not distinguishable |
| ablation/rerank_dense_w150 minus dense | Recall@10 | +0.111 | [+0.000, +0.233] | 0.171 | not distinguishable |
| ablation/rerank_dense_w150 minus dense | MRR@10 | +0.290 | [+0.124, +0.444] | 0.232 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus dense | nDCG@10 | +0.249 | [+0.120, +0.379] | 0.187 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus hybrid | Recall@10 | -0.064 | [-0.206, +0.067] | 0.197 | not distinguishable |
| ablation/rerank_dense_w150 minus hybrid | MRR@10 | +0.203 | [+0.061, +0.347] | 0.209 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus hybrid | nDCG@10 | +0.125 | [+0.002, +0.249] | 0.180 | ablation/rerank_dense_w150 higher |
| ablation/rerank_dense_w150 minus rerank | Recall@10 | -0.097 | [-0.222, +0.006] | 0.168 | not distinguishable |
| ablation/rerank_dense_w150 minus rerank | MRR@10 | -0.100 | [-0.233, +0.033] | 0.206 | not distinguishable |
| ablation/rerank_dense_w150 minus rerank | nDCG@10 | -0.100 | [-0.228, +0.008] | 0.173 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/dense_bge_base against dense (BASE = "dense" in p2/retrievers/dense_bge_base.py): it helped 6 queries, hurt 2 and left 22 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_bge_base RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c15 | topic | claude | 0.111 | 1.000 | +0.889 | helped |
| c20 | topic | claude | 0.500 | 1.000 | +0.500 | helped |
| h01 | reference | hand | 0.500 | 1.000 | +0.500 | helped |
| h05 | reference | hand | 0.500 | 1.000 | +0.500 | helped |
| c09 | quote | claude | 0.000 | 0.250 | +0.250 | helped |
| h07 | topic | hand | 0.000 | 0.143 | +0.143 | helped |
| c19 | topic | claude | 0.500 | 0.000 | -0.500 | hurt |
| c12 | quote | claude | 0.200 | 0.000 | -0.200 | hurt |

ablation/dense_w100 against dense (BASE = "dense" in p2/retrievers/dense_w100.py): it helped 5 queries, hurt 6 and left 19 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_w100 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| h02 | quote | hand | 0.000 | 1.000 | +1.000 | helped |
| c12 | quote | claude | 0.200 | 1.000 | +0.800 | helped |
| c07 | reference | claude | 0.333 | 1.000 | +0.667 | helped |
| h07 | topic | hand | 0.000 | 0.500 | +0.500 | helped |
| c15 | topic | claude | 0.111 | 0.250 | +0.139 | helped |
| c17 | topic | claude | 1.000 | 0.000 | -1.000 | hurt |
| c02 | reference | claude | 1.000 | 0.500 | -0.500 | hurt |
| c20 | topic | claude | 0.500 | 0.200 | -0.300 | hurt |
| c18 | topic | claude | 0.500 | 0.250 | -0.250 | hurt |
| c19 | topic | claude | 0.500 | 0.250 | -0.250 | hurt |
| h05 | reference | hand | 0.500 | 0.250 | -0.250 | hurt |

ablation/dense_w150 against dense (BASE = "dense" in p2/retrievers/dense_w150.py): it helped 7 queries, hurt 7 and left 16 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_w150 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| h06 | quote | hand | 0.000 | 1.000 | +1.000 | helped |
| c15 | topic | claude | 0.111 | 1.000 | +0.889 | helped |
| c09 | quote | claude | 0.000 | 0.333 | +0.333 | helped |
| h07 | topic | hand | 0.000 | 0.333 | +0.333 | helped |
| c12 | quote | claude | 0.200 | 0.500 | +0.300 | helped |
| h02 | quote | hand | 0.000 | 0.200 | +0.200 | helped |
| c07 | reference | claude | 0.333 | 0.500 | +0.167 | helped |
| c17 | topic | claude | 1.000 | 0.000 | -1.000 | hurt |
| c02 | reference | claude | 1.000 | 0.500 | -0.500 | hurt |
| c10 | quote | claude | 1.000 | 0.500 | -0.500 | hurt |
| h05 | reference | hand | 0.500 | 0.000 | -0.500 | hurt |
| c18 | topic | claude | 0.500 | 0.143 | -0.357 | hurt |
| c20 | topic | claude | 0.500 | 0.167 | -0.333 | hurt |
| c19 | topic | claude | 0.500 | 0.333 | -0.167 | hurt |

ablation/dense_w200 against dense (BASE = "dense" in p2/retrievers/dense_w200.py): it helped 7 queries, hurt 8 and left 15 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_w200 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c09 | quote | claude | 0.000 | 1.000 | +1.000 | helped |
| c12 | quote | claude | 0.200 | 1.000 | +0.800 | helped |
| c07 | reference | claude | 0.333 | 1.000 | +0.667 | helped |
| h01 | reference | hand | 0.500 | 1.000 | +0.500 | helped |
| c15 | topic | claude | 0.111 | 0.250 | +0.139 | helped |
| h07 | topic | hand | 0.000 | 0.111 | +0.111 | helped |
| c14 | quote | claude | 0.000 | 0.100 | +0.100 | helped |
| c17 | topic | claude | 1.000 | 0.000 | -1.000 | hurt |
| c02 | reference | claude | 1.000 | 0.500 | -0.500 | hurt |
| c06 | reference | claude | 1.000 | 0.500 | -0.500 | hurt |
| c10 | quote | claude | 1.000 | 0.500 | -0.500 | hurt |
| c20 | topic | claude | 0.500 | 0.000 | -0.500 | hurt |
| h05 | reference | hand | 0.500 | 0.111 | -0.389 | hurt |
| c18 | topic | claude | 0.500 | 0.200 | -0.300 | hurt |
| c19 | topic | claude | 0.500 | 0.200 | -0.300 | hurt |

ablation/dense_w250 against dense (BASE = "dense" in p2/retrievers/dense_w250.py): it helped 7 queries, hurt 6 and left 17 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_w250 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| h07 | topic | hand | 0.000 | 1.000 | +1.000 | helped |
| c19 | topic | claude | 0.500 | 1.000 | +0.500 | helped |
| h01 | reference | hand | 0.500 | 1.000 | +0.500 | helped |
| c15 | topic | claude | 0.111 | 0.500 | +0.389 | helped |
| c12 | quote | claude | 0.200 | 0.500 | +0.300 | helped |
| h03 | topic | hand | 0.000 | 0.250 | +0.250 | helped |
| c09 | quote | claude | 0.000 | 0.143 | +0.143 | helped |
| c17 | topic | claude | 1.000 | 0.000 | -1.000 | hurt |
| c02 | reference | claude | 1.000 | 0.500 | -0.500 | hurt |
| c20 | topic | claude | 0.500 | 0.000 | -0.500 | hurt |
| h05 | reference | hand | 0.500 | 0.000 | -0.500 | hurt |
| c18 | topic | claude | 0.500 | 0.333 | -0.167 | hurt |
| c07 | reference | claude | 0.333 | 0.250 | -0.083 | hurt |

ablation/dense_w350 against dense (BASE = "dense" in p2/retrievers/dense_w350.py): it helped 5 queries, hurt 5 and left 20 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_w350 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c09 | quote | claude | 0.000 | 1.000 | +1.000 | helped |
| c12 | quote | claude | 0.200 | 1.000 | +0.800 | helped |
| h01 | reference | hand | 0.500 | 1.000 | +0.500 | helped |
| c15 | topic | claude | 0.111 | 0.333 | +0.222 | helped |
| h07 | topic | hand | 0.000 | 0.200 | +0.200 | helped |
| c17 | topic | claude | 1.000 | 0.125 | -0.875 | hurt |
| h05 | reference | hand | 0.500 | 0.000 | -0.500 | hurt |
| c20 | topic | claude | 0.500 | 0.167 | -0.333 | hurt |
| c19 | topic | claude | 0.500 | 0.250 | -0.250 | hurt |
| c07 | reference | claude | 0.333 | 0.200 | -0.133 | hurt |

ablation/rerank_dense_w150 against rerank (BASE = "rerank" in p2/retrievers/rerank_dense_w150.py): it helped 1 queries, hurt 4 and left 25 unchanged.

| Query | Class | Origin | rerank RR | ablation/rerank_dense_w150 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| h03 | topic | hand | 0.000 | 1.000 | +1.000 | helped |
| c11 | quote | claude | 1.000 | 0.000 | -1.000 | hurt |
| c13 | quote | claude | 1.000 | 0.000 | -1.000 | hurt |
| c14 | quote | claude | 1.000 | 0.000 | -1.000 | hurt |
| c17 | topic | claude | 1.000 | 0.000 | -1.000 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

I changed the embedding model. 

My hypothesis is that the model will not make a big difference in the evaluation metrics but that there will be a slight increase of maybe say 0.01-0.04 (0.1-0.4 is a typo, I was definitely not expecting that big of a jump) in the MRR scores. 

Comparing dense to ablation/dense_bge_base I noticed that the MRR score was .07 in increase which was not distinguishable. That is actually a little more than I was expecting. It still may not be enough to definitively say that that model is better though. What I did not expect was that the recall fell about 0.033. 

My claim was correct in saying that there will be an increase in the MRR scores. I was a off on the range but I also do not think that means that model is definitevely better. The gain is too small for the 30 queries to confirm. A difference of .126 would show up in the interval 80% of the time but since it is only 0.7, it may only show up closer to 50% of the time. 

Three queries went from rank 2 to rank 1. It is possible that the base model understand the query better but even a small change could bump something from rank 2 to rank 1. For c15 I think the model definitely helped. The KJV uses some words that we do not use much anymore but increase to the base model adds the connections needed to recognize that the words have similar meanings and help it identify the correct passage. c19 got worse because it may have identified the wrong queen (Queen Vashti). c12 is hard because there are many passages that talk about sin and death but I was hoping for a more exact match but since that is not a dense retriever strong suit, it does worse. 

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| h03 | 0.0 | Nothing | The KJV only has the word slave twice in all the chapters combined (Jeremiah 2 and Revelation 18). The KJV uses the word servant instead of slave. This is tricky because a slave and a servant are usually not associated as very similar. | I would use the word servant instead of slave and also understand how those words were translated from the original language. I do not think think this is a problem with the RAG, I think it is a prompt problem that causes the RAG to fail. There is very little context in the prompt and the little it does have is not helpful for either bm25 or dense. |
| h07 | MRR: 0.333333 | After looking at the passages it returned (Mark 1, Matthew 3, Colossians 2, Acts 19, 1 Peter 3) the passages definitely look relevant. | They are all talking about baptism but the problem is that there are actually a ton of verses about baptism and the specific ones that came to my mind first when writing the evaluation were generally not the same ones that the RAG returned. | This could also be a prompt problem. Making the query more specific could help the RAG lock in on a smaller set of passages. This is also not a failure based on the relevance rule because for topic queries I may want a broad range of passages and I feel like the RAG did a good job of that. I could try maybe searching for a specific word (like baptism) instead of specifing a couple random passages. |
| h09 | 0.0 | Nothing | This is also a hard passage because the only actually relevant information in the query is "haughty eyes" which does not appear in the KJV version. This is again more of a prompt problem, not giving the RAG enough information. It is also very hard for the embedding model to pick up on the connection between a proud look and haughty eyes. | I would try rephrasing the query. I would also experiment with a different translation because a translation like the ESV uses different wording which I am more used to. |
| h10 | 0.0 | Nothing | Again discipline appears only once in the KJV and proverbs 3 uses chasten instead. The embedding model is not able to make that connection. | Updating the query and or using a different version of the Bible. |
| c17 | MRR 1.0, Recall 0.5 | Genesis 22 | There is one short clause in Hebrews that talks about Abraham and it is hard for the embedding model to pick it out and it needs more specfic information in the query in order to find that chapter. That chapter is also more than a thousand words and includes references to many other people. | If I was trying to find the Hebrews passage, I would use the Genesis passage to tailor the query to try to match more words. |

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

Rerank was the winning system for both the shared corpora and my corpora. The MRR of the shared corpora was only slightly higher. 
My corpus documents were significantly longer and so more information was getting compacted into each embedding vector. My quote class was similar to the paraphrase class. bm25 did not do well on the shared paraphrase queries but it did great on my quote class getting a MRR of 0.9. That may because I roughly know the verse I am trying to find and most of the words actually appear in the verse allowing bm25 to find the right verse. My reference class was similar to the identifier class. dense did well at finding my references possibly because for most of the queries I also gave it some other information that the dense retriever needs to succeed and it was just enough to get it to a MRR of 0.78. I did not test different document length or how the queries were written which are my best guesses. 

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 202,019 | 5,104 | 90.9 | 16,835 | 425 | 7.6 |
| traces/own-own-ablation-rerank_dense_w150.jsonl | rerank_dense_w150 | 30 | 30 | 0 | 341,209 | 4,029 | 127.9 | 11,374 | 134 | 4.3 |
| traces/own-own-rerank.jsonl | rerank | 30 | 30 | 10 | 485,344 | 3,217 | 104.0 | 16,178 | 107 | 3.5 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 289,025 | 1,930 | 131.7 | 14,451 | 96 | 6.6 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 518,873 | 3,640 | 189.5 | 12,972 | 91 | 4.7 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.393 | [-0.595, -0.200] | 14,451 | 6.6 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.338 | [-0.533, -0.150] | 14,451 | 6.6 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.313 | [-0.478, -0.160] | 14,451 | 6.6 | rerank higher |
| own: bm25 minus rerank | 30 | -0.220 | [-0.354, -0.094] | 16,178 | 3.5 | rerank higher |
| own: dense minus rerank | 30 | -0.390 | [-0.537, -0.249] | 16,178 | 3.5 | rerank higher |
| own: hybrid minus rerank | 30 | -0.303 | [-0.432, -0.177] | 16,178 | 3.5 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-dense_bge_base.jsonl | dense_bge_base | 30 | 1.46 | 48.8 |
| traces/retrieval/own-own-ablation-dense_w100.jsonl | dense_w100 | 30 | 0.71 | 23.7 |
| traces/retrieval/own-own-ablation-dense_w150.jsonl | dense_w150 | 30 | 0.73 | 24.2 |
| traces/retrieval/own-own-ablation-dense_w200.jsonl | dense_w200 | 30 | 0.72 | 24.0 |
| traces/retrieval/own-own-ablation-dense_w250.jsonl | dense_w250 | 30 | 0.86 | 28.8 |
| traces/retrieval/own-own-ablation-dense_w350.jsonl | dense_w350 | 30 | 0.87 | 29.1 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 30 | 0.13 | 4.3 |
| traces/retrieval/own-own-dense.jsonl | dense | 30 | 1.17 | 39.1 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 30 | 1.64 | 54.7 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.06 | 2.8 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.68 | 34.1 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 1.78 | 89.1 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.16 | 4.1 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 2.00 | 50.0 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 2.84 | 71.0 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

I am going to experiment with the chunk size to see if a different chunk size would produce better results. My hypothesis is that the chunk size will not make a ton of difference but I suspect a slight drop in MRR scores on chunk sizes of 100, 150, and 350. I suspect a chunk size of 200 to be about the same but I suspect a chunk size of 250 to have a slight increase in MRR of 0.01-.0.02. 

My prediction on the hybrid_w150 vs hybrid is that the recall will be similar and the MRR will be about 0.1 (a non-distinguishable amount higher). I predict the same for the rerank_hybrid_w150 vs rerank. 

Option 4. I experimented with changing the chunk size. I added a new retriever for each chunk size value I wanted to test and put each file in with the other retrievers in p2/retrievers. 

Table name: own-ablation

The interval does not let me claim that there is a chunk size that will produce better results most of the time. The interval does let me claim that for the two rerank systems tested, performance increased a distinguishable amount for almost all cases and did not change by a distinguishable amount for the rest of the cases compared to a non-rerank. I can not say which rerank will perform best though. 

I would also test just the hybrid using dense_w150 because I am changing two things going from dense_w150 to rerank_dense_w150. A higher dense score does not necessarily mean a higher hybrid score which affects the rerank score. A distinguishably higher MRR hybrid score with a similar recall score would show that using a smaller chunk size results in a better hybrid system. It does not guarantee anything about rerank though. 

I changed two things from rerank to rerank_dense_w150 where I changed the 

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
_No repeated runs or answers files yet (598E: `p2 run ... --repeat 3` and `p2 answer ... --repeat 3`)._
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
