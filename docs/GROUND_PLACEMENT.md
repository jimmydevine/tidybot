# Compact ground assembly placement

> **Scope update, 2026-09-13:** [Whole-system design](SYSTEM_DESIGN.md) now controls
> cross-module layout, carried mass, lift sizing and battery decisions. This
> earlier study remains supporting evidence; its lift deferral or battery-first
> recommendation, where present, is superseded.


**2026-09-12 status:** this is the earlier inventory-based placement. The
[new component recommendation](GROUND_COMPONENT_RECOMMENDATION.md) requires a
fresh placement pass; the linked models do not establish fit for the new wheels,
hub stack or suction components. The 275 × 275 × 180 mm limits still apply.

2026-09-06. **Placement proposal; not fabrication geometry.** The current
[offline viewer](../design/ground/output/ground_layout.html) shows the vacuum
bottom, electronics core, cap, complete stack and service paths. Its
[coordinate report](../design/ground/output/ground_report.md),
[FreeCAD model](../design/ground/output/ground_placement.FCStd) and
[STEP model](../design/ground/output/ground_placement.step) use the same inputs.
The previous 380 × 400 × 230 mm layout is preserved in
[the archive](../archive/ground-placement-380x400/README.md).

## Owner constraints and resulting size

Interpret the request for “width and height” of 275 mm followed by height of
180 mm as **275 mm width × 275 mm depth × 180 mm overall height**. The owner
explicitly confirmed that the footprint includes the rigid body and wheels;
flexible side-brush bristles may extend. Height includes the installed LiDAR.

| Item | Current proposal | Consequence |
|---|---:|---|
| Rigid body and wheels | 275 × 275 mm | Hard limit for this everyday ground layout |
| Height including A1 reference | 178 mm | 2 mm below the 180 mm limit; no uncounted mast or cover above it |
| Main printed panels | 270 × 270 mm | Whole-piece targets; separate bumper and pickup pieces reach the 275 mm body outline |
| Roller pair | 184.15 × 28 mm each | Short owned complementary pair; actual rubber working length remains unmeasured |
| Roller cassette footprint | 254.15 × 72 mm | Fits inside body; former 324 mm long-pair cassette does not |
| Drive wheels | 60 × 8 mm | Owner confirms 3 mm center hole and no hub protrusion; selected motor adapter still to fit |
| Debris cavity | 133 × 122 × 52 mm; 0.844 L gross | Target 0.5–0.6 L usable, not a demonstrated hair capacity |
| Brush travel outline | 305 × 275 mm | Based on an unmeasured 70 mm sweep extending 30 mm to the left; only bristles extend |

