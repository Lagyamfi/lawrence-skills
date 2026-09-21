# The API Book — Distilled: Introduction (Ch. 1–8) and Section I: The API Design (Ch. 9–13)

Source: Sergey Konstantinov, *The API*, CC BY-NC 4.0 — https://twirl.github.io/The-API-Book/API.en.html
Rule prefixes: `I<n>-` = Introduction chapter n; `D<n>-` = Design chapter n (book chapter numbering, so Ch. 9 → `D9-`, Ch. 13 → `D13-`).

---

## Introduction — key takeaways at a glance

- **What an API is:** a formal, *programmable* obligation (contract) that connects two distinct programmable contexts. Its consumers are engineers who build their own structures on top of it, so every API flaw is multiplied through them.
- **Definition of a good API:** one that lets developers go from "task stated" to "correct code written" with the least friction, and that keeps that property as it grows over time.
- **Quality criteria:** (1) *obviousness* — the structure itself reveals which entities solve a task, on both the happy and unhappy paths; (2) *readability* — correct code can be written from the nomenclature alone, without knowing implementation details; (3) *consistency* — new, previously unseen parts of the API behave like the parts already learned, and the API respects the conventions of its host platform. The hard part is preserving these while the API is extended.
- **API-first (technical sense):** the contract, as a machine-readable spec (OpenAPI, .proto, ...), is written and committed *before* implementation; when spec and implementation disagree, the implementation is the thing that gets fixed.
- **Backward-compatibility stance:** breaking compatibility is a hidden tax levied on partners; if a break can be avoided, never break. Old versions cost too, so a break is eventually inevitable — but must be justified and explained.
- **Versioning:** semver (`MAJOR.MINOR.PATCH`). MAJOR = incompatible change; MINOR = compatible additions; PATCH = fixes only. "Major version" and "backward-incompatible version" mean the same thing. `v1`, `v2` shorthand refers to the latest stable release of the `1.x.x` / `2.x.x` family.
- **Terminology:** *entity* = any atomic unit of functionality (class, method, object, endpoint...), with *fields* and *methods*; *client* / *agent* / *user agent* = the application running on the user's device (native or web); *partner* = the external developer/company integrating the API; *API vendor / provider* = the party publishing the contract; *contract / specification* = the formal, IDL-expressed obligation; *SDK* = vendor-provided code that wraps the contract for a specific platform. Examples are written as JSON-over-HTTP purely as notation: `GET /v1/orders` is interchangeable with `orders.get()`.

---

### Chapter 1. On the Structure of This Book
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-structure

**Core idea:** API development is its own engineering discipline, distinct from general software development. The book moves from technology-agnostic theory (design, patterns, backward compatibility) to concrete tech (HTTP/REST, SDKs/UI libraries) and finally to the API as a product, and expects readers to already be practicing engineers.

**Rules:**
- I1-1: Treat API work as a separate discipline with its own lifecycle, not as a by-product of building a service. *Why:* the constraints (contract, external consumers, compatibility) differ from ordinary code. *Check:* Does the team have a distinct design/review step for the public contract, separate from feature implementation?
- I1-2: Involve product and engineering jointly in API decisions. *Why:* developer-facing products only thrive when both sides own them. *Check:* Are non-engineering concerns (positioning, support, KPIs) considered when the API is designed?

**Anti-patterns / smells:** the "API" is whatever endpoints the app happens to call; no one owns the contract as an artifact.

---

### Chapter 2. The API Definition
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-api-definition

**Core idea:** An API is a formal obligation to connect two programmable contexts — the Roman aqueduct metaphor: it links two areas and has never broken compatibility. Your customers are engineers plugging their own pipes into yours; you cannot control their quality, but you will be blamed for their failures, so an API amplifies both your reach and your mistakes.

**Rules:**
- I2-1: Design the API as a long-lived contract, not as an implementation detail. *Why:* others build on it and cannot inspect or change your internals. *Check:* Could the implementation be replaced entirely without partners noticing?
- I2-2: Hide the distributed-system topology behind the contract. *Why:* clients should not need to know how many sources/destinations serve them. *Check:* Does any client need to know which internal service/node handles a request?
- I2-3: Assume every design flaw will be multiplied by the number of consumers. *Why:* an API is a multiplier of both opportunities and mistakes. *Check:* Has the cost of a flaw been assessed as "N partners × their users", not "one bug"?

