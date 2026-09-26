# Wheel-pod mechanism — revision J candidate

The [K follow-up](POD_JOINTS_AND_STOPS.md) now adds metal load-path candidates,
bolted supports, captured travel stops and a complete local pod mass estimate.
The J geometry and partial subtotal below are retained for comparison.

The proposed wheel pod now has a dimensioned motor bracket, moving cradle,
pivot/bearing stack and rocking spring seats. Start with the
[interactive mechanism](../design/system/output/wheel_pod.html) or the
[nominal FreeCAD model](../design/system/output/wheel_pod.FCStd).
This is a packaging study; connected hard stops, structural joints and bearing
fits remain unfinished. No new print or purchase is needed at this stage.

## Motor and wheel mounting

The left motor gearbox face stays at X=26 mm. A 2 mm bracket sits at X=24–26,
inside the recessed centre of the Hogback wheel. The nominal tire occupies
X=2–26 mm; the mirrored right tire ends at X=273 mm. This retains the 275 mm
nominal rigid width and the H wheel-axis locations.

Use the [Pololu 2676 bracket](https://www.pololu.com/product/2676) as the metal
mounting candidate. It weighs 8.5 g and avoids fabricating a bent motor plate.
The model reconstructs its main dimensions and mounting pattern from the
[manufacturer drawing](https://www.pololu.com/file/0J825/2676-bracket-dimensions.pdf);
small bend/edge radii are omitted. It includes a proposed countersink modification
for the two motor screws. The supplied bracket is **not** already countersunk.

Flush M3×6 screw candidates would enter the motor 4 mm through this 2 mm plate.
The [motor drawing](https://www.pololu.com/file/0J1634/25d-metal-gearmotor-dimension-diagram.pdf)
allows at most 6 mm insertion. The 7 mm bearing boss passes through the bracket's
7.5 mm centre hole. Nominal hub engagement is 8.5 mm, with 1.5 mm between the
motor boss and hub back. Actual countersink depth, head dimensions, clamp access,
motor orientation and assembly tolerances must be checked before fabrication.

The supplier wheel/hub CAD was checked against the reconstructed bracket,
flush screw envelopes and cradle through twelve wheel angles. Those checks are
recorded separately from the spring mechanism checks. A nominal CAD clearance
does not establish motor bearing capacity, grip on wet wood or hub clamp strength.

## Pivot and spring

The retained leading-arm geometry has a 40 mm pivot-to-wheel distance, 10 mm
upward travel and 2.5 mm proposed downward travel. An **8 × 80 mm steel pin**
replaces H's 6 mm candidate. Two internal collars leave room for 10 mm long
bushings centred at X=44 and 88 mm. Large outer retention heads would conflict
with the nearby tire, so retention remains inside the fixed cheeks.

The [Ruland MCL-8-A](https://www.ruland.com/mcl-8-a.html) is the collar candidate:
18 mm body diameter, 9 mm width, but **22.4 mm clearance diameter** including its
clamp screw. The latter leaves only 0.8 mm to the bin's Y=157 mm boundary. That
is nominal packaging space, with no completed manufacturing/deflection reserve.
The [igus G1SM-0810-10](https://www.igus.com/iglide-ibh/sleeve-bearings/product-details/iglide-g1-m?artnr=G1SM-0810-10)
is an 8 mm bore, 10 mm OD, 10 mm long bushing candidate. Its housing and shaft
fit must follow the supplier specification; a raw printed hole is not a qualified
precision housing. Collar retention and bearing load/life remain unverified.

Accounting for the actual spring direction and shorter stop lever at full bump,
the preliminary 150 N wheel/25 N fore-aft load screen gives approximately
**211 MPa for a 6 mm pin and 89 MPa for an 8 mm pin**, against the project's
150 MPa bending screen. This checks the pin, not the entire pod. The stop must
carry about **219 N** in the most demanding sampled preload case, above H's
earlier 173 N estimate.

Rocking cups keep the spring aligned as the arm moves. Two short telescoping
guides centre it without crossing the cups' transverse pivot pins. The sourcing
target is 5 N/mm rate, 32.5 mm free length, OD no larger than 10 mm, ID at least
7 mm and solid height no greater than 13.5 mm. **No actual spring is selected.**
The dimensional samples retain 2.26 mm above the proposed maximum solid height,
2.01 mm guide overlap and 1.26 mm guide-to-opposite-seat clearance at their
respective worst poses. Those margins still need spring and print tolerances.

A 0–6 mm shim under the upper fork sets preload separately on each side and
each bottom module. At nominal travel this balances 13–25 N per wheel. It covers
the current vacuum/mop nominal calculations. The sofa module's left wheel reaches
25.04 N, just beyond the range, before any revised pod weight is included.
Do not round that into a pass or choose a production spring from this study.
Payload changes and actual mass/CG need a broader ride-height/equilibrium check.

## Weight and completion sequence

The [CAD check and mass ledger](../design/system/output/wheel_pod_cad_checks.json)
totals **106.2 g per side** using solid printed-part volumes, the catalog
bracket/collars, calculated pin mass and explicit spring/fastener/stop allowances.
This is a partial installed pod estimate, excluding motor, wheel, hub and fixed
cap/cheeks/frame. It must not
be substituted for G's 62 g pod allowance without reconciling those boundaries.
G remains the complete mass baseline; no new flight or endurance result is claimed.

This mechanism makes the weight problem clearer: the solid pin alone is 31.6 g
per side, before retainers and moving structure. The earlier allowance was too
optimistic for this particular arrangement. Any lighter pin/retention or cradle
alternative needs the same load and clearance checks.

Complete these connected features next:

1. Metal load path and fasteners between motor bracket, cradle, bearing housings,
   fixed cheeks/cap and floor frame. The cup-clearance relief in the inner bearing
   web must be included in that strength check.
2. Adjustable bump contact and positive droop capture, followed by a wheel-drop
   switch and motor/encoder cable loop. CAD currently shows **contact targets**,
   not finished stops; the 219 N load needs a real strike surface and fasteners.
3. Reconcile the installed mass, solve ride height across module/payload states,
   and source the spring. Caster pull-out retention from I remains separate work.

This pass does not require machining by the owner. Before releasing parts, the
build plan must identify how the pin is cut, the bracket is countersunk and the
bushing housings are finished, or replace those operations with purchased parts.

## Files and reproduction

- [Inputs](../config/wheel_pod.json), [calculated report](../design/system/output/wheel_pod.md),
  [verification record](../design/system/output/wheel_pod_validation.md).
- [Nominal](../design/system/output/wheel_pod.FCStd),
  [full bump](../design/system/output/wheel_pod_bump.FCStd),
  [full droop](../design/system/output/wheel_pod_droop.FCStd).
  Same-named STEP files are also generated. These show one left pod; the right
  uses the mirrored X layout. No structural STL is released.

```sh
python3 design/system/wheel_pod.py
python3 -m unittest discover -s design/system -p 'test_*.py' -q
freecadcmd design/system/export_wheel_pod_freecad.py
```

The default export uses labeled wheel/hub envelopes. To reproduce the supplier
geometry check, extract the manufacturer's
[hub ZIP](https://www.gobilda.com/content/step_files/1309-0016-0004.zip) and
[wheel ZIP](https://www.gobilda.com/content/step_files/3626-0014-0072.zip) into one
directory and set `TIDYBOT_VENDOR_CAD` to that directory when running the exporter.
Input STEP hashes are recorded in the CAD checks. B-rep bounding boxes for these
curved supplier shapes are loose; the previous tessellated dimension check and
actual shape intersections are used instead of interpreting the loose wheel
bounding box as its diameter.
