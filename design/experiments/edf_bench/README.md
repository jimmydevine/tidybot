# EDF bench draft, retaining cradle and fit gauge

Status: **bench build and purchases deferred; fan remains mounted in v2 cradle**.
The owner rejected the fixture cost and then deferred all propulsion work until
the other modules' dimensions and masses are established. Current work is
[core and ground modules](../../../docs/GROUND_MODULE_DESIGN.md).
The build instructions and hardware below are retained records.
The owner reports a successful local housing-gauge fit, followed by interference
between v1 and the central raised ring. V2 now fits that ring and body on the
cable-free side; the cable-exit side interferes. No
physical thrust, electrical or structural measurements have been taken. This experiment
supports the [EDF test brief](../../../docs/EDF_BENCH_PLAN.md); it does not change
the robot's reference lift design.

The draft uses a horizontal fan and a rigid, pivoting lever to press on the
owner's existing AWS SC-2kg scale. A 2:1 force ratio extends its usable thrust
range while keeping the fan's intake and exhaust away from the scale platform.
The owner has installed the fan with M3 nuts and bolts and can cut wood. The
[complete hardware proposal](HARDWARE_LIST.md) records the deferred pivot, stand,
wiring and measurement package. The [mounting-board step](MOUNTING_BOARD.md)
is part of that assembly. The stand
uses one cradle below the fan with cables upward; see the
[orientation diagram](output/mounting_orientation.svg).
V1 artifacts are retained for comparison.

## Review and print files

| Artifact | Purpose |
|---|---|
| [Deferred hardware proposal](HARDWARE_LIST.md), [CSV](hardware.csv), [budget](purchase_totals.md) | Historical package and cost; not a current purchase instruction |
| [Mounting-board build step](MOUNTING_BOARD.md) | Next: 120 × 140 × 18 mm board, drill pattern and M4 fastening |
| [V2 print and assembly instructions](CRADLE_V2.md) | Current prototype: confirmed body/ring fit, cable-up orientation and M3 hardware |
| [Cable orientation](output/mounting_orientation.svg) | One cradle below the fan, three cables above it; schematic routing |
| [V1 record and assembly notes](CRADLE_V1.md) | Failed physical fit; retained as a record |
| [V2 cradle STL](output/retaining_cradle_v2.stl) | Existing successful body/ring print: one part, 48 x 112 x 52.5 mm, base flat |
| [Cradle preview](output/retaining_cradle_v2_preview.svg), [assembly preview](output/retaining_mount_assembly_v2_preview.svg) | Review part and nominal fan/hardware fit |
| [Dimensioned side view](output/layout.svg) | Force direction, lever arms and packaging allowances |
| [Bench FreeCAD](output/bench_layout.FCStd), [STEP](output/bench_layout.step) | Includes cradle and mounting board; lever joints, stops and shielding remain to design |
| [Fit-gauge STL](output/unpowered_fit_gauge.stl) | Two loose half-rings for an unpowered fit trial |
| [Gauge FreeCAD](output/unpowered_fit_gauge.FCStd), [STEP](output/unpowered_fit_gauge.step) | Editable/exportable gauge geometry |
| [Calculations](output/calculations.md) | Static range and thrust targets; example preload is not a measurement |
| [Inputs](config.json) | Owner dimensions, source labels and proposed geometry |

## Measurement basis

| Item | Basis |
|---|---|
| EDF | Owner reports 66 mm duct length excluding the motor, 74 mm minimum body diameter, 75.5 mm lip diameter and 91 mm span across ears. Ear-hole spacing is approximately 82.5 mm; further ear details are recorded below. |
| Scale | Owner identifies AWS SC-2kg and measures a 100 x 100 mm platform. AWS specifies 2,000 g capacity and 0.1 g readability; readability is not accuracy under motor vibration. |
| Meter | Owner's KREATORDIRECT listing says 50 A continuous and 0-60 V. Photo says 150 A, while listing range says 0-200 A. Those inconsistent range labels do not increase the adopted continuous limit. |
| Wiring | Meter photo shows bare/tinned SOURCE and LOAD leads; a visible wire is marked 12 AWG. Actual connector, joint and complete harness capability remain to verify. |

