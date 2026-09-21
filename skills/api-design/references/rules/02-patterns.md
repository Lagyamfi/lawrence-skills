# Section II: The API Patterns (Chapters 14-24) — distilled rules

Source: "The API" by Sergey Konstantinov, CC BY-NC 4.0. Everything below is paraphrased; examples are original.

---

### Chapter 14. On Design Patterns in the API Context
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-context

**Core idea (2-3 sentences, own words):** Classic GoF patterns fit library-style APIs, but APIs over distributed systems raise higher-level problems (caching, pagination, sync) they do not cover. Three facts shape every solution in this section: failures at any layer are routine, partners will misuse the API, and any step may be arbitrarily slow.

**Rules:**
- P14-1: Design every flow so a client that crashed or timed out mid-operation can rediscover the current state and continue. *Why:* failures are normal, not exceptional. *Check:* If the client dies after any single call, is there an endpoint it can hit on restart to learn what happened?
- P14-2: Assume partners will implement the workflow wrongly and isolate them so one partner's bug cannot degrade service for others. *Why:* more integrators means more broken clients. *Check:* Are there per-partner quotas that contain a misbehaving caller?
- P14-3: Never let correctness depend on an operation finishing fast; make multi-step flows resumable from the current step. *Why:* seconds-long latencies can appear anywhere. *Check:* Can a multi-call scenario be resumed rather than restarted?
- P14-4: Guard shared resources with a lock or equivalent for the duration of modifying operations. *Why:* concurrent writes otherwise corrupt state. *Check:* Are concurrent writes to one resource serialized or detected?

**Patterns / recipes:**
- *Resumable flow*: expose a status per long process, e.g. `GET /orders/{id}` → `{ "status": "awaiting_payment", "next_step": "confirm" }`. Trade-off: more server-side state.

**Anti-patterns / smells:**
- Workflows that must restart from scratch after any failure.
- No rate limits, so one partner's retry loop starves others.
- Logic that assumes "the second call always lands after the first completes."

---

### Chapter 15. Authenticating Partners and Authorizing API Calls
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-aa

**Core idea (2-3 sentences, own words):** Two models exist: act through a "robot" user account inside the existing user system, or authenticate the calling system itself with keys, signatures, or certificates. Robot accounts give per-user granularity but need exceptions in every human-oriented security control; API keys are simpler but usually only endpoint-granular. Always use standard protocols.

**Rules:**
- P15-1: Use established auth standards (OAuth, mTLS, request signing), never homegrown schemes. *Why:* security mistakes multiply across partners. *Check:* Is every auth mechanism a named standard?
- P15-2: Use robot accounts when the API supplements an end-user product and must inherit its scoping; use API keys when the caller is a system working over a full dataset. *Why:* the two differ in access granularity. *Check:* Does the model match the dataset scope callers need?
- P15-3: If using robot users, provide a machine-friendly token issuance flow plus long-lived or renewable tokens, and explicitly exempt robots from captchas, cookie checks, IP heuristics, and forced logouts. *Why:* interactive login and human protections break unattended clients. *Check:* Can a robot obtain, renew, and keep using credentials without human intervention?
- P15-4: With API keys, let partners restrict which endpoints a key may call. *Why:* least privilege at the only cheap granularity. *Check:* Can a key be scoped to a subset of endpoints?

**Patterns / recipes:**
- *Robot account*: `Authorization: Bearer <robot-user-token>`; server applies the robot's per-user ACL. Trade-off: exceptions everywhere; acting "on behalf of other users" gets awkward.
- *System credential*: `X-Api-Key: <key>` plus signature; key maps to allowed endpoints. Trade-off: coarse access control.
- *Hybrid*: require both a key and a user token when a partner acts for a user.

**Anti-patterns / smells:**
- Custom signing/hashing invented in-house.
- Robot accounts getting logged out or captcha-challenged.
- One all-powerful key with no scoping.

---

### Chapter 16. Synchronization Strategies
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-sync-strategies

**Core idea (2-3 sentences, own words):** Reads and writes happen at different moments, so a client can never be sure state did not change in between; pick a consistency model and a sync strategy, preferring strong consistency where affordable. Explicit API-level locks are heavy and fragile; optimistic concurrency via revisions hides locking inside the backend and is the usual choice.

