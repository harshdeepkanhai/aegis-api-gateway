"""The headline story under test: resolving books for N authors must fan out to
exactly ONE upstream call, not N. This is the N+1 fix the gateway exists to show.
"""

import asyncio

import pytest

from aegis.adapters.graphql import make_book_loader


class FakeUpstream:
    """Records every call so the test can assert batching, not just correctness."""

    def __init__(self) -> None:
        self.calls: list[list[int]] = []
        self._rows = [
            {"id": 10, "author_id": 1, "title": "The Dispossessed"},
            {"id": 11, "author_id": 1, "title": "A Wizard of Earthsea"},
            {"id": 12, "author_id": 2, "title": "Kindred"},
        ]

    async def books_for_authors(self, author_ids: list[int]) -> list[dict]:
        self.calls.append(list(author_ids))
        ids = set(author_ids)
        return [r for r in self._rows if r["author_id"] in ids]


@pytest.mark.asyncio
async def test_loader_batches_all_authors_into_one_call() -> None:
    upstream = FakeUpstream()
    loader = make_book_loader(upstream)  # type: ignore[arg-type]

    # Two concurrent loads, as GraphQL issues while resolving two authors in the
    # same tick — gather is what lets the DataLoader coalesce them into one batch.
    books_a1, books_a2 = await asyncio.gather(loader.load(1), loader.load(2))

    # The whole point: a single batched upstream request for both authors.
    assert len(upstream.calls) == 1
    assert sorted(upstream.calls[0]) == [1, 2]

    assert {b.title for b in books_a1} == {"The Dispossessed", "A Wizard of Earthsea"}
    assert [b.title for b in books_a2] == ["Kindred"]


@pytest.mark.asyncio
async def test_loader_returns_empty_list_for_author_with_no_books() -> None:
    upstream = FakeUpstream()
    loader = make_book_loader(upstream)  # type: ignore[arg-type]

    assert await loader.load(999) == []
    assert upstream.calls == [[999]]