**Anti-patterns / smells:** partners must read your source code to use the API; internal deployment topology leaks into URLs or IDs.

---

### Chapter 3. API Quality Criteria
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-api-quality

**Core idea:** A high-quality API minimises the distance between formulating a task and writing working code. It must be obvious, readable and consistent — but the real difficulty is keeping these qualities as the API grows; the design principles in the book exist to make evolution smooth, at the cost of some upfront redundancy that is only worth paying if the API has a future.

**Rules:**
- I3-1: Make the entity structure reveal how to solve a task at first glance. *Why:* obviousness shortens the task-to-code gap. *Check:* Can a newcomer name the entities needed for a common task from the method list alone?
- I3-2: Make the unhappy path as obvious as the happy path. *Why:* error handling is part of the developer's task. *Check:* Are the errors of each operation and their handling discoverable from the contract?
- I3-3: Ensure code can be written correctly from names alone, without implementation knowledge. *Why:* readability. *Check:* Does any correct usage depend on knowing how the server is implemented?
- I3-4: Keep new functionality consistent with existing concepts so code written "by analogy" works. *Why:* consistency lets learning transfer. *Check:* If a developer mimics an existing call for a new entity, does it work?
- I3-5: Follow the conventions of the host platform/framework. *Why:* fits developer expectations. *Check:* Does the API contradict platform idioms (naming, error style, async style)?
- I3-6: Invest in extensibility only proportionally to the API's expected lifetime. *Why:* reserved growth points add complexity; without a future it is overengineering. *Check:* Is each abstraction justified by a concrete plausible extension?

**Anti-patterns / smells:** each new feature adds a slightly different convention; conflicting concepts coexist "for compatibility"; heavy abstraction layers in an API nobody plans to extend.

---

### Chapter 4. Choosing Solutions for API Development
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-api-choosing-solutions

**Core idea:** Partners prefer familiar "pipe fittings". Where an established standard exists, using it is part of quality; inventing your own is only defensible if the gains are so obvious that developers will forgive learning it. Where paradigms compete (REST vs RPC vs GraphQL; UI component approaches), a deliberate choice must be made.

**Rules:**
- I4-1: Adopt the established standard for your domain unless you are certain a custom solution is overwhelmingly better. *Why:* familiarity lowers adoption cost. *Check:* Does the API reinvent something (auth, pagination, transport, date formats) that a widely used standard already covers?
- I4-2: Where paradigms compete, choose one explicitly and consistently. *Why:* mixing paradigms confuses consumers. *Check:* Is the client-server paradigm a single documented choice rather than a mix?

**Anti-patterns / smells:** home-grown RPC-over-HTTP with REST-ish URLs; custom signature schemes; half-REST, half-GraphQL.

---

### Chapter 5. The API-First Approach
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-api-first-approach

**Core idea:** Technically, API-first means the contract precedes and defines the implementation. This gives partners a guarantee: they can code (and code-generate) against the spec without coordinating with you, and never have to change their code because your implementation drifted.

**Rules:**
- I5-1: Write and commit the machine-readable specification before implementing. *Why:* partners can start (and generate code) from the spec alone. *Check:* Does a versioned IDL document (OpenAPI/.proto/etc.) exist and predate the implementation?
- I5-2: When implementation and spec disagree, fix the implementation. *Why:* partners coded against the spec. *Check:* Is spec conformance tested and are discrepancies treated as implementation bugs?
- I5-3: Design carefully before committing, because the only escape from rule I5-2 is an irreparable spec flaw. *Why:* breaking the spec breaks the guarantee. *Check:* Has the spec been reviewed for design flaws before publication?

**Anti-patterns / smells:** spec generated after the fact from code; "the docs are wrong, the server is right"; spec and server tested independently.

---

### Chapter 6. On Backward Compatibility
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-back-compat

**Core idea:** Backward compatibility is the temporal dimension of an API and the main thing that separates API work from other software. Every incompatible release is a tax on partners; large players can afford to levy it but should not. Maintaining old versions is also a cost, so breaks eventually happen — but they must be avoidable-avoided and explainable.

