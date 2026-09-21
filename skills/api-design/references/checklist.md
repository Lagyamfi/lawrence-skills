# Master checklist

Yes/no checks grouped by area. Rule IDs point to `rules-0N-*.md` (same folder), where each rule has a *Why* and a *Check*, plus a link to the book chapter. Score 0 (absent), 1 (partial), 2 (met) when reviewing.

Apply the scope gate from `../SKILL.md` first: skip the mutable-entity items in C and E if the API has no mutable, addressable entities; skip D (except the `limit` item) if it has no events or growing lists; skip H if there is no SDK. Mark skipped items `n/a`. Controls delegated to a gateway you cannot inspect (most of F for many services) are `unverifiable`, not 0. Section I items about monetisation, KPIs, support and SLA are answered by the owner, not the code. For inference-style APIs (one heavy pure POST plus metadata GETs) also apply the house rules in `additions.md`.

## Sections

Each line is a yes/no check. The rule ID points to the full rule (with *Why*) in `rules-0N-*.md`.

### A. Contract, naming and data
Book: https://twirl.github.io/The-API-Book/API.en.html#api-design-describing-interfaces

- [ ] Every entity has a one-line reason to exist; nothing is exposed "just in case". (D10-2, B26-1)
- [ ] Names say what an operation does; mutating operations do not look like reads. (D13-2)
- [ ] Expensive operations are visible as such in the signature (e.g. mandatory date range). (D13-2)
- [ ] Sync vs async is visible in the name or signature. (D13-3)
- [ ] Every date, duration, unit, coordinate, money value names its format and unit; money always has a currency code. (D13-4)
- [ ] No abbreviations, no "amoeba" verbs (`get`, `apply`, `make`) without a noun. (D13-5/6)
- [ ] Names imply types: plural for collections, `is_`/`has_` for booleans, `_id` for identifiers, `_at`/`_date` for times. (D13-7)
- [ ] Paired operations share vocabulary, argument order and semantics. (D13-8)
- [ ] No negative flags expected to be `false`; no double negations. (D13-9)
- [ ] No sentinel values (`null`, `-1`, absence) meaning something other than "default". New optional booleans default to `false`. (D13-10)
- [ ] Every field has a documented bound (length, range, size) and a specific error when exceeded. (D13-11)
- [ ] Every request's data volume is capped; every list has `limit`. (D13-12, P19-1)
- [ ] Binary/media data is served from separate endpoints, not Base64 in JSON. (D13-14, H33-6)
- [ ] Fixed-precision numbers (money) are never floats. (D13-23)
- [ ] External identifiers are globally unique and non-sequential, ideally namespaced (`order:<uuid>`). (D13-27, B28-5)
- [ ] No object exposes more than about ten top-level attributes; related fields are grouped, and fields needed for one action are co-located. (D12-14/15)
- [ ] A field name means exactly one thing across all entities. (D11-2)
- [ ] Every endpoint accepts a language; user location is tracked separately from language; all strings UTF-8. (D13-30)
- [ ] The public surface is much smaller than the code behind it; a typical integration is tens of lines. (B26-2)

### B. Validation and errors
Book: https://twirl.github.io/The-API-Book/API.en.html#http-api-errors

- [ ] Invalid input is rejected, never silently clamped or coerced; suspicious input produces a warning, with an optional strict mode. (D13-16)
- [ ] Missing required-in-practice values produce an error, not a plausible default. (D13-17)
- [ ] An empty result set is a success (`200` with empty list). (D13-15)
- [ ] An explicitly empty array filter is treated as "match nothing" or an error, never as "no filter". (D13-15)
- [ ] Every error has a machine-readable `reason`, a user-facing `localized_message`, and developer `details`. (D12-9/12, H38-3/4)
- [ ] Validation errors list all failed checks with field path, error type and constraints, in one response. (D13-18, H38-5)
- [ ] Unresolvable errors are reported before resolvable ones; among resolvable ones, the one needing the biggest change comes first. (D13-19/20)
- [ ] No pair of business rules can produce an error ping-pong the client cannot escape. (D13-21)
- [ ] Every documented error has a stated client reaction; optional endpoints are marked with a fallback. (P24-1/2)
- [ ] There is a default recovery procedure for timeouts and unknown errors, and new error codes degrade safely for old clients. (P24-3)
- [ ] Retryable errors say so and carry `Retry-After`; 5xx bodies say whether the operation is known to have failed. (H38-8/9)
- [ ] Internal error details are stripped at the edge; externally only 500/503 plus guidance. (H38-10)
- [ ] Error kinds are distinguishable in logs without parsing bodies (header such as `X-ApiName-Error-Kind`). (H38-3/13)

