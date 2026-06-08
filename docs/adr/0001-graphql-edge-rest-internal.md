# ADR 0001 — GraphQL at the edge, REST internally

- **Status:** Accepted
- **Date:** 2026-06-08

## Context

Clients of the gateway (web, mobile, partner integrations) need to compose data
from several upstream domains — authors and books today, more later — in a single
round-trip, and they want to select only the fields they use. The upstream services
themselves are simpler: each owns one domain, is independently deployable, and is
happiest exposing a plain resource-oriented HTTP API.

A naive stitched query (`authors { name, books { title } }`) is the textbook N+1:
one call to list authors, then one call per author to fetch books.

## Decision

Expose **GraphQL at the edge** and keep upstreams on **REST internally**.

- The gateway publishes a single GraphQL schema and resolves it by fanning out to
  REST upstreams over `httpx`.
- A per-request **DataLoader** batches all book lookups into one
  `/books?author_ids=...` call, collapsing the N+1 into N+0.
- A REST fallback (`GET /authors`, auto-documented at `/docs`) stays available for
  simple consumers and for OpenAPI/Swagger tooling.
- Hot upstream responses are cached in **Redis** with a short TTL.

## Consequences

**Positive**
- Clients get flexible, typed, single-round-trip queries.
- Upstream services stay small, independently deployable, and cache-friendly.
- The DataLoader makes fan-out cost predictable regardless of result size.

**Negative / accepted costs**
- GraphQL HTTP caching is harder than REST's (everything is `POST /graphql`).
  Mitigated for now with Redis caching at the upstream-client layer; the roadmap is
  **persisted queries** so common operations get cacheable, fixed identifiers.
- A second schema to maintain at the edge. Accepted: it is the contract clients
  actually want, and it decouples them from upstream shape changes.

## Alternatives considered

- **REST all the way through** — simplest to cache, but pushes composition and
  over-fetching onto every client.
- **GraphQL federation across upstreams** — more power than two domains justify
  today; revisit when the number of upstreams grows.