**Rules:**
- I6-1: Never break compatibility when it can be avoided. *Why:* every break costs partners real money and goodwill. *Check:* Does each proposed change have a compatible alternative that was considered and rejected for a stated reason?
- I6-2: When a break is unavoidable, be able to explain to partners why. *Why:* an explained break is a fair trade; a hidden levy is not. *Check:* Is there a written rationale for each major version?
- I6-3: Do not penalise partners who have not migrated by disabling them without cause. *Why:* punitive deprecation destroys trust. *Check:* Is there a deprecation window and support policy for old versions?

**Anti-patterns / smells:** frequent major bumps; field renames shipped as "minor"; forced upgrades with app shutoff.

---

### Chapter 7. On Versioning
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-versioning

**Core idea:** The book uses semantic versioning throughout: three numbers where the major changes on incompatible changes, minor on compatible additions, patch on bug fixes only. `v1`/`v2` refer to the latest stable release of a major family.

**Rules:**
- I7-1: Version the API as `MAJOR.MINOR.PATCH` with semver meaning. *Why:* partners can reason about upgrade risk from the number. *Check:* Does every release carry a semver version whose bump matches the nature of the change?
- I7-2: Bump the major number for any backward-incompatible change, and only then. *Why:* "major" and "incompatible" must be synonyms. *Check:* Can any change in a minor/patch release break an existing client?
- I7-3: Let clients target a major family (`v1`) and receive the latest compatible release. *Why:* clients want fixes without migration. *Check:* Does `v1` resolve to the newest `1.x.x`?

**Anti-patterns / smells:** date-based or single-number versions with unspecified compatibility semantics; unversioned endpoints (like `/programs` in the coffee-machine example).

---

### Chapter 8. Terms and Notation Keys
Link: https://twirl.github.io/The-API-Book/API.en.html#intro-terms-notation

**Core idea:** The book deliberately uses paradigm-neutral vocabulary ("entity" with "fields" and "methods") and a JSON-over-HTTP notation that could equally be method calls in any language. Notation: `{id}` = placeholder for the nearest left term; `<...>` = semantic description of a value; `…` = omitted parts; `→` = response (200 OK if no status shown); `↵` = line continuation; pseudocode is typeless JavaScript/Python-like and shows how partners or SDKs use the contract.

**Rules:**
- I8-1: Use one neutral, consistent vocabulary for API units across documentation. *Why:* avoids paradigm arguments and ambiguity. *Check:* Are "entity/field/method" (or equivalents) used uniformly in docs?
- I8-2: Separate examples of the contract (what the API is) from examples of usage (how a partner calls it). *Why:* different audiences and purposes. *Check:* Does documentation distinguish endpoint definitions from client code samples?

**Anti-patterns / smells:** docs that mix "object", "resource", "method", "endpoint" for the same thing; samples where it is unclear which side (server or client) the code belongs to.

---

## Section I: The API Design

### Chapter 9. The API Contexts Pyramid
Link: https://twirl.github.io/The-API-Book/API.en.html#api-design-context-pyramid

**Core idea:** Design top-down in four steps: define the application field, separate abstraction levels, isolate responsibility areas, describe final interfaces. Mistakes higher up cost exponentially more — renaming is cheap; misunderstanding what the API is for is practically irreparable. Unlike internal architecture, your subsystem split is *not* something consumers should have to see.

**Rules:**
- D9-1: Follow the four-step order: field → abstraction levels → responsibilities → interfaces. *Why:* each level constrains the next; skipping ahead bakes in high-level mistakes. *Check:* Were use cases and abstraction levels written down before endpoint names?
- D9-2: Spend review effort in proportion to the cost of a mistake at that level. *Why:* naming fixes are cheap; purpose fixes are not. *Check:* Did the "what problem, for whom" review get more scrutiny than field naming?
- D9-3: Do not expose your internal subsystem decomposition in the contract unless consumers need it. *Why:* partners care about the nomenclature, not your architecture. *Check:* Do entity names reflect the consumer's domain rather than your microservices?

**Anti-patterns / smells:** endpoints named after internal services (`/billing-svc/...`); naming debates before use cases exist.

---

### Chapter 10. Defining an Application Field
Link: https://twirl.github.io/The-API-Book/API.en.html#api-design-defining-field

