# Section IV — HTTP APIs & the REST Architectural Principles (Chapters 32–39)

Distilled from "The API" by Sergey Konstantinov (CC BY-NC 4.0). All rules are paraphrased; chapter links point to the original text.

Working definition used throughout this section: an "HTTP API" (or "JSON-over-HTTP API") is one where HTTP is the *application* protocol, not a dumb transport — URLs, verbs, status codes, headers and caching directives are used with the meaning the standard gives them, and bodies are JSON (except dedicated binary/file endpoints). The book deliberately avoids the term "REST API" because it has no agreed definition.

---

### Chapter 32. On the HTTP API Concept. Paradigms of Developing Client-Server Communication
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-concepts

**Core idea (own words):** Client-server protocols oscillated between RPC ("call a remote function as if it were local", convenient but hard to scale, proxy, and shard) and the resource-oriented model HTTP popularised ("apply a small, fixed set of standard operations to an addressable resource, carrying all needed state in the request"). Modern RPC frameworks (gRPC etc.) and HTTP APIs now differ mainly in *what is addressed* (operation name vs. resource) and *how cacheability is signalled*. Calling something an "HTTP API" means committing to use HTTP's own semantics, not merely tunnelling through port 443.

**Rules:**
- H32-1: Decide explicitly whether HTTP is your application protocol or just a transport, and do not mix the two styles in one API. *Why:* half-used semantics confuse both tooling and developers. *Check:* Can you state, for this API, whether status codes/headers/verbs carry meaning, or whether everything meaningful lives in the body?
- H32-2: Address resources (data fragments), not procedures, and pass every parameter the operation needs explicitly in the request. *Why:* explicit, self-contained requests enable sharding, proxying and caching without shared server state. *Check:* Could any request be routed to a fresh server instance with no session memory and still succeed?
- H32-3: Restrict operations to the standard verb set with their standard side-effect semantics rather than inventing per-call operation names. *Why:* intermediaries can only reason about operations whose meaning is standardised. *Check:* Does every endpoint use one of GET/POST/PUT/PATCH/DELETE (plus OPTIONS/HEAD) with the standard's meaning?
- H32-4: Design so that proxies, gateways and caches placed between client and server do not change the protocol contract. *Why:* layering is what lets you scale, cache and secure without touching clients. *Check:* Would inserting a generic caching reverse proxy in front of the API break any call?
- H32-5: Put the identifiers that determine routing/sharding into the URL, not only into the body. *Why:* intermediaries can read URLs without parsing bodies. *Check:* Can a gateway route each request using only the request line and headers?
- H32-6: Let the server mark every response as cacheable or not; never leave caching to client guesswork. *Why:* HTTP's caching model is one of its main scalability advantages, but only if directives are explicit. *Check:* Does each response carry cache-control metadata?

**Reference table — RPC vs. HTTP-style contrast**

| Aspect | Classic / modern RPC | HTTP API (as defined by the book) |
|---|---|---|
| Addressing unit | Operation name; resource ids are parameters | Resource URL; operation is the verb |
| Operation vocabulary | Arbitrary, per-service | Small fixed set with standard side effects |
| Metadata visibility | Inside the body (custom format) | Request line + headers, readable by any agent |
| Caching | Custom, if any | Standard directives, honoured by intermediaries |
| Coupling | Historically tied to language/platform | Language-agnostic text format (JSON) |
| Scaling/sharding | Requires body parsing | Route on URL/headers |

**Anti-patterns / smells:**
- Every request is `POST /api` with the operation name in a JSON field, yet the API is described as "REST".
- Server keeps per-client session state needed to interpret later requests.
- Resource identifiers appear only in the body so a gateway must parse JSON to route.
- Custom "transport" envelope duplicating things HTTP already expresses (status, request id, content type).

---

### Chapter 33. Advantages and Disadvantages of HTTP APIs Compared to Alternative Technologies
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-pros-and-cons

**Core idea (own words):** The decisive property of an HTTP API is that request/response *metadata* (method, URL, status, headers) is readable by every layer in the stack — client libraries, OS, proxies, web servers, API gateways, monitoring — without parsing bodies, so retries, timeouts, logging, routing and dashboards come "for free". The cost is that those same layers will act on your metadata whether you like it or not, and the fragmented, sometimes low-quality tooling and fragmented developer knowledge make mistakes common. Performance complaints about JSON-over-HTTP are mostly about JSON and are largely neutralised by compression, fast parsers, separate binary endpoints and HTTP/2.