**Rules:**
- P16-1: Provide strong consistency by default when you can afford it. *Why:* most robust contract for clients. *Check:* Does a read after a successful write always reflect it?
- P16-2: Make operations idempotent where possible and accept client-generated idempotency keys for creates. *Why:* retries become harmless. *Check:* Does repeating a create with the same key avoid duplicates?
- P16-3: Do not expose lock primitives in a public API. *Why:* unpredictable waits, lost locks, need for quotas and debugging tools. *Check:* Are there acquire/release endpoints partners must pair correctly?
- P16-4: Use optimistic concurrency: mutating calls carry the revision the client last saw and are rejected if stale. *Why:* locking moves into a controlled backend. *Check:* Do mutating endpoints accept a version/ETag and return a distinct "stale revision" error?
- P16-5: Version the narrowest sensible resource; prefer monotonic counters or ETags over timestamps (if timestamps are unavoidable, store maximum precision). *Why:* a global version makes everyone conflict; clocks drift. *Check:* Does an unrelated user's write invalidate this client's revision?
- P16-6: Document that revision conflicts are normal and must be handled by re-reading and retrying. *Why:* otherwise apps loop forever on a stale version. *Check:* Do docs/SDKs show the re-read-and-retry loop?

**Patterns / recipes:**
- *Idempotency token*: `POST /orders` with `Idempotency-Key: 7f3a…`; server caches key → result. Trade-off: keys must be persisted with a TTL.
- *Optimistic locking with revisions*: `GET /orders/state` → `{ "revision": 42 }`; `POST /orders { "expected_revision": 42, … }` → `409 { "error": "stale_revision", "current_revision": 43 }`. Trade-off: conflict errors become routine client work.
- *API-level lock* (rarely justified): `POST /locks { "scope": "user:123:orders" }` → `{ "lock_id", "expires_at" }`; `DELETE /locks/{id}`. Trade-off: latency, orphaned locks, extra subsystem.

**Anti-patterns / smells:**
- Creates with neither idempotency key nor revision check.
- A single system-wide version number.
- Second-precision timestamp versions.
- Locks without expiry or orphan-detection tooling.

---

### Chapter 17. Eventual Consistency
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-weak-consistency

**Core idea (2-3 sentences, own words):** When writes are rare and reads frequent, serving reads from replicas buys throughput while revision checks on writes still block conflicts. The price is a permanent background error rate that hides real bugs in monitoring. "Read-your-writes" tokens plus serving master data when no token is present shrink that rate to near zero for typical client apps.

**Rules:**
- P17-1: Relax consistency only for new endpoints; never downgrade an existing one even if the behavior was undocumented. *Why:* clients depend on observed behavior. *Check:* Is this a brand-new endpoint?
- P17-2: Keep writes strictly ordered (single leader); use multi-leader only if operations are idempotent, duplicates are acceptable, or clients are pinned to one replica. *Why:* otherwise "latest version" is meaningless. *Check:* Is there a single authority for the current revision?
- P17-3: Implement read-your-writes: clients pass the id or revision of their last write on reads, and the server re-queries, hits master, or returns an explicit retry error if its data is older. *Why:* clients should not wait to see their own changes. *Check:* Can a list endpoint accept a `last_known_*` token and guarantee that change is included?
- P17-4: When no token is supplied, serve master data. *Why:* a missing token usually means an app restart, where stale data causes duplicate actions. *Check:* Does a token-less read fall back to authoritative storage?
- P17-5: Drive background consistency errors toward zero for the typical usage profile and make them distinguishable in monitoring. *Why:* 1% noise hides a 0.1% real bug for months. *Check:* Can dashboards separate lag errors from client bugs?
- P17-6: Serve eventually consistent reads by default only if replication lag is much shorter than the caller's restart-and-retry time (true for end-user apps, false for server-to-server). *Why:* error probability is roughly lag / retry interval. *Check:* Is lag documented and far below the fastest realistic retry?
- P17-7: If client-app and server-to-server profiles conflict, split them into separate API products. *Why:* one policy cannot fit both. *Check:* Are interactive and batch callers sharing endpoints with conflicting needs?

**Patterns / recipes:**
- *Read-your-writes token*: `POST /orders` → `{ "order_id": "o91" }`; `GET /orders/ongoing?last_known_order_id=o91`. If the replica lacks `o91`: re-read master, or `503 { "error": "not_yet_consistent", "retry_after_ms": 200 }`. Trade-off: unpredictable master load vs. more client error handling.
- *Recommended combo*: revision-checked writes + read-your-writes reads + master fallback without token. Remaining errors come only from partner bugs or one user on two devices.