**Core idea:** Ask "what problem do we solve?" four times, stressing a different word each time: *what* problem (can we describe the situation), what *problem* (is it real, would someone pay), do *we* have the expertise, and do we actually *solve* it (or create a new one). Then ask specifically why an *API* is needed rather than an app — only when the answer is "this is our expertise" should you build one. End with a clear statement of *what* and *how*.

**Rules:**
- D10-1: Write a short answer to "what situation needs this API and why" before any design. *Why:* an unexplainable purpose means no purpose. *Check:* Is there a one-paragraph problem statement that a stranger would understand?
- D10-2: Apply the "why" question to every single entity; if it cannot be answered briefly, drop the entity. *Why:* unneeded entities are pure cost. *Check:* Does each endpoint/field have a one-line justification?
- D10-3: Validate that the problem is real and worth paying for, ideally with measured metrics; in a new market, state that you are relying on intuition. *Why:* solving non-problems wastes everyone's effort. *Check:* Are there numbers (or an explicit assumption) behind the claimed pain?
- D10-4: Confirm you have the expertise and resources in both domains: the API and the end-user product. *Why:* API work is meta-engineering. *Check:* Does the team understand how partners' end products work?
- D10-5: Define how impact will be quantified. *Why:* otherwise "solved" is unverifiable. *Check:* Is there a metric the API is expected to move?
- D10-6: Justify why this must be an API rather than an application, i.e. why provider and consumer roles are split. *Why:* the split has real costs. *Check:* Is there a stated reason partners cannot or should not build this themselves?
- D10-7: Record a two-line "what we do / how we do it" statement before proceeding. *Why:* it anchors all later decisions. *Check:* Do the what/how statements exist and match the designed entities?

**Anti-patterns / smells:** the API exists "because everyone has one"; entities nobody can explain; success undefined.

---

### Chapter 11. Separating Abstraction Levels
Link: https://twirl.github.io/The-API-Book/API.en.html#api-design-separating-abstractions

**Core idea:** An API transforms terms of one context into terms of another; the further apart the contexts, the more intermediate levels are needed. Well-separated levels reduce what a developer must hold in mind, preserve compatibility, and allow porting low-level parts without touching high-level ones. Levels must be found by studying the real subject area (e.g., the actual coffee-machine APIs), not invented speculatively, and only adjacent levels may talk to each other. A data-flow chart is the tool for checking the hierarchy.

**Rules:**
- D11-1: Never make a developer combine data from different levels to answer a high-level question (e.g. comparing a recipe's reference volume to an order's poured volume to know if it is ready). *Why:* the concept is unguessable and leaks physical details. *Check:* Can every high-level question (is it ready? where? when?) be answered from the high-level entity alone?
- D11-2: Do not let one field carry different meanings in different entities. *Why:* legacy-named fields become traps (`volume` = default in recipes, = progress in orders). *Check:* Does each field name mean exactly one thing everywhere?
- D11-3: Separate levels along three axes: user scenarios → their decomposition; user-domain terms → raw-domain terms; user-facing data structures → raw data structures. *Why:* this is how the abstraction gap actually sorts itself. *Check:* Can each entity be assigned to one level on each axis?
- D11-4: Study the actual lower-level systems before inventing an intermediate abstraction. *Why:* a speculative "connecting link" may not reflect the real domain; if volume comparison is the only readiness method, expose it. *Check:* Is each intermediate level grounded in documented capabilities of the layer below?
- D11-5: Derive the intermediate level from the tasks developers need at the higher level (create uniformly, learn state/ETA/errors, locate in space/time, cancel). *Why:* the level exists to serve those tasks. *Check:* Is there a list of higher-level developer tasks that the intermediate level satisfies?
- D11-6: Provide a uniform interface at each level regardless of underlying variants (same statuses, same method names, same behavior for both machine kinds). *Why:* consumers should not need to know the backend kind. *Check:* Does any consumer-facing call require knowing which underlying provider/type serves it?
- D11-7: Give each level its own status vocabulary rather than passing lower-level statuses upward. *Why:* forbidding level-jumping requires levels to synthesise their own state. *Check:* Does each level define and own its state fields?
- D11-8: Allow only adjacent levels to interact; a call chain that skips a level indicates a design error. *Why:* isolation keeps levels replaceable. *Check:* Does any handler at level N call level N-2 or lower directly?
- D11-9: Reformulate state-changing operations (like cancel) at every level, and explicitly couple divergent states (outer "canceled" vs inner "still discarding cup"). *Why:* the same verb means different things per level. *Check:* For each mutating operation, is its meaning at each level written down?
- D11-10: Keep lower-level execution cycles independent of upper-level calls (e.g., a runtime updates itself in the background). *Why:* the low level must not depend on being polled. *Check:* Does the low-level loop still progress if the high-level caller disappears?
- D11-11: Draw the data-flow chart: what data enters at the bottom, what new concepts each level injects, and how it is enriched upward. *Why:* it is the one view of a large API that fits in a human head. *Check:* Does a chart exist showing each level's inputs, new context variables, and outputs?
- D11-12: Ensure each level both (a) does not leak raw data from below and (b) introduces and initialises its own meta-variables. *Why:* the "bad" design both leaked `volume` and failed to define `status`. *Check:* Are there fields in a high-level entity that came unchanged from a lower level, or missing concepts that only that level can define?
- D11-13: Accept that isolation adds interface overhead, and pay it deliberately. *Why:* zero-overhead access to the microcontroller is unusable and unextendable. *Check:* Is the trade-off between overhead and clarity documented rather than accidental?

