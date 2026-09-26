# H suspension/support verification

2026-09-14. H is a mechanism and support study. G remains the complete mass
baseline; no H assembly is released for fabrication or flight.

## Completed

- Generated the report, interactive HTML and stock ledger with
  `python3 design/system/floor_support.py`.
- Ran `python3 -m unittest discover -s design/system -p 'test_*.py' -q`:
  **75 tests passed**, including 11 new H tests. The tests check arm geometry,
  spring motion ratio, motor-envelope clearance and a failing roof position,
  beam equilibrium, impact-stop loading, pin diameter sensitivity, plate bending,
  fitting-height failure, stock routes, support-plane constraints, height failure,
  unchanged G mass and corrected gearbox limits.
- Sampled **7,776 ideal support poses** across three caster positions, wheel
  travel combinations and caster heading. The worst sampled height is 181.876 mm;
  the candidate droop therefore fails the 180 mm height screen.
- Candidate stock boxes have no mutual volumetric overlaps and clear the external
  vacuum/mop/sofa functional bays in the declared replacement check. Own old
  pod/caster envelopes and the six proposed removed F supports are excluded from
  that external check. This does not qualify their joints or moving hardware.
- Exported five FreeCAD/STEP references with FreeCAD 1.1.3. **615 shapes** passed
  shape validity: vacuum 125, mop 115, sofa 125, bump 125 and droop 125. See
  [CAD results](floor_support_cad_checks.json).
- Executed the final embedded JavaScript with a minimal DOM stub in Node.
  Nominal and full-bump spring/angle outputs were checked; two droop/roll height
  cases agreed with the Python model within 1e-8 mm and selected the failure
  indicator. This checks script behavior, not browser layout or accessibility.
- Rendered the generated mechanism SVG with QtSvg, which reported a valid
  document, and visually inspected the drawing. A full Chromium page check could
  not run because the installed snap's confinement setup rejected launch. No
  browser-rendering verification is claimed.

Input SHA-256 fingerprints are recorded in [floor_support.json](floor_support.json).
The generated stock CSV contains gross blanks only, including material later
removed for holes. It is not a complete purchasing list.

## Limits

No physical tests were performed. Nominal component envelopes do not verify the
wheel/hub cavity, motor-shaft radial capacity, wiring bends, bushing ratings,
spring fatigue, stop contact or mounting-head clearances. Motor-box clearance at
full bump is only about 0.77 mm; it needs tolerance and cable/bracket review.

The caster plate calculation assumes a rigid rear attachment. Stock angles,
fasteners, countersinks, the actual retained stem and its complete installed
height remain to detail. The reference allows 5 mm above the plate for retaining
hardware; that allowance is not a supplier-verified mounting stack.

The suspension-plane calculation uses spherical tire reach and an ideal caster
support point. It is a sampled geometric screen, not a continuous extremum proof,
spring equilibrium/contact simulation or proof of step climbing. Droop remains
unadopted pending the height revision. Retention during airborne transfer and
wet-floor performance remain unqualified.

The fixed rails still need complete connections to all four module seats, and
the moving tray/ears, travel stops and support fasteners need an installed ledger.
Accordingly, the existing bottom-frame, pod, caster and F carrier allowances are
retained in G without claiming a mass reduction from this partial design.