**Anti-patterns / smells:**
- Silently switching an endpoint to replica reads.
- "Just retry" as the only guidance for consistency errors.
- Server-to-server clients seeing stale reads right after their own writes.

---

### Chapter 18. Asynchronicity and Time Management
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-async

**Core idea (2-3 sentences, own words):** Slow mutations widen the window in which a client cannot tell whether its request took effect; accepting the request quickly as a task with visible state closes it. Async also gives result caching, idempotent confirmation, load smoothing, and tolerance for jobs longer than timeouts. But blanket asynchronicity adds queue failure modes, burdens partners, and lets a "100% available" SLA hide unbounded latency, so apply it only where needed.

**Rules:**
- P18-1: If a mutation can outlast a client's plausible restart-and-retry interval, accept it fast and make the pending state visible in reads immediately. *Why:* shrinks the gray zone. *Check:* Does the in-progress entity appear in state reads right after the accept response?
- P18-2: Use async tasks only for operations exceeding timeouts, with unpredictable duration, or needing peak-load queuing. *Why:* async everywhere is a single point of failure and complicates client code. *Check:* Is each async endpoint justified by a concrete latency or load reason?
- P18-3: Never return either a result or a task handle from one endpoint depending on runtime conditions, and do not ship parallel sync/async variants. *Why:* clients must maintain two paths. *Check:* Does every endpoint have exactly one response shape?
- P18-4: Give each functional domain its own queue. *Why:* one backlog must not stall all endpoints. *Check:* Can a backlog in one domain delay unrelated endpoints?
- P18-5: Handle and document lost, duplicated, reordered, or mis-attributed tasks. *Why:* queue faults surface as unreproducible client bugs. *Check:* Are delivery, ordering, and uniqueness guarantees stated?
- P18-6: Attach a real completion-time expectation to async work; "eventually" does not satisfy an SLA. *Why:* users need results in reasonable time. *Check:* Is a target or maximum processing time documented?
- P18-7: Express pending work as a status on the domain entity, reusing the future entity id, rather than a separate "task" object; expose progress where useful. *Why:* the best queue does not look like a queue. *Check:* Can clients poll the entity itself?

**Patterns / recipes:**
- *Async operation object with polling*: `POST /reports` → `202 { "report_id": "r5", "status": "queued" }`; `GET /reports/r5` → `{ "status": "running", "progress": 40 }` … `{ "status": "done", "result_url": "…" }`. Trade-off: extra endpoint, queue infra, polling traffic.
- *Pending status on the entity*: `POST /orders` → `{ "order_id": "o7", "status": "new" }` immediately; `GET /orders/ongoing` lists it. Trade-off: "new" must be a first-class domain status.
- *Draft-commit via task confirmation*: create task, then confirm by task id (idempotent).

**Anti-patterns / smells:**
- Read-only endpoints made asynchronous.
- Responses that are sometimes `{ result }` and sometimes `{ task_id }`.
- One global queue for all endpoints.
- Tasks stuck for days still counted as "available."

---

### Chapter 19. Lists and Accessing Them
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-lists

**Core idea (2-3 sentences, own words):** Unbounded lists must be limited, and limiting turns traversal into a correctness problem: offset paging over changing data duplicates or silently skips items. Pick the scheme by data shape: offsets for immutable lists, boundary/cursor traversal for append-only immutable items, and for mutable lists a snapshot, a newest-page-only view, or a reframing into an immutable event log.

**Rules:**
- P19-1: Every list endpoint has a `limit` with a sensible default and a server-enforced maximum. *Why:* unbounded responses fail on large accounts. *Check:* Is there a cap?
- P19-2: Guarantee a client can read the complete dataset exactly once even while items are added or reordered. *Why:* offset paging over live data loses and duplicates items. *Check:* If an item is inserted between page fetches, is every item still returned once?
- P19-3: Use limit/offset only for lists whose contents never change. *Why:* only correct there. *Check:* Is the list truly immutable?
- P19-4: For append-only lists, traverse by a boundary on a strictly monotonic attribute (`newer_than`/`older_than`), not by position; avoid creation timestamps as the anchor, or add a delay window / document instability if forced. *Why:* the tail is stable and cacheable; timestamps tie and skew. *Check:* Does the anchor define an unambiguous total order?
- P19-5: Wrap the anchor in an opaque cursor, fix sort/filter at cursor creation, and always return a cursor even for an empty last page. *Why:* implementation can change, new modes stay compatible, the list can grow at the tail. *Check:* Is the cursor encoded, and present on the final page?
- P19-6: For mutable lists, choose one of: dated snapshot (async task), newest-page-only (search results, take-and-mark queues, raw feeds), or an immutable event log of changes. *Why:* mutable lists cannot be paged consistently. *Check:* Which strategy does the endpoint use?
- P19-7: Return list metadata (`has_more`, count) and hide raw incremental ids behind secondary ids or the cursor. *Why:* convenience; avoids leaking volume. *Check:* Does the response say whether more items exist without exposing auto-increment ids?

