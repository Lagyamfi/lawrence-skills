# Backward compatibility

What counts as a breaking change, what does not, and the policy defaults recommended by the book. Detailed rules: `rules-03-backward-compatibility.md`.

## Breaking vs non-breaking
Book: https://twirl.github.io/The-API-Book/API.en.html#back-compat-statement and https://twirl.github.io/The-API-Book/API.en.html#back-compat-serenity-notepad

Breaking (requires a new major, documented rationale, and a deprecation window):

- Removing or renaming any documented entity, field, method, event, status value, or platform.
- Changing observable behaviour: consistency model, sync vs async, callback cadence, event order, allowed state transitions.
- Imposing new obligations on existing partners (new required inputs, "defaults" that were never agreed).
- Fixing a bug partners rely on without emulating the old behaviour.
- Product changes that skip documented flows or stop emitting expected events.
- Removing behaviour that was undocumented but shown in samples, talks or support answers.
- Spec changes that alter generated-client behaviour even with an unchanged wire protocol.

Not breaking:

- Cosmetic changes with no functional effect.
- Additive optional parameters whose omission reproduces prior behaviour exactly.
- New endpoints, fields, events or enum values, provided clients were told to tolerate unknown values.

Policy defaults recommended by the book:

| Item | Default |
|---|---|
| Major version cadence | only for a critical mass of otherwise-impossible changes; never before the previous major has stabilised (months to a year) |
| Major support horizon | as long as apps live in your domain; use platform LTS windows as a yardstick; retire by measured audience share with a published schedule |
| Minors kept | at least the two latest once mature; allow pinning to exact `major.minor.patch` |
| Pre-release | alpha/beta channels so partners can test migrations |
| Version in URL | `/v1/...`; `v1` means the newest `1.x` |
| Undocumented behaviour | written policy up front; treat anything observable as promised |
| Design debt | log in a serenity notepad; fix in the next major, never in a minor |

---

