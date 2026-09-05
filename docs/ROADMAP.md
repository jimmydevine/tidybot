# TidyBot Roadmap

Each phase has a single **exit criterion**. Do not start the next phase until it is met —
the phases are ordered by risk, not by how interesting they are.

| Phase | Deliverable | Exit criterion | Status |
|---|---|---|---|
| **0. Spec** | Interface spec, budgets, ADRs, parametric port library, generated coupons | Port geometry validates and coupons generate | **Done** |
| **1. The port** | Bench coupons, no robot | T1–T5 pass; `SPEC_VERSION` → 1.0.0 | Next |
| **2. Rolling base** | Chassis, drive, LiDAR, SLAM, CAN discovery, ballast module | Base navigates a room; detects attach/detach; adapts its mass model | |
| **3. Vacuum module** | First real module | Cleans a room end to end, module attached by hand | |
| **4. Dock: charging** | Charge-only dock | 50/50 autonomous docks; **repeatability distribution measured** | |
| **5. Dock: swapping** | Rack + actuator | 20 unattended swaps, zero drops | |
| **6. Fleet + stairs** | Mop, duster, cargo; stair research spike | — | |

## Why this order

**Phase 1 before everything.** The coupler is the single component every future module
depends on. A change to it after three modules exist means reprinting three modules.

**Phase 4 before Phase 5.** Docking repeatability is the *input* to the swap mechanism's
tolerance budget. Designing the swapper before measuring it is guessing.

**Phase 2 uses a ballast module** — a weighted block with an ID chip. It proves discovery,
descriptors and the mass-model update without waiting on a working vacuum.

## Phase 3 note — the runtime problem

REQUIREMENTS.md §4 already shows a conflict: a 6S 6 Ah pack gives roughly 43 minutes of
vacuuming against a 60-minute target. Resolve it in Phase 3 by growing the pack to ~9 Ah
or lowering the target. Don't discover it with the robot half-built.

## Phase 6 — stairs

Per [ADR 0001](decisions/0001-locomotion-in-base.md), the practical options are a
pass-through drive sled (tracked or tri-star) or a second base chassis variant.

The original quadcopter-carries-the-base concept stays a **documented research spike**,
not a dependency. The arithmetic is unfriendly: lifting a ~4 kg base plus module needs
roughly 2:1 thrust-to-weight including the drone's own mass, so ~14 kg of thrust, which
means 13–15" props on a 700–900 mm frame. A residential stairwell is 900–1100 mm wide.
That is a drone as wide as the stairwell, indoors, GPS-denied, in wall-vortex turbulence,
over a hard drop.

Split the requirement instead and both halves become tractable:

- **Stairs** → a locomotion module (tracks or tri-star), or one base per floor.
- **Flying** → a small drone carrying only itself and a duster (~500 g class) to high
  shelves and ceiling fans. Entirely reasonable, and a good Phase 6.