**Patterns / recipes:**
- *Boundary traversal*: `GET /events?older_than=ev_900&limit=100` (history, cacheable); `GET /events?newer_than=ev_900&limit=100` (fresh). Trade-off: needs sequential insert guarantees.
- *Cursor pagination*: `POST /offers/search { "order_by": […], "filter": {…} }` → `{ "cursor": "opaque" }`; `GET /offers?cursor=opaque&limit=100` → `{ "items": […], "cursor": "next", "has_more": true }`. Trade-off: no random page access (rarely needed programmatically; a dual `?offset=` interface can serve UI pagers).
- *Snapshot export*: `POST /orders/archive/retrieve { "from": "2020-01-01", "to": "2020-12-31" }` → `{ "task_id" }`; then page the frozen result. Trade-off: compute/storage cost, separate pricing.
- *Newest-page-only queue*: `GET /orders/new` returns top N; partner accepts them, removing them from the list. Trade-off: only works when reads are coupled with a state change.
- *Event-driven list*: `GET /orders/created-history?older_than=ev_1&limit=50` → `{ "events": [{ "id", "occurred_at", "order_id" }] }`. Trade-off: client re-fetches each order for current state.

**Anti-patterns / smells:**
- List endpoint without `limit`.
- Offset/page-number paging over inserted, reordered, or status-sorted data.
- Human-readable cursors partners start crafting by hand.
- Missing cursor used as the end-of-list signal.

---

### Chapter 20. Bidirectional Data Flows. Push and Poll Models
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-push-vs-poll

**Core idea (2-3 sentences, own words):** Polling trades latency for wasted requests; push (duplex sockets, pub/sub brokers, platform notifications, webhooks) improves responsiveness at the cost of connection management and reliability. For public APIs, polling stays the baseline with push as an accelerator; backend-to-backend push is done via webhooks, which make integration quality depend on partner code, so the vendor must design for recovery, documentation, monitoring, and degradation.

**Rules:**
- P20-1: Provide polling over an ordered, cursor-traversable event list as the baseline; add push channels only as an optimization. *Why:* push tech is fragmented, hard to spec, and lossy. *Check:* Can a partner get every event by HTTP polling alone?
- P20-2: Avoid long polling. *Why:* clients cannot distinguish a dead connection from silence. *Check:* Do any endpoints hold responses open for many seconds?
- P20-3: Treat push notifications as triggers for ahead-of-time polling and keep low-frequency polling as a safety net. *Why:* drop rates can reach tens of percent; OSes kill connections. *Check:* Does the client converge to correct state if every push is lost?
- P20-4: Deliver public-API notifications backend-to-backend via webhooks, and let partners relay to their own users. *Why:* partners will not let third parties push to their apps. *Check:* Is the push target the partner's server?
- P20-5: Give webhooks a formal spec for request/response/error formats and a dedicated authentication scheme the partner can verify (prefer mTLS/signatures over IP lists). *Why:* callbacks invert trust direction. *Check:* Can the partner cryptographically verify a callback against a spec?
- P20-6: Treat setting a webhook URL as hazardous: require a second factor, validate the URL, block internal addresses. *Why:* data theft, DoS on third parties, SSRF. *Check:* Does changing the callback URL require extra authorization and validation?
- P20-7: Keep state recoverable independent of webhooks: partners can list missed events or pull full state. *Why:* partners will falsely ack or lose events. *Check:* If every webhook were dropped, could the partner catch up?
- P20-8: Document for webhook consumers: per-message idempotency keys, delivery guarantee, max parallel calls, ordering guarantee or its absence, byte limits, and retry policy. *Why:* exactly what integrators get wrong. *Check:* Are all six present?
- P20-9: Monitor partner endpoint health with tiered escalation and controllable degradation, from throttling up to disconnecting the partner. *Why:* a broken partner must not degrade your platform. *Check:* Is there an automated response to a failing partner endpoint?
- P20-10: For internal flows, prefer message queues over direct calls when guarantees matter, accepting eventual consistency, possibly no ordering, and backlog growth. *Why:* queues fix false negatives and ordering at a cost. *Check:* Are the queue's guarantees acknowledged in the design?

