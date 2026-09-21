# Section V: SDKs & UI Libraries (chapters 40-48)

Source: "The API" by Sergey Konstantinov (CC BY-NC 4.0); everything below is paraphrased. **SDK** = native client library wrapping a technology-agnostic API; **UI library** = client library that also ships visual components.

---

### Chapter 40. On Terminology. An Overview of Technologies for UI Development
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-toc-technology-overview

**Core idea:** The useful narrow meaning of "SDK" is a high-level, platform-native library over a general-purpose API; UI libraries add a second audience (end users) and much more design complexity. No UI framework is universally right, and cross-platform toolkits trade peak performance and native tooling for speed and reuse.

**Rules:**
- S40-1: State explicitly which parts of the kit are pure API wrappers and which are user-facing components. *Why:* the two have different audiences and constraints. *Check:* Does the architecture doc separate transport-wrapper modules from visual-component modules?
- S40-2: Choose target UI frameworks per platform from measured market adoption, and record what a cross-platform choice gives up (performance, native debugging/profiling). *Why:* every framework enforces its own methodology and the trade-off must be conscious. *Check:* Is there a written, data-backed rationale for supported and unsupported frameworks/platforms?

**Techniques:** *Layered toolkit* — a maps-style SDK exposes HTTP wrappers (`client.search()`), domain components (`MapView`), and generic widgets (`Button`, `Popup`) usable without the domain part.

**Anti-patterns / smells:**
- A docs-plus-zip bundle called an "SDK" with no native high-level surface.
- A UI library locked to one framework with no stated reason while customers use another.
- Two mobile SDKs whose method names diverge for no reason.

---

### Chapter 41. SDKs: Problems and Solutions
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-problems-solutions

**Core idea:** An SDK should absorb the mistakes and boilerplate every client would otherwise repeat: type and naming conversion, native errors, safe retries, id-to-object joins, caches, subscriptions, and recovery from expected business errors. Generators solve the mechanical half; the high-level half needs handwritten code. The payoff is fewer client bugs, less irrelevant partner work, and more vendor control.

**Rules:**
- S41-1: Convert wire data into native types (dates, maps, enums), native naming, and the platform's idiomatic error mechanism. *Why:* wire formats lack these and each client would reinvent them. *Check:* Do methods return native datetime/collection objects and raise typed language-native errors?
- S41-2: Put retries inside the SDK: honor `Retry-After`, back off exponentially, cap attempts, and retry only idempotent requests. *Why:* clients skip this and blind retries can overload servers. *Check:* Does the SDK refuse to auto-retry non-idempotent calls and respect server delays?
- S41-3: Accept and return object references, and hydrate related entities (eagerly or lazily, with a cache) so one SDK call replaces several dependent API calls. *Why:* pass-by-value responses force clients into error-prone join code. *Check:* Can a caller pass a fetched object instead of its id, and do results already link to related entities?
- S41-4: Let the SDK own cross-request state (auth tokens, idempotency keys, draft ids, read-your-writes tokens). *Why:* these rules are hard to formalize and clients get them wrong. *Check:* Is there any protocol token a caller must carry manually between calls?
- S41-5: Offer subscriptions on entity objects (`order.on('stateChange')`) and guarantee no event is lost between fetching and subscribing. *Why:* raw streams require id mapping and are race-prone. *Check:* Can a developer watch one returned object without touching transport topics or polling?
- S41-6: Handle recoverable business errors (expired offer, optimistic-lock conflict, consistency lag) inside the SDK. *Why:* the recovery loop is bulky, error-prone, and invisible to users. *Check:* Is there an error type every correct client would handle with the identical retry/renew loop?
- S41-7: If the SDK hides the raw API, make it complete enough that nobody needs to bypass it, including across major API versions; use generated clients as a base, never as the whole SDK for a non-trivial API. *Why:* vendor control only works without leaks, and generators cannot solve callbacks or recovery. *Check:* Is every API capability reachable through the SDK, and is there a handwritten layer above the generated client?

**Techniques:**
- *Error normalization:* status + body -> `RateLimited(retryAfter=…)` subclass of `SdkError`.
- *Retry policy:* `retry(fn, {idempotent: true, maxAttempts: 5, backoff: exp(200ms), honorRetryAfter: true})`.
- *Hydration / coalescing:* `sdk.search({recipes})` returns offers with `offer.recipe` attached; concurrent `getRecipe('lungo')` calls share one request and a TTL cache.
- *Pagination helper:* `for await (const o of sdk.listOrders())` hides cursors.
- *Transparent recovery:* `sdk.placeOrder(offer)` renews an expired offer up to N times internally.

