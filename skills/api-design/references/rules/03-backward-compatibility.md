# Section III: Backward Compatibility — Distilled Rules

Source: "The API" by Sergey Konstantinov, CC BY-NC 4.0, https://twirl.github.io/The-API-Book/API.en.html (chapters 25-31). All text below is paraphrased.

---

### Chapter 25. The Backward Compatibility Problem Statement
Link: https://twirl.github.io/The-API-Book/API.en.html#back-compat-statement

**Core idea:** Backward compatibility means partner code keeps doing its job (not necessarily behaving bit-for-bit identically) for roughly the lifetime of applications in your domain. You will be forced to ship new versions anyway because consumer apps fragment across old builds, the underlying subject area shifts, and platforms drift beneath you; so the real job is deciding a versioning and support policy up front and designing so that most change stays inside minor versions.

**Rules:**
- B25-1: Define "still works" as "still solves the user's task," not "identical output," and treat only functionally significant changes as breaking. *Why:* it separates cosmetic drift from real breakage. *Check:* Does this change alter what partner code can accomplish, or only how it looks internally?
- B25-2: Set the support horizon for a major version to match how long apps in your domain live (use platform LTS windows as a yardstick). *Why:* partners rewrite apps when platforms die, and not before. *Check:* Is the stated end-of-support date for this major version at least as long as a typical app lifetime on your target platforms?
- B25-3: Assume some consumers will never upgrade (abandoned apps, users refusing updates, unsupported devices) and plan version retirement around measured audience share rather than wishful thinking. *Why:* compiled clients freeze your API at build time. *Check:* Do you know what percentage of traffic each live version serves before announcing its retirement?
- B25-4: Ship an official SDK where the platform allows code-on-demand, because otherwise partners write their own and their bugs become your reputation. *Why:* an SDK you control is one you can keep compatible. *Check:* Is there a vendor-maintained client for each major platform, and can old SDK majors be reimplemented over the current server API?
- B25-5: Own the facade over third-party and low-level dependencies; do not assume their vendors care about compatibility as much as you do. *Why:* their breakage otherwise becomes your breakage. *Check:* Is every upstream API wrapped by an adapter you control?
- B25-6: Release a new major only when there is a critical mass of features that cannot be added compatibly, and never before the previous major has stabilized (months to a year). *Why:* frequent majors signal permanent instability to partners. *Check:* Can each proposed breaking change be listed with why it is impossible in the current major?
- B25-7: Keep every previously released version reachable for as long as its audience justifies, and publish the rules for when support ends. *Why:* a version rollback is destructive once many partners depend on the API. *Check:* Is there a written sunset policy per version with a discoverable schedule?
- B25-8: Let partners pin to an exact major.minor.patch, and expose at least the two latest minors once the API is mature. *Why:* pinned, tested versions are the safest integration for partners. *Check:* Can a partner explicitly request a specific minor/patch and get the same behavior they tested against?
- B25-9: Offer alpha/beta channels so partners can test upcoming versions before they go live. *Why:* it moves breakage discovery to before release. *Check:* Is there a pre-release endpoint or SDK track partners can opt into?
- B25-10: Avoid IDL features whose compatibility semantics are ambiguous (e.g., OpenAPI `additionalProperties: false`), and evaluate every change as if generated client code were hand-written code. *Why:* codegen tools evolve unpredictably and can turn a "safe" spec change into a runtime break. *Check:* Would every known code generator's output for the old spec still work against the new server?
- B25-11: Do not rely on the spec diff alone; a change can break behavior with an unchanged spec (e.g., switching to eventual consistency) or change the spec without breaking anyone. *Why:* the spec is not the contract, behavior is. *Check:* Has the change been reviewed for behavioral (timing, consistency, ordering) impact, not just schema impact?
- B25-12: Isolate unversioned shared dependencies (databases, shared services) behind the versioned API so old versions do not silently break when those dependencies change. *Why:* otherwise "keeping the old build" is a false guarantee. *Check:* Can the previous version keep running correctly after the shared storage schema changes?

