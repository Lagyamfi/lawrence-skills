# Section VI: The API Product (Chapters 49-61) — distilled rules

Source: "The API" by Sergey Konstantinov, CC BY-NC 4.0. All text below is paraphrased.

---

### Chapter 49. The API as a Product
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product

**Core idea:** An API is a real product and needs real product management (market research, customer needs, competitor analysis), but it is sold to three stacked audiences at once: end users (want their problem solved), business owners (want cheap, reliable functionality), and developers (the only ones who touch the API directly). Which layer actually makes the buying decision varies by market, so you must be able to state precisely why anyone would want to do this thing *programmatically*.

**Rules:**
- Q49-1: Write down, in one paragraph, why a customer would prefer to perform the API's actions via code rather than a UI. *Why:* without this the product has no reason to exist. *Check:* Does the product brief contain an explicit "why an API" statement?
- Q49-2: Identify which of the three audiences (users, business, developers) drives the adoption decision in your market and weight product effort accordingly. *Why:* developer-led products over-invest in elegance; customer-led ones under-invest in it. *Check:* Does the vision name the decision-making audience and the evidence for it?
- Q49-3: Address all three audiences in positioning: user value, business guarantees and cost, developer capability and convenience. *Why:* each layer can veto adoption. *Check:* Does the landing/pitch material speak to each of the three groups?

**Anti-patterns / smells:**
- API team is composed entirely of engineers who evaluate competitiveness only on code elegance.
- No market research or competitor comparison exists for the API.
- Nobody can explain how end users would know or care which API powers the app.

---

### Chapter 50. API Business Models
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-business-models

**Core idea:** The way an API makes (or saves) money determines its product decisions and KPIs, so pick the model deliberately. Models range from selling developer tooling, to the API being the sole gateway to a paid service, partner programs, paid access to unique data/expertise, ad placement, brand/tech-PR, UGC collection, and "terraforming" a market for free. Exposing an internal API externally without reworking it for partners is a reputational trap.

**Rules:**
- Q50-1: Choose and document one primary monetization model before setting KPIs or roadmap. *Why:* target actions, pricing and support budgets all derive from it. *Check:* Is the monetization model written down and referenced by the KPI definition?
- Q50-2: Do not publish an internal API as an external product without redesigning it for partners' stacks, docs, support and compatibility needs. *Why:* partner interests get starved and the API damages the brand. *Check:* Does the external API have its own roadmap, support budget and compatibility policy independent of internal consumers?
- Q50-3: If resources for a proper external product are absent, do not launch it. *Why:* a bad API to a skeptical audience is worse than none. *Check:* Is there a funded team whose primary customers are external partners?
- Q50-4: In partner programs, define measurable integration-quality thresholds (e.g., minimum conversion ratio) and pay for goal completions, not raw traffic. *Why:* prevents partners gaming payouts. *Check:* Does the partner agreement state performance requirements?
- Q50-5: For data/expertise APIs, prefer hybrid pricing (free up to a threshold or for non-commercial use, paid beyond). *Why:* maximizes ecosystem growth while capturing value. *Check:* Are free limits and paid tiers defined and enforced?
- Q50-6: Treat monetizing user request data as a legal grey zone; obtain legal review per jurisdiction before doing it. *Why:* legality varies by place and time. *Check:* Has legal signed off on every data-analysis revenue stream?
- Q50-7: Go API-first only if the market has paying builders, quality does not suffer from API-only access, and the team has genuine API design expertise. *Why:* otherwise the product will be redesigned or discontinued. *Check:* Are all three preconditions documented as met?
- Q50-8: Do not use an API merely to "test the market" before building a first-party product. *Why:* it ends with the API being cut or crippled, betraying partners. *Check:* Is the API committed to as a long-term product regardless of first-party plans?

**Checklist — business model choice:**
- [ ] Which of the nine models applies (tooling, sole gateway, partner program, added access to expertise, ad site, self-PR, UGC/feedback, terraforming, data)?
- [ ] Who pays, for what unit (license, calls, service usage, goal completions, nothing)?
- [ ] Is the free tier bounded and the paid trigger clear?
- [ ] Are partner obligations (branding, performance, licensing restrictions) contractually stated?
- [ ] Is the external API materially different from the internal one (docs, SDKs, lineup, compat policy)?
- [ ] API-first preconditions verified (market heat, quality, expertise)?

