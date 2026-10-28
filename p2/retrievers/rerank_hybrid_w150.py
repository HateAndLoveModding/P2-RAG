"""Variant of rerank: Claude reorders hybrid_w150's top 20 (bm25 fused with dense_w150) instead of hybrid's.

The only change from rerank is the chunk size, 150 words instead of p2.toml's 300, in the first stage
and in the passages Claude sees (each document shown as its best 150-word chunk). The prompt, the
model in p2.toml and the 20 candidates are rerank's.
"""

from __future__ import annotations

from p2.retrievers.dense_w150 import WORDS
from p2.retrievers.rerank import Rerank

NEEDS_CLAUDE = True
BASE = "rerank"


def build(corpus, cfg):
    return Rerank(corpus, cfg.replace(chunk_words=WORDS), first="hybrid_w150")