The TAZ 6 nominal build volume is 280 × 280 × 250 mm. A centered 270 mm panel
leaves nominally 5 mm per bed edge; a 275 mm part leaves 2.5 mm. Confirm the actual
printer profile, skirt/brim, bed keepouts, adhesion and flatness before a large
print. Whole-piece dimensions do not establish print success or strength.
[Manufacturer documentation](https://download.lulzbot.com/TAZ/6.0/documentation/manual/)

The main robot remains outside the 50 mm sofa gap. The separate
[reaching bottom](LOW_CLEARANCE_HEAD.md) still needs its own stowed/deployed
packaging for front-only access to approximately 36-inch-deep sofas. This layout
does not establish that its long extension will stow inside the same footprint.

## Three sections with overlapping height envelopes

The bottom mating plane is 68 mm above the floor. The core frame extends from
68 to 113 mm, and the cap from 113 to 123 mm. The core-mounted A1 reference starts
at 123 mm and is 55 mm tall: **68 + 45 + 10 + 55 = 178 mm**. Cap and frame values
are envelopes, not solid wall thicknesses.

To keep this stack short, the bottom-owned vertical filter, clean-air plenum,
blower and exhaust project into passive openings at the rear-right of the core.
The tallest bottom reservation reaches 105 mm, or 37 mm above its mating plane.
These heights overlap; do not add 105 mm to the 45 mm core height. The core has
no blower, filter, dirt or water circuit of its own. All vacuum hardware lowers
out with the complete bottom, without an air connection through the electrical mate.

This requires a frame with open equipment wells, rather than a full-width solid
core floor. Its load paths around those openings and replaceable joint carriers
remain to detail. The openings also constrain the occupied space of future
bottoms; matching the connector alone will not make a new module compatible.

The battery tray is 63 × 154 × 33 mm, the Pi tray 104 × 80 × 33 mm. The owned 3S
pack remains the power reference. The A1 stays on the core on a pedestal; a
107 × 81 mm cap opening passes over its full 96.8 × 70.3 mm reference footprint.
Actual scanner revision, fasteners and scan-plane offset remain to confirm.
[SLAMTEC dimensions](https://www.slamtec.com/cn/lidar/a1spec)

## Bottom placement and cleaning tradeoffs

The short cassette leads across the front, with the wheel axes 108 mm behind the
front edge. Its roof reference is 35 mm; a separate 40 mm-wide side-drive allowance
reaches 62 mm. The wheel H-bridge sits independently above the cassette roof.
Bottom MCU and tool power boards sit above the wheel motors. These compact bays
need actual board, header, terminal, cooling and cable-bend checks before selection.

Use the 25D HP 12 V **75:1 Pololu #4846** as the replacement motor reference for
60 mm wheels: 25 mm diameter, 69 mm body and 12.5 mm output-shaft extension. Its
published 130 RPM no-load speed corresponds to about 0.408 m/s at 60 mm wheel
diameter; loaded cleaning speed and torque still require evaluation. The two
owned 18 RPM motors remain a slow prototype alternative. Neither replacement
motors nor wheel hubs have been ordered. The wheel's 3 mm bore requires a
qualified bolt-on hub/adapter for this 4 mm output shaft. The BDUAV wheel-drive
alternative is assessed in the [motor comparison](DRIVE_MOTOR_OPTIONS.md); it
now has an owner-confirmed direct M2 wheel attachment, but remains unqualified
for sustained traction because the purchase-page spec image conflicts with the
physical motor label. [Motor specifications](https://www.pololu.com/product/4846/specs)

The central dirty-air corridor is 50 × 34 mm outside, ending fully inside the
front dirt-bin face. Proposed 3 mm walls would leave 44 × 28 mm before adapters.
It leads to a low bin with an adjoining vertical filter holder. The filter's broad
face is normal to the robot's width axis. Its 19 mm depth envelope conservatively
reserves the roughly 5 mm tab across the full 14 mm-thick filter face; grip relief
is detailed after the bin/filter assembly is withdrawn.

The upright CBM blower takes filtered air from the left and exhausts tangentially
toward the rear. The 97 × 95 × 33 mm reference is rotated, not resized. Duct adapters,
seals and the rear grille remain unmodeled. Its published free-air flow and
zero-flow pressure are separate endpoints; they do not prove pickup in this air
path. [Blower drawing and specifications](https://www.sameskydevices.com/product/resource/cbm-97b.pdf)

There is insufficient front-corner space for the current side-brush allowance.
The proposal moves it behind the left wheel and gives it a **separate gated floor
inlet into the front dirt well**. Since the main rollers have already passed,
this brush cannot simply feed them during forward travel. The extra inlet needs
a gate to manage suction sharing, a small drive, jam handling and pickup testing.
Those parts are unselected; this is a material complication of the compact layout.

Automatic emptying uses a downward-facing door beneath the dirt well. A station
manifold under the tray evacuates directly, with an intentional make-up-air path
and the onboard blower isolated. Packed-hair bridging, filter loading, wrap
resistance, floor marking and achievable emptying intervals remain physical tests.
Frequent automatic emptying may be needed for three dogs.

Two drive wheels and one rear-left compliant caster define the proposed support
polygon; small compliant front skids control head contact. The newly photographed
owned ball casters are reserve candidates. Their reported 28 × 45 mm plate
exceeds the modeled 20 × 20 mm support, while their 13 mm overall height fits
its height allowance. Mount height is reported as 3 mm; mounting datum and floor
behavior remain unqualified. A revised mount/placement would be necessary. See the [support assessment and
replacement priorities](OWNED_PARTS_REUSE.md). Actual caster hardware,
floor sensors, suspension and loaded center of gravity are unresolved. Empty and
loaded module masses remain blank in the ledger.

## Joints, service and station exchange

Top retention has four corner zones. Bottom retention has three corner zones
plus a fourth zone on a proposed rear bridge above the dirt bin, moved inboard
to avoid the blower. That zone starts 3 mm above the bin roof. Its bridge must
transfer loads to the frame without a post through the drawer's removal path.
Joint zones combine provisional guides, seats and retention space; they are not
selected latch dimensions or released hole patterns. The bottom's slotted locator
moves with the rear bridge zone. Top and bottom use different keys.

| Operation | Proposed clearance or stroke | Conditions |
|---|---:|---|
| Battery maintenance | 100 mm left | Tray passes below pickup rail; only 1 mm nominal vertical clearance |
| Pi maintenance | 140 mm right | Same rail clearance; wiring disconnects and actual cooling still need fitting |
| Bin and filter maintenance | 160 mm rear | Clean seal retracts 3 mm right first; low bin and tall filter move as one assembly |
| Bottom exchange | 50 mm downward | Tray top lowers from 60 to 10 mm above floor with core captured |
| Separated bottom clearance | 13 mm | 50 mm drop minus 37 mm tool projection; minimum modeled allowance is 8 mm |
| Bottom storage transfer | 310 mm rear | Begins only after the complete bottom has cleared the core |
| Cap removal | 70 mm upward | Cap underside then clears scanner top by 5 mm |

The bin/filter drawer is an L-shaped assembly in front view: its low bin passes
beneath core equipment while its taller filter slides through the rear opening.
Service checks use each occupied region, not the empty space of a full bounding
cuboid. Bin maintenance and automatic whole-bottom exchange are separate states.

The station tray reservation is 320 × 290 mm to accommodate the brush sweep.
Allow 80 mm side access on each side of the robot; this gives 435 mm body-plus-side
access width before cabinet walls and mechanisms. It is not a completed station
footprint. The ramp to the raised tray, supports, interlocks, drives, manifold,
charging and storage cabinet remain to design. Maintenance of battery/Pi trays
occurs off station or with its support fingers withdrawn.

The owner permits replacement parts for improvements in size, mass or performance.
In particular, compare a compact vacuum blower/filter arrangement before freezing
the current core openings, and qualify a floor-friendly support caster before
releasing its mount. The present owned-part arrangement remains a packaging
reference that can change with that evidence.

## Evidence, reproduction and next work

[ground_layout.json](../config/ground_layout.json) is the placement input.
[owned_parts.json](../config/owned_parts.json) separates owner evidence from
allowances. [ground_components.csv](../config/ground_components.csv) contains the
complete assembly accounting categories and open component selections, not a
ready-to-order hardware kit. Actual masses stay unknown until weighed.

Regenerate head drawings, placement views and CAD after changing inputs:

```sh
python3 design/ground/generate.py
python3 design/ground/place_modules.py
python3 -m unittest discover -s design/ground -p 'test_*.py'
freecadcmd design/ground/export_placement.py
```

Checks cover the 275 × 275 × 180 mm rigid limits, reference containment, 3D
reservation interference, core clearance openings, tray removal sweeps, station
separation and panel spans. They do not validate unmodeled structure, tolerances,
fasteners, wiring, airflow, optics, traction, runtime or automation. Touching
routing faces and nested references are intentional. The very small rail/tray
margins particularly need a tolerance and deflection review.

The next design step is to fit actual wheel hubs, roller end supports and drive
hardware into these reservations and detail the core bridge/joint sample. Resolve
filter seals, board heights and cable exits in the same review, then publish one
consolidated compatible first-build parts list before proposing purchases. Print
small fit samples before committing to the whole panels. Lift work remains deferred
until the complete modules have measured operating masses.