**Anti-patterns / smells:**
- Roadmap is opaque to partners and obvious partner-facing bugs sit unresolved for years.
- Internal teams break compatibility whenever convenient and external partners find out afterwards.
- Docs cover only the internal use cases; no SDKs beyond the internal stack.
- Revenue relies on reselling user data without a documented legal basis.

---

### Chapter 51. Developing a Product Vision
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-vision

**Core idea:** The vision must link end-user needs, the businesses that would serve them, and the technical tools developers would need. Because the audiences are layered, the vision is built via two-step heuristics and remains fuzzy; that is normal and should be refined as the market forms. Validating hypotheses is expensive because partners must invest to try an MVP, so the team needs reference apps, internal customers, and its own "pet projects."

**Rules:**
- Q51-1: State the vision as three linked parts: user problem, how businesses would solve it with tools, and what technical capabilities make that possible (and their limits). *Why:* missing any layer produces features no one integrates. *Check:* Does the vision document have all three sections?
- Q51-2: Gather feedback from developers and business owners separately and correct for each group's blind spots. *Why:* devs report integration pain, businesses report market pain; neither sees the whole. *Check:* Are interview results tagged by audience and cross-analysed?
- Q51-3: When analysing usage logs, do it per application and cluster common scenarios rather than aggregating globally. *Why:* per-app behaviour differs widely. *Check:* Are scenario clusters derived per partner app?
- Q51-4: Budget an MVP to include either partner compensation or a vendor-built reference implementation. *Why:* partners will not risk their money on your experiment. *Check:* Does every product experiment have a funded reference app or partner incentive?
- Q51-5: Use internal teams as early adopters, but note which hypotheses cannot be validated that way. *Why:* internal customers are loyal but only reflect internal needs. *Check:* Is each hypothesis marked as validated internally, externally, or not at all?
- Q51-6: Fund team pet projects on the API (free quotas, compute) and rotate roles. *Why:* dogfooding reveals doc gaps and gives PMs and devs each other's perspective. *Check:* Do team members have active applications built on the public API?

**Checklist — API vision/roadmap:**
- [ ] User need, business opportunity, technical enablers written and linked.
- [ ] Decision-making audience identified.
- [ ] Terraforming stage acknowledged and revisited on a schedule.
- [ ] Feedback sources: dev interviews, business interviews, per-app log clustering.
- [ ] Each hypothesis has a validation path (reference app, internal customer, funded partner).
- [ ] Pet projects exist and are reviewed for documentation friction.

**Anti-patterns / smells:**
- Vision is purely technical ("we expose X") with no stated user outcome.
- MVP shipped with no reference app and no partner takes it up.
- Team has never integrated its own API from scratch.

---

### Chapter 52. Communicating with Developers
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-devrel

**Core idea:** Developers are rational, skeptical, verify claims, distrust influencers and adverts, and get information from specialised communities. Reach them with substantive content (articles, answers, talks, courses) produced by your own engineers to review-level quality, with incentives. Open-sourcing has real benefits and real costs and must be decided carefully. A large share of your audience are non-professional developers, which shapes support, content and product lineup.

**Rules:**
- Q52-1: Promote via technical content (code-backed articles, Q&A answers, talks, courses), not direct advertising. *Why:* developers verify claims and ignore ads. *Check:* Does every promotional piece contain runnable code or concrete numbers?
- Q52-2: Reward engineers for tech-PR work and review content with the same rigour as code. *Why:* poor or thinly disguised sales pitches are counter-advertising. *Check:* Is there a content review step and an incentive for authors?
- Q52-3: Keep developer-facing communication expertise inside the product team even if evangelists exist. *Why:* direct contact feeds the product vision. *Check:* Do team engineers personally answer community questions or speak at events?
- Q52-4: Decide on open-sourcing only after costing code cleanup, tooling migration, community moderation, security exposure, fork risk and license choice. *Why:* preparation is expensive and irreversible. *Check:* Is there a written pros/cons and license decision record?
- Q52-5: Design content, support and products for two audiences: amateurs needing simplicity and professionals needing customisation. *Why:* one product cannot serve both well. *Check:* Are materials and tiers labelled by target skill level?