**Rules:**
- H33-1: Design every endpoint so that the meaning of the request and the outcome of the response can be determined from metadata alone. *Why:* this is the one thing HTTP gives you that custom protocols do not. *Check:* Looking only at access logs (method, path, status, headers), can you tell what happened to each call?
- H33-2: Do not re-implement in the body what HTTP already expresses (error status, request id, content type, retry hints). *Why:* duplicating creates two sources of truth and hides information from intermediaries. *Check:* Is there any body field whose value should always equal a status code or standard header?
- H33-3: Assume intermediaries will retry, cache, time out, and rewrite based on your metadata, and make that safe. *Why:* you cannot opt out of the ecosystem's behaviour. *Check:* Is every GET safe to auto-retry and cache; is every PUT/DELETE safe to repeat?
- H33-4: Default public APIs to JSON-over-HTTP; reserve gRPC/GraphQL/binary formats for specialised or internal cases with a documented justification. *Why:* broadest developer familiarity and platform reach. *Check:* If the public API is not JSON-over-HTTP, is the reason written down?
- H33-5: Address JSON overhead with compression (gzip/brotli), fast parsers (e.g. simdjson) and HTTP/2 before switching protocols. *Why:* measured differences are small for typical domains once compression is on. *Check:* Is response compression enabled and is HTTP/2 supported?
- H33-6: Serve binary data (images, files) from dedicated endpoints rather than Base64 inside JSON. *Why:* avoids encoding bloat; extra round-trips are cheap with HTTP/2 and server-to-server. *Check:* Are there JSON fields carrying Base64 blobs larger than a few KB?
- H33-7: Do not try to reduce payload by returning field subsets unless there is a proven need. *Why:* partial representations complicate caching and consistency for little gain (cross-ref: Partial Updates chapter). *Check:* Does every GET on a resource return its full representation by default?
- H33-8: Do not maintain dual interfaces (e.g. HTTP + gRPC) for the same API without a strong reason. *Why:* maintenance overhead exceeds the convenience benefit. *Check:* Is there more than one protocol surface for the same operations?

**Reference table — technology choice**

| Technology | Best fit | Main strengths | Main weaknesses |
|---|---|---|---|
| JSON-over-HTTP | Public APIs; general purpose | Universal familiarity, readable, huge tooling ecosystem (nginx/envoy, OpenAPI, Postman), metadata transparent to all agents | Fragmented standard; tooling of uneven quality; developers often ignorant of the spec |
| gRPC | Internal service-to-service; performance-critical | HTTP/2 + Protobuf, contract-first, codegen, single-vendor coherent toolset | Hard to debug/decode, poor browser support, higher entry threshold, vendor lock-in |
| GraphQL | Data-heavy domains with complex entity graphs | Rich field selection and query language | Hard to operate at scale; rarely suitable as an external API |
| XML-based (SOAP, XML-RPC) | Legacy | — | Considered outdated |
| Avro/Thrift/etc. | Specialised ecosystems (e.g. Hadoop) | Ecosystem integration | Niche |

**Anti-patterns / smells:**
- Custom error envelope inside a `200 OK` ("JSON-RPC style") when the API otherwise claims HTTP semantics.
- Complaining about JSON size while not enabling gzip/brotli.
- Base64-encoded files embedded in JSON responses.
- Choosing gRPC for a public partner-facing API without browser/developer-reach analysis.

---

### Chapter 34. The REST Myth
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-rest-myth

**Core idea (own words):** Fielding's 2000 dissertation defines REST as a handful of abstract constraints on any distributed system (client/server independence, statelessness, cacheability, uniform interface, layering, optional code-on-demand) — nothing about HTTP, URLs, verbs, or JSON. Fielding's 2008 clarification (HATEOAS, media-type-driven, no fixed URL templates) is so strict that no real system satisfies it. The popular "RESTful API" is therefore an undefined folk concept; the book keeps Fielding's constraints as useful engineering principles but drops the label.

**Rules:**
- H34-1: Do not use "REST"/"RESTful" as a requirement or a claim in specs and reviews; state the concrete HTTP practices you follow instead. *Why:* the term has no checkable definition and invites arguments. *Check:* Does the API guideline list specific rules (verbs, URLs, status codes, caching) rather than "must be RESTful"?
- H34-2: Treat the Fielding-2000 constraints as design principles to consciously apply, not as a compliance checklist. *Why:* they describe what makes distributed systems scalable, but nearly any system can be argued to "satisfy" them. *Check:* For each constraint below, can you name a concrete design decision in the API that honours it?
- H34-3: Do not chase HATEOAS-style "client with zero prior knowledge"; ship a specification and fixed URL templates. *Why:* clients must know error formats and operations anyway to recover from failures; no production system is truly hypermedia-driven. *Check:* Are URL templates and error formats documented in the spec rather than discovered at runtime?

**Reference table — What REST actually means and what to care about**

| Fielding-2000 constraint | Meaning | Why the book says to care |
|---|---|---|
| Client–server (implementation independence) | Neither side knows the other's internals | Lets you swap servers/gateways, or move gateway logic to the client |
| Stateless | Session state lives on the client; each request carries what it needs | Any server node can serve any request; no token/session lookups on every hop |
| Cacheable | Every response is marked cacheable or not | Standard caches (client, proxy, gateway) work out of the box |
| Uniform interface | Components talk in one standard way | Intermediaries can be inserted or removed without protocol changes |
| Layered system | Any server may be a proxy to another | Enables gateways, sharding, cold/hot storage splits |
| Code on demand (optional) | Server may ship executable code | Contradicts independence; ignore for API design |

| Fielding-2008 addition | Verdict |
|---|---|
| Focus on media types; client agnostic of them | Impractical: client needs prior knowledge of formats |
| No fixed resource names/operations; URLs come from responses (HATEOAS) | No real system does this; do not target it |

**Anti-patterns / smells:**
- Design debates that appeal to "that's not RESTful" without citing an RFC or a concrete consequence.
- Spec that claims HATEOAS compliance while clients hard-code URL templates anyway.
- Rejecting a readable design (e.g. `POST /search`) purely to satisfy a "nouns only" folk rule.

