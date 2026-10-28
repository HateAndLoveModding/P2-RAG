# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

My faith is very important to me and I aspire to read the Bible every day which is why I chose to use it as my corpus. I often do not remember where a passage is in the Bible and a RAG system that could search for a specific passage or verse would be very helpful.

I already know the answer on whether bm25, dense, hybrid, or rerank performs best. 

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

Right at the beginning I was going to use the entire KJV Bible but when Claude told me that that it was too big I had to decide whether to find a different corpus, keep the whole KJV Bible, or cut some books. I decided to cut some books because I didn't want to try to find a different corpus and I didn't want to go over 1 million tokens. But that also meant that I had to choose which books to keep and which ones to get rid of. I ultimately decided to keep the books that I thought I referenced the most so I just looked at each book and subjectively decided which books to keep.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

I overruled the agent when evaluating the logic of claude on prompt a01. I thought Claude was wrong. There was no side effect per se so I didn't anything instead. 

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

I don't trust the Claude queries for my own corpora. The rerank on those queries give a MRR of 1 but my hand ones have a MRR of 0.633. Granted some of my queries are very difficult, but I kind of feel like Claude is cheating a little bit. I don't know if I can trust the actual queries but I can grow my trust in the RAG by writing more of my own hand written queries that I actually want to know. 

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

I would experiment with a different version of the Bible as well as chunk and document sizes. I would also write more test queries and evaluate everything and compare to see if the values improve which show that those things do matter. 
