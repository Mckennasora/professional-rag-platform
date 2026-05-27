import hashlib
import math
import re

VECTOR_SIZE = 128


def _tokens(text: str) -> list[str]:
    ascii_words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", text)
    return ascii_words + cjk_chars


def embed_text(text: str) -> list[float]:
    """Create a deterministic lightweight embedding for the stage-1 demo.

    TODO: Replace with sentence-transformers or BGE embeddings in stage 2.
    """
    vector = [0.0] * VECTOR_SIZE
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % VECTOR_SIZE
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def embed_texts(texts: list[str]) -> list[list[float]]:
    return [embed_text(text) for text in texts]
