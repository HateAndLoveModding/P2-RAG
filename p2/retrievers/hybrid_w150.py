"""Variant of hybrid: reciprocal rank fusion of bm25 and dense_w150, with 150-word chunks throughout.

Everything else is hybrid's: rrf_k from p2.toml and fusion over full rankings. bm25 is cut into the
same 150-word chunks as dense_w150 (the overlap stays at p2.toml's 50), because search_chunks fuses
chunk rankings and the two systems' chunk ids have to match.
"""

from __future__ import annotations

from p2.retrievers.dense_w150 import WORDS
from p2.retrievers.hybrid import Hybrid

NEEDS_CLAUDE = False
BASE = "hybrid"


def build(corpus, cfg):
    return Hybrid(corpus, cfg.replace(chunk_words=WORDS), systems=("bm25", "dense_w150"))
