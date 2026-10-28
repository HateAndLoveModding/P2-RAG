"""Ablation of dense: the embedding model is bge-base-en-v1.5 instead of bge-small-en-v1.5.

Everything else is dense's: the [chunking] settings of p2.toml, no query prefix, cosine similarity
over chunks, and a document scored by its best chunk. Its vectors cache in their own file,
.cache/vectors/BAAI_bge-base-en-v1.5.npz, so dense's cache is untouched.
"""

from __future__ import annotations

from p2.retrievers.dense import Dense

NEEDS_CLAUDE = False
BASE = "dense"
MODEL = "BAAI/bge-base-en-v1.5"


def build(corpus, cfg):
    return Dense(corpus, cfg, model_name=MODEL)