**Checklist — developer relations:**
- [ ] Channels: community blogs, Q&A sites, educational platforms, conferences/webinars.
- [ ] Content pipeline with authorship incentives and editorial review.
- [ ] Engineers rotate through community engagement.
- [ ] Evangelist role (if any) complements, not replaces, team involvement.
- [ ] Open-source decision: cleanup cost, license, split open/proprietary, security review.
- [ ] Beginner track and professional track for talks, docs, samples.

**Anti-patterns / smells:**
- Banner ads on developer sites; talks that are product pitches in disguise.
- Conference slides with errors nobody reviewed.
- Interfaces claimed as intellectual property, provoking community backlash.
- All docs assume expert-level knowledge, or all assume none.

---

### Chapter 53. Communicating with Business Owners
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-business-comms

**Core idea:** Business partners are more enthusiastic than developers but far harder to explain an API to, and the further their industry is from IT the less their enthusiasm converts into integrations. Bridge the gap by cultivating a pool of freelancers/integrators and certified specialists, and treat non-technical feedback critically.

**Rules:**
- Q53-1: Sell the API to business owners in terms of product outcomes and guarantees, not interfaces. *Why:* non-technical buyers cannot evaluate API concepts. *Check:* Is there business-facing material with no code and clear benefit statements?
- Q53-2: Build an integrator ecosystem (freelancers, agencies) plus training courses and certifications. *Why:* non-IT businesses need someone to do the integration. *Check:* Is there a partner/integrator directory or certification program?
- Q53-3: Interpret business feedback critically and creatively, since non-IT businesses articulate needs poorly. *Why:* raw requests often misstate the underlying problem. *Check:* Are business requests reframed into problem statements before entering the backlog?

**Anti-patterns / smells:**
- Many enthusiastic signed LOIs, few live integrations.
- Feature requests from business partners implemented literally without root-cause analysis.

---

### Chapter 54. An API Services Lineup
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-lineup

**Core idea:** Ship a two-dimensional lineup, not a single API. Horizontally, split into independently usable, versioned and priced services when audiences and use cases do not overlap. Vertically, offer the same capability at several abstraction levels: low-level/physical, base API, platform SDKs, code generators, and ready-made widgets. Higher levels give the vendor more control over partner integrations (versions, UI experiments, KPIs) and suit typical partners; lower levels suit expert partners building unique services.

**Rules:**
- Q54-1: Split an API into separate products only when a part is independently useful, independently versionable, independently priced, or has a distinct audience. *Why:* otherwise you create a version-compatibility matrix nightmare. *Check:* Does each separately branded API meet at least one of the four criteria and maintain strict compatibility?
- Q54-2: Offer a vertical ladder (base API, SDKs, code generation, embeddable widgets) so amateurs and professionals each have a fitting entry point. *Why:* a single product cannot serve both entry thresholds. *Check:* Can a novice integrate a typical case with a one-liner, and can an expert access the base API?
- Q54-3: Steer typical-use partners to the highest-level (most controlled) integration and expert partners to the most flexible one. *Why:* control eases version fragmentation and experimentation; flexibility wins niche partners. *Check:* Does onboarding recommend an integration level based on the partner's needs?
- Q54-4: Ensure high-level components fully encapsulate their internals (no "escaping the sandbox"). *Why:* control only exists if partners cannot reach low-level objects. *Check:* Are widget internals inaccessible from partner code?
- Q54-5: Prefer integration options that retain vendor control (e.g., avoid raw hotlinkable URLs as the primary integration). *Why:* uncontrolled integrations cannot be evolved or monetised. *Check:* Does every offered integration path allow the vendor to change behaviour server-side?
- Q54-6: Bundle split APIs into a unified SDK where it simplifies developers' lives. *Why:* product granularity should not fragment the developer experience. *Check:* Is there one SDK entry point across services?

**Checklist — API lineup/tiers:**
- [ ] Horizontal split justified per service (usefulness, versioning, tariffs, audience).
- [ ] Vertical levels present: low-level, base, SDKs per major platform, codegen/point-and-click, widgets/iframes/deep links.
- [ ] Each level documented with target audience and control trade-offs.
- [ ] Widgets encapsulate internals; iceberg-waterline rule enforced.
- [ ] Per-integration-type partner counting in analytics (see KPIs).

