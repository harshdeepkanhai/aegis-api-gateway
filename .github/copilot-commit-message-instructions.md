# Commit Message Instructions

Generate all commit messages following the Conventional Commits 1.0.0 specification.

## Structure

Format every commit message as:

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

The `type` and `description` are REQUIRED. Everything else is OPTIONAL.

## Type

- The message MUST begin with a type, which is a noun such as `feat` or `fix`, followed by an OPTIONAL scope, an OPTIONAL `!`, and a REQUIRED colon and space.
- Use `feat` when the commit adds a new feature (correlates with MINOR in SemVer).
- Use `fix` when the commit patches a bug (correlates with PATCH in SemVer).
- Other allowed types: `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`. These have no implicit SemVer effect unless they contain a breaking change.
- Write the type in lowercase and stay consistent.

## Scope

- A scope MAY be added after the type, inside parentheses, e.g. `feat(parser):`.
- The scope MUST be a noun describing a section of the codebase, e.g. `api`, `ui`, `auth`, `parser`.

## Description

- A description MUST immediately follow the colon and space after the type/scope prefix.
- Keep it a short, single-line summary of the change.
- Use the imperative, present-tense mood: "add", "fix", "remove" — not "added", "fixes", or "adding".
- Do not end the description with a period.
- Keep the first line to 72 characters or fewer.

## Body

- A longer body MAY be added to give additional context about the change.
- The body MUST begin one blank line after the description.
- The body is free-form and MAY span multiple newline-separated paragraphs.
- Use bullet points in the body when there are several distinct points.

## Footers

- One or more footers MAY be added one blank line after the body.
- Each footer MUST consist of a word token, followed by either a `: ` (colon-space) or ` #` (space-hash) separator, then a value, e.g. `Reviewed-by: Jane` or `Refs #123`.
- A footer token MUST use `-` in place of spaces, e.g. `Acked-by`, `Co-authored-by`. The only exception is `BREAKING CHANGE`, which keeps its space.
- A footer value MAY contain spaces and newlines; parsing ends when the next valid footer token/separator pair appears.

## Breaking changes

- A breaking change MAY accompany any type, not just `feat`. It correlates with MAJOR in SemVer.
- Indicate a breaking change in one of two ways (or both):
  1. Append a `!` immediately before the colon in the type/scope prefix, e.g. `feat!:` or `feat(api)!:`.
  2. Add a footer that begins with the uppercase text `BREAKING CHANGE:`, followed by a space and a description.
- `BREAKING CHANGE` MUST be uppercase. `BREAKING-CHANGE` is treated as synonymous.
- If `!` is used, the `BREAKING CHANGE:` footer MAY be omitted, and the description itself explains the break.

## Casing

- Treat all units of the message as case-insensitive EXCEPT `BREAKING CHANGE`, which MUST be uppercase.

## SemVer mapping

- `fix:` -> PATCH release.
- `feat:` -> MINOR release.
- Any `BREAKING CHANGE` (footer or `!`), regardless of type -> MAJOR release.

## One change per commit

- If a change fits more than one type, prefer splitting it into multiple focused commits.

## Reverts

- For revert commits, use the `revert` type and reference the reverted commit SHAs in a footer:

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## Examples

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

```
feat(lang): add Polish language
```

```
feat(api)!: send an email to the customer when a product is shipped
```

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Reviewed-by: Z
Refs: #123
```

```
docs: correct spelling of CHANGELOG
```