**Anti-patterns / smells:**
- Callers build `new Map()` to join two responses by id.
- App code contains `do { try create } catch (OfferExpired) { renew } while` loops.
- Fetch-then-subscribe races; events for unknown ids crash listeners.
- Dates as strings, snake_case in a camelCase language.
- The "SDK" is only a generated client and every partner repeats the same rookie mistakes.

---

### Chapter 42. Problems of Introducing UI Components
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-ui-components

**Core idea:** A visual component is not a projection of API methods; it merges API functionality with platform interaction conventions and carries its own state. Three structural problems follow: one entity couples logic, look, and UX behavior; components share the screen and the user's attention so concurrent callers collide; and properties inherit from both a visual and a data hierarchy with unclear precedence. Full customizability roughly triples the API surface, so expose it sparingly.

**Rules:**
- S42-1: Make appearance, business action, and interaction behavior of a control independently replaceable. *Why:* partners restyle, add actions, or change UX one at a time. *Check:* Can a partner restyle a standard button without touching what it does or how it animates?
- S42-2: For every component method that a user can also trigger (e.g. `search()`), document the conflict policy: which caller wins, and what the interrupted call returns. *Why:* unlike HTTP calls, UI callers share one screen. *Check:* Does each async component method's doc say what happens when it overlaps a user action?
- S42-3: When a property can come from data and from control type, give the more specific (semantic) source precedence and write the rule down. *Why:* two inheritance lines otherwise yield surprising rendering. *Check:* Is there one documented ordering for resolving e.g. a button icon?
- S42-4: Add a customization hook only when a real partner scenario needs it and its natural use reads cleanly; no hook beats a misleading one. *Why:* patching view options inside a data-fetch override is unmaintainable. *Check:* For each override point, would a reviewer expect that customization to live where the example puts it?

**Techniques:** *Three-axis control* — `new Button({view: PrimaryLook, action: callShop, behavior: StackedPress})`, each axis defaulting independently. *Latest-wins search* — tag requests with a sequence number and drop responses older than the newest issued.

**Anti-patterns / smells:**
- Subclassing a button to change color also changes what it does.
- An older search response overwrites newer results.
- `item.createOrderButtonIconUrl = …` set inside a search override to swap an icon.
- Undefined ordering between injected factories, render callbacks, and custom layouts.

---

### Chapter 43. Decomposing UI Components
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-decomposing

**Core idea:** Naive nesting (SearchBox creates OfferList creates OfferPanel) fails every realistic customization: swapping the list for a map needs feedback from the panel, merging list and panel needs a rewrite, extra buttons need option plumbing through each layer. Events, parent routing, and event proxying each fix one problem and add coupling, level-jumping, or loops. The root cause is a missing abstraction level: a "Composer" that owns the context, builds subcomponents, prepares their data, and translates their events.

**Rules:**
- S43-1: Insert a composer/presenter layer between the abstract top-level component and concrete subcomponents; the top level must not know how results are displayed. *Why:* customization breaks when code jumps abstraction levels. *Check:* Does the top-level interface mention any specific subcomponent or its state?
- S43-2: The composer creates subcomponents through overridable builder methods and generates their data facets and options through overridable generator methods. *Why:* swapping a subcomponent or enriching its data then needs one override. *Check:* Can a partner replace the list with a map, or add a panel field, by overriding a single method?
- S43-3: Subcomponents never construct, hold, or call siblings; they emit low-level events, and the composer translates them into differently named high-level events and owns shared state such as the current selection. *Why:* direct links prevent independent reuse, and same-named re-emitted events loop. *Check:* Does any subcomponent receive a sibling in its constructor, or re-emit an event under the same name it listens to?
- S43-4: Do not extend interfaces through optional methods guarded by runtime type checks. *Why:* it hides coupling and grows unreadable. *Check:* Are there `if (typeof x.onSomething === 'function')` guards between components?

