import strawberry
from strawberry.dataloader import DataLoader
from strawberry.fastapi import GraphQLRouter
from aegis.adapters.upstream import UpstreamClient


@strawberry.type
class Book:
    id: int
    title: str


@strawberry.type
class Author:
    id: int
    name: str

    @strawberry.field
    async def books(self, info: strawberry.Info) -> list[Book]:
        # one batched upstream call per request, regardless of author count
        return await info.context["book_loader"].load(self.id)


def make_book_loader(client: UpstreamClient) -> DataLoader[int, list[Book]]:
    async def batch(author_ids: list[int]) -> list[list[Book]]:
        rows = await client.books_for_authors(author_ids)
        grouped: dict[int, list[Book]] = {aid: [] for aid in author_ids}
        for r in rows:
            grouped[r["author_id"]].append(Book(id=r["id"], title=r["title"]))
        return [grouped[aid] for aid in author_ids]  # order must match keys
    return DataLoader(load_fn=batch)


@strawberry.type
class Query:
    @strawberry.field
    async def authors(self, info: strawberry.Info) -> list[Author]:
        rows = await info.context["client"].list_authors()
        return [Author(id=a["id"], name=a["name"]) for a in rows]


schema = strawberry.Schema(query=Query)


def build_graphql_router(client: UpstreamClient) -> GraphQLRouter:
    async def context_getter() -> dict:
        return {"client": client, "book_loader": make_book_loader(client)}
    return GraphQLRouter(schema, context_getter=context_getter, path="/graphql")