**Anti-patterns / smells:**
- Several "separate" APIs whose versions must be matched pairwise.
- Only a raw HTTP API offered; beginners churn on onboarding.
- Widgets expose internal objects that partners hack, freezing the widget's evolution.

---

### Chapter 55. API Key Performance Indicators
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-kpi

**Core idea:** If the API earns money directly, measure money. Otherwise raw user and partner counts are necessary but misleading (widgets inflate numbers, partners over-embed, penetration saturates); the real KPI is target actions tied to the monetization model. Availability, capacity headroom and security are hygiene metrics, and all numbers must be benchmarked against the market.

**Rules:**
- Q55-1: Define the KPI as counts of target actions derived from the monetization model, not as raw users or integrations. *Why:* raw counts are distorted by lightweight embeds and sub-optimal usage. *Check:* Is the primary KPI a target action (ad click, transition, review, paid partner) rather than a headcount?
- Q55-2: Count partners and usage separately per integration type (widget vs SDK vs base API). *Why:* one full integration can equal hundreds of trivial embeds. *Check:* Does the dashboard segment by integration level?
- Q55-3: Track feature-level usage to prioritise development, and disclose any telemetry in libraries. *Why:* silent data collection triggers backlash. *Check:* Is telemetry documented and opt-in/opt-out where applicable?
- Q55-4: For PR-driven APIs, track indirect proxies (docs traffic, mentions, blog/event audience). *Why:* effects are cumulative and indirect. *Check:* Are proxy metrics defined and trended?
- Q55-5: Track and publish SLA/availability, especially for paid APIs. *Why:* outages multiply across every partner. *Check:* Is uptime measured and reported against a stated SLA?
- Q55-6: Provision capacity to survive your largest partner suddenly calling the API on every page/screen (or doubling their init calls). *Why:* a one-line partner change can multiply load. *Check:* Does the load test model at least a 2x surge from the top partner?
- Q55-7: Apply maximum security posture (strong crypto, fast vulnerability response) even for trivial APIs. *Why:* one vendor hole becomes a hole in every partner app. *Check:* Is there a vulnerability disclosure process with response SLAs?
- Q55-8: Benchmark market share and growth rate against competitors, using scraping of partner sites or commissioned research if needed. *Why:* growth may be market-driven, not effort-driven. *Check:* Is there a periodic competitor-share estimate?

**Checklist — KPIs to track:**
- [ ] Revenue (if direct).
- [ ] Users and partners, segmented by integration type and by direct vs derivative partners.
- [ ] Target actions aligned to model (ad interactions, transitions to core service, UGC edits, paid partners).
- [ ] Feature usage frequency.
- [ ] PR proxies: docs audience, mentions, blog/webinar reach.
- [ ] SLA: availability, latency; capacity headroom vs top partner.
- [ ] Security: vulnerability reports, time to fix.
- [ ] Market share and relative growth.

**Anti-patterns / smells:**
- Success reported as "N integrations" with no engagement metric.
- Dashboards do not distinguish widgets from full integrations.
- No load headroom; a partner deploy takes the API down.
- Undisclosed usage telemetry in an SDK.

---

### Chapter 56. Identifying Users and Preventing Fraud
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-antifraud

**Core idea:** You must identify both developer-partners (applications and their legal owners, separately) and end users to plan capacity, cost usage and bill correctly. API keys are the standard but are weak: they are easily multiplied, stolen, and contact data goes stale. Cross-check keys against app-store IDs, Referer/Origin and network aggregates, and accept that end-user identification is heuristic and legally constrained.

