"""Hybrid retrieval (stage 1): reciprocal rank fusion (RRF) of bm25 and dense.

It is rrf() from the 13 lab's pipeline.py: each document scores the sum of 1 / (k + rank) over the
rankings it appears in, rank counted from 1, so a document near the top of either list rises and one
near the top of both rises most. Only ranks count, never the raw scores, which is why BM25's
unbounded scores and dense's cosine similarities can be fused without scaling.

k is rrf_k in the [hybrid] table of p2.toml (60, the lab's value, if the table has none). On the
shared corpus's 2,484 documents, k = 60 let a document ranked moderately by both systems beat one
ranked first by one of them, so p2.toml sets a smaller k.

- the two systems come from p2.retrievers.build, so each index is built once per run;
- they are fused over full rankings (every document, or every chunk), because a document that is
  11th in both lists can belong in the fused top 10;
- search fuses document rankings and search_chunks fuses chunk rankings (both systems chunk with the
  same [chunking] settings, so their chunk ids match), and p2.runfile.order puts equal scores in id order.

The fused systems are arguments of Hybrid, so a variant can fuse others (bm25_ref with dense, say).
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False
RRF_K = 60


def rrf(rankings: Sequence[Sequence[tuple[str, float]]], k: int = RRF_K) -> list[tuple[str, float]]:
    """Fuse rankings of (id, score) pairs, best first, into one: an id scores the sum of 1 / (k + rank)."""
    fused: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, (item, _score) in enumerate(ranking, 1):
            fused[item] += 1 / (k + rank)
    return order(fused.items())


class Hybrid:
    def __init__(self, corpus, cfg, systems: Sequence[str] = ("bm25", "dense")):
        self.rrf_k = cfg.table("hybrid").get("rrf_k", RRF_K)
        if not isinstance(self.rrf_k, int) or isinstance(self.rrf_k, bool) or self.rrf_k < 1:
            raise ValueError(f"rrf_k in [hybrid] of p2.toml should be a whole number of at least 1, not {self.rrf_k!r}; fix the value.")
        self.systems = [retrievers.build(name, corpus, cfg) for name in systems]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([s.search(text, self.n_docs) for s in self.systems], self.rrf_k)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([s.search_chunks(text, self.n_chunks) for s in self.systems], self.rrf_k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
