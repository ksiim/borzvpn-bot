from typing import Iterable


def chunked(items: Iterable[int], size: int):
    chunk = []

    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