**Anti-patterns / smells:** recipes that depend on machine IDs; `volume` and `volume_requested` coexisting; the client computing "ready" itself; endpoints suffixed by backend type (`/v1/{api_type}/programs/{id}/run`) without need; no order-level status field.

---

### Chapter 12. Isolating Responsibility Areas
Link: https://twirl.github.io/The-API-Book/API.en.html#api-design-isolating-responsibility

**Core idea:** For each level, state in domain terms what every entity *is*, why it belongs in the API, and which operations apply to it directly versus by delegation. Then write the partner's code in your head: the gaps you find (e.g., no way to search) become helper methods. Errors must tell the client what to do, and every interface should be decomposed so a developer never juggles more than about seven to ten things at once.

**Rules:**
- D12-1: For every entity, write its definition in subject-area terms, its reason to exist, and its permitted operations. *Why:* this is the "why" principle applied per entity. *Check:* Is there a table of entities × allowed operations (create/read/status/cancel...)?
- D12-2: Prototype the partner's code against the draft API before finalising it. *Why:* it exposes missing methods and boilerplate immediately. *Check:* Has someone written a realistic client for the main use case and measured how much glue it needed?
- D12-3: Add helper methods that encapsulate known usage scenarios (e.g. `offers/search` instead of "fetch all recipes, fetch all machines, build a geo-index yourself"). *Why:* removes boilerplate and prevents common mistakes. *Check:* Do the top three scenarios each map to one or two calls?
- D12-4: Design search/listing from the end user's scenarios (discovery vs targeted search), thinking like a UX designer. *Why:* the API serves the app's UX. *Check:* Are the user-facing scenarios listed and covered?
- D12-5: Do not merge different ranking modes (by relevance vs by ordinal listing) into one endpoint. *Why:* they imply different features and usage. *Check:* Is a "search" endpoint separate from a plain "list" endpoint?
- D12-6: Name and place functionality according to what the user cares about (an *offer*, not a *coffee machine*). *Why:* the user's key feature should be the first-class entity. *Check:* Is the main value-bearing concept a named entity rather than a side field?
- D12-7: Make helpers prevent mistakes, not just save typing: e.g. give volatile data (price) an identifier with a validity period (`offer.id`, `valid_until`) that must be passed when acting on it. *Why:* it solves stale caches, over-polling and price mismatch at once. *Check:* Can a client act on outdated volatile data without the server noticing?
- D12-8: Any API dealing with money must require the client to submit the amount it displayed and reject mismatches. *Why:* the user must never be charged a different sum than shown. *Check:* Does order creation carry the price/offer the user saw?
- D12-9: Every error response must tell the client what to do: who is at fault (client vs server), whether retrying makes sense and when, whether it is resolvable, and which kind of resolvable problem it is. *Why:* clients can only handle problems they can identify. *Check:* Does the error contain a machine-readable `reason` the client can branch on?
- D12-10: Distinguish resolvable errors (book uses `409`) from unresolvable ones (`400`) consistently. *Why:* the client's reaction differs entirely. *Check:* Is there a fixed convention mapping resolvability to status codes?
- D12-11: When several parameters can produce the same error, say which parameter failed and which values are acceptable. *Why:* otherwise the developer must guess. *Check:* Does a validation error name the field and the constraint?
- D12-12: Provide a user-facing localized message as a fallback for unknown error reasons, alongside developer-facing details. *Why:* unhandled errors still need a sane UX. *Check:* Does each error include both `localized_message` and `details`?
- D12-13: Even for unresolvable errors, include diagnostic details for the developer. *Why:* it is read while fixing the code. *Check:* Do `400`-class errors still carry specifics?
- D12-14: Keep the number of things a developer must handle at once around 7±2 (at most ~10) by grouping related fields into nested objects. *Why:* short-term memory limits; flat prefixed lists are unreadable. *Check:* Does any object expose more than ~10 top-level attributes?
- D12-15: Decompose so a reader can skip whole sub-objects that are irrelevant to the current task; do not scatter fields needed for one action across several composites. *Why:* grouping only helps if it matches how the data is used. *Check:* Are the fields needed for each action co-located?
  - Example: `place_name, place_lat, place_lng, walking_distance, offer_id, price...` (flat) → `place: {name, location}`, `route: {distance, duration}`, `offer: {id, valid_until}`, `pricing: {currency_code, price}`.

