# Whole-system engineering model

The [T bottom-chassis comparison](../../docs/BOTTOM_CHASSIS.md) is explicitly
rejected: the integrated surrounding frame is heavier and obstructs head
movement/withdrawal. Run `export_bottom_chassis_freecad.py` under FreeCAD, then
`bottom_chassis.py` and `bottom_chassis_viewer.py`. The [review](output/bottom_chassis.html)
and [ledger](output/bottom_chassis.md) preserve failed geometry and complete mass
ownership. Tests passing means the comparison is reproducible, not that the
frame passes its design requirements. Refresh P/Q/R/S/T exports after source changes.

The [S core-support study](../../docs/CORE_SUPPORT.md) audits the common core and
replaces only `core_prints` + `battery_receiver` with a material-based candidate.
Run `core_support.py`, `export_core_support_freecad.py` under FreeCAD, then
`core_support_viewer.py`. Review [the report](output/core_support.md),
[interactive exchange view](output/core_support.html), and installed/withdrawn
`core_support_*.FCStd` / `.step` models. CAD checks include protected cartridge
reservations and new-part removal paths on vacuum/mop. The duster comparison is
mass only. Refresh P/Q/R/S CAD fingerprints after model-source changes before
running the full tests.

The [R integrated head frame](../../docs/INTEGRATED_HEAD.md) replaces the gross
head box with end walls, bearing seats, skid ramps, pitch-stop slots and a hood.
Its [report](output/integrated_head.md) reconciles the complete 170 g local scope
and calculates air-connector motion. Review the [drawing](output/integrated_head.svg)
and `integrated_head_*.FCStd` / `.step` assemblies. Run
`freecadcmd design/system/export_integrated_head_freecad.py`, then
`python3 design/system/integrated_head.py` from the repository root. After source
changes refresh P and Q CAD as well before the full test suite. R corrects the P
carrier riser/shoe placement and includes the N wheel envelopes in withdrawal
checks. No new weight saving or fabrication release is booked.

The [Q passive-head comparison](../../docs/PASSIVE_HEAD.md) evaluates twin-slide
kinematics, low pivots, force sensitivity and complete local mass scope. Run
`passive_head.py`, `passive_head_viewer.py` and `export_passive_head_freecad.py`
(under FreeCAD). Its [viewer](output/passive_head.html) and
[report](output/passive_head.md) retain the failed friction cases and necessary
head-frame rework. The powered-lift allowance remains until its functions are
covered; no weight reduction is booked. Refresh P's CAD fingerprint too after
model source changes before running the full tests.

Owner requirements are in `config/mass_budgets.json`: 4.5 kg transfer maximum
and 3.5 kg hover target for complete loaded non-lift assemblies. Run
`python3 design/system/mass_budgets.py` for the
[comparison](output/mass_budgets.md) and CSV/JSON outputs. Cap removal, maximum
contents, hardware uncertainty and unfinished candidate status are explicit.
See [budget definitions](../../docs/MASS_BUDGETS.md); these limits do not change
historical component masses or establish sufficient propulsion.

The [P removable head coupling](../../docs/HEAD_COUPLING.md) details a fixed
carrier, captured guides, spring-engaged keys, air face and protected electrical
interface. Run `head_coupling.py`, `head_coupling_viewer.py`, then
`export_head_coupling_freecad.py` under FreeCAD. Review the
[withdrawal illustration](output/head_coupling.html), [report](output/head_coupling.md)
and [CAD check scope](output/head_coupling_cad_checks.json). The latter includes
a model-source fingerprint; regenerate after source changes. P's 120 mm stroke
supersedes O's provisional 100 mm for this interface; whole assembly mass is
unchanged. Compliance, latch housings and service supports are not complete.

The [O sofa-attachment comparison](../../docs/SOFA_ATTACHMENT.md) leaves one
extension at each floor station and uses the normal vacuum for transfer flights.
Run `sofa_attachment.py` for the [interactive layout](output/sofa_attachment.html),
SVGs, mass CSV and [calculation report](output/sofa_attachment.md), then refresh
`mass_budgets.py`. The new head interface adds an explicit candidate allowance;
the existing manual cassette is not an automatic exchange mechanism. These are
space reservations, with room clearance, complete joints and cleaning/traction
unresolved; the previous dedicated sofa bottom remains a comparison.

The [weight correction](../../docs/MASS_OPTIMIZATION_REVIEW.md) is the current
priority. Run `mass_growth_audit.py` for the [G–M reconciliation](output/mass_growth_audit.md)
and complete row ledger. K/M remain comparison candidates while simpler chassis
and head support arrangements are evaluated; the audit changes no mass values.

