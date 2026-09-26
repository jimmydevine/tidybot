# Wheel suspension and caster support — H study

Follow-up: the [I height/mounting overlay](HEIGHT_AND_CASTER_LAYOUT.md) retains
this travel and passes the sampled height screen with a C1 lidar and revised
connector layout. It also replaces the assumed caster fitting height below with
a documented fitting and moves adjacent equipment. Caster pull-out retention
remains open. This H document and its artifacts retain the earlier failing case.

The next candidate uses **rear-mounted suspension pivots and a shallow caster
saddle**, with fixed rails carrying both their loads and the floor electronics.
The [interactive mechanism view](../design/system/output/floor_support.html)
shows wheel travel and the resulting height screen. The
[generated report](../design/system/output/floor_support.md) contains dimensions,
load calculations, stock accounting and unresolved connections.

The wheel axle moves 3 mm forward to leave room for the pivot supports ahead of
the mop mechanism. A 40 mm leading arm preserves 10 mm upward travel. A 6 mm
smooth pin with replaceable bushings is the current candidate: the earlier 4 mm
pin fails the preliminary impact bending screen once the separate bump-stop
force is included. This does not qualify the motor output shaft or its bearings
for the same load.

The spring acts closer to the pivot than the wheel. A 5 N/mm spring therefore
provides approximately 0.8 N/mm at the wheel. The spring needs module-specific
preload, a guided/pivoting seat and separate mechanical travel stops. These are
component requirements, not a selected spring or finished moving pod.

The caster's 40 mm-wide support uses a flat 3 mm aluminum plate, attaching
to a rear crossbar through bolted angles. It reserves another 5 mm above the plate
for retaining hardware. Its separate stem fitting matters: the 2.5 mm added
height case leaves only **1 mm beneath the vacuum/mop bin allocation**. A 5 mm
fitting fails that space. The reference fitting is an assumption pending an exact
manufacturer drawing; the bare caster's rolling load rating does not establish
its retention during lifting.

**The full height requirement is still open.** The previous 179.1 mm result
describes the nominal suspension pose. Sampling an ideal three-support model
with 2.5 mm downward wheel travel produces heights up to **181.9 mm**, beyond the
180 mm constraint. That travel has not been adopted. Sensor/cap placement and
the full suspension envelope must be resolved together, with manufacturing
clearance. Removing wheel travel silently would not resolve that design tradeoff.

Candidate stock routes clear the existing vacuum, mop and sofa allocations;
the candidate blanks also avoid volumetric overlaps with each other. Their
mounting angles, fasteners, the moving tray, stop fingers, cable loops and all
four module-seat connections remain incomplete. The existing **G complete
mass estimates remain unchanged**. Partial stock masses cannot establish a
replacement frame weight or justify removing the existing power carrier.

The manufacturer review also corrects the earlier drive torque screen:
Pololu's gearbox guidance limits continuous loading to **0.392 N·m**, below the
earlier 0.539 N·m fraction-of-stall estimate. Its general 25%-of-stall-current
guidance corresponds to 1.25 A; treat the existing 2 A setting as a bounded
transient setting, with motor thermal limits still applying.
[Manufacturer guidance](https://www.pololu.com/product/4846).

Review artifacts:

- [Editable inputs](../config/floor_support.json) and
  [candidate stock ledger](../design/system/output/floor_support_stock.csv).
- Reference CAD: [vacuum](../design/system/output/floor_support.FCStd),
  [mop](../design/system/output/floor_support_mop.FCStd),
  [sofa](../design/system/output/floor_support_low.FCStd),
  [full bump](../design/system/output/floor_support_bump.FCStd),
  [candidate droop](../design/system/output/floor_support_droop.FCStd).
  Each has a same-named STEP file. Wireframes show functional allocations and
  mechanism routes; these are not complete motor cartridges or fabrication files.
- [Verification record](../design/system/output/floor_support_validation.md).

Reproduce from the repository root:

```sh
python3 design/system/floor_support.py
python3 -m unittest discover -s design/system -p 'test_*.py' -q
freecadcmd design/system/export_floor_support_freecad.py
```

Next, resolve the suspension height envelope and the retained caster fitting,
then finish moving-pod and rail/seat fasteners before replacing the frame/carrier
allowances. No purchase or print is needed for this review.