**Techniques:**
- *Semver as a granularity contract:* major = compatible surface, major.minor = feature availability guaranteed, full triple = frozen behavior including bugs. Example: a partner pins `2.4.1` in production, runs `2.x` in CI to catch drift early.
- *Reimplement old majors on top of the new one:* keep v1's client library, but make it a thin adapter over the v2 server so only one backend is maintained.

**Anti-patterns / smells:**
- Shipping a new major while the previous one still has open design churn.
- "Only one version in production, roll back on problems" for a public API with many integrations.
- A code-first spec pipeline where server code, generated spec, generated SDK, and client app can each drift.
- Retiring a version without measuring who still uses it.

---

### Chapter 26. On the Waterline of the Iceberg
Link: https://twirl.github.io/The-API-Book/API.en.html#back-compat-iceberg-waterline

**Core idea:** Draw a clear line between what is promised and what merely exists. Expose as little as possible, make the promise unambiguous, and write down every convention partners could reasonably infer (ordering, timing, consistency), because anything observable becomes part of the contract whether you intended it or not.

**Rules:**
- B26-1: Expose only functionality with a concrete product justification; everything else stays hidden until needed. *Why:* anything published must be supported for the version's lifetime. *Check:* Can each public entity, field, and method name the product need it serves?
- B26-2: Aim for the API's public surface to be far smaller than the code behind it (roughly one-to-ten), so partner code stays short. *Why:* if partners must write more than you did, the abstraction is failing. *Check:* Is the typical integration measured in tens of lines rather than hundreds?
- B26-3: State explicitly which capabilities are guaranteed and what happens to undocumented behavior partners "discover." *Why:* it gives you standing when a hidden feature changes. *Check:* Does the documentation contain a written policy on undocumented functionality?
- B26-4: Never return undocumented fields or use private features in samples, support answers, or talks. *Why:* any hint of a feature is a de facto promise. *Check:* Are all response fields and all sample-code calls present in the reference docs?
- B26-5: Write down every implicit assumption your example code depends on (synchronous callbacks, read-after-write consistency, callback frequency, event order). *Why:* partners copy examples, so the examples define the contract. *Check:* For each code sample, what would break if timing, ordering, or consistency changed, and is that behavior documented?
- B26-6: If you are not strictly consistent, make the write operation asynchronous or hide retries inside the read; never push a retry loop onto partners. *Why:* documenting weak consistency after the fact is a breaking change. *Check:* Does `get` immediately after `create` in the sample code work without a loop?
- B26-7: Once a callback cadence or event sequence is observable, document it and preserve it even when the underlying implementation changes. *Why:* partner state machines and throttling assume it. *Check:* Does the doc list allowed states, transitions, and the guaranteed order of events?
- B26-8: When business logic gains a new path (e.g., cancellation via a phone call), keep emitting the events partners expect, and design entities so external state changes were possible from the start. *Why:* product behavior is part of the contract, not just the schema. *Check:* Could a partner's analytics pipeline built on documented events misreport after this product change?

**Techniques:**
- *Waterline / iceberg:* the documented part sits above water; everything below is private. Example: mark internal fields with a documented "reserved, may change" annotation or strip them at the gateway so they never leak.
- *Codifying implicit agreements:* before changing an implementation, enumerate every behavior partners could observe. Example: a status history endpoint explicitly documents "payment_approved always precedes preparing_started," and the trusted-customer fast path still emits payment_approved synthetically.

**Anti-patterns / smells:**
- Undocumented fields in responses.
- Sample code relying on synchronous callback execution or immediate read-after-write.
- Changing observer callback frequency when moving to native platform APIs.
- Skipping an intermediate state in a documented pipeline.
- Introducing a "flag per exception" (e.g., `cancellable_by_phone`) that users cannot understand.