Scale references: [AWS product page](https://awscales.com/sc-2kg-precision-digital-pocket-scale-2kg-x-0-1g/)
and [SC-Series manual](https://awscales.com/content/scales/SC-Series/SC-Series_manual.pdf).
Use the owner's measured platform dimensions where catalog dimensions differ.
The meter rating comes from the listing text supplied by the owner, not a test
of this unit. Original photos remain outside this repository.

## Completed physical check: housing fit gauge

**Owner result:** "ring gauge fits around the housing without force." This is
recorded in `physical_checks.housing_fit_gauge` in [config.json](config.json).
It supports retaining the 74.4 mm bore for the plain body region. The full cradle
subsequently failed to clear the raised central ring. The gauge instructions below
are retained for reproduction; its success did not validate the longer saddle.

The STL contains two separate semicircular pieces with a **74.4 mm bore**, 4 mm
radial wall and 6 mm axial height. The extra 0.4 mm is a trial diametral clearance,
not a claim about printer accuracy or the eventual mount fit. Combined print
footprint is approximately 172.8 x 41.2 mm, within the TAZ 6 bed.

Print flat at 100% scale, in millimetres. PLA or PETG, 0.25 mm layers and 3-4
perimeters are reasonable starting choices for this unpowered gauge; no supports
are needed. With the battery disconnected, bring the two halves together around
the measured 74 mm section. They should meet at their flat ends without forcing
or squeezing the duct. Report whether they meet, leave a gap, or have noticeable
radial play, and whether a full 6 mm-wide band of housing is available there.

These pieces have no fasteners or positive axial retention. **Do not use them to
hold a running fan.** Do not remove the bellmouth or disturb the balanced rotor
for this check. Remove loose hair around the fan with power disconnected before
any subsequent powered work.

### Mount measurements

| Owner measurement | Value (mm) | Interpretation |
|---|---:|---|
| Duct length | 66 | Along airflow, excluding protruding motor |
| Minimum body outside diameter | 74 | Gauge bore remains 74.4 mm |
| Inlet-lip outside diameter | 75.5 | Not the rotor diameter |
| Outside span across mounting ears | 91 | Overall width, not a circular body diameter |
| Opposite ear-hole center spacing | Approximately 82.5 | Owner's best estimate; not an exact hole-pattern tolerance |
| Hole diameter | 4 | Owner confirmed the opening diameter |
| Ear thickness along mounting screw | 3 | Owner confirmed this is the material the screw passes through |
| Ear width | 8 | Hole reported centered, 4 mm from each width edge |
| Ear height along the duct | 20 | Hole centered height-wise |
| Intake-side end of ear, measured from motor-side duct end | 39 | Motor excluded from reference |
| Hole center from motor-side duct end | 29 | Derived: 39 - 20/2 |
| Hole center from intake face | 37 | Derived: 66 - 29 |
| Ear ends from intake face | 27 and 47 | Derived from the 20 mm ear height |
| Central ring OD and axial width | 75.5 and 1.5 | Owner measured |
| Central ring center from intake face | 37 | Owner confirms alignment with the ear-hole centers |
| Central ring edges from intake face | 36.25 and 37.75 | Derived from its center and width |

The CAD now includes nominal rectangular **20 x 8 x 3 mm ears with 4 mm holes**.
Hole centers lie 37 mm from the intake face and approximately 41.25 mm either
side of the fan axis. In the bench layout, the ears are oriented sideways and
their screw axes are vertical. Corner shapes and root fillets are not measured;
these ear solids represent the existing fan, not replacement parts to print.

The 8 mm nominal ear width and approximately 82.5 mm center spacing imply a
90.5 mm outside span, versus the owner's 91 mm overall measurement. Keep 91 mm
for clearance and treat the 0.5 mm difference as measurement uncertainty rather
than forcing all dimensions to be exact. The retaining mount should accommodate
the approximate spacing and be checked on the actual fan before powered use.

A separate 100 x 95 x 95 mm package allowance remains while motor protrusion is
unmeasured; its inlet face aligns with the duct's inlet face. The 66 mm measurement
is the duct length, not the complete assembly length. The
[updated dimension sketch](output/mount_measurement.svg) shows the resolved
37 mm intake-side and 29 mm motor-side references. The earlier 3.25 mm offset
derived from radial lip overhang is not an axial mounting dimension.

The gauge fit is confirmed, but the v1 cradle trial failed at the central ring.
The [v2 groove](CRADLE_V2.md) is 76.1 mm diameter × 2.5 mm wide, centered at
37 mm from the intake. The fan model now includes the measured 75.5 × 1.5 mm
ring. The owner confirms v2 fits on the cable-free side, including the ring.
Use that side underneath with the three cables upward. The exit area is reported
as 6 × 11 mm, between the ears and on the motor side of the ring; exact dimension
axes/protrusion remain unconfirmed. V2 uses 6 mm OD M3 washers; hardware fit
has now been reported with M3 nuts and bolts. Final cable routing and retention
under load remain to check.

## Force measurement geometry

All dimensions below are proposed, not owner measurements. Bench coordinates are
x toward the exhaust, y across the bench, z up. Heights use the base's top face.

| Feature | Proposed geometry |
|---|---:|
| Fixed base allowance | 600 x 320 x 18 mm |
| Horizontal pivot axis | x = 330 mm, z = 180 mm |
| Fan thrust line | 120 mm above pivot; exhaust to the right |
| Scale contact | 240 mm left of pivot, centered on its platform |
| Selected pivot shaft | 8 mm round diameter, 200 mm stock length; bearings initially at y = +/-65 mm |
| Measured fan duct envelope | 66 mm long, 75.5 mm lip diameter, 91 mm span across ears; motor excluded |
| Full fan package allowance | 100 x 95 x 95 mm; motor protrusion remains unmeasured, ear corners/root fillets simplified |
| Cradle and board | 48 x 112 x 52.5 mm cradle on a 120 x 140 x 18 mm board; fan axis 54 mm above board top |
| Scale case allowance | 132 x 110 x 21 mm; check display and cover clearance |

Thrust acts left above the pivot. The left lever arm therefore presses down on the
scale. The pivot carries the remaining static load and the horizontal reaction.
With the lever level and its actual distances measured:

```text
thrust_gf = (gross_scale_g - baseline_scale_g) * L / h
L = 240 mm, h = 120 mm -> thrust_gf = 2 * change_in_scale_g
```

| Reference thrust | Increment on scale |
|---|---:|
| 1,000 gf | 500 g |
| 1,055.6 gf, hover per fan at the current four-fan robot mass | 527.8 g |
| 1,810 gf, DD seller's unverified maximum claim | 905 g |
| 2,111.2 gf, current per-fan available-thrust target | 1,055.6 g |

Record the actual gross baseline before taring; taring does not restore load
capacity. The proposed working stop is **1,800 g gross**, allowing 200 g below the
scale's rated capacity. With an *example* 200 g baseline, that corresponds to
3,200 gf thrust. Actual usable range depends on the measured baseline and dynamic
loads. The 2,111.2 gf target fits below that working stop only if the baseline is
below 744.4 g, with further margin needed for fluctuations. Printed display steps
of 0.1 g become 0.2 gf at this ratio; this is not an accuracy specification.

Use a rounded, adjustable contact at the center of the platform. Avoid side load
or contact with the fixed scale case. Arrange flexible motor cables so they do
not restrain lever motion; the ESC and battery remain on the fixed side. Moving
parts must clear the fixed structure except at the pivot and scale contact.

Before power, apply known masses at the marked calibration point 120 mm left of
the pivot: 1,000 g there should add 500 g to the scale. Check several loads while
increasing and decreasing, dwell at each, then remove them and check baseline
return. Repeat with the final cables installed. This checks the moment ratio,
friction and scale behavior; it does not fully validate horizontal-force coupling
or readings during fan vibration. A later known horizontal load along the fan
axis should also verify the assembled thrust load path.

Reject readings if auto-zero, hold/filtering, power-off, bearing friction, drift
or cable forces prevent repeatable load changes. If those cannot be controlled,
use a suitable load cell/thrust instrument. The lever avoids an immediate scale
replacement; it does not guarantee this pocket scale will perform adequately.

## Construction and electrical work remaining

The stand CAD combines a packaging study with a printable cradle prototype;
it is not a proof of strength or a complete fixture cut list. The intended
fabrication approach uses drilled timber/metal sections, bolts and purchased
bearings/shaft; printed adapters locate the housing after a fit check. No lathe
or mill is assumed. Purchased parts are selected in the
[complete hardware list](HARDWARE_LIST.md); installation checks remain:

| Item | Installation / verification still needed |
|---|---|
| Selected goBILDA 8 mm pillow blocks, 200 mm shaft and round clamping hubs | Detail lever joints and confirm delivered dimensions, friction and retention; 24 mm bearing axis height |
| Fixed supports, braced moving lever, base clamps and bolts | Stiffness, load capacity, clearance and fastening details |
| Fan mount | Fan installed in v2 with M3 nuts and bolts. Next attach the cradle to the moving board; load validation remains |
| Adjustable contact and mechanical stops | Central contact, travel limit and overload protection without shunting normal measured force |
| Access barrier and shielding | Independent support outside the flow path; duct and printed gauge are not containment |
| Manual servo tester | Recommended TST-20 and ESC BEC wiring are in the test brief |
| Selected harness, MIDI fuse and Albright ED125-1 | Complete circuit assembly, accessible shutdown and insulated connections; see purchasing list |

Connect the main power path as battery -> suitable protection/interrupter -> meter
**SOURCE** -> meter **LOAD** -> ESC. The photo's exposed wire ends need properly
soldered, insulated mating connections. Match the battery's XT60 contact type at
SOURCE and the actual ESC input at LOAD (product page lists XT90); check polarity
with the multimeter before connecting the battery. Connector names alone do not
specify mating orientation. Confirm the EDF's phase bullets against the ESC's
listed 4 mm bullets. Do not use an ordinary multimeter's current input for EDF
current.

Leave the meter's thin auxiliary lead unused and insulated for the 3S experiment;
its pinout is unverified and auxiliary power is unnecessary at this pack voltage.
Despite the listing's wording about preventing current damage, treat this device
as a meter: **it does not establish current limiting or automatic shutdown**.

Proposed limits for the existing meter are a **20 A initial ceiling**, with a
later **40 A operator stop** if the first checks support it, below the supplied
50 A continuous rating. These are experiment choices, not hardware validation or
automatic protection. Component temperatures, individual-cell voltage limits, run
duration, circuit protection and interruption capability still need to be fixed
before the powered protocol is released. No full-throttle or 4S run is specified
by this layout. A future higher-current run needs a separately rated power path.

## Regeneration and verification

From the repository root:

```sh
python3 design/experiments/edf_bench/generate.py
freecadcmd design/experiments/edf_bench/export_freecad.py
freecadcmd design/experiments/edf_bench/verify_mount.py
```

Set `TIDYBOT_PROJECT_ROOT` if invoking FreeCAD from another directory. Inputs and
scripts govern the retained outputs; do not hand-edit generated files. The
exporter checks nonempty valid CAD shapes and a closed STL mesh. These software
checks establish file integrity, not physical strength, fit or measurement quality.

The [current verification report](output/mount_verification.json) records v2
geometry checks, the reported cable-free-side body/ring fit and subsequent M3
installation. The moving board and complete fixture remain to assemble. The v1 failure remains
in config and its historical print record. The [v2 instructions](CRADLE_V2.md)
describe the measured-ring checks and separate synthetic regression.
No thrust readings have been entered in the recording sheet.