### C. Idempotency, concurrency and asynchronicity
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-sync-strategies and https://twirl.github.io/The-API-Book/API.en.html#api-patterns-async

- [ ] Every mutation is idempotent, via natural semantics or an idempotency token scoped per user/resource. (D13-24, P16-2)
- [ ] A client that crashed after any single call can rediscover state and continue. (P14-1)
- [ ] Mutations carry the revision the client last saw (`If-Match`/`expected_revision`) and stale writes fail with a distinct error. (P16-4, H36-9)
- [ ] Revisions are per narrow resource and monotonic (ETag/counter), not timestamps or a global version. (P16-5)
- [ ] No lock primitives are exposed publicly. (P16-3)
- [ ] Reads after writes are consistent by default; if replicas are used, a read-your-writes token is supported and token-less reads hit master. (P17-3/4)
- [ ] Consistency is never relaxed on an existing endpoint. (P17-1)
- [ ] Operations that may exceed a client's retry window are accepted immediately and show a pending status on the entity itself. (P18-1/7)
- [ ] No endpoint returns sometimes a result and sometimes a task handle; no parallel sync/async variants. (P18-3)
- [ ] Each functional domain has its own queue; queue guarantees (loss, duplication, ordering) are documented; completion time expectations are stated. (P18-4/5/6)
- [ ] A published retry policy exists (exponential backoff with a cap) and the SDK implements it. (D13-13, S41-2)

### D. Lists, events and notifications
Book: https://twirl.github.io/The-API-Book/API.en.html#api-patterns-lists and https://twirl.github.io/The-API-Book/API.en.html#api-patterns-push-vs-poll

- [ ] Every list has a `limit` with a default and a server-enforced maximum. (P19-1)
- [ ] Offset pagination is used only on immutable lists. (P19-3)
- [ ] Mutable or growing lists use an opaque cursor that fixes sort and filter, and the cursor is returned even on the last page. (P19-4/5)
- [ ] Genuinely mutable lists use a snapshot export, a newest-page-only view, or an immutable event log. (P19-6)
- [ ] Responses say whether more items exist without leaking auto-increment ids. (P19-7)
- [ ] Polling over an ordered event log is available; push is optional on top. No long polling. (P20-1/2)
- [ ] The client converges to correct state even if every push is lost. (P20-3/7)
- [ ] Webhooks have a spec, verifiable signatures or mTLS, and setting the URL requires extra authorization and SSRF checks. (P20-5/6)
- [ ] Webhook docs state idempotency key, delivery guarantee, parallelism, ordering, size limit, retry policy. (P20-8)
- [ ] Failing partner endpoints are monitored with tiered degradation. (P20-9)
- [ ] Notification payloads are bounded; "received" and "processed" are distinguishable; every message has `event_id`, `event_type`, `occurred_at` and a fetch handle. (P21-2/4/5)

### E. HTTP specifics
Book: https://twirl.github.io/The-API-Book/API.en.html#http-api-requests-semantics and https://twirl.github.io/The-API-Book/API.en.html#http-api-urls-crud

