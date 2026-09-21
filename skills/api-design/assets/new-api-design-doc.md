# API Design Document: <API name>

Follows Procedure A in `../SKILL.md`. Fill sections in order; do not name endpoints before Step 3 is agreed. Rule IDs refer to `../references/rules-*.md`.

| Field | Value |
|---|---|
| Owner | |
| Status | draft / in review / approved |
| Target major version | v1 |
| Transport | JSON over HTTP (default) / other, with justification (H33-4) |
| Date | |

---

## Step 1. Field of application (D10, Q49-Q51)

**Problem statement** (one paragraph a stranger would understand; D10-1):

**Why an API rather than an application** (why are provider and consumer separate parties? D10-6):

**Who pays and how** (monetisation model, Q50-1):

**Decision-making audience** (end users / business owners / developers, Q49-2):

**Success metric** (what number this API is expected to move, D10-5):

**What we do / how we do it** (two lines, D10-7):

---

## Step 2. Abstraction levels (D11)

List the levels from the consumer's domain terms down to the raw system. Each must be grounded in real capabilities of the layer below (D11-4).

| Level | Consumer-facing concepts | Concepts it adds (its own status vocabulary) | Raw inputs from the level below |
|---|---|---|---|
| 1 (highest) | | | |
| 2 | | | |
| 3 | | | |

**Data-flow chart** (D11-11): what enters at the bottom, what each level enriches, what reaches the top.

**Cross-level verbs** (D11-9): for each state-changing operation (e.g. cancel), what it means at each level.

| Operation | Level 1 meaning | Level 2 meaning | Level 3 meaning |
|---|---|---|---|
| | | | |

**Checks:** no call skips a level (D11-8); no raw field leaks upward unchanged (D11-12); each field name means one thing everywhere (D11-2).

---

## Step 3. Entities and responsibilities (D12)

| Entity | Definition in domain terms | Why it exists (one line) | Operations (create / read / list / update / cancel / ...) | Interfaces it implements (B30-1) |
|---|---|---|---|---|
| | | | | |

**Top three client scenarios, as pseudo-code** (D12-2). Note every place the client must combine data, poll, or repeat boilerplate; each is a candidate helper (D12-3).

```
// Scenario 1:

// Scenario 2:

// Scenario 3:
```

**Helpers added as a result:**

**Volatile data with validity** (prices, offers, availability; D12-7/8):

| Data | Identifier | Validity window | Must be echoed back on |
|---|---|---|---|
| | | | |

**Error model** (D12-9 to D12-13, P24): list every business error, whether it is resolvable, and the client's expected reaction.

| Error `reason` | Status | Resolvable? | Client reaction | Fields/constraints reported |
|---|---|---|---|---|
| | | | | |

---

## Step 4. Cross-cutting patterns (D13, P16-P24)

| Concern | Decision | Rule |
|---|---|---|
| Idempotency for each mutation | token header / natural / draft-commit | D13-24, P16-2 |
| Concurrency control | ETag + If-Match on <resources> | P16-4, H36-9 |
| Consistency model | strong / replicas with read-your-writes token | P17 |
| Async operations | which ones, why, status field on the entity | P18-2, P18-7 |
| Pagination per list | cursor / offset (immutable only) / snapshot / event log | P19 |
| Notifications | polling event log; webhooks (spec, signature, retry, size) | P20, P21 |
| Bulk operations | none / atomic with per-item breakdown | P22 |
| Partial updates | sub-resources with PUT/DELETE | P23 |
| Retry policy | exponential backoff, cap, in SDK | D13-13 |
| Caching policy | Cache-Control per GET, validity windows on volatile data | D13-22 |
| Localisation and location | Accept-Language on all endpoints; user location stored separately | D13-30 |
| Reserved restrictions | 429, captcha / second factor, MFA responses documented now | D13-28, Q57-3 |
| API families on separate endpoints | server-to-server / end-user / widget | D13-28 |
| Identifier scheme | namespaced UUID (`order:<uuid>`) | D13-27 |
| Money and fixed precision | integer minor units or decimal strings, with currency | D13-4, D13-23 |

---

## Step 5. Transport mapping (H35-H39; skip if not HTTP)

**Happy-path call sequence** (H39-1):

**Resource and URL nomenclature** (H37):

| Resource | URL | GET | POST | PUT | DELETE | Notes (cache, ETag, idempotency) |
|---|---|---|---|---|---|---|
| | `/v1/...` | | | | | |

**Per-endpoint error enumeration with recovery** (H39-3): reference the error table in Step 3.

**HTTP features relied on** (H39-4): caching, conditional requests, CORS, compression, HTTP/2.

**Conventions:** casing per component (H35-12), trailing slash policy (H39-7), custom header prefix (H35-4).

---

## Step 6. Spec and sample client

- Spec location (OpenAPI or equivalent), with prose on every field (Q59-1):
- Sample client written against the spec (H39-6):
- Quick start in ten lines or fewer (Q59-7):

```
// quick start
```

---

## Step 7. Product and operations (Q54-Q61)

| Item | Plan |
|---|---|
| Lineup (base API, SDKs, widgets) | |
| Documentation set (reference, samples, sandbox, tutorial, quick start, FAQ, changelog, snapshot) | |
| Sandbox: side effects, lifecycle control, failure scenarios, fast-forward | |
| Keys, quotas, key scoping, abuse detection, compromised-key runbook | |
| Support: first line, second line rota | |
| SLA, platform-support policy, roadmap and deprecation lead time | |
| Compatibility policy (breaking definition, major cadence, minors kept, pinning) | |

---

## Master checklist sign-off

Walk sections A through I in `../references/checklist.md`. Record deviations here with the reason (D13-1: deviations must be deliberate and uniform).

| Rule | Deviation | Reason |
|---|---|---|
| | | |

## Serenity notepad (B31-9)

Known flaws accepted for v1, to be revisited at the next major:

- 
