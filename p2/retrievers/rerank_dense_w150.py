"""Variant of rerank: Claude reorders dense_w150's top 20 instead of hybrid's.

dense_w150 had the best first column of the chunk-size sweep among the dense systems, so this asks
whether reranking its candidates beats reranking hybrid's. Everything else is rerank's: the prompt,
the model in p2.toml, 20 candidates, and each document shown to Claude as its best chunk, here a
150-word chunk, because the chunks come from the same settings dense_w150 uses.
"""

from __future__ import annotations

from p2.retrievers.dense_w150 import WORDS
from p2.retrievers.rerank import Rerank

NEEDS_CLAUDE = True
BASE = "rerank"


def build(corpus, cfg):
    return Rerank(corpus, cfg.replace(chunk_words=WORDS), first="dense_w150")
