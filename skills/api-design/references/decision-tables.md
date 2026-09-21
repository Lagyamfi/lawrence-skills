# Decision tables

Quick answers for the recurring choices: HTTP method, status code, error shape, pagination, notifications, bulk operations, partial updates, sync vs async, consistency.

## Tables

### HTTP methods
Book: https://twirl.github.io/The-API-Book/API.en.html#http-api-requests-semantics

| Method | Safe | Idempotent | Cacheable | Body | Use for |
|---|---|---|---|---|---|
| GET | yes | yes | yes (set directives) | no | Read one resource or a bounded list; must reflect the last PUT/DELETE |
| PUT | no | yes (URL is key) | no | yes | Full replacement, commit, idempotent state transition, create when client owns the id |
| DELETE | no | yes | no | no | Remove; afterwards GET gives 404/410. Prefer PUT archive |
| POST | no | no | no | yes | Create with server id, rich search, actions, anything heavy or non-idempotent |
| PATCH | no | no | no | yes | Avoid; decompose into PUT on sub-resources instead |
| HEAD / OPTIONS | yes | yes | - | no | Metadata; CORS preflight (must be supported) |

### Status codes
Book: https://twirl.github.io/The-API-Book/API.en.html#http-api-errors

| Situation | Code | Client retries? |
|---|---|---|
| Malformed or logically invalid request | 400 (422 acceptable for logical) | after fixing; list all failed checks |
| Missing or invalid credentials | 401 | after re-auth |
| Authenticated but not allowed | 403 | no |
| Not found, or cause deliberately hidden | 404 | maybe; set `Cache-Control` explicitly |
| Revision conflict / integrity | 409 | after re-reading state |
| Permanently gone | 410 | no |
| Quota or rate limit | 429 + `Retry-After` | after the delay |
| Unknown server error | 500 (+ body: retryable? failed?) | per body/`Retry-After` |
| Overload or maintenance | 503 + `Retry-After` | after the delay |
| Created | 201 + `Location` | - |
| Success with no data | 200 `{}` (204 allowed, not extensible) | - |
| Not modified | 304 | - |

Do not pick codes by how their name sounds (402, 418, 451 for business states). Distinguish business causes with a `reason`, not with more codes.

### Error response shape
Book: https://twirl.github.io/The-API-Book/API.en.html#http-api-errors

```json
{
  "reason": "constraint_violation",
  "localized_message": "Text safe to show the end user",
  "details": {
    "checks_failed": [
      { "field": "position.latitude", "error_type": "out_of_range",
        "constraints": { "min": -90, "max": 90 }, "message": "developer-facing text" }
    ],
    "can_be_retried": false,
    "is_operation_failed": true
  }
}
```

Plus headers: correct status class, `X-<ApiName>-Error-Kind: <reason>`, and `Retry-After` when retrying is the answer. Order checks so unresolvable errors come before resolvable ones.

### Pagination
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-lists

| Data shape | Scheme |
|---|---|
| Immutable, fixed list | `limit` + `offset` |
| Append-only, items immutable | boundary on a monotonic id: `older_than` / `newer_than`, wrapped in an opaque cursor |
| Mutable (reordering, status changes) | dated snapshot as an async export; or newest-page-only view (take-and-mark queue); or an immutable event log of changes |
| Any | always return `limit` default and max, `has_more`, and a cursor even on the last page |

### Notifications
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-async-event-processing

| Need | Choice |
|---|---|
| Baseline for every public API | Polling an ordered event log with cursors |
| Faster reaction, same reliability | Push as a trigger to poll early; keep slow polling as a safety net |
| Backend-to-backend | Webhooks with spec, signature, retry policy, idempotency key, size limit, ordering statement, monitoring, degradation ladder |
| Payload: entity has bounded size | Full state in the message |
| Payload: entity may be large | Reference (`event_type` + id), partner fetches |
| Many events per entity / bursts | Aggregate trigger (`pending_count`), partner pulls, partner confirms via a follow-up call that proves processing |

### Bulk operations
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-atomicity

Default: do not offer bulk mutations. If unavoidable: atomic and idempotent, per-item breakdown in every response, dependent operations grouped into one atomic unit, each sub-operation with a deterministic idempotency identity, and an SDK that implements the retry logic.

### Partial updates
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-partial-updates

| Approach | Verdict |
|---|---|
| PATCH with "send only changed fields", `null` meaning reset/skip | avoid: ambiguous, order-dependent |
| Sub-resources with full-replacement PUT and DELETE, computed fields on separate resources | default |
| Explicit operation log with known revision and idempotency token | for real collaborative editing; escalate order-dependent conflicts to users |

Always return the resulting state from a modifying call.

### Sync vs async
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-async

Make an operation async only if it can exceed a client's timeout, has unpredictable duration, or needs peak-load queuing. Represent it as a status on the domain entity, created with its final id, visible in reads immediately after acceptance. Never make reads async.

### Consistency
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-weak-consistency

Strong consistency by default. If reads go to replicas: writes still revision-checked on a single leader; reads accept a `last_known_*` token and guarantee inclusion (re-query master or return an explicit retry error); token-less reads hit master. Only ever relax consistency on brand-new endpoints.

---