- [ ] Every manipulable entity has its own URL; the URL is the cache key (GET) and idempotency key (PUT/DELETE). (H35-1, H36-1)
- [ ] Path = strict ownership hierarchy; query = loose relations and parameters; version in the path (`/v1/`). (H35-2, H37-1/2)
- [ ] Nesting only where the child can never have another parent. (H37-3)
- [ ] Cross-entity actions get a dedicated resource; action endpoints are readable, not forced into nouns. (H37-4/5)
- [ ] No GET mutates; no body on GET/HEAD/DELETE; PUT/DELETE are idempotent; GET reflects the last PUT/DELETE. (H35-5/6/7/8)
- [ ] Heavy or dynamic operations (rich search) use POST; simple lookups use GET. (H37-6)
- [ ] Creation is safe to retry: idempotency token, or draft then PUT-commit, or client-generated id. (H37-8/9)
- [ ] Deletion is an idempotent archive transition unless physical deletion is truly required. (H37-12)
- [ ] Partial updates are done via addressable sub-resources with full replacement, not diff-style PATCH with magic values. (P23-1/3, H37-11)
- [ ] 4xx for caller faults, 5xx for server faults; status codes used per RFC 9110 meaning, business subtypes in metadata. (H38-1/2, H35-11)
- [ ] 401 for missing/invalid credentials, 403 for permissions, 404 for missing or hidden, 410 for permanently gone, 409 for revision conflict, 429 with `Retry-After`. (H38-7/8/11)
- [ ] Every GET, and every 404, carries explicit `Cache-Control`. (H35-9, H39-12)
- [ ] ETag on reads, `If-None-Match` for revalidation, `If-Match` on writes, `Content-Location` and new ETag on success. (H36-8/9)
- [ ] Custom headers carry a vendor prefix and never change what an operation means; the core operation works with no custom headers. (H35-4, H36-3, H37-7)
- [ ] Trailing slash policy is uniform; one casing rule per component with a written policy. (H35-3/12, H39-7/10)
- [ ] Response root is always a JSON object; `{}` rather than empty body. (H39-11)
- [ ] Standard headers on every response (`Date`, `Content-Type`, `Content-Length`, `Cache-Control`); compression and HTTP/2 enabled. (H39-8, H33-5)
- [ ] OPTIONS and CORS implemented. (H39-9)
- [ ] No custom query-string encodings for arrays/objects; no escapable characters in paths or hostnames. (H39-14/15)
- [ ] Tokens are stateless and self-describing where possible, short-lived, with revocation; authorization compares the request's resource ids to the token's permissions. (H36-5/6/7)
- [ ] CSRF, SSRF, response splitting and open-redirect protections reviewed. (H39-16)

### F. Security, identification and abuse
Book: https://twirl.github.io/The-API-Book/API.en.html#api-product-antifraud and https://twirl.github.io/The-API-Book/API.en.html#api-product-tos-violations

- [ ] Only standard auth protocols (OAuth, mTLS, request signing); nothing home-grown; TLS 1.2+ everywhere. (D13-25, P15-1)
- [ ] Robot accounts (if used) get machine-friendly token flows and are exempt from captchas and forced logouts; API keys can be scoped to endpoints, IPs, referers, apps, geography. (P15-3/4, Q57-8)
- [ ] User-supplied content is sanitised by default; raw modes are explicit opt-ins; parameterised inputs instead of raw scripts. (D13-26)
- [ ] No bulk access to sensitive data; small pages, rate limits and ideally MFA in front of anything sensitive. (D13-29)
- [ ] Rate limits, captcha and "further verification required" responses are in the contract from version one. (D13-28, Q57-3)
- [ ] Different API families (server-to-server, end-user, embeddable widget) live on separate endpoints. (D13-28)
- [ ] Applications and legal owners are modelled separately; keys require a domain or store app id; referer/app-id mismatches are alerted. (Q56-1/2/3)
- [ ] Localhost and the sandbox are whitelisted with unlimited quota. (Q56-4)
- [ ] Detection runs on both tokens and networks; sanctions escalate on a documented ladder; there is a compromised-key runbook. (Q57-1/6/10)
- [ ] Per-partner quotas contain a misbehaving caller. (P14-2)

### G. Backward compatibility and evolution
Book: https://twirl.github.io/The-API-Book/API.en.html#back-compat-statement