**Techniques:**
- *Composer layout:* `SearchBox` (context, `search()`, `createOrder()`) -> `Composer` (state `offerList`, `currentOffer`; `buildOfferList()`, `generateOfferPreviews()`; `performAction()`) -> `OfferList`/`OfferPanel` (render, emit).
- *Three customization routes:* same concept, new rendering -> override a builder; new concept (in-place expansion) -> custom composer reusing standard leaves; extra data/buttons -> override generators and add action translations.
- *Weak coupling:* panel emits `action:{type:'close'}`; composer clears `currentOffer` and emits `offerFullViewToggle`.

**Anti-patterns / smells:**
- `OfferList` instantiates `OfferPanel`; panel calls `searchBox.createOrder()` two levels up.
- `offerPanelCreateOrderButtonText` threaded through an intermediate component.
- Top-level component is a bulk proxy for child events.
- A subclass that only works with one specific sibling implementation.

---

### Chapter 44. The MV* Frameworks
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-mv-frameworks

**Core idea:** Restricting interaction directions (views read the model and emit events, controllers mutate the model, the model notifies) gives MVC and its siblings; their shared core is that the model deterministically defines the UI. This removes loops, separates semantic data from rendering, and enables deep links, undo, and crash recovery. Costs: a "complete" model absorbs low-level visual state and becomes version-fragile, and nested controllers reintroduce coupling. MVP's stateless presenter resembles the composer but limits subcomponent replacement.

**Rules:**
- S44-1: Enforce one-way flow: views only read state and emit interaction events; only the controller/composer mutates the context. *Why:* two-way access creates feedback loops. *Check:* Does any view write to the shared model directly?
- S44-2: Fire change notifications only when a value actually changes. *Why:* makes accidental oscillation nearly impossible. *Check:* Does setting a field to its current value emit an event?
- S44-3: Keep only semantic data in the model; derive presentation values (icon URLs, animation progress) in the presenter, and treat any serialized model (URL, app link) as a versioned public contract. *Why:* mixed models serialize into blobs that break on UI refactors. *Check:* Can a serialized state be restored by a newer SDK whose subcomponents render differently?
- S44-4: Give nested components their own local models (a slice of the parent plus own state) rather than one global model every nested controller mutates. *Why:* otherwise nested controllers recreate the coupling MV* removed. *Check:* Do child components depend only on a projected slice of parent state?

**Techniques:** *MVC mapping* — model = SearchBox context, views = list/panel/input, controller = composer. *Deep-link state* — `model.toURL()` -> `/search?q=lungo&selected=o42`, restored with `SearchBox.fromURL()`. *MVP presenter* — stateless `presenter.panelProps(model)`; a color change means adding a semantic model field the presenter maps to color.

**Anti-patterns / smells:**
- Views calling `model.set()`.
- Model holds `animationProgress` or `computedIconUrl`.
- Deep links break after a minor UI refactor.
- Nested controllers reaching into the global model or calling parent controllers ad hoc.

---

### Chapter 45. The Backend-Driven UI
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-backend-driven

**Core idea:** Removing business logic from the client altogether (the server returns markup or a list of actions; the component renders and forwards events) gives the vendor runtime control and avoids designing a rich SDK vocabulary, but it needs a fast link, forgoes client-only capabilities, forces opaque hybrid code, and hides component state from partners. It works for widgets and ad inlets, not as a general SDK paradigm. It is not SSR, where clients can still parse server output into data.

**Rules:**
- S45-1: Use backend-driven rendering only for narrow, low-interactivity surfaces where instant vendor control outweighs latency and opacity. *Why:* no notable full product has succeeded with it. *Check:* Is the component simple enough that partners never need to inspect or extend its state?
- S45-2: When shipping server-rendered content, publish an explicit protocol for permitted client-side enrichment (styling, event hooks). *Why:* undocumented hybrid code is harder than pure client code. *Check:* Is there a documented interface between server content and partner code?
- S45-3: If the client must extract structured data from the response, build SSR, not backend-driven UI. *Why:* the two differ in whether the client understands the content. *Check:* Can the client parse semantic data out of what the server sends?

**Techniques:** *Markup mode* — `search(q)` fetches `{html}` and injects it. *Action-list mode* — client sends `(model, patch)` and receives `[{op:'show', target:'panel'}, …]`.

**Anti-patterns / smells:**
- A "full SDK" whose components are opaque iframes with no state accessors.
- Partner code scraping server HTML for element ids.
- UI freezes on slow networks because every interaction round-trips.

---

### Chapter 46. Shared Resources and Asynchronous Locks
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-shared-resources