**Anti-patterns / smells:** a `409 { "message": "Invalid price" }` with no reason code; clients building their own spatial index; prefixed field soup (`coffee_machine_brand`, `place_open_now`, ...); a listing endpoint that also does relevance search.

---

### Chapter 13. Describing Final Interfaces
Link: https://twirl.github.io/The-API-Book/API.en.html#api-design-describing-interfaces

**Core idea:** Once entities and responsibilities are fixed, the remaining job is to make partner code readable and hard to get wrong, remembering that whatever *can* be misunderstood *will* be, by more people as the API grows. The chapter is a checklist of naming, typing, validation, error, caching, idempotency, security and i18n rules — all to be applied with judgement, not mechanically.

**Rules:**
- D13-1: Apply rules thoughtfully; if a rule produces a worse API in your case, deviate — but if you adopt your own convention (e.g. a single `entity()` getter/setter), apply it uniformly or give it a distinguishing naming rule. *Why:* rules are generalisations, not laws; inconsistency is the real sin. *Check:* Is every deviation from a convention either universal or clearly marked?
- D13-2: Make names explicit about what an operation does and its side effects; mutating operations must not look like reads. `order.canceled = true` → `order.cancel()`; `orders.getStats()` (unbounded, expensive) → `orders.calculateAggregatedStats({begin_date, end_date})`. *Why:* readers should not need docs to know something changes state or is costly. *Check:* Is there any `get*`/`GET` that mutates, or any expensive op whose cost is invisible in its name/signature?
- D13-3: Make sync vs async visible in the signature or via a naming convention. *Why:* mixing them silently breaks callers. *Check:* Can you tell from the name/signature whether a call is asynchronous?
- D13-4: State which standard every ambiguous value follows: `"date": "11/12/2020"` → `"iso_date": "2020-11-12"`; `"duration": 5000` → `"duration_ms": 5000`; money always with a currency code. *Why:* humanity agrees on nothing, not even weekday order. *Check:* Does every date, duration, unit, coordinate order and money field name or carry its format?
- D13-5: Use concrete names, not amoeba words (`get`, `apply`, `make`): `user.get()` → `user.get_id()`. *Why:* the reader cannot guess the return value. *Check:* Does any method name lack a noun saying what it returns/affects?
- D13-6: Do not abbreviate: `order.getTime()` → `order.getEstimatedDeliveryTime()`; `strpbrk(str1, str2)` → `str_search_for_characters(str, lookup_character_set)`. *Why:* saved letters cost comprehension; transport compression makes traffic savings moot. *Check:* Does any identifier need a comment or docs to expand it?
- D13-7: Let names imply types: `recipe` holds a `Recipe`, `recipe_id` an identifier; collections are plural (`GET /news` → `GET /news-list`); booleans describe a state (`task.status: true` → `task.is_finished: true`); dates get `_at`/`_date`; polysemous words get a clarifier (`/functions` → `/builtin-functions-list`). *Why:* type confusion is the commonest signature mistake. *Check:* Could a reader infer the type of every field from its name alone?
- D13-8: Give paired/related entities matching names, argument order and behavior: `begin_transition / stop_transition` → `start_transition / stop_transition`; `strpos(haystack, needle)` vs `str_replace(needle, replace, haystack)` is a triple violation. *Why:* developers should find the pair without docs. *Check:* Do sibling methods share vocabulary, parameter order and cardinality semantics?
- D13-9: Avoid double negations: `"dont_call_me": false` → `"prohibit_calling": true`; avoid designs where clients must combine negated flags (`!no_beans && !no_cup`). *Why:* people misapply De Morgan. *Check:* Is any flag negative in name and expected to be `false`?
- D13-10: Avoid implicit type casting / sentinel values; make new optional booleans default to `false` and split "special absence" into two fields: `spending_monthly_limit_usd: null` (meaning "no limit") → `abolish_spending_limit: true` plus an optional limit field. *Why:* clients cannot distinguish "explicitly false" from "not set". *Check:* Does any field use `null`/`-1`/absence to mean something other than "use the default"?
- D13-11: Declare every technical restriction (max lengths, sizes, ranges) for every field, and return a machine-readable error naming the violated bound; expose quota usage the same way. *Why:* unknown limits mean partner code can break at any time for reasons outside its control. *Check:* Does every field have a documented bound and a specific error for exceeding it?
- D13-12: Cap every request's data volume (`getOrders()` → `getOrders({limit, ...})`) and provide a way to refine or continue the query. *Why:* a million orders must not be one response. *Check:* Is there any list/aggregate call without a limit and a way to page or narrow?
- D13-13: Publish a retry policy with exponential backoff and a cap (1s, 2s, 4s ... up to ~1 min), and ship it in your SDKs. *Why:* retry storms after a hiccup can take the service down. *Check:* Do docs/SDK specify how and when clients should retry?
- D13-14: Budget traffic: limit field sizes, paginate, and split heavy binary data (images, media) into separate endpoints referenced by link so they can be cached differently. *Why:* careless design overloads even modern networks. *Check:* Has the request count and bytes for the app's main flow (e.g., one order) been modelled?
- D13-15: An empty result is a success, not an error (`404 "No one makes lungo nearby"` → `200 { "results": [] }`); conversely, treat an explicitly empty array parameter differently from an absent one — return empty or an error, never silently ignore it. *Why:* the client made no mistake; ignoring an empty filter silently returns wrong data. *Check:* Does any search return 4xx for zero matches, or treat `recipes: []` as "no filter"?
- D13-16: Validate all inputs against the contract and reject violations instead of silently correcting them (`latitude: 100` → `400`, not "snap to 90"); proactively warn about suspicious input (`[0, 0]`, misspelled fields) and offer a strict mode that escalates warnings, with per-error bypass. *Why:* silent fixes hide bugs from the developer forever. *Check:* Does the server ever clamp, coerce or drop invalid input without an error or warning?
- D13-17: Defaults must help, never mask mistakes: a missing required-in-practice value (user location) → `400`, not results for a default location. *Why:* "null island" becomes your busiest venue. *Check:* Could a missing parameter silently yield plausible-looking wrong results?
- D13-18: Make errors informative: `400 {}` → `{ reason, localized_message, details.checks_failed: [{field, error_type, constraints, message}] }`, with "did you mean" hints, and report all detectable errors at once. *Why:* the handler already knows what is wrong; withholding it wastes developer time. *Check:* Does every error identify field, constraint and a readable message, and are multiple errors batched?
- D13-19: Return unresolvable errors before resolvable ones (do not say "offer expired" when the recipe is misspelled). *Why:* renewing the offer would be wasted work. *Check:* Does validation of static/unfixable inputs run before checks on volatile state?
- D13-20: Among resolvable errors, report first those needing the biggest state change (order-limit exceeded before price changed). *Why:* fixing the small one first is pointless if the big one blocks anyway. *Check:* Are error checks ordered by severity of required client action?
- D13-21: Analyse error deadlocks where fixing one error triggers another and back (free delivery above 9000 forces the sum below the 10000 minimum); redesign the rule or add a dedicated error. *Why:* the client can never converge. *Check:* For each pair of business-rule errors, can both be satisfied simultaneously?
- D13-22: Specify caching policy and lifetime in every dimension that matters (time *and* space): `GET /price?...` → `{ offer: { valid_until, valid_within } }` or `Cache-Control`; choose TTLs by how bad a wrongly cached value would be, not "a year". *Why:* clients cache everything; a cached `404` for a year is a disaster. *Check:* For every response, is it clear how long and under which parameter variations it may be reused?
- D13-23: Keep fixed-precision numbers exact: use `Decimal` where available, else integers with a fixed multiplier or strings; avoid lossy conversions (`0.3333` hours → `00:20`) or ship an SDK and document rounding. *Why:* floats corrupt money. *Check:* Is any monetary or fixed-precision value transmitted as a float?
- D13-24: Make every operation idempotent; where not natural, add an idempotency token or resource version (`POST /orders` → `POST /v1/orders` + `X-Idempotency-Token`, or draft-then-confirm); scope tokens per user/resource and document/SDK them since clients get this wrong. Tokens on naturally idempotent calls still let you tell retry (`201`) from conflict (`409`). *Why:* network retries are routine, not exceptional. *Check:* Does repeating any request with the same parameters create a second effect?
- D13-25: Do not invent security mechanisms: use standard, proven protocols (mutual TLS, certificate pinning), follow OWASP API Security, and serve everything over TLS 1.2+ (preferably 1.3). *Why:* home-grown signing/token schemes have vulnerabilities you have never heard of. *Check:* Is any auth, signing or password-exchange scheme custom-designed?
- D13-26: Help partners stay secure: sanitise stored user-supplied content that may be rendered (prevent stored XSS), isolate partners' data spaces to bound blast radius, make raw/unsafe modes explicit opt-ins (`X-Dangerously-Disable-Sanitizing`), and prefer typed/parameterised input over raw scripts (`query` + `values` instead of one SQL string). *Why:* some partner will forget, and one partner's exploit can hit all. *Check:* Can a partner store and retrieve unsanitised markup/scripts by default, or pass raw executable strings?
- D13-27: Use globally unique, preferably URN-like namespaced identifiers (`order:<uuid>`), semantic or random; never expose sequential numbers. *Why:* aids merging data sources and legacy mapping; sequential IDs leak business volumes to competitors. *Check:* Is any external ID an auto-increment integer?
- D13-28: Stipulate future restrictions in the docs now (429, captchas, honeypots, MFA for payments) even before implementing them, and serve different API families (server-to-server, end-user, embeddable widget) from separate endpoints so each can get its own protections. *Why:* you cannot add these later without breaking clients. *Check:* Are rate-limit/captcha/MFA errors documented, and are API families on separate endpoints?
- D13-29: Provide no bulk access to sensitive data (PII, card numbers, private messages); if access is needed, put rate limits, small page sizes and ideally MFA in front, or do ad-hoc offloads outside the API. *Why:* one leak harms users, partners and vendor. *Check:* Is there any endpoint that can dump sensitive records at scale?
- D13-30: Accept a language parameter (e.g. `Accept-Language`) on every endpoint from day one, and always know the user's location (country at least) separately from language, since number/date/unit formats follow jurisdiction; separate user-facing localized messages (`localized_message`) from developer-facing English details; all strings UTF-8. *Why:* language ≠ locale, and retrofitting i18n breaks contracts. *Check:* Do all endpoints accept a language, store a location, and mark user- vs developer-facing strings?

**Anti-patterns / smells:** `GET` that mutates; `duration: 5000`; `str` and `pbrk`-style abbreviations; `status: true`; `dont_*` flags; `null` meaning "unlimited"; unbounded `getAll*`; `404` on empty search; clamped-instead-of-rejected coordinates; `400 {}`; "price changed" reported before "limit exceeded"; year-long cache on a `404`; money as float; `POST` create without idempotency key; custom HMAC signing scheme; stored `<script>` echoed back raw; auto-increment order IDs; no `429`/captcha in docs; a single endpoint serving widgets and server integrations; no `Accept-Language`.
