# Architecture Decision Records

One file per decision that would be expensive to reverse. The point is to preserve the
*reasoning*, so that in two years you can tell the difference between "we chose this
deliberately" and "it just ended up that way."

Format: `NNNN-short-title.md`, numbered in the order decided.

Status is one of: **Proposed** / **Accepted** / **Superseded by NNNN** / **Rejected**.

Never edit an Accepted ADR's decision. Write a new one that supersedes it.

## Template

```markdown
# NNNN. Title

**Status:** Proposed
**Date:** YYYY-MM-DD

## Context
What forces are at play? What makes this a real decision rather than an obvious one?

## Decision
What we are doing. Stated plainly, in the active voice.

## Consequences
What gets easier. What gets harder. What we are accepting as a cost.

## Alternatives considered
What else was on the table, and the specific reason it lost.
```

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-locomotion-in-base.md) | Locomotion lives in the base, not in floor modules | Accepted |
| [0002](0002-bus-voltage-24v.md) | 24 V nominal DC bus | Accepted |
| [0003](0003-can-bus.md) | CAN for the inter-module bus | Accepted |
| [0004](0004-two-ports-top-bottom.md) | Two ports (top and bottom); sensors use an accessory rail | Accepted |
| [0005](0005-print-constraints-taz6.md) | Design rules for the LulzBot TAZ 6 | Accepted |
| [0006](0006-tri-post-coupling.md) | Three tapered posts with cross pins | Accepted |
| [0007](0007-coaxial-ports-tension-path.md) | Coaxial ports; the base is a structural member | Accepted |
