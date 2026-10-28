"""Reranking (stage 1): Claude reorders hybrid's top 20, one claude -p call per query.

It is rerank_one() from the 13 lab's pipeline.py with these changes:
- the first stage is hybrid (p2.retrievers.build, so its indexes are built once per run);
- for a document, Claude sees its best chunk (the one hybrid's fused chunk ranking puts highest for
  this query) instead of the document's first 600 characters, because a long CFR section or a KJV
  chapter often holds the part that matters far from its start; for a chunk, it sees the chunk;
- RERANK_SCHEMA's items carry "minimum": 1 and "maximum": n, so every number names a passage;
- every call goes through p2.claude.call, which caches the reply in .cache/claude/ and records the
  tokens in the run's trace.

The first stage is an argument of Rerank, so a variant can rerank another system's top 20
(rerank_dense_w150 reranks dense_w150's); the chunks it shows Claude are cut with that cfg's settings.

A reply that is not each of 1 to n once, or a call that fails, keeps the first stage's order (with a
warning), and everything below the top 20 keeps the first stage's order underneath. Scores are positions counted from the
bottom (the last item scores 1), so they are distinct and non-increasing, as a run file needs.
"""

from __future__ import annotations

from p2 import claude, retrievers
from p2.corpus import docid_of

NEEDS_CLAUDE = True
CANDIDATES = 20

RERANK_PROMPT = """Below are {n} passages, numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def rerank_schema(n: int) -> dict:
    order = {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": n}, "minItems": n, "maxItems": n}
    return {"type": "object", "properties": {"order": order}, "required": ["order"]}


class Rerank:
    def __init__(self, corpus, cfg, first: str = "hybrid"):
        self.cfg = cfg
        self.model = cfg.model  # recorded in traces
        self.first_name = first
        self.first = retrievers.build(first, corpus, cfg)
        self.chunk_text = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)
        self.n_chunks = len(self.chunk_text)

    def reorder(self, query: str, ids: list[str], passages: list[str]) -> list[str]:
        """The ids in Claude's order of their passages, or in the given order if the reply is unusable."""
        n = len(ids)
        if n < 2:
            return ids
        numbered = "\n\n".join(f"[{i}] {p}" for i, p in enumerate(passages, 1))
        prompt = RERANK_PROMPT.format(n=n, query=query, passages=numbered)
        reply = claude.call(prompt, rerank_schema(n), model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
        order = (reply.output or {}).get("order")
        if reply.error or not isinstance(order, list) or sorted(order) != list(range(1, n + 1)):
            problem = reply.error or f"the reply was not each of 1 to {n} once: {order}"
            print(f"    rerank kept {self.first_name}'s order: {problem}", flush=True)
            return ids
        return [ids[i - 1] for i in order]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        ranking = [d for d, _ in self.first.search(text, max(k, CANDIDATES))]
        top = ranking[:CANDIDATES]
        best_chunk: dict[str, str] = {}
        wanted = set(top)
        for chunk_id, _ in self.first.search_chunks(text, self.n_chunks):  # best first, so the first chunk seen per document is its best
            docid = docid_of(chunk_id)
            if docid in wanted and docid not in best_chunk:
                best_chunk[docid] = chunk_id
                if len(best_chunk) == len(wanted):
                    break
        passages = [f"({d}) {self.chunk_text[best_chunk[d]]}" for d in top]
        return self._scored(self.reorder(text, top, passages) + ranking[CANDIDATES:], k)

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        ranking = [c for c, _ in self.first.search_chunks(text, max(k, CANDIDATES))]
        top = ranking[:CANDIDATES]
        passages = [f"({docid_of(c)}) {self.chunk_text[c]}" for c in top]
        return self._scored(self.reorder(text, top, passages) + ranking[CANDIDATES:], k)

    @staticmethod
    def _scored(ids: list[str], k: int) -> list[tuple[str, float]]:
        return [(item, float(len(ids) - i)) for i, item in enumerate(ids)][:k]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