**Patterns / recipes:**
- *Polling on event log*: `GET /events?newer_than=ev_120&limit=200` every N seconds. Trade-off: latency vs. wasted calls; easiest to spec.
- *Duplex connection (WebSocket)*: one connection, frames both ways; web apps needing real-time UI. Trade-off: custom framing, no IDL support, heartbeat logic.
- *Pub/sub broker (MQTT, AMQP)*: client subscribes to a topic. Trade-off: low-level formats, broker ops, awkward for request-response.
- *Platform push (FCM)*: tiny wake-up `{ "type": "orders_changed" }` → app polls. Trade-off: cost, ~4 KB limit, lossy.
- *Webhook*: partner registers `https://partner.example/hook`; vendor `POST`s `{ "event_id", "event_type", "occurred_at", "order_id" }` with a signature header; partner replies `200`. Often implemented as an internal queue feeding a dispatcher with retries. Trade-off: quality depends on partner code.

**Anti-patterns / smells:**
- Push as the only channel, no way to enumerate missed events.
- Webhook URL changeable by a plain API call with no secondary verification.
- Undocumented retry, ordering, or parallelism behavior.
- Trusting a partner's `200` as proof of processing with no reconciliation.

---

### Chapter 21. Multiplexing Notifications. Asynchronous Event Processing
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-async-event-processing

**Core idea (2-3 sentences, own words):** Message size limits force a choice between sending the full entity, sending a reference the partner must fetch, or sending a bare "N items pending" trigger. Thin notifications separate "received" from "processed," so design an explicit follow-up action or ack that proves the partner handled the event; that signal is what makes monitoring and degradation possible.

**Rules:**
- P21-1: Choose deliberately between full-payload, reference, and aggregate notifications based on transport size limits and partner processing needs. *Why:* each implies a different flow. *Check:* Is the notification shape documented with its rationale?
- P21-2: Use full payloads only when the entity cannot contain unpredictably large fields. *Why:* 4 KB push, 256 KB queue, 1 MB webserver limits will be hit. *Check:* Is the maximum message size bounded below all transport limits?
- P21-3: Use aggregate triggers when there are many events per entity, only fresh state matters, or sequential processing is required. *Why:* collapses bursts into one signal. *Check:* Do partners need every intermediate event or just the latest state?
- P21-4: For thin notifications, model "received" and "processed" separately and tie "processed" to a natural follow-up call, or provide an explicit ack endpoint. *Why:* a `200` on a thin message proves nothing; without a processed signal you cannot detect stalled partners. *Check:* Can the vendor measure the partner's processing backlog?
- P21-5: Include `event_id`, `event_type`, `occurred_at`, and identifiers sufficient to fetch full state in every notification. *Why:* idempotent handling and dereferencing. *Check:* Does each message carry a unique id and a fetch handle?

**Patterns / recipes:**
- *Full-state message*: `POST /hook { "event_id", "occurred_at", "order": {…} }`. Trade-off: simplest; size risk; ack ≈ processed.
- *Reference message*: `POST /hook { "event_id", "event_type": "new_order", "order_id": "o7" }` → partner `GET /orders/o7`. Trade-off: extra round-trip; ack ≠ processed.
- *Batch trigger + pull + follow-up*: `POST /hook { "occurred_at", "pending_count": 12 }` → `GET /orders/pending` → `POST /orders/bulk-status-change { "status_changes": [{ "order_id", "new_status": "accepted" }] }`; the status change is the processed signal. Trade-off: robust to bursts; most steps.
- *Explicit ack*: `POST /events/ev_44/ack`.

**Anti-patterns / smells:**
- Webhook payloads with open-ended arrays or uncapped user text.
- Vendor treating HTTP 200 on a reference notification as "handled."
- No visibility into whether a partner has fallen behind.

---

### Chapter 22. Atomicity of Bulk Changes
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-atomicity

