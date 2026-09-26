# Replaceable vacuum head and brush comparison plan

**Sofa interface update, 2026-09-14:** the [resident extension study](SOFA_ATTACHMENT.md)
adds a proposed automatic exchange of the **complete powered head** for a sofa
extension. This requires a new station-actuated receiver/air/electrical joint;
the manual captive-M3 arrangement below does not implement it. Roller changes
and consumable servicing remain manual maintenance operations. One extension
stays on each floor, and the normal head is restored before transfer flight.

2026-09-13. **Design for two levels of replacement: a removable roller within
one brush family, and a removable complete head cassette for different brush
mechanisms.** This extends the [hair-priority recommendation](VACUUM_RECOMMENDATION_REVIEW.md).
It is an interface proposal, not dimensioned fabrication CAD. Keep the complete
robot within 275 × 275 × 180 mm, including wheels and LiDAR.

**Order update, 2026-09-13:** the owner reports rollers, filters and blower kit
ordered, awaiting delivery. The samples below are the assumed references from
the preceding recommendation; exact purchased variants and quantities remain to
record on receipt. Follow the [current build plan](VACUUM_MODULE_NEXT_PASS.md)
for work that can proceed during delivery.

## First comparison

Start with one genuine Dreame TriCut and one genuine Dreame plain rubber brush,
using the **L40 Ultra / X40 Ultra compatibility family** as the reference.
Both manufacturer listings explicitly name those models. That supports trying
one common mount; exact purchased ends, restraints and guard clearance must still
be matched before printing. The same-family plain brush is a comparison control,
not a replacement for the preferred hair-management investigation.

