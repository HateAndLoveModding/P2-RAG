"""Ablation of dense: chunks of 350 words instead of the 300 in p2.toml, one point of a chunk-size sweep.

Everything else is dense's: bge-small-en-v1.5, the overlap of p2.toml (50 words), no query prefix,
cosine similarity over chunks, and a document scored by its best chunk. The vectors share dense's
cache, .cache/vectors/BAAI_bge-small-en-v1.5.npz, which keys each chunk by its text.
"""

from __future__ import annotations

from p2.retrievers.dense import Dense

NEEDS_CLAUDE = False
BASE = "dense"
WORDS = 350


def build(corpus, cfg):
    return Dense(corpus, cfg.replace(chunk_words=WORDS))
