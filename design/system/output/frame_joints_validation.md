# Revision G verification record

Checked 2026-09-13. This is a mechanical design candidate, not a fabrication or
flight release. The [generated report](frame_joints.md) explains the calculations;
[frame_joints.json](frame_joints.json) records the inputs and their SHA-256
fingerprints.

## Completed checks

- Generated the report, stock/hardware ledger, layout and section drawing with
  `python3 design/system/frame_joints.py`.
- Ran `python3 -m unittest discover -s design/system -p 'test_*.py' -q`:
  **64 tests passed**, including 12 revision G tests. These cover beam equation
  units, thin-wall rejection, unequal load sharing without applying the load
  factor twice, corner-radius clearance failures, mass accounting, unchanged
  revision F inputs, component placement, slider travel, battery extraction,
  capacity screens and the proposed floor-bridge route.
- Exported five FreeCAD/STEP assemblies with FreeCAD 1.1.3 using
  `design/system/export_frame_joints_freecad.py`. All **481 exported shapes**
  passed the script's shape-validity check, as recorded in
  [frame_joints_cad_checks.json](frame_joints_cad_checks.json): vacuum 117,
  mop 106, sofa 117, airborne duster 97 and core-only 44.
- Rendered the SVG with QtSvg, which reported a valid document, and visually
  inspected the rendered corner section for legible labels and dimensions.

The layout checks retain the nominal 275 mm width through the complete modeled
slider stroke and place the ground configuration's highest allocation at
179.1 mm. The existing floor carrier remains installed and fully counted; a clear
route for its proposed replacement is not a completed replacement structure.

## Scope and remaining work

Shape validity does not establish assembly fit or strength. The checks use
nominal dimensions and allocation envelopes, not a complete tolerance stack.
Tube corner radii are screened analytically; the CAD uses sharp reference
corners. Verify the purchased stock's actual radii and wall tolerances.

The calculations are preliminary beam and average-shear screens. They do not
qualify local hole bearing, stud-head pull-through, slider prying, fatigue,
fastener joints or the automatic latch. Guides, positive pawls, springs, sensing,
wear allowances, drilled-hole locations and tool access still need detail.
The new 124.1 mm upper seat requires corresponding mating-fixture changes.

The floor bridge still needs fixed suspension-pivot and caster connections before
the existing carrier can be removed or any mass saving credited. Bin/tank
capacities pass a declared wall-and-reserve volume screen; actual usable capacity,
ports, seals and evacuation performance remain unverified.

No physical fit test, load proof test, cleaning test, endurance test or flight
test was performed for revision G. The 6S comparison battery and airborne power
estimates remain design assumptions. No parts are released for purchase or print
by this verification record.
