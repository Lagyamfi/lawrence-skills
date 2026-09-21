---
name: api-design
description: Design a new API or review an existing one against the rules distilled from "The API" book by Sergey Konstantinov. Use when asked to design, structure, name, version, document or evaluate an HTTP/JSON API, SDK, webhook or event contract, or when asked whether an API change is backward compatible. Covers naming, errors, idempotency, concurrency, pagination, async operations, notifications, HTTP semantics, compatibility policy, SDK design and API product concerns.
license: CC-BY-NC-4.0 derivative of "The API" by Sergey Konstantinov; see NOTICE.md
metadata:
  author: lagyamfi
  version: "0.2.0"
  source: https://twirl.github.io/The-API-Book/
---

# API design and review

Distilled from *The API* by Sergey Konstantinov (CC BY-NC 4.0, https://twirl.github.io/The-API-Book/). Everything here is paraphrased; each rule links to the chapter that explains it. Rule IDs: `I` intro, `D` design, `P` patterns, `B` backward compatibility, `H` HTTP, `S` SDK/UI, `Q` product.

## Files in this skill

| File | Load when |
|---|---|
| `references/checklist.md` | reviewing an API, or finishing a design (120 yes/no items in sections A-I) |
| `references/decision-tables.md` | choosing a method, status code, error shape, pagination, notification, bulk or partial-update design |
| `references/compatibility.md` | judging whether a change is breaking; setting a versioning policy |
| `references/rules-0N-*.md` | you need the *Why* behind a specific rule ID (416 rules) |
| `references/rules-index.md` | you are writing a report that must cite book chapters: it maps every prefix to its chapter link |
| `references/additions.md` | house rules not in the book (`X` prefix): health endpoints, deprecation headers, gateway errors, warnings, inference-style APIs |
| `assets/new-api-design-doc.md` | designing a new API (fill it in order) |
| `assets/api-review-scorecard.md` | reporting a review |

Do not load whole rule files. Each rule is one bullet starting with its ID, so fetch exactly the rules you need:

```
grep -h -A0 '^- H38-9:' references/rules-*.md
grep -h -E '^- (D13-24|P16-2|H37-8):' references/rules-*.md
```

Chapter links sit at the top of each chapter section in the rules files and in `references/rules-index.md`, not on the individual bullets.

Notation: a bare prefix such as `H38` means "the chapter as a whole"; `H38-9` is one rule; `P19-1/3` means rules 1 and 3. When reporting a finding, cite the specific rule, not the bare prefix.

## The 20 principles

1. An API is a long-lived contract, not an implementation detail; every flaw is multiplied by the number of consumers. (I2, I6)
2. A good API is the shortest path from "task stated" to "correct code written", and stays that way as it grows: obvious, readable, consistent. (I3)
3. Spec first: write the machine-readable contract before the code; when they disagree, the code is wrong. (I5)
4. Design top-down: field of application, abstraction levels, responsibility areas, then final interfaces. Mistakes at the top cost exponentially more than naming mistakes. (D9)
5. Every entity needs a one-line "why"; if there is none, drop it. Expose as little as possible. (D10, B26)
6. Only adjacent abstraction levels talk; each level owns its own vocabulary and status; never make callers combine data from two levels. (D11)
7. Write the partner's code before finalising the contract; where it is verbose or error-prone, add a helper. (D12, H39)
8. Names carry types, units, standards and side effects: `duration_ms`, `is_finished`, `iso_date`, `cancel()` rather than `canceled = true`. No abbreviations, amoeba verbs, or double negatives. (D13)
9. Reject bad input, never silently correct it. Empty result is `200`, not `404`. Missing required data is `400`, not a default. (D13)
10. Every error tells the client what to do: who is at fault, retryable or not, which field and constraint, a user-facing message and developer details. (D12, D13, P24, H38)
11. Assume everything fails and every step can be slow: every flow resumable, every mutation idempotent, every list bounded. (P14, D13)
12. Concurrency via optimistic revisions (ETag / If-Match), never public locks; conflicts are routine and the remedy is re-read and retry. (P16, H36)
13. Long operations become a status on the entity, visible immediately; never sometimes-a-result, sometimes-a-task. (P18)
14. Lists: always a limit; cursors for mutable data, offsets only for immutable data. (P19)
15. Polling over an event log is the baseline; push is an accelerator. Webhooks need a spec, signatures, recovery and monitoring. (P20, P21)
16. Avoid bulk mutation endpoints and diff-style PATCH; decompose into addressable sub-resources with full-replacement PUT. (P22, P23)
17. Anything observable is part of the contract, including bugs, ordering and timing; document implicit assumptions and emulate old behaviour until the next major. (B26, B31)
18. Extend by generalising: the old call becomes a helper with defaults for a more general call. Higher levels define contexts; lower levels interpret them. (B27, B28, B29)
19. If you call it an HTTP API, use HTTP semantics honestly: verbs, status classes, caching headers, URL as cache and idempotency key. Never argue from "REST". (H32, H34, H35)
20. The API is a product: docs, sandbox, SDKs, support, quotas, anti-fraud hooks and a deprecation roadmap are part of the deliverable. (Q49-Q61)

## Procedure A: design a new API

Record answers in `assets/new-api-design-doc.md`. Steps 1-3 are the expensive-to-change decisions; get them confirmed before naming endpoints.

1. **Field of application (D10).** One paragraph: what situation, for whom, why an API rather than an app, how impact is measured. Two-line "what we do / how we do it". Name the monetisation model and the audience that drives adoption (Q49-Q51).
2. **Abstraction levels (D11).** List the levels from the consumer's terms down to the raw system, grounded in real capabilities of the layer below. Draw the data flow. Verify no level-skipping, no raw fields leaking upward, each level owns its status, each state-changing verb is defined per level.
3. **Entities and responsibilities (D12).** Table of entities: definition, reason to exist, allowed operations, interfaces implemented. Write client pseudo-code for the top three scenarios; every gap is a helper. Give volatile data (prices, offers) an id and validity window. Group fields so no object exceeds about ten top-level attributes. Define the error model now.
4. **Final interfaces (D13).** Apply checklist section A. Decide cross-cutting patterns: idempotency for every mutation, revisions with ETag/If-Match, sync vs async per operation, pagination per list, notifications, localisation and location inputs, and reserve future restrictions (429, captcha, second factor) in the contract now.
5. **Transport mapping (H35-H39, if HTTP).** Draw the happy-path call sequence, recast each call as verb + resource, derive URLs, enumerate every error with recovery, state which HTTP features you rely on. Apply checklist section E.
6. **Spec, then sample client (I5, H39).** OpenAPI with prose on every field. Write a client against it and judge readability. Quick start in ten lines or fewer. Publish the compatibility policy before the first integration.
7. **Productise (Q54-Q61).** Lineup, docs set, sandbox with lifecycle control and failure scenarios, keys and quotas, support rota, SLA, roadmap with deprecation notices. Apply checklist section I.

## Procedure B: review an existing API

1. Gather evidence: spec, docs, a real client (or write one for the main scenario), sample error responses, changelog, versioning policy. When an artefact is missing, use the nearest substitute and say so: tests as error samples, git log as changelog, the framework's runtime schema (FastAPI, Spring, etc.) as the de facto spec. A spec generated from code after the fact scores 0 on the spec-first check (I5); a checked-in spec that the code is tested against scores 2.
2. Scope gate. Answer three questions and drop what does not apply, so the score is honest rather than padded:
   - Does the API have mutable, addressable entities? If not, skip the revision and partial-update items in sections C and E.
   - Does it emit events, lists that grow, or notifications? If not, skip section D except the `limit` item.
   - Does it ship an SDK or UI components? If not, skip section H.
   Mark skipped items `n/a` and reduce that section's maximum. Controls delegated to a gateway you cannot see (auth, quotas, rate limits) are `unverifiable`, listed separately, and excluded from the score. Section I items about monetisation, KPIs, support and SLA are answered by the API's owner, not the repository; ask, or mark `not evidenced`.
3. Run the fast triage below, then the applicable parts of `references/checklist.md`. Score 0 (absent), 1 (partial), 2 (met) with evidence, not opinion.
4. Group findings by fix cost, following the book's point that mistakes at higher design levels cost far more to fix than naming (D9-1, D9-2): design-level (needs a major; goes in the serenity notepad), additive (fits a minor), docs-only.
5. Cite the specific rule ID and its chapter link for every finding. Never cite "not RESTful" as a reason (H34-1); cite the concrete rule. If no book rule covers a real finding, check `references/additions.md`; if still none, report it under "outside the rulebook" rather than forcing a mis-cite.
6. Report with `assets/api-review-scorecard.md`.

Fast triage (the twelve most predictive checks):

| Check | Rule |
|---|---|
| Spec written before the code, and the server conforms | I5 |
| Main scenario codeable from names alone | I3-3 |
| No GET mutates; every mutation idempotent | H35-6, D13-24 |
| Every list has a limit; no offsets over mutable data | P19-1/3 |
| Errors carry reason, field, constraint, user message, retry guidance | D13-18, H38 |
| Empty search is 200; invalid input rejected, never clamped | D13-15/16 |
| Dates, durations, money, units named with their format | D13-4 |
| No undocumented fields or unwritten behaviour partners rely on | B26 |
| External ids are not sequential integers | D13-27 |
| Cache policy on every GET and every 404 | H35-9, H39-12 |
| Client can recover after a mid-flow timeout without duplicates | P14-1 |
| Written versioning, support and deprecation policy | B25, Q61 |

## Inference-style APIs

Many modern APIs are one heavy, side-effect-free POST (translate, transcribe, synthesise, classify, generate) plus a few metadata GETs. For these, the checks that matter most are: a declared input-size bound tied to the synchronous latency budget (D13-11, D13-12, P18-1); an async job path once inputs can exceed that budget (P18-7); a readiness-aware health endpoint (X1); whether identical input yields identical output within a major and how model upgrades are announced (B26-5, X5); whether input structure (line breaks, markup, placeholders) is preserved or the loss is declared (D13-16, X4); machine-readable warnings (X4); and gateway-produced errors (413, 504, 429) that honour the API's error envelope (X3). Section F is usually delegated to a gateway for these APIs; score it as described in the scope gate.

## Judging a change

Load `references/compatibility.md`. Breaking means existing partner code stops solving its task: removals, renames, changed observable behaviour (consistency, sync/async, ordering, cadence), new obligations, fixing a relied-upon bug without emulation, dropping a platform. Additive optional parameters whose omission reproduces old behaviour are not breaking. Breaking changes need a new major, a written rationale and a deprecation window; never ship one in a minor (B31-8).

## Defaults when the user has not specified

JSON over HTTP; snake_case fields; major version in the path (`/v1/`); ISO 8601 timestamps in UTC with `_at` suffix; money as integer minor units or decimal strings with a currency code; namespaced UUID ids (`order:<uuid>`); `Accept-Language` on every endpoint; error body `{ reason, localized_message, details }` with an `X-<ApiName>-Error-Kind` header; ETag on reads, If-Match on writes; cursor pagination with `limit` and `has_more`. Rules are not applied unthinkingly (D13-1): a deviation is fine when deliberate, documented and uniform.

## Output expectations

- Design: a filled design doc, then the spec. Flag every checklist deviation with a reason.
- Review: a filled scorecard with evidence, findings grouped by fix cost, each with a rule ID and chapter link.
- Single question (status code, pagination, PATCH vs PUT): answer from the decision table, cite the rule ID, link the chapter.