The [N fixed-drive comparison](../../docs/FIXED_DRIVE_COMPARISON.md) provides
nominal CAD and an itemized replacement scope with a conditional 230 g saving.
Run `fixed_drive.py` for its [report](output/fixed_drive.md) and
[interactive view](output/fixed_drive.html), then
`export_fixed_drive_freecad.py` for CAD. Head motion, mop weight distribution
and complete joints remain gates before adoption; no STLs are released.

The [M floating-head integration](../../docs/FLOATING_HEAD_DESIGN.md) proposes
working/raised clearance and solves head force with wheel equilibrium. Use the
[viewer](output/floating_heads.html), [report](output/floating_heads.md), or
`floating_heads_{vacuum,mop}_{working,raised}.FCStd` / `.step` exports. Generate
with `floating_heads.py`, then `export_floating_heads_freecad.py` using FreeCAD.
These are motion allocations, not finished guides or printable mounts. Added
hardware allowances give 5.32 kg vacuum and 4.95 kg mop planning cases; shared
core changes still require integration with sofa/duster. L wheel-spring
tolerance failures remain open.

The [L spring/ride-height study](../../docs/SUSPENSION_SPRING_SELECTION.md) corrects
spring loading for moving wheel/pod mass, compares catalog springs and solves
empty/full contents and tool-contact cases. Run `suspension_springs.py` for the
[interactive results](output/suspension_springs.html) and
[report](output/suspension_springs.md), then `export_suspension_springs_freecad.py`
with FreeCAD for representative pod assemblies. K carried masses remain the
planning scenario. Spring tolerances, floating-head travel and dynamic threshold
crossing remain open; the catalog candidate is not a purchase release.

The [K connected pod/stop study](../../docs/POD_JOINTS_AND_STOPS.md) is the current
ground-drivetrain mass planning candidate. It replaces G's two pod allowances
with modeled metalwork, hardware and completion reserves, preserving other
frame/carrier allowances. Run `pod_joints.py`, `export_pod_joints_freecad.py` with
FreeCAD, then `pod_joints.py` again to import the CAD mass. Use the
[interactive stop view](output/pod_joints.html), [report](output/pod_joints.md) or
[FreeCAD](output/pod_joints.FCStd). Complete joint/fatigue qualification, spring
selection and fabrication release remain open. J exports are retained unchanged.

The [J wheel-pod mechanism](../../docs/WHEEL_POD_MECHANISM.md) adds a reconstructed
catalog motor bracket, relieved moving cradle, internal pivot-retainer stack and
rocking spring/guide geometry. `wheel_pod.py` generates the
[interactive mechanism](output/wheel_pod.html) and [report](output/wheel_pod.md)
from [J inputs](../../config/wheel_pod.json). Run
`freecadcmd design/system/export_wheel_pod_freecad.py` for nominal/bump/droop
candidate solids and a partial mass ledger. The design record explains the
optional supplier STEP inputs for exact wheel/hub mating checks. Complete
frame joints, stops, bearing fits and spring selection remain open; G mass is
unchanged. The nominal sofa preload slightly exceeds the adjustment range.

The [I height/mounting overlay](../../docs/HEIGHT_AND_CASTER_LAYOUT.md) proposes
a C1 lidar, rotates the lift-connector reservation and makes room for a documented
caster fitting. It passes the sampled 180 mm height screen including a 2 mm
reserve, with the same H wheel travel. `height_mounting.py` generates the
[comparison](output/height_mounting.html) and [report](output/height_mounting.md)
from [I inputs](../../config/height_mounting.json). Run
`freecadcmd design/system/export_height_mounting_freecad.py` for the three revised
ground layouts. Caster pull-out retention and detailed suspension joints remain
unqualified; complete G masses are retained separately from candidate deltas.

The [H suspension/support study](../../docs/FLOOR_SUPPORT_DESIGN.md) details pivot
and caster candidates without replacing G's complete mass ledger.
`floor_support.py` generates the [travel viewer](output/floor_support.html),
load calculations and stock ledger from [inputs](../../config/floor_support.json).
`export_floor_support_freecad.py` exports three bottom references and bump/droop
poses. Its height screen fails with the proposed droop, so the nominal G fit must
not be treated as a verified suspension envelope.

The [G frame/joint candidate](../../docs/FRAME_JOINT_DESIGN.md) uses dimensioned
stock-tube corners, edgewise rails, bearing pads and slider geometry. It adds
load/radius/capacity screens and clears a replacement floor-bridge route while
retaining the current carrier mass. `frame_joints.py` applies
[G inputs](../../config/frame_joints.json) to F; `export_frame_joints_freecad.py`
exports the full layouts and a core-only reference. The top seat changes to
124.1 mm. Start with [the generated report](output/frame_joints.md).

