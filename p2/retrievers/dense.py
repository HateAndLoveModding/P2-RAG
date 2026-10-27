"""Dense retrieval (stage 1): embed every chunk once, embed the query, and rank chunks by cosine similarity.

It is the bge arm of the 12 lab's retrieve.py (dense_rankings) moved from whole articles to chunks:
- the chunks are the [chunking] settings of p2.toml, embedded once with p2.embed.doc_vectors, which
  caches them in .cache/vectors/<model>.npz so later runs only encode new chunks;
- the query is embedded at search time, with an optional prefix put in front of it (some models,
  such as Qwen3-Embedding, expect an instruction line before each query; bge-small works without one);
- every vector has length 1, so one matrix-vector product gives the cosine similarity of the query
  with every chunk, and ChunkScorer lifts that to documents (a document scores its best chunk).

The model name and the query prefix are arguments of Dense, so a variant for an ablation can be a
file of its own that builds Dense with another model (and, through cfg.replace, other chunk settings).
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg, model_name: str = embed.BGE, query_prefix: str = ""):
        super().__init__(corpus, cfg)
        self.model = model_name  # recorded in traces
        self.query_prefix = query_prefix
        self.embedder = embed.load(model_name)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)  # one unit row per chunk

    def score_chunks(self, text: str) -> list[float]:
        if not self.chunks:
            return []
        query = self.embedder.encode([self.query_prefix + text])[0]
        return (self.vectors @ query).tolist()


def build(corpus, cfg):
    return Dense(corpus, cfg)