- [ ] Semver: major = incompatible, minor = additive, patch = fixes; `v1` resolves to the newest `1.x`. (I7)
- [ ] A written policy states what is breaking, how long majors are supported, how many minors are kept, pinning, alpha/beta channels, and the treatment of undocumented behaviour. (B25, B26-3)
- [ ] No undocumented fields in responses; no private features in samples, talks or support answers. (B26-4)
- [ ] Implicit assumptions in samples (sync callbacks, read-after-write, event order, callback cadence) are documented and preserved. (B26-5/6/7)
- [ ] Extensions are done by generalising: the old call becomes a helper with defaults for the new call; omitting new parameters reproduces old behaviour exactly. (B27-2/3)
- [ ] No field exists because a specific screen displays it; presentation and localisation are separate, partner-extensible contexts. (B28-1/2/3)
- [ ] Lower levels are not told what methods to implement; higher levels publish context state and events that lower levels interpret. (B29-1/2)
- [ ] Every entity names the interface(s) it implements; an alternative (even mock) implementation exists and passes the interface tests. (B30-1, B31-3)
- [ ] Bugs partners rely on are emulated until the next major; nothing incompatible ships in a minor. (B31-1/8)
- [ ] Upstream and third-party APIs are wrapped, never proxied as-is, with rate limiting, retries, caching and fallback in the wrapper. (B31-4/5)
- [ ] Your own products run on the public API, not private shortcuts. (B31-6)
- [ ] A "serenity notepad" of known design debt exists and feeds the next major. (B31-9)
- [ ] Spec changes are assessed as if generated client code were hand-written; contested IDL constructs are avoided. (B25-10/11)

### H. SDKs and UI libraries
Book: https://twirl.github.io/The-API-Book/API.en.html#sdk-problems-solutions

- [ ] SDK converts to native types, naming and error mechanisms. (S41-1)
- [ ] SDK owns retries (idempotent only, backoff, `Retry-After`), auth tokens, idempotency keys and read-your-writes tokens. (S41-2/4)
- [ ] SDK accepts and returns object references and hydrates related entities; pagination is a helper. (S41-3)
- [ ] SDK offers per-entity subscriptions with no lost events between fetch and subscribe. (S41-5)
- [ ] SDK absorbs recoverable business errors (expired offer, revision conflict). (S41-6)
- [ ] SDK is complete (no need to bypass it); generated clients are the base, not the whole SDK. (S41-7)
- [ ] UI components separate look, action and behaviour; conflict policy for overlapping user/developer actions is documented. (S42-1/2)
- [ ] A composer layer sits between top-level components and leaves; siblings never reference each other. (S43-1/3)
- [ ] One-way data flow; only semantic data in the model; serialised state is a versioned contract. (S44-1/3)
- [ ] Shared UI resources are guarded by named, timed locks with a "lost" hook. (S46-1/2/3)
- [ ] Multi-source properties resolve via a small, documented rule mechanism; computed values are readable separately. (S47-1/2)

### I. Product, documentation and operations
Book: https://twirl.github.io/The-API-Book/API.en.html#api-product-documentation

- [ ] Monetisation model and primary KPI (target actions, not raw counts) are written down. (Q50-1, Q55-1)
- [ ] Lineup: base API, SDKs per major platform, higher-level widgets where relevant; separate products only when independently useful, versionable, priced or audienced. (Q54-1/2)
- [ ] Reference spec with prose on every field, documenting side effects and ordering. (Q59-1/2)
- [ ] Production-quality, atomic code samples cross-linked with the reference; live sandbox. (Q59-3/4/5)
- [ ] Tutorial (domain primer, happy paths, error handling, advanced); quick start of ten lines or fewer; FAQ from real tickets. (Q59-6/7/8)
- [ ] Versioned docs with version badge, link to current, de-indexed old versions; downloadable dated snapshot. (Q59-9/10)
- [ ] Sandbox with no-cost side effects, full lifecycle control, selectable failure scenarios, fast-forward, and a manual path. (Q60)
- [ ] First-line support triage, second-line by API developers with budgeted time and a rota; tickets feed the FAQ. (Q58)
- [ ] Published SLA, platform-support policy (dropping a platform is breaking), and a public roadmap with deprecation lead times. (Q61)
- [ ] Capacity survives the largest partner doubling its traffic; vulnerability disclosure process exists. (Q55-6/7)
- [ ] Team members have their own apps built on the public API. (Q51-6)

---