---

### Chapter 35. Components of an HTTP Request and Their Semantics
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-requests-semantics

**Core idea (own words):** A request is verb + URL + version + headers + optional body; a response is version + status + headers + optional body. Each component has standardised semantics (RFC 9110 for core, 9111 for caching, 5789 for PATCH) and the most common and damaging design failures come from violating them: modifying via GET, non-idempotent PUT/DELETE, bodies on GET/DELETE, and breaking the symmetry that a GET must reflect a prior PUT/DELETE. Casing, escaping and case-sensitivity differ per component, so a deliberate consistency policy is needed.

**Rules:**
- H35-1: Give every entity the API can manipulate its own URL. *Why:* the URL is the cache key and idempotency key; granular addressing enables routing and caching. *Check:* Is there any entity that can be modified but has no URL of its own?
- H35-2: Use path segments for strict ownership hierarchies and query parameters for loose relations and operation parameters. *Why:* this is the widely expected convention; deviating causes misreading. *Check:* Does every nested path express a real one-to-many ownership?
- H35-3: Treat `/a/b` and `/a/b/` as the same resource. *Why:* the standard says they differ, but no practical reason exists to distinguish them. *Check:* Does a request with/without trailing slash return the same result or a redirect?
- H35-4: Name custom headers `X-<ApiName>-<Field>` (vendor prefix mandatory; `X-` optional but aids readability). *Why:* proxies add/remove/rewrite headers freely; vendor prefix avoids collisions with present and future standard headers. *Check:* Does every non-standard header carry the vendor/API name?
- H35-5: Never send a body with GET, HEAD or DELETE. *Why:* no meaning is defined, and any intermediary may drop it. *Check:* Is any GET/HEAD/DELETE handler reading a request body?
- H35-6: Never put state-changing logic behind GET. *Why:* caches may serve stale results, agents auto-retry, and link-preview bots issue GETs without user consent. *Check:* Does every GET handler leave server state unchanged?
- H35-7: Make PUT and DELETE genuinely idempotent with the URL as the idempotency key. *Why:* frameworks and agents may repeat them. *Check:* Does executing the same PUT/DELETE twice produce the same end state?
- H35-8: Maintain GET/PUT/DELETE symmetry: after `PUT /x` a `GET /x` returns what was put (normalised, with defaults); after `DELETE /x` a `GET /x` returns 404/410. *Why:* this is what "the URL identifies the resource" means. *Check:* Does `PUT /x` take its identifiers from the URL, not the body, and does GET reflect the last PUT/DELETE?
- H35-9: Remember that `404`, `405`, `410`, `414` are cacheable by default; set explicit cache directives on error responses too. *Why:* a cached 404 can keep clients broken for hours after the resource is restored. *Check:* Do 404 responses carry an explicit `Cache-Control`?
- H35-10: Treat unknown status codes by their first digit (xyz → x00). *Why:* the standard requires it of clients, so servers may rely on it and clients must implement it. *Check:* Does the client SDK fall back to the class behaviour for unrecognised codes?
- H35-11: Use HTTP status codes for protocol-level errors, and add machine-readable subtype metadata for business errors instead of bending codes. *Why:* the code nomenclature was not designed for business logic. *Check:* Is every non-standard use of a status code documented and justified?
- H35-12: Pick one casing per request component and one transformation rule when a parameter moves between components; minimise entropy rather than chase purity. *Why:* domains/headers are case-insensitive, paths/query/JSON are not; mixed conventions cause bugs. *Check:* Is there a written casing policy and does the API follow it uniformly?
- H35-13: Understand the caching RFC before relying on protocol-level caching. *Why:* half-understood caching causes outages. *Check:* Has someone on the team read RFC 9111 and reviewed the cache headers?

**Reference table — HTTP method semantics**

| Method | Semantics | Safe? | Idempotent? | Cacheable response? | Request body? | When to use |
|---|---|---|---|---|---|---|
| GET | Return representation of the resource at URL | Yes | Yes | Yes (per directives; only `no-store`/`no-cache` guarantee revalidation) | No (should not) | Read a resource or a listing; must reflect last PUT/DELETE |
| PUT | Fully replace resource at URL with the enclosed entity | No | Yes (URL is the key) | No | Yes | Overwrite/commit/state transition where the client names the target; idempotent create when the client owns the id |
| DELETE | Remove resource at URL | No | Yes | No | No (should not) | Delete; subsequent GET must give 404/410 |
| POST | Process enclosed entity according to the resource's own semantics | No | No | No (rare exceptions) | Yes | Create with server-generated id, complex searches, actions, anything non-idempotent or computationally heavy — not only "create" |
| PATCH | Partially modify resource at URL | No | No (in general; may be order-dependent) | No | Yes | Partial updates; beware retries |
| HEAD | Like GET, metadata only | Yes | Yes | Yes | No | Rarely used; never return a body |
| OPTIONS | Capabilities / CORS preflight | Yes | Yes | — | No | Must be supported for browser access |

**Reference table — URL components and conventions**