---

### Chapter 27. Extending through Abstracting
Link: https://twirl.github.io/The-API-Book/API.en.html#back-compat-abstracting-extending

**Core idea:** To add capability compatibly, treat the current interface as a special case of a more general one where some parameters were implicitly defaulted. Make the implicit contract explicit, add the more general operation, then redefine the old one as a helper that fills in defaults. This only works well if the entity hierarchy and growth direction were sound from the start; otherwise defaults fossilize the API's history.

**Rules:**
- B27-1: Before extending, run a "what if" pass over every entity: list all implicit assumptions and coupling mechanisms the current design relies on. *Why:* you cannot generalize what you have not named. *Check:* Is there a written list of assumptions (e.g., "all machines support all options") for the interface being changed?
- B27-2: Extend in three steps: document the present contract, add a more general method or optional parameter, then declare the old method a helper with fixed defaults. *Why:* old callers keep working while new ones gain control. *Check:* Is the old call exactly equivalent to the new call with specific default values?
- B27-3: Prefer adding optional parameters with defaults that reproduce current behavior over adding parallel endpoints. *Why:* it keeps the surface small. *Check:* Does omitting the new parameter produce byte-identical behavior to before?
- B27-4: Only formalize defaults that were genuinely part of the negotiated contract; never invent new obligations for existing partners during an extension. *Why:* newly imposed requirements are breaking changes. *Check:* Were existing partners already required to satisfy the "default" you are now writing down?
- B27-5: Be aware that defaults age; do not let the helper set of defaults become a historical accident that new users cannot explain. *Why:* helpers should reflect common use, not release chronology. *Check:* Would a new developer understand why these specific defaults exist without knowing version history?

**Techniques:**
- *Extending via abstracting (reduction to a general interface):* Example: `createUser(email)` is retroactively defined as `createUser({email, role: "member", locale: "en"})`; the object form is the general call, the scalar form the helper.
- *Versioned defaults switch (with caution):* a `use_defaults_version` setting can bundle updated defaults, but at a documentation cost.

**Anti-patterns / smells:**
- Extending an interface by declaring requirements partners never agreed to.
- A "default" method whose parameter set makes sense only as a snapshot of past releases.
- Multiple sibling endpoints (`/things`, `/things-with-options`, `/things-with-more-options`) that differ only in default sets.

---

### Chapter 28. Strong Coupling and Related Problems
Link: https://twirl.github.io/The-API-Book/API.en.html#back-compat-strong-coupling

**Core idea:** Strong coupling is when one entity's shape is dictated by another entity's implementation (a recipe carrying fields shaped by a particular UI layout or localization rule). Neither low-level entities should define high-level ones nor vice versa; instead, higher levels define contexts that lower levels interpret, and entities collapse to identifiers linking those contexts.

**Rules:**
- B28-1: Ask why each field exists; if the answer is "because a specific UI/consumer displays it," the field belongs to that consumer's context, not to the core entity. *Why:* it otherwise binds the entity to one presentation forever. *Check:* Can you name the field's meaning without referring to a particular screen or client?
- B28-2: Do not embed presentation constraints (lengths, tone, display slot) in fields with generic names like `name`. *Why:* the name lies about the real contract. *Check:* Is every human-readable field named for its role (e.g., `search_title`) and tied to a described layout?
- B28-3: Model cross-cutting concerns (localization, formatting, layout) as separately registrable contexts partners can extend rather than fixed enumerations inside entities. *Why:* partners can then reach new regions or UIs without waiting for you. *Check:* Can a partner add a new locale/format/layout without an API release?
- B28-4: Let core entities shrink to context identifiers when they have no semantics of their own, and supply a builder endpoint to create all related contexts in one call. *Why:* thin entities do not accumulate scrapyard fields. *Check:* Are there optional fields on the entity that only some consumers ever read?
- B28-5: When identifiers are supplied by partners, namespace them (composite ids) to prevent collisions and to allow shared vs isolated scopes. *Why:* meaningful ids across partners will clash. *Check:* Does every partner-created id carry a partner-owned prefix or namespace?
- B28-6: Do not force developers to learn a lower level's implementation type to use a higher-level operation. *Why:* it violates abstraction isolation. *Check:* Can the common case be completed without knowing which backend/hardware type is involved?