**Core idea:** Once opening a view is asynchronous, overlapping attempts (user vs. developer vs. another click) need arbitration. Leaf-emitted `isLoading` flags are unreadable, unextendable, and deadlock on exceptions. Reframe it as a shared resource (the screen slot) protected by named, timed locks acquired by the composer, carrying acquirer metadata for priority and a "lost" hook for cancellation. Spinners don't remove the need for a policy.

**Rules:**
- S46-1: Name locks after the UI resource (`offerFullView`), not the technical cause (`isDataLoading`), and let the composer that prepares the data own them. *Why:* the arbiter must see all contenders and readers must know what is blocked. *Check:* Are blocking flags named for a UI resource and set by the coordinating layer, not a leaf?
- S46-2: Implement acquire/release with a mandatory TTL and release in `finally`. *Why:* exceptions or hung requests otherwise block the UI forever. *Check:* Does every acquire carry a timeout and a release path on error?
- S46-3: Pass acquirer identity and reason, let the holder yield or refuse, and fire a "lost" hook so the displaced actor cancels in-flight work. *Why:* contenders are not equal (API call may outrank a click) and stale results must not land later. *Check:* Can a request state who wants the resource and why, and is there a callback when it is taken away?
- S46-4: Define the overlapping-open policy even when using placeholders. *Why:* placeholders change rendering, not arbitration. *Check:* Does the doc say what happens if a second open arrives during loading?

**Techniques:** *Timed lock* — `lock = await locks.acquire('offerFullView','10s',{reason:'userSelect',offer}); try {…} finally {lock.release()}`. *Priority policy* — `lock.on('tryAcquire', a => a.reason==='apiSelect' ? lock.release() : false)`. *Model-level locks* — read/write locks per model field group.

**Anti-patterns / smells:**
- `beginDataLoad`/`endDataLoad` events from a panel flipping a flag in another component.
- UI stays blocked after a failed request.
- Two rapid selections: panel shows the first, list highlights the second.
- No way to say "developer-initiated open beats user-initiated".

---

### Chapter 47. Computed Properties
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-computed-properties

**Core idea:** A property such as an icon may be inheritable from data hierarchies, option hierarchies, base classes, and theme overrides. Forbidding inheritance produces boilerplate; a single fixed precedence produces the same boilerplate for anyone needing a different order. Better: let developers declare resolution rules per component/property (CSS-like, but a small subset), and always expose the applied value separately from the set value, with change events.

**Rules:**
- S47-1: For any multi-source property, provide a scoped rule mechanism (declarative mapping or resolver function) instead of a hard-wired precedence, and keep the rule language small. *Why:* fixed precedence pushes logic into copy-pasted client code; a full CSS cascade is overkill. *Check:* Can a partner change where `button.checkout.iconUrl` comes from without subclassing or patching data, using a syntax documented in under a page?
- S47-2: Distinguish set from computed values: expose a computed accessor and emit an event when the computed value changes. *Why:* callers need the applied value (`100%` -> `320px`), and upstream changes alter it silently. *Check:* Is there a `computed*` reader for every rule-resolved property, and does changing a parent option notify the child?

**Techniques:** *Declarative rule* — `{"button.checkout.iconUrl": "@data.chain.iconUrl"}`. *Imperative rule* — `sdk.rules.add('button.checkout.iconUrl', (data, opts) => data.iconUrl ?? opts.iconUrl)`. *Computed read* — `view.width = '100%'; view.computed.width // 320`.

**Anti-patterns / smells:**
- Partner code with `if (data.x) btn.icon = data.x; else if (data.parent.y) …` repeated per button.
- `this.data.iconUrl || this.options.iconUrl` hardcoded with no override path.
- No way to read the final rendered value of an inherited or percentage property.

---

### Chapter 48. Conclusion
Link: https://twirl.github.io/The-API-Book/API.en.html#sdk-conclusion

**Core idea:** A quality UI library is a hard engineering product; it cannot be mechanically derived from a spec or data model, because the hard parts (abstraction bridges, shared-resource arbitration, property resolution) are architectural.

**Rules:**
- S48-1: Plan and staff the UI library as a full product with handwritten composer, lock, and rule layers on top of any generated client. *Why:* generation solves only the mechanical layer. *Check:* Does the roadmap include work beyond code generation from the API spec?

**Techniques:** none new.

**Anti-patterns / smells:**
- "We'll generate the UI SDK from the OpenAPI schema" as the entire plan.
