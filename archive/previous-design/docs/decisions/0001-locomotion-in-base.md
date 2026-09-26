# 0001. Locomotion lives in the base, not in floor modules

**Status:** Accepted
**Date:** 2026-08-22

## Context

The 2022 design split the robot into a base electronics unit with **no drive**, and a
vacuum module below it that carried its own locomotion. The reasoning was sound: the
floor tool and the drivetrain interact closely, so co-designing them lets wheel
placement suit the brush roll and suction throat.

The question on resuming: keep that split, or move drive into the base?

## Decision

**The base carries compute, sensing, power and drive.** It is a complete, functional,
mobile robot on its own. The bottom port carries *tools*, not drivetrains.

## Consequences

Easier:

- **The base can always reach the dock.** With drive in the tool, a module-less base is
  furniture — and the swap sequence (arrive with vacuum → release → acquire mop)
  requires mobility *between* release and acquire. A stuck or stranded robot is also
  self-recoverable.
- **The docking station stays simple.** A rack plus one actuator, rather than a lift
  and carousel that has to hold the base while shuffling modules under it.
- **Modules get cheap.** No motors, encoders, drivers, wheels, suspension or caster per
  module. A vacuum module becomes a shell, impeller, brush and bin. This is what makes
  six modules plausible instead of two.
- **One kinematic model, forever.** Odometry, wheel geometry and the Nav2 tune are
  calibrated once. A module swap perturbs payload mass only — a small correction driven
  straight from the descriptor's `mass_g` / `com_xyz_mm`.
- **Cliff sensors sit with the wheels they protect**, in the base, covering a geometry
  the base actually knows.

Harder / accepted costs:

- Ground clearance: tools hang below the base. Mitigated by making the bottom port a
  recessed bay between the wheels, so the module intrudes *up* into the base envelope
  rather than purely hanging below it.
- One drive geometry must serve vacuum, mop and sweeper. Acceptable — these are all
  differential-drive floor tools with the working element ahead of the axle.
- Swapping wheels for tracks is no longer a 30-second operation. See below.

## Stairs

The strongest objection to drive-in-base is that a stair-climbing module can no longer
replace the wheels. Two answers, either acceptable:

1. **Pass-through drive sled** — base → sled → tool, where the sled has a male port up
   and a female port down. The sled is an open frame with wheels at its perimeter and a
   central aperture the tool's working element passes through, so stack height stays
   sled height rather than sled + tool. A tracked or tri-star sled swaps in at the same
   interface.
2. **Second base chassis variant** — print a tracked chassis reusing the identical
   electronics stack and both ports. Loses the quick swap; keeps every module compatible.

Deferred to Phase 6. Recorded here so the choice is made with eyes open rather than
discovered as a constraint.

## Alternatives considered

- **Drive in each floor module (the 2022 design).** Rejected primarily because an
  undocked base is immobile, which breaks the module-swap story that the whole project
  is built around, and secondarily because per-module drivetrains dominate module cost
  and force a per-module odometry calibration.
- **Drive in the base *and* optionally in modules.** Rejected: two drivetrains that must
  cooperate is a control problem far harder than anything else in the project, for no
  benefit at this scale.