**Techniques:**
- *Rule of contexts:* high-level entities publish a context (state plus expectations); low-level entities read the context and interpret the parts meaningful to them. Example: a "layout" resource declares required fields and rendering rules; a product entity provides values per layout rather than hardcoded `name`/`description`.
- *Registrable formatters:* `PUT /formatters/volume/{lang}/{region}` lets partners define how a number renders instead of the API enumerating regions.
- *Composite identifiers:* `namespace:id` with reserved namespaces (e.g., `common`) for vendor-managed records.

**Anti-patterns / smells:**
- Entities whose fields mirror a specific screen's slots.
- A growing bag of optional presentation fields (image, calories, allergens...) on a domain object.
- Localization baked into fixed, vendor-maintained tables partners cannot extend.
- Operations that require the caller to discover and branch on backend/API type.

---

### Chapter 29. Weak Coupling
Link: https://twirl.github.io/The-API-Book/API.en.html#back-compat-weak-coupling

**Core idea:** Requiring lower-level implementations to support a fixed set of imperative methods produces a pile of mostly optional, mostly meaningless endpoints as new implementation kinds appear. Weak coupling replaces that with two contexts and a data flow between them: the upper level states what it wants in its own terms, the lower level reacts only to what applies to it. Where alternative implementations grow only downward, one-way "inversion of responsibility" (lower calls upper's methods) is a cheaper, acceptable compromise.

**Rules:**
- B29-1: Do not design the integration interface as a transcript of the integrations you already have; design for the implementations you have not met yet. *Why:* "three imperatives to rule them all" fails on the first new device type. *Check:* Would a substantially different backend (e.g., a vending machine vs a staffed cafe) need to stub methods that mean nothing to it?
- B29-2: Express upper-level intent as context state and events (e.g., `takeout_requested`) rather than mandated method calls on the lower level. *Why:* each side implements only what is meaningful to it. *Check:* Can a lower-level implementation ignore an upper-level signal without writing a no-op handler?
- B29-3: Keep product concepts (e.g., "contactless takeout") out of hardware-level interfaces. *Why:* abstraction levels must stay isolated. *Check:* Does any low-level contract mention a term that only makes sense to end users?
- B29-4: Prefer one-way inversion of responsibility (lower level calls or sets state on its parent context) over full two-way event plumbing when alternative upper-level implementations are unlikely. *Why:* it cuts complexity without much design loss. *Check:* Is there a realistic scenario where a second higher-level context would sit on top of this lower-level entity?
- B29-5: Route state changes through the nearest higher-level neighbor, not a global dispatcher, and translate actions into that neighbor's vocabulary at each hop. *Why:* global state breaks abstraction isolation in deep hierarchies. *Check:* Does any low-level component call a global store or top-level method directly?
- B29-6: Delegate concrete work to the lowest level that can perform it; upper levels describe contexts, never algorithms. *Why:* upper-level prescriptions produce inconsistent, inapplicable methods. *Check:* Does the top-level API tell implementations how to execute rather than what outcome is expected?
- B29-7: Stop subdividing contexts when the context maps directly to what you can programmatically control; depth may differ per platform. *Why:* over-abstraction is waste. *Check:* Does each extra abstraction level add a real alternative implementation?
- B29-8: Recognize that weak coupling does not stop deprecation; its payoff is that partner code stays clean, so still track deprecated events and fields. *Why:* technology drift is unavoidable. *Check:* Is there a deprecation register for events/fields, not just methods?

**Techniques:**
- *Two contexts + two-way pipe:* Example: a job orchestrator emits `pause_requested`; a worker that supports pausing listens and then sets `paused` on the parent context; a worker that cannot pause simply never subscribes.
- *Inversion of responsibility:* the worker calls `job.setCompleted(result)` on its parent instead of emitting an event for the parent to catch.
- *Hierarchical dispatch:* each level exposes `dispatch(action)` that rewrites the action in its own terms and forwards it upward.

**Anti-patterns / smells:**
- Optional endpoints that some implementations must implement and others must not, decided by reading docs.
- Handlers that always return `true`/`ok` because the operation is meaningless for that backend.
- A shared global store mutated directly from leaf components.
- New device types requiring new mandatory methods on all existing implementations.

---

### Chapter 30. Interfaces as a Universal Pattern
Link: https://twirl.github.io/The-API-Book/API.en.html#back-compat-universal-interfaces

**Core idea:** The three preceding chapters reduce to SOLID applied to contracts: extend by generalizing, let higher levels be contexts, delegate concrete work downward. To avoid ad-hoc growth, model every entity from day one as an implementation of an explicit interface (or a composition of interfaces), even with no alternative implementation planned; the act of naming the interface reveals hidden coupling and future evolution paths.

**Rules:**
- B30-1: For each entity, name the abstract interface(s) it implements and which facet serves which consumer. *Why:* it exposes composite entities before they calcify. *Check:* Can you state "X implements I1 and I2, used respectively by A and B" for the entity?
- B30-2: Where one entity serves several consumers with different data needs, split it into sub-interfaces and define the linkage explicitly (e.g., machine price vs formatted price via a formatter). *Why:* otherwise consumers' needs leak into each other. *Check:* Are related values (machine-readable and human-readable) linked by a documented mechanism rather than assumed to agree?
- B30-3: Ask whether each interface is itself a subtype or composition of something more general, and record possible future directions. *Why:* it seeds extension points cheaply. *Check:* Does the design note list at least one anticipated alternative implementation per interface?

**Techniques:**
- *Interface decomposition:* Example: a "search result" is `IOrderParameters` (ids, price, currency) plus `IItemView` (title, description, formatted price); an `offer_id` can encode the former so the latter can evolve independently.

**Anti-patterns / smells:**
- Entities with no stated interface whose fields serve unrelated consumers.
- Human-readable and machine-readable values that "just happen" to match.

---

### Chapter 31. The Serenity Notepad
Link: https://twirl.github.io/The-API-Book/API.en.html#back-compat-serenity-notepad

**Core idea:** A short set of practical reminders for changing a live API: honor informal behavior, test the formal contract, insulate yourself from upstream APIs, build on your own public surface, and record the flaws you cannot fix now so the next major actually addresses them instead of being rushed.

**Rules:**
- B31-1: Treat observed behavior, including bugs, as part of the contract; if a bug fix would break real partners, emulate the old behavior until the next major. *Why:* partners depend on what happens, not what is documented. *Check:* Has usage data been examined to confirm nobody relies on the behavior a fix removes?
- B31-2: Write tests for the formal interface itself, including "trivial" invariants such as getters returning what setters stored. *Why:* trivial contracts are where untested bugs hide. *Check:* Is every documented invariant covered by an automated test?
- B31-3: Keep at least a provisional alternative implementation of every interface to prove the abstraction actually allows substitution. *Why:* an interface with one implementation may be secretly concrete. *Check:* Does a second (even mock) implementation exist and pass the same interface tests?
- B31-4: Never proxy an upstream or third-party API through as-is; wrap it in your own abstraction with extension points. *Why:* upstream changes and outages would otherwise hit your partners directly. *Check:* Is there any endpoint whose request/response mirrors an external vendor's format?
- B31-5: Put protective machinery in the isolation layer: rate limiting toward the upstream, retry/recovery policies, caching for partial degraded service, and automatic fallback to alternative providers. *Why:* it converts upstream failures into degraded rather than broken service. *Check:* What does your API return to partners when the upstream is fully down, and is it more than an error?
- B31-6: Build your own products and internal tools on the public API, not on private shortcuts that bypass it. *Why:* otherwise the public path is untested under real load and partners hit issues you never see. *Check:* Is there any public method whose internal equivalent takes a different code path?
- B31-7: When an interface is generalized, migrate the old concrete implementation onto the new general one instead of leaving both. *Why:* divergent behavior and hidden bugs accumulate. *Check:* After adding the general mechanism, does the legacy case run through it?
- B31-8: Never ship a backward-incompatible change as a minor version to fix a design flaw. *Why:* the API multiplies every mistake across all partners. *Check:* Does the proposed minor release change any documented or observable behavior?
- B31-9: Maintain a "serenity notepad": a running log of design flaws, inconsistencies, and lessons learned, reviewed when planning the next major. *Why:* you cannot foresee everything, but you can avoid repeating it. *Check:* Is there a living document of known design debt, and was it consulted for the next-major plan?

**Techniques:**
- *Bug emulation:* keep a `legacy_behavior` code path (e.g., default-stacking of unpositioned buttons) gated by API version until the next major.
- *Compiler bootstrapping analogy:* build version N of your tooling with the public interface of version N-1 to guarantee the public path is exercised.

**Anti-patterns / smells:**
- Fixing a long-standing bug without checking who relies on it.
- Interfaces with exactly one implementation and no substitution tests.
- Pass-through gateway endpoints mirroring a vendor's schema.
- Internal callers using private methods for functionality the public API also exposes.
- A "small" incompatible fix slipped into a minor release.

---

## Recommended Backward-Compatibility Policy (synthesized)

**Breaking change = anything that stops existing partner code from solving its task:**
- Removing/renaming any documented entity, field, method, event, or status.
- Changing observable behavior: consistency model, sync vs async callbacks, callback cadence, event order, allowed state transitions.
- Imposing new obligations on existing integrations (new mandatory inputs, "defaults" that were never agreed).
- Fixing a bug partners rely on without emulating it.
- Product changes that bypass documented flows without preserving expected events.
- Removing features that were undocumented but shown in samples, talks, or support answers.
- Spec changes that alter generated-client behavior even with an unchanged wire protocol.

**Not breaking:** cosmetic changes with no functional effect; additive optional parameters whose omission reproduces prior behavior; new endpoints/events that displace nothing.

**Cadence and support:**
- Majors: only for a critical mass of otherwise-impossible features (every several years in stable domains); never before the previous major has stabilized (months to a year).
- Major support: as long as apps live in the domain (platform LTS as a guide, usually years); retire by measured audience share with a published schedule.
- Minors: server/compiled-SDK APIs expose at least the two latest minors once mature; code-on-demand SDKs keep prior minors for at least one app-release cycle (up to several months); code-on-demand majors: latest plus penultimate, optionally reimplemented over the new server.
- Allow pinning to exact major.minor.patch for a reasonable period; provide alpha/beta channels.

**Deprecation:** publish the undocumented-feature policy up front; announce deprecations explicitly; keep deprecated behavior working or emulated until the next major; log flaws in the serenity notepad instead of fixing them incompatibly; give partners pre-release access to test migrations.

## What a "Backward-Compatible Specification" Entails

A spec change is compatible only if every client written or generated against the old spec keeps working against a server implementing the new one. Since that depends on every code generator's behavior, it is not verifiable in general. So: avoid spec constructs with contested semantics (e.g., `additionalProperties: false`); assess generated code as if hand-written; remember behavior can break with an unchanged spec and vice versa; prefer spec-first over code-first to limit drift; and when in doubt, test each supported generator's output manually.