**Rules:**
- Q56-1: Model applications and owners as distinct entities and track each owner's apps separately. *Why:* limits and tariffs differ by app type. *Check:* Can the system list all applications under one legal owner?
- Q56-2: Require formal partner identification (key plus domain or store app ID at initialisation). *Why:* it enables cross-checks and contact. *Check:* Is a store ID or domain mandatory when obtaining/initialising a key?
- Q56-3: Never trust key-based identity alone; cross-check Referer/Origin and app IDs against the registration and flag mismatches. *Why:* keys are stolen, shared and multiplied. *Check:* Are key-vs-Referer and key-vs-app-ID mismatches alerted on?
- Q56-4: Whitelist localhost/loopback Referers and your own sandbox with unlimited quota. *Why:* otherwise you block local development and your own site first. *Check:* Do requests from 127.0.0.1/[::1]/localhost bypass limits?
- Q56-5: Count both direct partners and downstream partners built on top of them. *Why:* large partners resell your API to smaller ones. *Check:* Does partner accounting capture derivative integrations?
- Q56-6: Require server-to-server partners to forward end-user IPs (e.g., X-Forwarded-For). *Why:* enables audience stats and helps partners fight fraud. *Check:* Is IP propagation part of the S2S integration contract?
- Q56-7: Aggregate IP statistics hierarchically (/8, /16, /24, AS, known proxies/Tor) instead of counting unique addresses. *Why:* IPv6 makes unique addresses meaningless. *Check:* Do dashboards show network- and AS-level aggregates?
- Q56-8: Treat cookies and IPs as regulated personal data; prefer dropping cookies and hashing/anonymising per jurisdiction. *Why:* legal and browser restrictions are tightening. *Check:* Has data-collection been reviewed by legal for each region served?

**Checklist — identification design:**
- [ ] Key issuance requires contact info plus domain/app ID.
- [ ] Owner vs application separation in data model.
- [ ] Multi-account detection (phone/card checks acknowledged as bypassable).
- [ ] Referer/Origin/app-ID cross-checks with investigation workflow.
- [ ] Loopback and sandbox whitelist.
- [ ] Network aggregate dashboards; proxy/Tor tagging.
- [ ] Legal review of IP/cookie handling.

**Anti-patterns / smells:**
- Contact emails for keys bounce or belong to departed employees.
- Free-tier abuse via dozens of keys per app goes undetected.
- Local development is rate-limited or banned.
- Partners' public endpoints become free proxies to your API with no detection.

---

### Chapter 57. The Technical Means of Preventing ToS Violations
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-tos-violations

**Core idea:** Fighting misuse is three steps: detect suspicious users (static surges and behavioural patterns, tracked by both tokens and IPs), optionally demand a second factor (which must be designed into the API upfront), and restrict access. Real restriction options are few (IP bans, mandatory identification, fake responses, abuse reports); mostly you raise the attacker's cost and buy time for administrative action. Escalate technical defenses only when the threat justifies it, and give partners tools to limit what stolen keys can do.

**Rules:**
- Q57-1: Run detection on two parallel identities, tokens and IP/network, because attackers discard or rotate tokens. *Why:* single-identity tracking is trivially evaded. *Check:* Are both token-based and IP-based anomaly monitors in place?
- Q57-2: Combine static surge detection (by network, Referer, OS, language) with behavioural analysis (inhuman sequences, too-short intervals). *Why:* each catches different abuse. *Check:* Are both detector types implemented?
- Q57-3: Reserve a "further verification required" response (captcha, phone, 3-D Secure step) in the interface from version one. *Why:* it cannot be added backward-compatibly later. *Check:* Does the API contract include an extra-authentication-required state?
- Q57-4: Do not rely on bans keyed to client-supplied data (cookies, Referer, User-Agent). *Why:* trivially forged. *Check:* Are effective restrictions based on IP/network, identity tiers, or abuse filings?
- Q57-5: Avoid fake responses as a default sanction; treat them as legally and ethically risky given false positives. *Why:* real users may receive bogus data. *Check:* Is any decoy response gated by legal approval and high confidence?
- Q57-6: Monitor and log all abusers continuously, but enable heavy countermeasures only past a defined threshold (money or data at stake). *Why:* over-engineering selects for smarter attackers and complicates legal proof. *Check:* Is there a written escalation threshold and an abuser registry?
- Q57-7: Respond to script upgrades with the minimal change that breaks them, keeping detection signals hidden. *Why:* exhausts amateur attackers cheaply. *Check:* Are detection features undisclosed and rotated?
- Q57-8: Let partners scope keys (IP ranges, Referers, app IDs, function whitelist, geography). *Why:* limits damage from stolen keys. *Check:* Does the key management UI support these restrictions?
- Q57-9: Offer request signing (HMAC over parameters) or TOTP tokens in place of static keys for client-side use. *Why:* stolen signatures are useless beyond the signed request. *Check:* Is a signed/short-lived credential option available?
- Q57-10: Have a procedure to ban compromised keys quickly and notify the partner. *Why:* brief downtime beats a huge bill. *Check:* Is there a runbook for compromised-key revocation with partner notification?

