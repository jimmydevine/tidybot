# Design files

The active design is now the [whole-system study](system/README.md), covering all
bottoms, the electronics core, lift and automatic stations. Open the
[interactive review](system/output/system_design.html) or
[design decisions](../docs/SYSTEM_DESIGN.md). It supersedes the earlier lift
deferral and battery-first recommendation. The layouts below remain earlier
studies; their dimensions and mass assumptions do not override the system model.


**Earlier phase: [core and ground modules](../docs/GROUND_MODULE_DESIGN.md).**
Use the [recorded vacuum component selection](../config/vacuum_selection.json) for the
everyday vacuum and [owned_parts.json](../config/owned_parts.json) for inventory.
Track assembly requirements in [ground_components.csv](../config/ground_components.csv) and actual
module weighings in [ground_assemblies.csv](../config/ground_assemblies.csv).
The owner confirmed a low head for 50 mm sofa clearance, suggested a separate
module, and reported 36-inch depth with front-only access. The working design is
[a dedicated low-clearance bottom](../docs/LOW_CLEARANCE_HEAD.md). Its mechanism
is separate from the first core/cap/everyday-vacuum layout.

## Earlier selected-component integration

Open the [offline rotatable viewer](ground/output/vacuum_integration.html),
[FreeCAD model](ground/output/vacuum_integration.FCStd) or
[STEP model](ground/output/vacuum_integration.step). This pass uses the selected
Pololu drivetrain, TriCut reference, new filter allocation and BIQU blower.
It includes trailing wheel-pod motion reservations and conditional service paths.
The [design decisions](../docs/VACUUM_INTEGRATION.md),
[generated check report](ground/output/vacuum_integration_report.md) and
[power/hardware record](../docs/VACUUM_POWER_AND_HARDWARE.md) identify remaining work.
These are component references and wire reservations, not printable parts.

```sh
python3 design/ground/integrate_vacuum.py
python3 -m unittest discover -s design/ground -p 'test_*.py' -v
freecadcmd design/ground/export_integration.py
```

Inputs: [vacuum_integration.json](../config/vacuum_integration.json).
The generator uses standard Python; the CAD export requires FreeCAD.
The standalone viewer needs no web service or downloaded JavaScript library.
The [hardware worksheet](../config/vacuum_build_hardware.csv) is a procurement
breakdown, not an additional mass ledger or a complete approved purchase list.

## Earlier inventory-based ground placement

The owner has also requested a [rolling BDUAV drive rig](experiments/drive_rig/README.md).
Its [offline layout](experiments/drive_rig/output/drive_rig.html), printable fit parts,
complete hardware allowance and CSV measurement tools are separate from the full
robot placement. Motor firmware and physical qualification remain outstanding.
This ground test does not resume EDF or lift work.

Open the [offline assembly placement](ground/output/ground_layout.html) for the
core, vacuum bottom, cap and service paths. The body proposal is 275 × 275 mm,
178 mm high including the A1 reference, within the owner's 180 mm limit. Flexible
bristles may extend; main panels target whole 270 × 270 mm prints. Component sizes, sources and modeled
clearance checks are in the [coordinate report](ground/output/ground_report.md);
read the [placement decisions](../docs/GROUND_PLACEMENT.md) for assumptions.

```sh
python3 design/ground/generate.py
python3 design/ground/place_modules.py
python3 -m unittest discover -s design/ground -p 'test_*.py' -v
freecadcmd design/ground/export_placement.py
```

The placement command uses [ground_layout.json](../config/ground_layout.json), the
inventory and existing head study. It generates HTML, five SVG drawings, a JSON
snapshot and a report. FreeCAD separately exports the
[STEP](ground/output/ground_placement.step) and
[FreeCAD](ground/output/ground_placement.FCStd) inspection models. Wire outlines
reserve space; reference solids show component envelopes. No fabrication STL or
flight capability is supplied. Re-export CAD after changing placement inputs.

## Earlier inventory roller clearance study

Open the [offline ground-head comparison](ground/output/vacuum_head_layout.html)
for dimensioned top and side views of both owned roller lengths. It uses the
reported 28 mm roller diameters and shows the filter separately. Grey housing
and amber drive spaces are proposed allowances, with no motor, transmission or
end-fitting geometry released. See the [calculation report](ground/output/report.md)
and [vacuum-head notes](../docs/VACUUM_HEAD.md).

Regenerate from inventory and [allowance inputs](../config/vacuum_head_layout.json):

```sh
python3 design/ground/generate.py
```

This produces HTML, two standalone SVG drawings, a JSON snapshot and the report.
It imports no archived CAD or flight model. No STL is issued from a clearance study.

**The model and commands below reproduce the earlier, deferred concept.** Its
200 × 280 × 190 mm floor robot, 6S battery and estimated flight mass are not the
current ground-build specification. All propulsion selection and testing are on
hold until the other modules' dimensions and carried masses are established.

## Earlier concept model and feasibility screens

Open [the offline viewer](output/concept.html) in a browser. It compares four
configurations, shows the component layout and three station working states, and
lists the checks and purchase allowances. It makes no network requests; source
links open manufacturer pages only when selected.

Read the [generated numerical report](output/report.md) and the
[engineering findings](../docs/CONCEPT_FINDINGS.md) alongside the pictures. These are
bounding models, not printable parts or a validated flight design.