The [revision F power-partition candidate](../../docs/CORE_POWER_PARTITION.md)
adds a dimensioned bottom-owned power carrier, corrected upward removal path,
raw-pack interface contract and full configuration mass comparisons.
`core_partition.py` applies [F inputs](../../config/core_partition.json) to the
unchanged C/E sources. Its [viewer](output/core_partition.html),
[report](output/core_partition.md) and `core_partition*.FCStd`/`.step` exports
are the current partition proposal; the original outputs below remain baseline
comparisons. Run `python3 design/system/core_partition.py` and
`freecadcmd design/system/export_core_partition_freecad.py` to regenerate F.

This is the active cross-module design study. It supersedes the earlier work order
that deferred lift and the battery-first recommendation. Hardware need not arrive
to refine this model. It is a preliminary engineering design, not a fabrication
release or a demonstration of autonomous flight.

The current [airborne supplement](../../docs/AIRBORNE_DUSTING.md) replaces the
old wheeled elevated duster with a passive-foot tool bottom. Revision E moves the
boom rearward, refines camera mass placement and compares two documented EDF
assemblies with the complete carried vacuum, mop, sofa and duster loads. Use its
[interactive comparison](output/airborne_dusting.html),
[hardware and results](output/airborne_dusting.md), and
[FreeCAD](output/airborne_dusting.FCStd) / [STEP](output/airborne_dusting.step).
`airborne_study.py` imports the core/pack/lift baseline and applies
[airborne_dusting.json](../../config/airborne_dusting.json). Reproduce it with
`python3 design/system/airborne_study.py`, then
`freecadcmd design/system/export_airborne_freecad.py`.
The original wheeled duster exports below remain earlier comparison geometry.
The [airborne verification record](output/airborne_validation.md) separates the
new calculation/CAD checks from physical tests and the earlier baseline exports.

- [Editable inputs](../../config/system_design.json): geometry, hardware, mass intervals,
  loads, mechanisms, battery comparison inputs and propulsion reference curve.
- `build.py`: assembly accounting, geometry checks, CG/support, traction, airflow,
  flight and energy calculations; generates the review artifacts.
- `viewer.html`: self-contained interactive layout and budget viewer template.
- `export_freecad.py`: exports dimensioned component proxies and reserved spaces.
- `test_system.py`: independent calculation and assembly-accounting checks.
- [Interactive review](output/system_design.html): start here.
- [Lift footprint review](../../docs/LIFT_LAYOUT_REVIEW.md): current size drivers,
  compact-layout direction and the updated ceiling-fan dusting target.
- [Battery exchange](../../docs/BATTERY_EXCHANGE.md): automatic cartridges, station
  power handover, charged spares and charging-throughput assumptions.
- [Design document](../../docs/SYSTEM_DESIGN.md): decisions, hardware interfaces and remaining gaps.
- [Verification record](output/validation.md): model/browser/CAD checks and input fingerprints.

Ground CAD: [vacuum](output/vacuum.FCStd), [mop](output/mop.FCStd),
[sofa tool](output/low.FCStd), [duster](output/dust.FCStd).
Lift comparisons include the vacuum bottom: [quad](output/quad10.FCStd),
[hex](output/hex10.FCStd), [octo](output/octo10.FCStd).
Also available: [extended sofa tool](output/low_extended.FCStd),
[extended duster](output/dust_extended.FCStd), [station](output/station.FCStd).
Each has a same-named `.step` export. The viewer composes all bottom/top choices;
the three lift CAD files use the vacuum as their common comparison payload.

Reproduce with `python design/system/build.py`, then
`python -m unittest discover -s design/system -p 'test_*.py'`.
Run `freecadcmd design/system/export_freecad.py` for FreeCAD/STEP exports.

Mass intervals are engineering allowances, not statistical confidence intervals.
Catalog figures are not owner measurements. Source URLs and the basis of each row
travel with the hardware worksheet. A single assembled robot contains one core,
one bottom, one top and one battery; station spares are counted separately.

Revision B adds one cartridge tare and fixed exchange hardware to each robot,
plus a four-bay battery rack per station. The core subtotal includes cartridge
hardware; the bare cell pack is separate. Stored spares never enter carried mass.

Revision C is a requirements/layout review. Existing rotor and horizontal duster
geometry remains comparison evidence; neither the large lift footprint nor fan
cleaning is approved by the numerical checks. Regenerate the explanatory drawing
with `python3 design/system/draw_lift_layout_review.py` after building the model.
