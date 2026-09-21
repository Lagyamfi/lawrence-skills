# API Review Scorecard: <API name>

Follows Procedure B in `../SKILL.md`. Score each item 0 (absent), 1 (partial), 2 (met). Items the scope gate rules out are `n/a` and reduce the section maximum; controls delegated to an invisible gateway are `unverifiable` and excluded. Record evidence (a URL, a response sample, a spec line), not opinions. Rule IDs refer to `../references/rules-*.md` and `../references/additions.md` (`X` prefix, house rules).

| Scope gate | Answer |
|---|---|
| Mutable, addressable entities? | yes / no |
| Events, growing lists, notifications? | yes / no |
| SDK or UI components? | yes / no |
| Auth, quotas, rate limits delegated to a gateway not in scope? | yes / no |

| Field | Value |
|---|---|
| Reviewer | |
| Date | |
| Version reviewed | |
| Evidence gathered | spec / docs / client code / error samples / changelog / versioning policy |

## Fast triage

| # | Check | Rule | Score | Evidence |
|---|---|---|---|---|
| 1 | Spec exists, predates code, server conforms | I5 | | |
| 2 | Main scenario codeable from names alone | I3-3 | | |
| 3 | No mutating GET; every mutation idempotent | H35-6, D13-24 | | |
| 4 | Every list has a limit; no offsets over mutable data | P19-1/3 | | |
| 5 | Errors carry reason, field, constraint, user message, retry guidance | D13-18, H38 | | |
| 6 | Empty search is 200; invalid input rejected, never clamped | D13-15/16 | | |
| 7 | Dates, durations, money, units named with format | D13-4 | | |
| 8 | No undocumented fields or unwritten relied-upon behaviour | B26 | | |
| 9 | External ids non-sequential | D13-27 | | |
| 10 | Cache policy on every GET and 404 | H35-9, H39-12 | | |
| 11 | Client can recover after a mid-flow timeout without duplicates | P14-1 | | |
| 12 | Written versioning, support and deprecation policy | B25, Q61 | | |

## Section scores

Score each section by walking its items in `../references/checklist.md`. Max = 2 x applicable items (total items shown; put the applicable count in brackets when some are n/a).

| Section | Items (applicable) | Score | Max | Worst findings (rule IDs) |
|---|---|---|---|---|
| A. Contract, naming and data | 19 ( ) | | | |
| B. Validation and errors | 13 ( ) | | | |
| C. Idempotency, concurrency, async | 11 ( ) | | | |
| D. Lists, events, notifications | 11 ( ) | | | |
| E. HTTP specifics | 21 ( ) | | | |
| F. Security, identification, abuse | 10 ( ) | | | |
| G. Backward compatibility | 13 ( ) | | | |
| H. SDKs and UI libraries | 11 ( ) | | | |
| I. Product, docs, operations | 11 ( ) | | | |
| **Total** | 120 ( ) | | | |

Unverifiable items (delegated controls, not scored):

| Item | Rule | Where it would be verified |
|---|---|---|
| | | |

## Findings

Group by fix cost (D9-2). Design-level findings usually need a major version; additive ones fit a minor; docs-only need no release.

### Design-level (needs a major; log in the serenity notepad, B31-9)

| # | Finding | Rule | Evidence | Suggested fix |
|---|---|---|---|---|
| | | | | |

### Additive (fixable in a minor without breaking anyone, B27)

| # | Finding | Rule | Evidence | Suggested fix |
|---|---|---|---|---|
| | | | | |

### Documentation only

| # | Finding | Rule | Evidence | Suggested fix |
|---|---|---|---|---|
| | | | | |

### Outside the rulebook

Real findings that no book rule or house rule covers. Consider adding a house rule to `../references/additions.md`.

| # | Finding | Evidence | Suggested fix |
|---|---|---|---|
| | | | |

## Deliberate deviations accepted

Rules the owner chose not to follow, with the reason (D13-1). A deviation is acceptable if it is deliberate, documented and applied uniformly.

| Rule | Reason |
|---|---|
| | |

## Summary

Three sentences: overall state, the single most expensive problem, and the recommended next release (patch, minor, or major).