| Component | Case-sensitive? | Typical casing | Use for |
|---|---|---|---|
| Scheme/host/subdomain | No | kebab-case, lowercase | Tenant/partner or environment; no underscores allowed |
| Path | Yes | kebab-case | Strict hierarchies `/places/{id}/coffee-machines/{id}`; avoid chars needing escaping |
| Query | Yes | snake_case (book's choice, so a param can move to a JSON body unchanged) | Many-to-many relations `/recipes?partner=<id>`, operation params `/search?recipe=lungo` |
| Fragment | context-dependent | — | Not sent to server; do not rely on it |
| Headers (names) | No | Kebab-Case with `X-ApiName-` prefix | Metadata, auth, content negotiation, conditional requests |
| JSON body fields | Yes | snake_case or camelCase (pick one) | Data |

Same parameter, different possible homes (choose one, keep it consistent): subdomain `{partner}.api.tld`, path `/v1/{partner}/orders`, query `/v1/orders?partner_id=`, header `X-ApiName-Partner-Id`, body field.

**Anti-patterns / smells:**
- `GET /orders/{id}/cancel` or any GET that writes.
- `DELETE /list/{id}?position=3` (non-idempotent; breaks GET/DELETE symmetry).
- `PUT /orders` with the id inside the body.
- `GET /x` still returning the entity after `DELETE /x` succeeded.
- Handlers that require a body on DELETE.
- Custom headers like `X-Token`, `X-Version` without a vendor prefix.
- Same field spelled `userId`, `user_id`, `User-Id` in different components with no stated rule.
- 404 responses with no cache headers on frequently-fetched resources.

---

### Chapter 36. Organizing HTTP APIs Based on the REST Principles
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-rest-organizing

**Core idea (own words):** Applying stateless/cacheable/uniform/layered to HTTP concretely means: the URL identifies the resource (serving as cache key for GET and idempotency key for PUT/DELETE), verbs mean what the spec says, and headers/status codes align with the standard. The worked example shows that `GET /state` with a bearer token bundles authentication, identification and authorization into one stateful call; refactoring to explicit identifiers (`/profiles/{user_id}`, `/orders?user_id=`), stateless tokens (JWT), and ETag/If-None-Match/If-Match lets a gateway, a proxy, or the client itself cache and coordinate using stock HTTP machinery — and the gateway becomes optional.

**Rules:**
- H36-1: Make the URL point at the resource being operated on so that it doubles as cache key (GET) and idempotency key (PUT/DELETE). *Why:* standard caches and retry logic keep to that contract. *Check:* Do two requests with the same URL and method target the same resource?
- H36-2: Pass operation parameters explicitly (e.g. `user_id` in the URL) rather than deriving them from a server-side session or a token lookup. *Why:* downstream services stay in their own responsibility area and need no shared state. *Check:* Could a downstream microservice serve the request without calling the auth service?
- H36-3: Keep an endpoint executable with no headers at all; headers may add auxiliary behaviour but must not define the operation. *Why:* headers are freely manipulated by intermediaries. *Check:* If all custom headers were stripped, would the core operation still be unambiguous?
- H36-4: Let each service own only its data; external entities are opaque context identifiers, and any external checks reduce to integrity checks. *Why:* separation of abstraction levels; avoids fan-out to auth on every hop. *Check:* Does the orders service interpret user tokens, or only compare identifiers?
- H36-5: Prefer stateless, self-describing tokens (e.g. JWT with `user_id`/`user_ids`, `iat`) that each service can verify locally. *Why:* removes the auth service as a per-request bottleneck. *Check:* Can services validate the caller without a network call to a token store?
- H36-6: Always compare the resource identifier in the request against the permissions in the token; do not assume "the caller is the owner". *Why:* who acts and on whom are distinct semantics; delegation (X acts for Y) will be needed. *Check:* Does the authorization check explicitly compare request `user_id` with the token's allowed ids?
- H36-7: Keep stateless tokens short-lived and keep a revocation/issuance cache. *Why:* permissions baked into a token cannot be changed until it expires. *Check:* What is the token TTL, and is there a revocation list?
- H36-8: Expose a revision as `ETag` on GET and accept `If-None-Match` so caches (gateway or client) can revalidate with `304`. *Why:* reuses the framework's caching for free. *Check:* Does a GET on a frequently-read, occasionally-changing resource return an ETag and honour If-None-Match?
- H36-9: Reuse the same revision for optimistic concurrency on writes via `If-Match`, and return the new `ETag` (with `Content-Location`) on success. *Why:* one mechanism gives both caching and conflict detection. *Check:* Do modifying endpoints accept If-Match and return the updated ETag?
- H36-10: Design so that gateway functions could be moved to the client or another proxy without changing services. *Why:* that is the practical test of a uniform, layered interface. *Check:* Could the gateway be deleted and the client call the services directly?

**Reference table — from stateful monolith to REST-aligned mesh**

| Step | Before | After |
|---|---|---|
| Identity | `GET /state` + bearer token; server resolves token to user | `GET /profiles/{user_id}`, `GET /orders?user_id=`; gateway or JWT supplies id |
| Auth fan-out | Every service calls token service | Services decode JWT locally; compare request id vs. token payload |
| Profile caching | Impossible (bundled response) | Gateway/client caches `/profiles/{user_id}` via standard cache headers |
| Orders freshness | Impossible | `ETag` + `If-None-Match` → `304 Not Modified` |
| Order creation | Blind write | `POST /orders?user_id=` with `If-Match: <rev>`; response `201` + `Content-Location` + new `ETag` |
| Access model | Auth+identify+authorize fused in one endpoint | Three separable steps; token may carry `user_ids` list for delegation |

**Header conventions used here**

| Header | Direction | Purpose |
|---|---|---|
| `Authorization: Bearer <token>` | Request | Carry credentials; stateless token preferred |
| `ETag` | Response | Resource revision; cache validator and concurrency token |
| `If-None-Match` | Request (GET) | Revalidate cache; expect `304` |
| `If-Match` | Request (write) | Optimistic concurrency / idempotency guard |
| `Content-Location` | Response (write) | URL of the representation returned in the body |
| `Cache-Control` | Response | Explicit cacheability |

**Anti-patterns / smells:**
- `GET /profile` / `GET /state` endpoints whose subject is implied by the token.
- Every microservice calling the auth service to translate token → user.
- Services that must keep a token cache in memory to function.
- Order creation with no revision/idempotency guard.
- Gateway logic (merging, caching) that cannot be reproduced by a generic proxy.

---

### Chapter 37. Designing a Nomenclature of URLs. The CRUD Operations
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-urls-crud

**Core idea (own words):** No standard prescribes URL semantics; conventions (path = strict hierarchy, query = loose relations/parameters) exist for readability and should be followed because ignoring them gets you misunderstood. Where conventions are ambiguous (versioning, format, cross-entity actions, nouns-vs-verbs, GET-vs-POST for searches), optimise for concise, readable signatures. CRUD-to-verb mapping is only a mnemonic: real systems need idempotent creation, drafts/commits, search, archiving and atomic actions, so expect ~8 URLs and ~10 methods per major entity.

**Rules:**
- H37-1: Follow the default path/query convention even though it is not a standard. *Why:* defying widespread expectations makes the API harder to read. *Check:* Are nested paths used only for unequivocal ownership and query params for everything else?
- H37-2: Put the major API version in the path (`/v1/...`). *Why:* other schemes only pay off if URL nomenclature survives a major version, in which case you should not have broken compatibility at all. *Check:* Does every URL start with a version segment?
- H37-3: Nest paths only when the subordination is certain to hold; otherwise create a new root prefix. *Why:* hierarchies that later become many-to-many force URL breakage. *Check:* For each nested path, could the child ever belong to more than one parent?
- H37-4: For operations that span entities of different abstraction levels, create a dedicated resource with the participants as query/body params (e.g. `/prepare?coffee_machine_id=&recipe=`). *Why:* avoids arbitrary choice of which entity "owns" the action. *Check:* Do cross-entity actions have their own root resource instead of being nested under one participant?
- H37-5: Do not contort names into "-ator" nouns to satisfy a "nouns only" rule; prefer readable signatures. *Why:* the rule is folklore, not standard, and hurts readability. *Check:* Are action endpoints named for what they do (e.g. `/cancel`, `/prepare`) rather than artificial nouns?
- H37-6: Verb semantics win over misleading side-effect signals; use POST for algorithmic/heavy or non-cacheable operations (e.g. rich search) even if they are technically safe. *Why:* POST signals "processing" and prevents caching of dynamic results. *Check:* Are heavy or dynamically computed operations behind POST, with simple lookups behind GET?
- H37-7: Never let metadata (headers, etc.) change what an operation means. *Why:* headers may be stripped in transit. *Check:* Is there any endpoint whose semantics differ based on a custom header?
- H37-8: Provide idempotent creation: POST with an idempotency token (`If-Match: <revision>`), or a draft/commit pair (`POST /drafts` → `PUT /drafts/{id}/commit`), or client-generated ids with PUT (rarely). *Why:* timeouts on create otherwise produce duplicates. *Check:* Can a client safely retry a create after a timeout without duplicating the entity?
- H37-9: Prefer draft-then-PUT-commit over relying on retrying POST for heavy creates. *Why:* PUT is idempotent by contract, so retries are legitimate even if the revision check is relaxed later. *Check:* Is the expensive step behind an idempotent verb?
- H37-10: Provide a separate enumerator resource with pagination (cursor) and simple filters for listings; move rich/multi-valued filters to a POST search endpoint. *Why:* query strings have no standard for structured values. *Check:* Are list endpoints paginated, and do complex filters use a body?
- H37-11: For complex or collaborative updates, decompose into atomic nested PUT handlers or a change-list resource with draft/commit rather than a single PUT/PATCH. *Why:* whole-resource PUT fights computed/immutable fields; PATCH is non-idempotent. *Check:* Do partial updates have an idempotent, conflict-aware path?
- H37-12: Do not delete; archive via an idempotent state transition (`PUT /orders/{id}/archive`). *Why:* real systems never physically delete. *Check:* Is there a DELETE endpoint that actually destroys data?
- H37-13: Expose attached media via sub-resources (`/orders/{id}/attachments/{id}`). *Why:* binary belongs on its own endpoints. *Check:* Are attachments addressable independently?
- H37-14: Keep parameters that need escaping out of paths and domains; use query or body. *Why:* escaping rules for `/ ? #` are inconsistent. *Check:* Can every path segment be plain alphanumerics/kebab-case?
- H37-15: In internal systems you may keep fixed paths and pass all ids as query params for gateway-friendliness; do not do this in public APIs. *Why:* declarative proxies rewrite paths trivially, but public readers expect semantic paths. *Check:* Is the URL style choice matched to the audience?

**Reference table — URL structure conventions**

| Need | Convention | Example |
|---|---|---|
| Strict parent/child | Nested path | `/partners/{id}/coffee-machines/{id}` |
| Many-to-many / loose relation | Query on the owning collection | `/recipes?partner=<id>` |
| Operation parameters | Query (GET) or body (POST) | `/search?recipe=lungo` |
| Cross-entity action | Dedicated root resource | `/prepare?coffee_machine_id=<id>&recipe=lungo` |
| Version | Path prefix | `/v1/orders/{id}` |
| Response format | `Accept` header (URL "extension" is a readability trade-off) | — |
| Atomic action on entity | POST/PUT sub-resource | `POST /orders/{id}/cancel`, `PUT /orders/{id}/archive` |
| Trailing slash | Pick one policy; book suggests trailing `/` so root ops read as `VERB /` | `/v1/orders/` |

**Reference table — CRUD mapping and its real-life expansion**

| Intent | Mnemonic | What actually works |
|---|---|---|
| Create | `POST /orders` | `POST /orders?user_id= + If-Match`, or `POST /orders/drafts` → `PUT /orders/drafts/{id}/commit`; `201 Created` + `Location` |
| Read one | `GET /orders/{id}` | Same, with `ETag`/cache headers |
| Read many | — | `GET /orders?user_id=&cursor=` with simple filters; `GET`/`POST /orders/search?user_id=` for rich queries |
| Update | `PUT`/`PATCH /orders/{id}` | Atomic nested `PUT /orders/{id}/address`, or `POST /orders/{id}/drafts` → `PUT /orders/{id}/drafts/{id}/commit` |
| Delete | `DELETE /orders/{id}` | `PUT /orders/{id}/archive` |
| Non-CRUD action | — | `POST /orders/{id}/cancel` (non-idempotent) or `PUT .../{action}` (idempotent transition) |
| Media | — | `GET /orders/{id}/attachments/{id}` |

**Anti-patterns / smells:**
- Deep nested paths that encode a relation likely to become many-to-many.
- `DELETE` with positional or body-supplied selectors.
- Multi-valued filters crammed into custom query syntaxes (`?recipe=lungo|latte`, JSON in query).
- Physical deletes in a domain with audit needs.
- A single `PUT /orders/{id}` used for every kind of update, including collaborative edits.
- Version passed via header or query when URLs would be broken anyway.
- Semantics hinging on a custom header.

---

### Chapter 38. Working with HTTP API Errors
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-errors

**Core idea (own words):** An error response must tell three audiences (user, client app, server operators) who is at fault, whether/when to retry, whether reformulating helps, and what to do otherwise. HTTP answers "who" (first digit) and "when" (`Retry-After`) but its codes cannot express business-logic subtypes, and abusing near-synonymous codes breaks uniformity and monitoring. The standards-compliant approach is a mixed one: correct status code for the error *family*, plus a machine-readable error kind in a header and a structured body with separate developer and user messages.

**Rules:**
- H38-1: Use the status code class correctly: 4xx = caller's fault, 5xx = server's fault. *Why:* every intermediary relies on the first digit. *Check:* Is any server failure reported as 4xx, or any client mistake as 5xx?
- H38-2: Restrict business errors to a small, semantically correct code set (400/422, 403, 404, 409, 410, 429) and distinguish causes with metadata, not with more codes. *Why:* choosing codes by keyword similarity violates the spec and confuses agents. *Check:* Is each status code used in accordance with RFC 9110's description, not its name?
- H38-3: Include a machine-readable error subtype both in a header (`X-ApiName-Error-Kind`) and in the body (`reason`). *Why:* monitoring reads headers without parsing bodies; clients need the body. *Check:* Can the error type be read from headers alone?
- H38-4: Separate a developer-facing `message`/`details` from a user-facing `localized_message`. *Why:* users need actionable text; developers need diagnostics. *Check:* Does every error body contain both?
- H38-5: For validation errors, list every failed check with field path, error type, constraints and message. *Why:* lets clients fix all problems in one round-trip. *Check:* Does a 400 for two bad fields report both?
- H38-6: Make the 400 error format the most general one, since clients must treat unknown 4xx as 400. *Why:* graceful degradation for unrecognised codes. *Check:* Is every 4xx body a superset-compatible shape of the 400 body?
- H38-7: Use `404` when the referenced entity is missing *or* when you intentionally hide the real cause; use `410` only for permanently gone resources. *Why:* 404 legitimately permits retry with a different outcome; 410 does not. *Check:* Are permanently deleted resources returning 410, not 404?
- H38-8: Send `Retry-After` on 429 and on 500/503 when the client should retry. *Why:* it is the one standard retry hint every agent understands. *Check:* Does every retryable error response include `Retry-After`?
- H38-9: In the body of a 5xx, state whether the request can be retried and whether the operation is known to have failed (`can_be_retried`, `is_operation_failed: "unknown"`). *Why:* the client cannot otherwise decide between retrying and re-reading state. *Check:* Does the 5xx format tell the client how to recover?
- H38-10: Externally, expose only 500 and 503 (plus Retry-After); internally, tag 5xx with machine-readable subtypes and strip them at the boundary gateway. *Why:* internal monitoring needs detail; public clients must not see internals. *Check:* Does the edge gateway rewrite internal error headers/bodies into client instructions?
- H38-11: Return 401 only in the de-facto sense (missing/invalid credentials → prompt login), knowing the spec technically requires `WWW-Authenticate`; use 403 for permission problems. *Why:* aligning with common client behaviour while not mixing "who are you" with "you may not". *Check:* Are authentication failures 401 and authorisation failures 403?
- H38-12: Document retry policy for unsafe operations explicitly in the docs; do not assume clients read error bodies for 5xx. *Why:* developers rarely see 5xx during development. *Check:* Does the documentation say which POST/PATCH calls are safe to retry and how?
- H38-13: Never make monitoring depend on status code alone; distinct error kinds (wrong password vs. expired token) must be distinguishable in logs. *Why:* different causes need different alerts (brute force vs. client bug). *Check:* Can dashboards split 4xx by error kind?

**Reference table — status code selection**

| Situation | Code | Retry? | Notes |
|---|---|---|---|
| Malformed request / syntax | 400 | No | Purists: 400 = format, 422 = logical; either way add subtype |
| Logical validation failure | 400 (or 422) | After fixing | List all failed checks |
| Missing/invalid credentials | 401 (de-facto) | After login | Spec wants `WWW-Authenticate`; nobody sends it |
| Authenticated but not permitted | 403 | No | Includes deactivated user |
| Entity missing or cause hidden | 404 | Maybe (state of uncertainty) | Cacheable by default — set `Cache-Control`! |
| Verb not applicable to resource | 405 | No | Protocol-level |
| Cannot satisfy `Accept*` | 406 | No | Protocol-level |
| Data integrity / revision mismatch | 409 | After re-reading state | Use for `If-Match` failures |
| Permanently deleted | 410 | No | Cacheable by default |
| Body length required | 411 | Yes, with header | Client may auto-fix |
| URI too long | 414 | No | Cacheable by default |
| Quota/rate limit exceeded | 429 | Yes, after `Retry-After` | No standard way to say *which* limit; use subtype |
| Unknown server error | 500 | Per `Retry-After` / body | Outcome of operation may be unknown |
| Temporary overload/maintenance | 503 | Yes, after `Retry-After` | Could be folded into 500 + Retry-After |
| Success, no body | 204 | — | Not extensible; prefer `200 {}` |
| Created | 201 | — | Add `Location` (and/or `Content-Location` + `ETag`) |
| Not modified | 304 | — | Reply to `If-None-Match` |

**Reference table — three strategies for error nomenclature**

| Strategy | Description | Book's verdict |
|---|---|---|
| 1. Extended status codes | New/unusual code per error type | Violates the standard; avoid |
| 2. Everything in 200 + custom envelope (2a: only 400/500[/404]) | RPC-style | Works, but opaque to intermediaries/logs |
| 3. Mixed | Correct code for the family + subtype header + structured body | Only standard-compliant option; modest but real gains in log readability and proxy transparency |

**Recommended error body shape (book's example, paraphrased):**

```json
{
  "reason": "<machine-readable kind>",
  "localized_message": "<text for the end user>",
  "details": {
    "checks_failed": [
      { "field": "recipe", "error_type": "wrong_value", "message": "..." },
      { "field": "volume_ml", "error_type": "out_of_range",
        "constraints": { "min": 50, "max": 500 }, "message": "..." }
    ],
    "can_be_retried": true,
    "is_operation_failed": "unknown"
  }
}
```
Plus header `X-ApiName-Error-Kind: <reason>` and `Retry-After` where relevant. RFC 9457 (Problem Details) is acceptable but covers only the basic case: no subtype in metadata, no user/developer message split, machine-readable details left to you.

**Anti-patterns / smells:**
- Status codes chosen because the name "sounds like" the error (e.g. 402, 418, 451 for business states).
- Single generic `"error": "Something went wrong"` with no `reason`.
- Same code for wrong password and expired token with no distinguishing field.
- 429 without `Retry-After`.
- Internal `db_timeout` details leaking to public clients.
- 404 used for permanently deleted resources; 410 never used.
- Retryability discoverable only by trial.

---

### Chapter 39. Final Provisions and General Recommendations
Link: https://twirl.github.io/The-API-Book/API.en.html#http-api-final-recommendations

**Core idea (own words):** Designing an HTTP API is a process: map the happy path as HTTP calls, recast each call as verb-on-resource, enumerate failures and recovery paths, decide exactly which protocol features you will rely on, write the spec, then validate by writing client pseudo-code against it. Layer on a short set of hygiene rules (slashes, standard headers, CORS, casing, extensible JSON roots, explicit caching, no grey-zone tricks, security basics). HTTP remains the default choice for public APIs; anything else needs justification.

**Rules — design process:**
- H39-1: Draw the full sequence of HTTP calls for a normal application session before designing endpoints. *Why:* the happy path reveals the real resources and their lifecycles. *Check:* Is there a call-flow diagram for the primary use case?
- H39-2: Recast each call as an operation on a resource and derive the URL nomenclature and applicable methods from that. *Why:* keeps URLs resource-centric and consistent. *Check:* Does every endpoint map to a named resource and a standard verb?
- H39-3: Enumerate every error each operation can raise and define how the client recovers. *Why:* recovery paths are part of the contract. *Check:* For each endpoint, is there a documented list of errors with recovery actions?
- H39-4: Decide explicitly which HTTP features (caching, conditional requests, content negotiation, CORS, etc.) the API relies on and with which tooling. *Why:* unstated reliance on protocol features leads to inconsistent behaviour. *Check:* Does the spec state the protocol capabilities in use?
- H39-5: Write a detailed specification covering the above (e.g. OpenAPI). *Why:* the contract must be explicit. *Check:* Is there a machine-readable spec that matches the implementation?
- H39-6: Validate by writing client pseudo-code for the business logic against the spec and judging its readability. *Why:* the API is only good if the consuming code is pleasant. *Check:* Has anyone written a sample client against the spec before shipping?

**Rules — code style:**
- H39-7: Treat trailing and non-trailing slashes as equivalent; adopt a default (book prefers trailing `/`), and redirect or give a clear error for the other form. *Why:* consistency and root-resource readability (`VERB /`). *Check:* Is slash handling uniform across all routes?
- H39-8: Always emit standard response headers (`Date`, `Content-Type`, `Content-Encoding`, `Content-Length`, `Cache-Control`, `Retry-After` where applicable). *Why:* never make clients guess protocol defaults. *Check:* Does every response include these headers?
- H39-9: Implement `OPTIONS` and CORS. *Why:* browser clients will appear sooner or later. *Check:* Does a preflight from a browser origin succeed?
- H39-10: Fix one casing rule per component and one transformation rule for moving parameters between components. *Why:* prevents naming drift. *Check:* Is the casing policy written and enforced?
- H39-11: Always return a JSON object at the response root; return `{}` rather than an empty body for 200 (204 is allowed but not extensible). *Why:* objects can gain fields without breaking clients; empty string is invalid JSON. *Check:* Does any endpoint return an array, primitive, or empty body with 200?
- H39-12: Set explicit caching directives on every GET response. *Why:* otherwise clients and proxies invent their own policy. *Check:* Does every GET carry `Cache-Control` (and `ETag`/`Last-Modified` where useful)?
- H39-13: Do not exploit grey zones: no unsafe GET, no non-idempotent PUT/DELETE, keep GET/PUT/DELETE symmetry, no bodies on GET/HEAD/DELETE requests, no bodies with HEAD responses or 204. *Why:* intermediaries will behave per the standard, not per your intent. *Check:* Does a linter/route review enforce these constraints?
- H39-14: Do not invent query-string encodings for arrays or nested objects; switch to a body-carrying verb, or as a last resort pass Base64-encoded JSON. *Why:* no standard exists, so every client/proxy parses differently. *Check:* Are structured parameters only in bodies?
- H39-15: Keep values needing escaping (non-alphanumerics) out of path and domain; put them in query or body. *Why:* escaping rules differ and are inconsistently implemented. *Check:* Are all path segments and hostnames plain identifiers?
- H39-16: Know and mitigate at the web-server level: CSRF, SSRF, HTTP response splitting, unvalidated redirects/forwards; follow the OWASP REST security cheat sheet. *Why:* these are the standard attack vectors against HTTP APIs. *Check:* Has a security review covered these four vectors?
- H39-17: Default public APIs to HTTP; document the justification if choosing another technology. *Why:* HTTP has the deepest shared vocabulary and tooling. *Check:* Is any non-HTTP public surface backed by a written rationale?

**Reference table — checklist of chapter 39 items**

| # | Item | Verify by |
|---|---|---|
| 1 | Happy-path call diagram | Diagram exists |
| 2 | Resource+method nomenclature | Every route = verb + resource |
| 3 | Error enumeration + recovery | Per-endpoint error table |
| 4 | Explicit choice of HTTP features/tooling | Stated in spec |
| 5 | Detailed spec | OpenAPI or equivalent |
| 6 | Self-check via client pseudo-code | Sample client written |
| 7 | Trailing slash policy | Redirect/error for the other form |
| 8 | Standard headers present | Inspect responses |
| 9 | OPTIONS + CORS | Preflight succeeds |
| 10 | Casing rules | Written policy |
| 11 | JSON object root, `{}` not empty | No array/primitive roots |
| 12 | Explicit caching on GET | `Cache-Control` present |
| 13 | No grey-zone verb usage | Route audit |
| 14 | No custom query encodings | Structured params in bodies |
| 15 | No escapable chars in path/domain | Path audit |
| 16 | CSRF/SSRF/response splitting/redirect protections | Security review |
| 17 | HTTP as default for public APIs | Rationale for exceptions |

**Anti-patterns / smells:**
- Endpoints designed before any end-to-end call flow was sketched.
- Responses without `Content-Type` or `Cache-Control`.
- Top-level JSON arrays in responses.
- `200 OK` with an empty body.
- `?ids[]=1&ids[]=2` or JSON-in-query conventions.
- User-supplied strings (emails, names) embedded in path segments.
- No CORS/OPTIONS support because "only our backend calls it".
- No spec, or a spec that drifts from the implementation.