**Core idea (2-3 sentences, own words):** A bulk endpoint must define what happens when some sub-requests fail, and every option interacts badly with some plausible partner retry strategy. Bulk mutation endpoints are therefore inherently undesirable; if unavoidable, make them atomic, ship SDKs, always return a per-item breakdown, and group interdependent operations so they execute atomically together.

**Rules:**
- P22-1: Avoid bulk state-change endpoints; with multiplexed transports the gain is marginal. *Why:* non-obvious logic on both sides. *Check:* Could clients use individual calls at acceptable cost?
- P22-2: If unavoidable, make the endpoint atomic and idempotent, and provide SDKs with correct retry handling. *Why:* partial application produces inconsistent states. *Check:* Does any sub-request failure roll back all others?
- P22-3: Always return a per-sub-request breakdown: for atomic endpoints, every validation error that blocked execution; for non-atomic, each item's status and error. *Why:* partners must know what to fix. *Check:* Can a caller identify exactly which item failed and why?
- P22-4: Choose semantics under which a naive blind retry eventually converges. *Why:* idempotent-but-non-atomic and revision-gated designs make retries loop forever. *Check:* Does repeating the same request ever succeed after the obstacle clears?
- P22-5: Group interdependent operations (refund + cancel on one order) into a unit executed atomically; let independent groups run in parallel. *Why:* dependent ops must not half-apply. *Check:* Are dependent operations one atomic group?
- P22-6: Ensure each nested operation is idempotent; if not, derive deterministic per-item tokens like `<item_id>:<outer_token>`. *Why:* retries must not re-apply items. *Check:* Does each sub-operation have a stable idempotency identity?

**Patterns / recipes:**
- *Option A, atomic + idempotent*: all or nothing; same key is a no-op. Best for public APIs; scalability cost; one bad item blocks all.
- *Option B, idempotent, non-atomic*: valid items applied once; failed items never re-run under the same key. Blind retry never fixes failures.
- *Option C, independent items*: each applied on its own; retries re-run everything. Simplest; dependent ops break.
- *Option D, revision-gated*: request carries resource revision; retry rejected as stale. No duplicates, no retries.
- *Grouped bulk request*: `POST /bulk { "changes": [{ "order_id": "o1", "operations": ["refund", "cancel"] }, { "order_id": "o2", "operations": ["accept"] }] }` → `{ "results": [{ "order_id": "o1", "status": "failed", "errors": [{ "op": "cancel", "reason": "already_served" }] }, { "order_id": "o2", "status": "ok" }] }`.

**Anti-patterns / smells:**
- Bulk endpoint returning a single `500` with no per-item detail.
- Refund and cancel as independent items in one bulk call.
- Sub-operations without their own idempotency identity.

---

### Chapter 23. Partial Updates
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-partial-updates

**Core idea (2-3 sentences, own words):** "Send only what changed" PATCH designs are ambiguous (does `null` mean reset, delete, or untouched?), push diffing onto every client, and only pretend to support concurrent editing because operations are order-dependent. The robust answer is to decompose the entity into independently addressable sub-resources replaced in full via PUT/DELETE; true collaborative editing needs an explicit operation log with revisions.

**Rules:**
- P23-1: Never give `null`, `{}`, `false`, omitted fields, or magic prefixes special meanings (reset/skip/delete) in update bodies. *Why:* ambiguous and undocumentable. *Check:* Does any value mean something other than "set to this"?
- P23-2: Do not require clients to compute diffs; the server must detect changes anyway. *Why:* duplicated, divergent logic. *Check:* Can a client safely send the whole sub-resource?
- P23-3: Split composite entities into sub-resources with their own addresses; update each by full idempotent replacement (PUT) or DELETE, where an omitted field means "reset to default." *Why:* removes ambiguity and makes operations on different parts order-independent. *Check:* Can each editable part be replaced in full via its own URL?
- P23-4: Keep read-only/computed fields (created_at, status) out of editable sub-resources. *Why:* avoids "what if the client edits created_at." *Check:* Are editable and computed fields on separate resources?
- P23-5: Return the resulting state from modifying operations. *Why:* otherwise concurrent editors never see each other's changes. *Check:* Do PUT/PATCH responses include the new state?
- P23-6: Declare data immutable only if it can never become editable without a breaking change, or if its reference is API-issued and can be re-issued per version. *Why:* "immutable" data tends to become mutable later. *Check:* Is there a plan if this field ever needs editing?
- P23-7: For real collaborative editing, use an explicit change-operation log with the client's known revision and an idempotency token; escalate order-dependent conflicts to users rather than auto-merging. *Why:* only explicit operations can be replayed and resolved; "edit text" vs. "delete document" has no automatic answer. *Check:* Does the format record the user's actual actions and the revision they saw?

