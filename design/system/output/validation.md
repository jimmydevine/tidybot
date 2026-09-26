# Whole-system model verification

**Revision D follow-up:** [airborne verification](airborne_validation.md) records the new wheel-less duster, 38 model tests and its CAD/viewer checks. The revision C record and fingerprints below are historical; the baseline viewer/report now link to the airborne supplement.

2026-09-13, revision C review. Preliminary engineering model; no physical test results.

Revision C records the owner's lift-footprint concern and ceiling-fan target.
It does not replace the rotor geometry or implement fan access. Revision B
CAD geometry is unchanged and retained as comparison evidence.

- 28 Python unit tests passed. Added cases cover exactly one carried cartridge,
  exclusion of station spares from carried mass, receiving/recovery vacancies,
  blocked battery withdrawal, rack/tank interference, and insufficient charging
  throughput despite a large pack inventory.
- All four ground configurations pass allocation, nested containment and sibling-reference checks.
- All twelve stowed lift/bottom combinations and the extended airborne duster pass the implemented static allocation checks.
- Battery downward withdrawal clears the modeled fixed core; four rack shelves fit their enclosure and the rack clears modeled static station equipment.
- Ten regenerated FreeCAD/STEP layouts contain 747 valid reference/outline shapes.
- Generated revision C viewer JavaScript passes `node --check`; footprint status and updated dusting requirements are visible.
- The new two-layout explanatory SVG parses as XML; local links resolve. A raster/browser rendering inspection of that drawing was not performed.
- Local links in the root/system READMEs, system design, battery exchange design and generated report resolve.

The full browser exercise of sixteen bottom/top combinations, two extensions
and unsupported 8S flight suppression was performed on revision A. Revisions B/C
have JavaScript syntax checks; a fresh browser rendering check was not performed.

Not verified: physical masses, material strength, seals, tool performance,
complete moving gantry/gripper swept volumes, wet traction, installed battery
cartridge/connector fit, charge/cooling time, battery-current capability, flight,
complete wiring/PCB implementation, uninterrupted power handover or automatic docking.
The two-minute exchange time is a design target. The existing horizontal duster
does not yet implement the 7 ft ceiling-fan / 2 ft tool-reach requirement.

Reproduce model tests with `python3 -m unittest discover -s design/system -p "test_*.py" -v`.

## Input fingerprints

- `config/system_design.json`: `0fcabe616ea34c53c47c1d3dbd72489484af97ee88e86682df02577d6bf473a2`
- `design/system/build.py`: `cf1179e47ad635789eed82a9b1cf718ab136e5496ad7da5692702b6d69c746bf`
- `design/system/viewer.html`: `42681ef17b7c438648b845d12b829e94fbc4d243b5954e4556c4ce7fe3feb1ad`
- `design/system/export_freecad.py`: `a3f4da25c06732f37ebdabeef0e110380a5a2e8d161c2a9f926128382d06a585`
- `design/system/test_system.py`: `befe771b4df07a0f54cfe23d3f316ebb15eba35c715e063f962391d91be0d5eb`
- `design/system/draw_lift_layout_review.py`: `cddd72caae6c1381ee2b1073310abb4e26408fccae4105da3fb84f5cdeb2013b`