The separate [EDF bench draft](experiments/edf_bench/README.md) provides a force
lever layout and a **retaining-cradle correction**. The local housing gauge fit,
but the full v1 cradle interfered with a raised ring. V2 includes the measured ring
and a clearance groove; the owner confirms body/ring fit opposite the cables.
The bench uses that side underneath with cables upward. The owner has installed
the fan with M3 nuts and bolts. Further stand work and the
[purchasing proposal](experiments/edf_bench/HARDWARE_LIST.md) are deferred because
of cost. The [published-data propulsion comparison](../docs/PROPULSION_COMPARISON.md)
is also deferred under the owner's ground-first work order. The bench's
inputs and exports are independent of the robot envelope model below.

## Inputs and generation

| File | Role |
|---|---|
| [concept.json](../config/concept.json) | Body/rotor/station dimensions, candidate propulsion curves and explicit screening assumptions |
| [components.csv](../config/components.csv) | Per-section component mass, power, cost basis and inventory substitution notes |
| [Example home](../config/examples/straight_stair_home.json) | Approximate owner measurements in metres and unmeasured geometry left null |
| [study.py](study.py) | Component positions, geometry checks, mass/energy calculation and report generation |
| [generate.py](generate.py) | Scene construction and offline viewer generation |
| [viewer.html](viewer.html) | Viewer template; open the generated version rather than this template |

From the repository root, using standard Python (no packages to install):

```sh
python3 design/generate.py
python3 -m unittest discover -s design/tests -v
```

The generated JSON, report and HTML are retained as reviewable outputs. Edit inputs
or source, then regenerate; do not hand-edit output files. Component placements in
`study.py` need checking again whenever their envelopes change.

## CAD exports

After generating the study, run the FreeCAD headless executable from the repository
root (set `TIDYBOT_PROJECT_ROOT` if running from elsewhere):

```sh
freecadcmd design/export_freecad.py
```

| Model | STEP | FreeCAD |
|---|---|---|
| Default robot and component envelopes | [STEP](output/robot_concept.step) | [FreeCAD](output/robot_concept.FCStd) |
| Robot on an interior stair tread | [STEP](output/stair_concept.step) | [FreeCAD](output/stair_concept.FCStd) |
| Station with supported core and bottom exchange volumes | [STEP](output/station_concept.step) | [FreeCAD](output/station_concept.FCStd) |

FreeCAD 1.1.3 was used for the first exports. Wire outlines represent overall module
and guard envelopes. Cylinders represent rotor swept space and motor allowances;
boxes represent purchased components with packaging allowances. None of these shapes
specifies a blade, protective cage, chassis wall, latch or machined bracket to make.
The retained `.FCStd` files contain named features for inspection; source dimensions
and generation scripts remain authoritative.

The STEP/FreeCAD files contain the default configuration only. Other variants are
available in the viewer; change `default_variant` and regenerate both outputs to
export another configuration. No archived CAD library is imported.

## Scope of the checks

- Coordinates are x forward/upstairs, y left and z up, in millimetres. The current
  tread is centered on x=0 with contact height z=0.
- The guard is a conservative occupied cylinder, not a designed access barrier.
  Arms and motor envelopes are included in the sampled stair test. The simple
  in-body vertical supports are drawn but are not separately collision-tested.
- Contact checks use level wheels with yaw/position error. Lift assembly checks
  sample yaw, pitch and roll at their assumed negative, zero and positive bounds.
  Intermediate angles and a complete timed trajectory are not proven clear.
- The combined rail projection is a conservative width gate. The rails' thicknesses,
  exact cross-sections and terminal geometry remain unknown. There is no fabricated
  headroom, landing, doorway, bookcase pose or pet-free route.
- The visual station states establish working-volume locations. Interlocks,
  mechanisms, cable/hose routing, approach trajectories and recovery are not yet
  designed or tested.
- Component-box intersection checks do not establish mounting, cooling, usable bin
  volume, air sealing, structural strength or sensor visibility.
- Larger variants substitute motor mass only. Their larger arms, guards and
  propellers need their own estimates before a final mass/cost comparison.
- Power interpolation stays within the published test points. Low-voltage thrust
  and guard-loss factors are sensitivity assumptions; continuous ratings and
  installed performance must come from the selected hardware and tests.

`PASS_MODEL` and `PASS_ASSUMPTION` are local results. Every configuration remains
`NOT_VALIDATED` overall while required geometry and physical checks are unresolved.

## Verification of this study

The initial generated study was checked with 16 passing Python unit tests covering
geometry, mass accounting, propulsion interpolation and unresolved validation gates.
A local Chromium smoke test exercised all 24 combinations of configuration, top mode
and station state; the generated JavaScript also passed a syntax check. All three
FreeCAD documents reopened successfully, and their STEP exports contained valid,
nonempty shapes. Markdown links and Git whitespace checks passed.

These checks verify the calculation and review artifacts within their stated scope.
No physical pickup, thrust, thermal, structural or autonomous-operation test has
been performed.

The current [converter/caster packaging update](../docs/VACUUM_POWER_PACKAGING.md)
adds a nominal Cincon cooling stack and full caster swivel reference to the
integration viewer and CAD. The updated station clearance includes the core bay
projecting below the mating plane. These remain design reservations.
