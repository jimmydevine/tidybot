# 0005. Design rules for the LulzBot TAZ 6

**Status:** Accepted
**Date:** 2026-08-22

## Context

All structural parts are printed on a LulzBot TAZ 6. Its capabilities and limits are a
hard input to the mechanical design, not an afterthought — particularly the stock 0.5 mm
nozzle, which is coarser than most current hobby printers.

## Decision

Adopt these as binding design rules for every printed part in the project.

| Rule | Value | Reason |
|---|---|---|
| Max single part | 250 × 250 × 230 mm | 280 × 280 × 250 volume, with margin |
| Base outer diameter | ≤ 250 mm | Single-piece printable |
| Min wall | 1.5 mm (3 × 0.5 mm) | Nozzle width |
| Min feature | 2.0 mm | Below this the nozzle won't resolve it |
| Layer height | 0.25 mm typical | |
| Default material | PETG | |
| Fasteners | M3 heat-set inserts | Never self-tap into printed plastic on a load path |
| Precision surfaces | **Steel hardware only** | See below |

## The 0.5 mm nozzle rule

**No printed plastic surface is a precision surface.** Anything that needs to locate,
repeat, or wear must be steel:

- Kinematic coupling: Ø8 mm bearing balls into Ø3 mm dowel-pin vees. The plastic only
  holds the steel in roughly the right place.
- Latch detent: Ø6 mm bearing balls.
- Rotating joints: real bearings, not printed bores.
- Threads: heat-set inserts, not printed threads.

This is good practice on any printer. On a 0.5 mm nozzle it is mandatory — a printed vee
groove would have visible layer stepping across exactly the surface whose job is
sub-0.1 mm repeatability.

## Other consequences

- **Frame-and-panel construction, not monolithic shells.** A 250 mm limit plus a machine
  that is slow by 2026 standards means large one-piece bodies are both risky and a
  10+ hour commitment per iteration. A frame with bolt-on panels iterates one panel at a
  time.
- **Test coupons stay small.** Phase 1 port coupons are ~110 mm square, ~2–3 h each, so
  a design iteration is same-day rather than overnight.
- **PETG over PLA**, everywhere. PLA's glass transition is reachable by a vacuum motor's
  waste heat and by a sunlit window. ASA is better still but wants an enclosure the
  TAZ 6 doesn't have stock; revisit if the base is enclosed later.
- **Design for no supports.** Overhangs ≤ 45°; bridge rather than support; split parts at
  natural planes. Support removal on a 0.5 mm nozzle leaves scars on exactly the mating
  faces we care about.
- **Print orientation is a spec, not a slicer setting.** The latch collar and port flanges
  carry load in shear across layers. Orientation is recorded per part in its generator
  script and must not be changed casually.

## Alternatives considered

- **Fit a smaller nozzle (0.4 / 0.25 mm).** Not required — the steel-hardware rule removes
  the need for fine printed features entirely, and a 0.5 mm nozzle gives stronger, faster
  parts. Revisit only if a module needs genuinely fine detail.
- **Outsource precision parts to a print service or CNC.** Rejected for now: it breaks the
  same-day iteration loop that Phase 1 depends on. Reasonable later for a final chassis.