**Checklist — anti-fraud and quota/rate-limit design:**
- [ ] Static + behavioural detectors, dual-identity (token and IP).
- [ ] Second-factor flow stipulated in the API contract.
- [ ] Honeypots / environment integrity checks where appropriate.
- [ ] Sanction ladder: monitor -> throttle -> identity tier -> IP/AS ban -> abuse report/legal.
- [ ] Escalation threshold documented.
- [ ] Per-key restrictions (IP, Referer, app ID, function, geo).
- [ ] Signed requests / TOTP option.
- [ ] Compromised-key revocation runbook and abuse-filing templates for hosts/stores.

**Anti-patterns / smells:**
- Captcha bolted on after launch, breaking existing clients.
- Subnet bans with large collateral damage and no review.
- Fully disclosed ban rules in error messages.
- Keys cannot be scoped; one leak exposes all functionality.

---

### Chapter 58. Supporting Customers
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-customer-support

**Core idea:** API support is mostly developer support, and most tickets come from inexperienced developers asking about things unrelated to the API. Set up a first line (technically literate staff, paid support, or community) that filters and redirects, but API developers must own second-line support, which means planning their time, distributing the load fairly and rewarding those who like it. End users should almost never need to contact you directly.

**Rules:**
- Q58-1: Design the product so end users never see vendor errors or need vendor contact (identify partners early, avoid unreachable-partner deprecations). *Why:* end-user-facing failures signal product flaws. *Check:* Are all breaking changes deliverable to a reachable partner contact?
- Q58-2: Staff a first line that can distinguish API questions from platform/language questions and redirect appropriately with FAQs. *Why:* most tickets are not about the API. *Check:* Does first-line have triage scripts and redirect targets?
- Q58-3: Route second-line tickets to API developers and budget that time explicitly in sprint planning. *Why:* only they can read partner code and debug remotely. *Check:* Is support time an allocated line in team capacity?
- Q58-4: Rotate support duty fairly (duty calendar) and reward customer-minded individuals. *Why:* developers resent unmanaged ticket load. *Check:* Is there a published rota and incentive?
- Q58-5: Mine tickets to feed the FAQ, docs and triage scripts. *Why:* recurring questions indicate documentation gaps. *Check:* Is there a periodic ticket-to-docs review?
- Q58-6: Monitor external platforms that offer tag subscriptions (e.g., Stack Overflow) and answer there. *Why:* customers ask wherever they are. *Check:* Is an official tag followed and answered?

**Checklist — customer support setup:**
- [ ] Legal/SLA inquiry channel for business owners.
- [ ] First line: technically literate staff or paid tier or moderated community.
- [ ] Second line: API developers, with rota and capacity budget.
- [ ] FAQ/knowledge base fed from tickets.
- [ ] External platform monitoring (tag subscriptions).
- [ ] Public Q&A archived as knowledge base if support is public.

**Anti-patterns / smells:**
- Engineers surprised by support load; ticket backlog grows silently.
- The same beginner question answered manually dozens of times without a FAQ entry.
- End users emailing the API vendor about a partner app's broken feature.

---

### Chapter 59. Documentation
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-documentation

**Core idea:** Documentation is the product's face and entry point, yet developers use it in two modes: newcomers copy-paste samples to solve one problem and leave; experienced users seek deeper concepts. Provide a full stack (machine-readable reference with prose, real-world atomic samples, live sandboxes, book-like tutorials with a tiny quick start, real FAQs, offline snapshots), keep it simple but literate and searchable, manage version/platform duplication, and treat docs as a product with KPIs.

