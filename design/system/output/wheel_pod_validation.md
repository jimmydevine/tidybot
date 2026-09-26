# J verification record — 2026-09-14

This records software and candidate-geometry checks. No physical motor, suspension,
wet-floor, load, fatigue or flight test was performed.

- Python regression suite: **89 tests passed** (82 existing, seven J tests).
  J covers preserved baseline inputs, seat-force moments, invalid guide/coil
  dimensions, the unresolved sofa preload shortfall, stop geometry, impact-moment
  balance, pin sensitivity and motor shaft/thread dimensions.
- Spring dimensions: **1,638 sampled travel/shim combinations**; positive preload,
  guide overlap, end clearance and specified solid-height margin pass. The exact
  spring, fatigue/buckling and manufacturing tolerances are unqualified.
- Revised full-bump load screen: **26 preload/direction cases**. It uses the actual
  contact lever and spring line. The 8 mm pin passes the project bending/shear
  screen; 6 mm fails. This is not a strength check of the printed cradle or joints.
- FreeCAD 1.1.3: **89 exported objects** across nominal, bump and droop documents.
  Candidate/source solids were checked with `isValid()` before export; context
  allocations and clearance reservations are displayed as edges. All three native
  archives pass integrity checks and contain `Document.xml`.
- Supplier CAD mating: **96 pair checks** (hub/wheel × bracket/two flush screw
  envelopes/cradle × twelve rotation angles); maximum intersection **0 mm³**.
  The candidate bracket is a drawing reconstruction with countersinks added,
  not the exact stock bracket CAD. See input STEP hashes in the CAD check JSON.
- Internal mechanism: **270 enumerated pair checks** across six wheel-travel
  positions and three shim heights; no intersections above 0.00001 mm³ after
  relieving the lower cup's adjacent bearing web. The test explicitly covers
  that relief, collars, cap/cheeks, upper fork and telescoping guides. It is not
  an all-parts or continuous/tolerance clearance proof. Contact interfaces and
  unmodeled fasteners are not certified by this result.
- Interactive SVG: six travel/preload combinations executed with a Node DOM stub,
  with no invalid coordinates or missing readouts. A QtSvg rendering of full bump
  at maximum preload was visually inspected. This is not a full browser or
  accessibility audit.
- Six source-config SHA-256 fingerprints matched the generated calculation data.
  Existing G/H/I files were retained; G complete masses are unchanged.
- Fifteen local links in the J review documents and viewer resolve.

The candidate pod subtotal is **106.216 g per side** before motor, wheel, hub,
fixed cap/cheeks/frame and completion of structural joints. Solid printed-part
volumes use an assumed 1.27 g/cm³ density; density, print process and hardware
allowances require reconciliation. The sofa preload check remains **failed** at
the upper nominal caster-heading case, and no structural fabrication is released.

Reproduction commands and supplier CAD download links are in
[the design record](../../../docs/WHEEL_POD_MECHANISM.md).