**Patterns / recipes:**
- *Decomposed sub-resources*: `PUT /orders/{id}/parameters { "delivery_address" }`; `PUT /orders/{id}/items/{item_id} { "recipe", "volume", "milk_type" }` (all fields every time); `DELETE /orders/{id}/items/{item_id}`. Trade-off: demands careful decomposition; many calls to change many parts, which tempts bulk endpoints.
- *Field mask / control-op PATCH* (discouraged): `PATCH /orders/{id}?field_mask=items { "items": [{ "__op": "skip" }, { "__op": "delete" }] }`. Trade-off: magic prefixes replace magic values; ordering issues remain.
- *Operation log*: `POST /orders/{id}/changes` + `Idempotency-Key`, body `{ "known_revision": 17, "changes": [{ "type": "set", "field": "delivery_address", "value": "…" }, { "type": "unset_item_field", "item_id": "i2", "field": "volume" }] }` → `{ "revision": 18 }` or `409`. Trade-off: complex; enables offline accumulation and server-side resolution.
- *Versioned references*: updating an image yields a new URL rather than overwriting the old one.

**Anti-patterns / smells:**
- `PATCH` bodies where `null` in an array means "unchanged."
- Positional array updates instead of addressing items by id.
- Empty `200` responses to updates.
- Field-level merges producing states no user ever saw.

---

### Chapter 24. Degradation and Predictability
Link: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-degrading

**Core idea (2-3 sentences, own words):** To the vendor, predictability means stable error metrics; to partner developers it means knowing in advance which errors can occur and what to do about each. Optimistic concurrency beats locks precisely because a revision conflict has an obvious remedy while a lock timeout has none. Design every failure mode by imagining the code the partner must write, including for timeouts, unknown errors, and errors added after their client shipped.

**Rules:**
- P24-1: Every error an endpoint can emit has a documented client reaction, and the response itself carries resolution guidance in two forms: user-facing text and developer detail. *Why:* an error without a remedy is unactionable; the audiences differ. *Check:* Does each error code have a "what to do" entry and does the body carry both messages?
- P24-2: Label non-critical endpoints as such and document the fallback value or behavior, ideally with code samples. *Why:* developers will not guess to wrap them in try/catch. *Check:* Is optional functionality marked with a fallback recipe?
- P24-3: Define a default recovery sequence for transport failures, timeouts, and unrecognized errors, and make sure new error types fall into it safely for old clients. *Why:* network errors bypass your error nomenclature; shipped clients cannot know new codes. *Check:* Does the generic fallback path handle an unknown error gracefully?
- P24-4: Prefer failure modes with clear remedies (re-read and retry on conflict) over ones without (lock timeout). *Why:* partner code must be deterministic. *Check:* Can a partner write a deterministic handler for this error?
- P24-5: If you offer a status meta-API for endpoint availability, do not assume it survives a real outage; fallbacks must trigger when it is unreachable. *Why:* status APIs commonly fail with the main API. *Check:* Does degradation still work with the status endpoint down?

**Patterns / recipes:**
- *Actionable error envelope*: `409 { "error": "stale_revision", "current_revision": 43, "retryable": false, "user_message": "This order changed elsewhere. Reload?", "developer_message": "Re-fetch /orders/{id} and resend with expected_revision=43" }`. Trade-off: per-error design work.
- *Graceful degradation contract*: docs mark `GET /recommendations` optional: "on any error, render without the block." Trade-off: must classify every endpoint's criticality.
- *Default unknown-error procedure*: exponential backoff, re-fetch authoritative state, reconcile, resume; surface to the user after N attempts.
- *Status meta-API*: `GET /status` → `{ "endpoints": { "/orders": "ok", "/recommendations": "degraded" } }`; treat unreachable as degraded.

**Anti-patterns / smells:**
- Errors whose only guidance is "try again later."
- Lock or wait timeouts with no client-side remedy.
- New error codes crashing old clients that assumed a fixed enum.
- Error bodies with one string aimed at neither users nor developers.