**Rules:**
- Q59-1: Publish a complete reference covering every method, parameter, type and allowed value, as a machine-readable spec (e.g., OpenAPI) with human descriptions on each field. *Why:* a bare schema only tests whether names are guessable. *Check:* Does every field and method in the spec have a prose description?
- Q59-2: Document implicit contracts (event ordering, side effects) in the reference. *Why:* developers consult it to resolve ambiguous situations. *Check:* Are side effects and ordering guarantees stated per method?
- Q59-3: Provide code samples that reflect real use cases, are atomic, and look like production code. *Why:* samples get copied verbatim into apps. *Check:* Would you be comfortable seeing each sample in a partner's production code?
- Q59-4: Link samples from the reference and vice versa. *Why:* users navigate between modes. *Check:* Does each reference entity link to a relevant sample?
- Q59-5: Make samples live and editable in a sandbox with real or test data, or an emulator for non-online environments. *Why:* runnable examples are far more useful. *Check:* Can a developer edit and run a sample without leaving the docs?
- Q59-6: Write tutorials as a coherent sequence covering domain basics, happy paths, error handling and advanced topics. *Why:* it bridges samples and reference. *Check:* Does the tutorial have sections for each of those four items per functional domain?
- Q59-7: Keep the Quick Start under ten lines of code. *Why:* a longer one means missing helper methods or a misidentified core use case. *Check:* Is the Hello-World sample ten lines or fewer?
- Q59-8: Build the FAQ from real questions with concise answers linking to deeper docs; never use it to repeat marketing. *Why:* fake FAQs annoy. *Check:* Is each FAQ entry traceable to support tickets or community questions?
- Q59-9: Publish an offline snapshot (generated file) of the spec per version/date. *Why:* partners need a fixed reference. *Check:* Is a downloadable dated spec available?
- Q59-10: Mark the API version on every page, link to the newest version of the same page, and de-index deprecated versions. *Why:* duplicate content wrecks search. *Check:* Does each page show its version and a link to the current one?
- Q59-11: For multi-platform docs, either merge platforms into one page with per-platform samples (identical content) or split into separate sites (divergent content). *Why:* neither can be pessimized against the other. *Check:* Is the multi-platform strategy chosen explicitly and applied consistently?
- Q59-12: Keep prose concise and plain with terms defined inline, while ensuring pages carry the keywords needed for search. *Why:* docs must be both readable and findable. *Check:* Can a newcomer read a page without a glossary, and does the page rank for its key terms?
- Q59-13: Manage docs as a product: analytics, feedback widgets, KPIs. *Why:* otherwise quality never improves. *Check:* Do docs pages collect helpfulness feedback and have owners tracking metrics?

**Checklist — documentation (every kind an API must have):**
- [ ] Reference/spec: machine-readable (OpenAPI), all entities described in prose, implicit contracts, Postman-style collections.
- [ ] Code samples: real use cases, atomic, production-like, cross-linked.
- [ ] Sandbox: live editable samples; test dataset or emulator.
- [ ] Tutorial: domain primer, happy paths, error handling, advanced sections per domain.
- [ ] Quick Start: <= 10 lines.
- [ ] FAQ and public knowledge base from real tickets.
- [ ] Changelog/versioned docs with version badges, links to current, de-indexed deprecated versions.
- [ ] Offline/downloadable snapshot per version.
- [ ] Platform strategy (merged vs split sites).
- [ ] Grammar/terminology review; search keywords present.
- [ ] Docs analytics, feedback capture, KPIs and owner.

**Anti-patterns / smells:**
- Schema published with empty descriptions.
- Kitchen-sink samples mixing several tricks; synthetic samples copied into real apps.
- Quick Start that requires dozens of lines of boilerplate.
- FAQ that only repeats terms-of-service reminders.
- Search returns five near-identical pages for different API versions with no version label.

---

### Chapter 60. Testing Environments
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-testing

**Core idea:** Any API with real-world or costly consequences must have a test environment where actions are suppressed or cheaply simulated. A plain test mode is often insufficient because partners need to drive workflows through their full lifecycle; solve this either with a testing meta-API (helper methods to advance state) or a scenario simulator that plays out the backend, including selectable failure scenarios. The end goal is letting partners automate QA, with fast-forward execution, while still supporting manual testing.

