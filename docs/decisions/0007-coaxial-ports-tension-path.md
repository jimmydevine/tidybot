# 0007. Coaxial ports; the base is a structural member

**Status:** Accepted
**Date:** 2026-09-04

## Context

The robot flies as a **3-stack**: rotor module on top, base in the middle, tool module
below, all attached. That makes the flight load path

```
lift module → TOP PORT → base structure → BOTTOM PORT → tool module
```

The base was designed as a box that houses components. Under lift it becomes the
structural member carrying 192 N between two ports.

## Decision

**The two ports are coaxial, and the structure between them is an annular tension member
at the post radius.**

## Consequences

**The load path is an annulus at r = 50, not a central column.** This corrects an earlier
reading. Load enters through posts at r = 50 and leaves through posts at r = 50, so the
tension member is a tube on that circle. Two benefits fall out:

- A tube at r = 50 is far stiffer in bending than a small central column of the same
  mass, which matters because port stiffness is what keeps this a rigid-body control
  problem rather than a slung-load one.
- **The centre stays completely free** for the connector cone and the harness. The
  earlier concern that the tension column would collide with the Ø20 harness bore
  dissolves — they were never competing for the same space.

**Both port faces must be parallel and coaxial** to within the joint's own tolerance, or
the two sets of posts fight each other. This is now a chassis requirement, not a port
detail.

**Battery and compute move outboard or between the ports**, clear of the annular
structure and the central connector volume.

**Every port is flight-critical.** A release in flight drops the stack. Both ports need
fail-secure retention, and the base needs pin-position sensing so it knows all six pins
(three per port) are actually home before the rotors spin.

## Load cases

| Case | Top port | Bottom port |
|---|---|---|
| Parked | compression | 15 N tension (tool hangs) |
| Driving | compression + shock | 15 N + threshold shock |
| Flight, static | 48 N tension | 15 N tension |
| **Flight, design** | **192 N** | **59 N** |

Design load = static × 2 (thrust-to-weight for control authority) × 2 (landing and gust
shock). Both multipliers are estimates; the port rating is directly proportional to them.

## Open

- Lift module mass is unbudgeted. REQUIREMENTS.md has no line for it; 2 kg was assumed,
  giving 6.9 kg all-up and ~13.8 kg of thrust required at 2:1.
- The 2× shock factor is a placeholder.
