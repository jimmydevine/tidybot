# Height and caster mounting — revision I candidate

The revised ground layout preserves the proposed **10 mm bump / 2.5 mm droop**
and reaches **177.35 mm** in the sampled support poses. Adding a 2 mm project
reserve gives **179.35 mm**, inside the 180 mm limit. That reserve still needs to
be replaced by a complete tolerance and deflection stack.

Use the [interactive comparison](../design/system/output/height_mounting.html)
or [calculation report](../design/system/output/height_mounting.md) to review it.
This pass proposes a **SLAMTEC C1 lidar**, rotates the existing lift-connector
reservation and adjusts the scanner mounting height. The connector retains its
allocated volume, while its top clears the full rotating optical enclosure.
The four structural module seats stay at 124.1 mm. The connector carrier and its
top-module mating route need to follow the revised layout.

The C1 has a smaller body and lower bare mass than the A1 reference, but different
scan characteristics. This is a packaging candidate; it does not establish
equivalent mapping or obstacle-detection performance. Nearby sensors, camera and
cliff detection remain. Manufacturer dimensions, optical-window geometry,
electrical requirements and source links are recorded in the calculation report.

The caster fitting assumption changes from 2.5 mm to a documented **6 mm added
height** for a TENTE S70-8x15 / 8 fitting. With the 3 mm plate and complete threaded
stem, overhead space must extend to at least 71.5 mm. Equipment starts at 74 mm,
leaving 2.5 mm clearance. The vacuum bin bridge floor, suction blower/plenum and
mop pump move upward to accommodate it. The volume screens still meet the
existing 0.50 L vacuum / 0.35 L water / 0.30 L sofa-bin targets.

**Caster retention remains unresolved:** the nut secures the fitting to our
plate, but the caster's retention on its plug end during lifting still needs
manufacturer confirmation or a mechanically captive alternative. Exact fitting
compatibility and supplied shoulder dimensions must also be confirmed. No
purchase or print is needed for this review.

The existing complete G mass estimates remain the baseline. The C1's 60 g bare
saving is mostly consumed by provisional mount and caster-retention reserves;
the illustrative combined change is only −12 g. No new flight endurance or
completed H frame weight is claimed.

Review files:

- [Inputs](../config/height_mounting.json),
  [generated data](../design/system/output/height_mounting.json) and
  [verification record](../design/system/output/height_mounting_validation.md).
- [Vacuum FreeCAD](../design/system/output/height_mounting.FCStd) /
  [STEP](../design/system/output/height_mounting.step).
- [Mop FreeCAD](../design/system/output/height_mounting_mop.FCStd) /
  [STEP](../design/system/output/height_mounting_mop.step).
- [Sofa FreeCAD](../design/system/output/height_mounting_low.FCStd) /
  [STEP](../design/system/output/height_mounting_low.step).

The CAD uses allocation outlines and stock references. It is not a printable
lidar carrier or completed suspension. Earlier G/H artifacts remain unchanged
for comparison.

Reproduce from the repository root:

```sh
python3 design/system/height_mounting.py
python3 -m unittest discover -s design/system -p 'test_*.py' -q
freecadcmd design/system/export_height_mounting_freecad.py
```

The [J mechanism follow-up](WHEEL_POD_MECHANISM.md) now details the moving motor
cradle, pivot stack and rocking spring seats. Travel-stop hardware, wheel-drop
switches and connected rail/seat joints remain next. Caster retention, connector
mating and the complete mounting/cable tolerance stack remain fabrication gates.
