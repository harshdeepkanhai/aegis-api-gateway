"""A throwaway upstream the gateway federates over.

Two domains — authors and books — so the gateway can stitch them into a single
GraphQL response. The `/books` endpoint takes a comma-separated `author_ids` list
so a DataLoader can fetch every author's books in ONE request (the N+1 fix).
"""

from fastapi import FastAPI

app = FastAPI(title="mock-upstreams")

AUTHORS = [{"id": 1, "name": "Le Guin"}, {"id": 2, "name": "Butler"}]
BOOKS = [
    {"id": 10, "author_id": 1, "title": "The Dispossessed"},
    {"id": 11, "author_id": 1, "title": "A Wizard of Earthsea"},
    {"id": 12, "author_id": 2, "title": "Kindred"},
]


@app.get("/authors")
def authors() -> list[dict]:
    return AUTHORS


@app.get("/books")
def books(author_ids: str) -> list[dict]:
    ids = {int(x) for x in author_ids.split(",")}
    return [b for b in BOOKS if b["author_id"] in ids]
