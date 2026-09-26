# Revision K verification record

Checked 2026-09-14. This records calculation and nominal CAD checks, not physical
testing or a fabrication release. See the [design record](../../../docs/POD_JOINTS_AND_STOPS.md)
for remaining qualification work.

## Calculations

`python3 -m unittest discover -s design/system -p 'test_*.py' -q`:
**96 tests passed**, including seven new K tests. They cover stop-clearance
compensation, invalid slot geometry, load and tray screens, wheel-moment balance,
inner rail bolt/edge checks, and mass/centre-of-mass replacement without counting
motors twice. Passing these tests does not establish that the assumed load cases
cover every real event.

## CAD

FreeCAD 1.1.3 exported nominal, bump and droop assemblies. The exporter checked
**275 non-null, valid shapes** across those files (92, 92 and 91 respectively).
All three FCStd archives passed CRC checks and contain Document.xml; their three
STEP exports are present.

- Moving/fixed clearance checks sampled wheel travel at −2.5, 0, 5 and 10 mm with
  0 and 6 mm spring shims: eight combinations, no recorded interference.
- An additional all-parts audit at the three exported poses performed **605
  exact Boolean intersection checks** after bounding-box filtering; no unexpected
  intersections remained. Intended tapped-joint intersections and motor screws
  entering the undrilled motor proxy are excluded. Envelope-only reservations
  are handled separately, including the collar-clearance checks.
- Selected adjacent battery, cleaning, extension and electronics allocations from
  the height/mounting layout were checked for vacuum, mop and sofa configurations
  at the exported poses; no recorded conflicts. This is not a check of every
  neighboring component or continuous motion.
- The sleeve contacts the closed slot at both nominal travel limits with zero
  intersection volume. At 0 and 5 mm travel the minimum gap is 0.25 mm. Extending
  travel another 0.1 mm beyond each limit produces approximately 0.564 and
  0.589 mm³ of intersection, confirming that the modeled endpoints constrain
  nominal travel.

Detailed results, mass rows and seven configuration SHA-256 fingerprints are in
[pod_joints_cad_checks.json](pod_joints_cad_checks.json). All seven fingerprints
were checked against the current input files after the final export.

## Review view and consistency

The generated HTML's JavaScript rendered −2.5, 0, 5 and 10 mm travel using a
Node DOM stub, with no NaN/undefined coordinates and the current 244.5 g pod
readout. The bump SVG was rendered through QtSvg and visually reviewed for
legibility. This does not substitute for full browser interaction or accessibility
testing. The drawing is a simplified side projection of parts at different X
positions; the FreeCAD assemblies contain the detailed joints.

The regenerated mass overlay replaces only the two G pod allowances. Nominal
loaded totals are 5.142 kg vacuum, 4.856 kg mop and 5.421 kg sofa vacuum, each
365.0 g above G. These remain estimates; no parts have been weighed in this pass.

## Limits

No physical load, wet-floor traction, fatigue, impact, fabrication-fit or spring
tests were performed. Actual spring selection and loaded ride height, remaining
joint qualification, thread engagement/preload, locking, spring-pin retention,
wheel-drop sensing, wiring and fabrication processes remain open. The sofa
configuration exceeds the existing 0–6 mm spring-shim range. Do not extend that
range without rechecking spring coil bind and guide end clearance.
