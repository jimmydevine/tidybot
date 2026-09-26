# Revision F verification record

2026-09-13. Candidate core/floor-power partition; no fabrication or physical
performance release. Inputs and their SHA-256 fingerprints are recorded in
[core_partition.json](core_partition.json).

- **52 Python model tests passed**, including 10 new partition tests and the
  existing 42 baseline/airborne tests. Checks cover complete mass accounting,
  converter ownership, unchanged cleaning/payload/energy assumptions, placement,
  and upward withdrawal of the core past the new bottom power hardware.
- Negative geometry tests detect both the old capacitor location and a filled-in
  shelf notch obstructing the core camera during withdrawal.
- Static allocation checks pass for vacuum, mop and sofa transit configurations.
  Duster core/tool/lift allocation checks pass for the three existing propeller
  layouts. These use functional boxes and conservative tube segments, not exact
  moving equipment, wiring or production tolerances.
- **290 valid FreeCAD reference shapes** exported across four F documents:
  vacuum 80, mop 69, sofa 80, airborne duster 61. Same-named STEP files exported.
  Shape validity does not certify strength, joints, interference of unfinished
  shells, station motion or feasibility of flight.
- Generated viewer JavaScript passed Node syntax checking and a mock-DOM check
  of initialization and both top/side controls. Top and side SVGs rendered with
  QtSvg and were visually inspected. No full browser-layout test was performed.

Reproduction commands are in [the design note](../../../docs/CORE_POWER_PARTITION.md).
The CAD counts are machine-readable in
[core_partition_cad_checks.json](core_partition_cad_checks.json).

No motor, airflow, pickup, wet-floor traction, electrical, thermal or flight test
was run. The stock carrier lacks released joints/hole patterns and qualification
of its narrow post spacing. The proposed raw-pack contact interface is unselected.
The barely passing nominal 2:1 static duster screen lies within the model's
uncertainty. Full floor transfer masses, guards and continuous thrust qualification
remain part of the design problem.