**Rules:**
- Q60-1: Provide a sandbox for any operation with end-user or financial consequences, where side effects are null or cheaply simulated. *Why:* partners cannot test against production costs. *Check:* Can every consequential endpoint be called in a no-cost test mode?
- Q60-2: Enable full lifecycle testing (e.g., order -> preparation -> delivery -> refund), not just creation. *Why:* partners must test every stage they handle. *Check:* Can a test entity be advanced through all its states?
- Q60-3: Do not require partners to operate your internal/back-office apps to advance test state; provide helper methods or a simulator instead. *Why:* learning unrelated tools and per-partner virtual sandboxes are prohibitively expensive. *Check:* Is state advancement possible without using operator-facing tools?
- Q60-4: If using a testing meta-API, cover every human-performed production action with a helper and ship scripts/collections for standard sequences. *Why:* partners need correct call orders. *Check:* Is there a helper per manual production step and a sample script per scenario?
- Q60-5: If using a scenario simulator, provide a selectable scenario per unhappy path (e.g., trigger via a pre-agreed marker in the request). *Why:* error handling must be testable. *Check:* Can each documented error be deliberately reproduced in the sandbox?
- Q60-6: Make external steps (3-D Secure, redirects) simulatable as success or failure, and support fast-forward execution. *Why:* automated QA needs determinism and speed. *Check:* Can a full happy path run programmatically in seconds?
- Q60-7: Always keep a manual testing path alongside the programmatic one. *Why:* not every partner has QA automation. *Check:* Can the sandbox be exercised via UI/manual requests without scripting?

**Checklist — testing environment:**
- [ ] Sandbox/test keys with unlimited quota (see Q56-4).
- [ ] Side effects nullified or cheaply simulated (email instead of SMS, etc.).
- [ ] Test accounts and mock/test datasets, or emulator for offline environments.
- [ ] Lifecycle control: meta-API helpers or scenario simulator.
- [ ] Failure scenarios selectable; external steps (payment auth) simulatable.
- [ ] Fast-forward mode; scripts/collections for standard flows.
- [ ] Manual path preserved.

**Anti-patterns / smells:**
- "Test mode" creates entities that can never progress or be refunded.
- Partners must log into a courier/operator dashboard to finish a test order.
- Only the happy path can be simulated; errors are untestable until production.

---

### Chapter 61. Managing Expectations
Link: https://twirl.github.io/The-API-Book/API.en.html#api-product-expectations

**Core idea:** Partners need to know what to expect: SLA, features, responsiveness, and above all how long their code will keep working. Issue major versions no more often than the natural application lifespan in your domain, keep old minor versions alive long enough for the slowest partner, publish explicit platform-support policies (dropping a platform is a breaking change), and publish roadmaps, especially deprecation plans, even if tentative.

**Rules:**
- Q61-1: Set the major-version cadence to match the typical lifespan of applications in your domain. *Why:* partners should rewrite only when they would anyway. *Check:* Is the stated major-version support window at least as long as a typical partner app's life?
- Q61-2: Keep outdated minor versions available until the slowest affected partner has migrated after a breaking fix. *Why:* even bug fixes can break integrations. *Check:* Is there a policy and mechanism to pin to a prior minor version?
- Q61-3: Publish a written platform-support policy with criteria (e.g., >N% share, last M versions, or contractual list) and treat dropping a platform as a breaking change. *Why:* large integrators have rigid platform policies. *Check:* Does the docs/contract state which platforms and protocol versions are supported and until when?
- Q61-4: Put support commitments (platforms, versions, durations) into commercial contracts. *Why:* expectations must be enforceable. *Check:* Do partner contracts enumerate supported platforms and periods?
- Q61-5: Publish a roadmap, at minimum for deprecations, even without exact dates, and honour it. *Why:* trust in the API's future is a competitive advantage. *Check:* Is there a public roadmap page with deprecation notices and lead times?
- Q61-6: Communicate SLA, feature availability and responsiveness expectations like any B2B product. *Why:* partners plan around them. *Check:* Are SLA terms published and measured?

**Checklist — managing partner expectations (SLA, deprecation):**
- [ ] Published SLA with measured availability.
- [ ] Versioning policy: major cadence, minor retention, pinning.
- [ ] Platform/protocol support policy with criteria and sunset schedule.
- [ ] Contracts specify supported platforms and durations.
- [ ] Public roadmap with deprecation timeline and advance notice.
- [ ] Reachable partner contacts for deprecation communication (see Q58-1).
- [ ] Track record of kept promises.

**Anti-patterns / smells:**
- Major versions released whenever internally convenient.
- TLS/platform support dropped without notice, breaking large integrators.
- No public roadmap; partners discover deprecations from error responses.