| Sample | Listed reference | Role |
|---|---|---|
| [Dreame TriCut](https://www.dreametech.com/products/anti-tangle-roller-brush) | $49.99; 200.6 × 45.1 × 45.1 mm; 200 g | Cutting candidate A |
| [Dreame Rubber Brush](https://www.dreametech.com/products/l20-ultra-roller-brush) | $22.99; 200.1 × 42.2 × 42.2 mm; 62.8 g | Non-cutting comparison B |

Prices observed 2026-09-13; combined sample cost **$72.98 before tax/shipping**.
Dimensions and weights are listing references, not verified installed geometry
or bare-component masses. In particular, do not use the apparent diameter or
weight difference as a measured result. Obtain the exact revision supplied with
its end components; retain its identifying label and source for open-source
reproduction. These two samples are not a complete powered-head hardware order.

The plain Roborock brush and owned iRobot-style pair remain alternatives. A
HyperStream or DuoDivide comparison should follow a complete mechanism/fit
review; buying loose rollers alone may omit necessary drive and end supports.
Do not design one set of end caps intended to fit every manufacturer's brush.

## What changes during a swap

| Swap | Parts removed | Shared parts |
|---|---|---|
| TriCut versus matching Dreame plain roller | Underside guard, roller and any identified end/height insert required by that revision | Cassette frame, drive if compatible, inlet, chassis and suction system |
| A different brush architecture | Complete cassette: rollers, end supports, drive/transmission, guard, floor-contact geometry and intake transition | Chassis-side receiver, bin, filter, blower, battery and drivetrain |

Each cassette carries only the drive hardware it needs. Put its motor power
stage and mechanism-specific feedback wiring on the cassette where practical,
so later motors do not force changes to a shared shaft or phase-wire pinout.
Only the installed cassette contributes to carried mass. Spare cassettes and
comparison rollers remain off the robot.

## Proposed cassette interface

- **Mechanical:** a common chassis-side receiver and removable cassette-side
  adapter. Locate against defined seats with one round and one slotted locator;
  use four captive M3 screws for initial retention, with metal nuts/inserts.
  Position and screw length follow the fit study. Aim for a few-minute swap
  without removing the core, wheels or bin; that time has not been demonstrated.
- **Floor following:** place compliance between the receiver and the rigid
  bottom chassis. Each cassette establishes its own brush-to-floor relationship
  using replaceable inserts or documented shims. Record contact depth/preload;
  the same axis height does not guarantee equivalent contact for different
  rollers. Check the full movement through the 4–10 mm transition requirement.
- **Air:** one common, gasketed outlet at the rear of the cassette, with a
  smooth internal transition to the fixed dirt duct. The moving receiver needs
  a short compliant duct connection. Keep gasket edges and fastener ends out of
  the hair path. Set the outlet size from the head, bin and required airflow
  together; a small convenient hose must not determine the dirty-air passage.
- **Electrical:** target one keyed, latching service connector carrying the
  selected protected supply, return, commands, feedback and hardware enable.
  Connector, voltage/current ratings and pinout are not selected. Reserve
  cassette identification so the controller loads the appropriate limits.
  A single plug is a design target, not a claim that existing boards provide it.
- **Servicing:** de-energize the head before opening the guard or unplugging.
  Guard-open or absent/unidentified cassette means drive disabled. Keep the
  purchased cutter enclosed; verify allowable rotation and clearing behavior
  before implementing a reverse-to-clear command.

The cassette outlet is a dirty-air joint. The bin/filter seals and blower remain
downstream, so a leaky cassette joint changes pickup even when the blower setting
is identical. Check seating and seals after every installation.

Manual roller/cassette swaps are development and consumable-service operations.
The station still exchanges **complete wheeled bottoms** automatically. This
does not add a requirement for the station to dismantle a brush cassette.

## Work order and complete hardware scope

1. **Resolve the paired brush interfaces.** Start with the two identified
   samples or dimensioned supplier information: overall and working length,
   rotating clearance, drive socket, stationary restraint, guard, cutter
   actuation and removable end components. Confirm whether one drive accepts
   both brushes. Public compatibility does not specify RPM or torque; prefer a
   documented drive or matched mechanism, with bounded commissioning if those
   values cannot be established from a supplier.
2. **Lay out the complete head in the robot.** Include the receiver, drive,
   removable guard, air joint, compliance, side-brush sweep and service access.
   Resolve the bin/filter/blower/core above and behind it before freezing the
   receiver envelope or bolt pattern. No fit of later paired heads is promised.
3. **Prepare one consolidated build list.** Include the brush samples, motor
   and reduction, coupler/end supports, power stage and feedback, receiver and
   retention hardware, floor seals/gasket/compliant duct, guard switch, service
   connector and harness. Include shared bin/filter/blower, power conversion,
   protection and controls needed for a working vacuum, with owned parts marked.
   A brush purchase is not sufficient for a powered pickup test.
4. **Print small interface pieces first, then the first cassette.** Check brush
   restraint and clearances without power before committing to the full body.
   Build onto the intended wheeled vacuum bottom so the work contributes to the
   robot rather than a separate characterization stand.
5. **Run paired pickup and accumulation trials.** Use the procedure below,
   then decide whether TriCut merits retention or a different complete cassette
   should be developed. Final drive sizing, fit and pickup remain unverified.

## Comparison procedure

Use wood and tile lanes with documented distance, lane width, actual travel
speed and representative weighed dog-hair loads. Include loose undercoat and
longer strands/clumps. Use matched fresh loads; do not reuse chopped trial hair
as the next candidate's starting material. Keep the side brush disabled for the
initial central-head comparison, then include it for edge and full-system trials.

Keep the bin, filter condition, supply and blower setting consistent. Log actual
voltage, roller speed/contact setup and electrical draw. Weigh the complete
installed cassette and record the robot's empty mass and starting bin load;
do not substitute published roller weights for carried assembly measurements.
The same blower command
does not ensure the same airflow through two different heads; if airflow is not
measured, describe the outcome as performance of each head on the shared suction
system. Do not claim a difference came from cutting alone, because roller surface
geometry also changes. For different architectures, use documented operating
settings for each and compare the resulting complete head, rather than imposing
an arbitrary common RPM.

For pickup trials, clean/reset between candidates and alternate A/B order. Record
hair delivered to the bin, left on the floor, wrapped around the roller/ends and
trapped elsewhere separately, plus elapsed time, jams and manual interventions.
For accumulation trials, start each candidate clean and run the same repeated
load sequence without detangling between cycles; document any necessary stop.
Repeat with a defined partly loaded filter and verify station evacuation later.

Report the mass balance and measurement resolution. The owned 2 kg scale is not
known to resolve small retained-hair quantities: use suitable larger loads or
report below-resolution results honestly, never as proven zero wrap. Track
maintenance time and damage/scuffing as well as pickup. These trials establish
application performance, not a universal zero-tangle certification.
