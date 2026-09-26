# H — wheel pivots and rear support

**Candidate mechanisms, with open integration gates. G remains the complete layout/mass baseline.** This pass adds load and travel checks; it does not release prints or claim a lighter robot.

## Wheel mechanism

Use a 40 mm leading arm with its pivot behind the axle. The proposed axle moves 3 mm forward to y=105; pivot y=145, z=36. This gives room for 6 mm pivot holes and rear edge material ahead of the mop drive at y=155. It corrects the earlier “trailing pod” terminology. The two motors, hubs and 72 mm wheels remain the same candidates.

Each fixed hanger has two 3 × 22 × 36 mm cheek blanks and an 80 × 45 × 3 mm roof plate at z=62–65. A smooth 6 mm pin runs through the cheeks, with two 6 mm-ID / 8 mm-OD / 8 mm-long bushings in moving ears. Retain both pin ends mechanically; threads do not run inside bushings. The roof needs both outer and inner rail support. Printed moving ears locate replaceable bushings; a metal motor-face bracket and under-motor tray carry motor loads. Their final shape, spring cups, stop fingers and attachment hardware remain to detail.

The proposed roof stays below the battery pocket. A compression spring sits 16 mm forward of the pivot, beside/behind the motor, with a pivoting lower seat. A separate compression stop acts 32 mm forward of the pivot; the spring must not be the travel stop. Two wheel-drop switches remain in the sensor budget.

| Wheel travel | Arm angle | Axle moves rearward | Motor-envelope gap below roof | Spring seat spacing |
|---|---:|---:|---:|---:|
| -2.5 mm | -3.58° | 0.078 mm | 15.24 mm | 27.00 mm |
| +0.0 mm | +0.00° | 0.000 mm | 13.50 mm | 26.00 mm |
| +10.0 mm | +14.48° | 1.270 mm | 0.77 mm | 22.00 mm |

Positive travel is bump; negative travel is droop. Rotating the full rectangular motor envelope is conservative relative to its cylindrical body, but does not include a qualified cable bend radius, bracket, screw-head or spring-seat envelope.

At a 0.4 spring-to-wheel motion ratio, the earlier 0.8 N/mm wheel rate requires approximately **5 N/mm at the spring**, not a 0.8 N/mm spring. Target OD ≤10 mm and solid height ≤18 mm, leaving at least 2 mm before coil bind at full bump in the reference geometry. Preload varies by module and must be set with its assembled load. No spring SKU is approved by this target.

| Bottom | Left normal load | Right normal load | Preload compression, left/right |
|---|---:|---:|---|
| vacuum | 22.2–23.1 N | 18.9–19.8 N | 11.1–11.5 / 9.5–9.9 mm |
| mop | 16.1–18.2 N | 13.5–15.6 N | 8.0–9.1 / 6.7–7.8 mm |
| low | 24.2–25.0 N | 17.6–19.2 N | 12.1–12.5 / 8.8–9.6 mm |

These are nominal G mass/CG calculations over caster heading, with the proposed contact position. They exclude mass uncertainty, cleaning-head support, asymmetric obstacles and the small CG change from moving the wheel assemblies. Spring procurement also needs free length, tolerances, fatigue and guided buckling checks.

## Pivot and impact load path

Wheel → motor bracket/moving tray → bushed ears and compression stop → fixed cheeks/roof → inner and outer rails → metal module-seat joints. The latter joints are not completed by this study. The motor output shaft remains another unqualified link; a stronger suspension pin does not establish the motor shaft’s radial-load capacity.

Screen one wheel at 150 N vertical and 25 N fore/aft, with 85 N spring force at bump. Moment balance about the suspension pivot requires **173.1 N** at the separate stop. Include this force when calculating pivot reactions; treating the pin as carrying only the wheel's vertical load misses the stop moment. These are engineering load cases, not a verified impact spectrum.

| Pin diameter | Bending bound | Mean shear bound | Project screen |
|---|---:|---:|---|
| 4 mm | 257.6 MPa | 22.8 MPa | Fail |
| 5 mm | 131.9 MPa | 14.6 MPa | Pass |
| 6 mm | 76.3 MPa | 10.1 MPa | Pass |

The selected 6 mm pin gives a projected bushing-pressure screen of 6.0 MPa. Select an actual bushing material and rated pin grade for this pressure and oscillatory duty. The 150 MPa steel bending / 90 MPa shear limits are declared screening assumptions. Retaining hardware, fatigue, printed-ear creep, roof-plate joints and stop contact still need verification.

## Rear caster saddle

Use a flat 40 × 44 × 3 mm aluminum plate, ending at a rear crossbar at y=266. A 40 mm-wide downward tab in that crossbar provides the rear attachment zone. Connect the plate with bolted stock angles, using flush underside screw heads; CAD shows the plate and tab, not completed angle joints. No sheet-metal brake or milled channel is required. The vacuum/mop saddle is centred at x=137.5; the sofa saddle moves to x=230. Reserve 5 mm above the plate for the stem retainer/washer/thread stack. No additional caster is added.

For the flat plate, I=90.0 mm⁴. A 100 N vertical load at a 34 mm cantilever plus the adverse 25 N horizontal load applied 50.5 mm below the plate gives **77.7 MPa** bending and **0.328 mm** deflection. This assumes rigid attachment; it excludes stem-hole concentration, torsion, fastener slip, countersink effects and wear.

The TENTE L51-8 is supplied with a blind fitting bore. Its separate retained fitting has to be specified; bare caster height is not installed mounting height. The manufacturer fitting table lists several stem families with different added heights. Do not substitute a generic M8 bolt or infer retention strength from the rolling load rating.

| Added fitting height | Top including 5 mm retainer reserve | Gap below vacuum/mop bin | Gap below sofa blower |
|---|---:|---:|---:|
| 0.0 mm | 58.5 mm | 3.5 mm | 5.5 mm |
| 2.5 mm | 61.0 mm | 1.0 mm | 3.0 mm |
| 5.0 mm | 63.5 mm | -1.5 mm | 0.5 mm |

The 2.5 mm case used in the reference CAD has only 1 mm beneath the vacuum/mop allocation. It is conditional on the actual fitting and fastener stack. A 5 mm fitting fails that space. Stem retention under lifting, access to its fastener and a supplier drawing are still required.

## Power shelf and frame integration

The proposed front bridge, two outer rails and two inner rails provide routes from the shelf to the fixed wheel hangers. The left rail also stiffens the shelf’s left edge; a separate 2 × 70 × 8 mm rib supports its right edge. The rear crossbar carries the caster saddle. Keep power electronics on these fixed members, with strain-relieved wiring to the moving motors.

Candidate aluminum blanks total **196.9 g**, before their joint hardware and the rest of the chassis. The six F post/foot/tab items that could be removed total **24.3 g**. Comparing those numbers alone is misleading: some candidates replace part of the existing 225 g bottom-frame and 112 g installed-caster allowances. The full old allowances, two 62 g pod allowances and F carrier remain in G until every replacement is accounted for. No mass saving is credited.

External allocation audit (own old pod/caster allocations and the six replacement items excluded):

- vacuum: no external stock-route overlap in this check.
- mop: no external stock-route overlap in this check.
- low: no external stock-route overlap in this check.

This audit is not an all-parts interference pass: contact/fastening between candidate plates, curved wheel cavity clearance, screws, moving trays and cable flex are unresolved. Close those joints and the rear/side connections to all four module studs before generating an installed H mass or deleting the F carrier.

## Two requirements corrected by this pass

**Height:** G's 179.1 mm result is a nominal pose. The ideal three-support calculation samples 7776 combinations of wheel travel and caster heading. Its highest case is **181.9 mm**, above 180 mm. This already fails the screen; no physical contact model or tolerance refinement can be assumed to fix it. Keep droop unadopted until sensor/cap placement and suspension attitudes are resolved. Do not reduce suspension performance silently to preserve the old fit claim. The calculation bounds tilted wheel-disk reach with a sphere and treats the caster as an ideal support point; it is not a continuous extrema proof or equilibrium solution.

**Continuous drive load:** Pololu's published gearbox guidance is 4 kgf·cm continuous and 8 kgf·cm intermittent. The continuous screen is therefore **0.392 N·m**, below the old 0.539 N·m fraction-of-stall estimate. The general motor-current guidance gives 1.25 A at 25% of 5 A stall; the existing 2 A setting must be treated as a bounded transient setting. Motor thermal duty and gearbox guidance both apply. Nothing in this study establishes wet-threshold performance.

## Next detail release

Finish the moving motor tray, positive stops and roof-to-rail fasteners; obtain a dimensional drawing for the retained caster fitting; solve the full suspension height envelope. Then close the rear/side/module-seat joints and replace the old frame/carrier allowances with the complete ledger. No purchases or printing are needed for this review.

[Motor guidance](https://www.pololu.com/product/4846) · [Motor drawing](https://www.pololu.com/file/0J1634/25d-metal-gearmotor-dimension-diagram.pdf) · [Caster](https://www.tente.com/en-ca/swivel-castor-50-mm/5940uap050l51-8-load-9011) · [Fitting table](https://www.tente.com/media/c0/dd/db/1770226623/Linea_for_furniture.pdf?ts=1771358769)

[Interactive mechanism](floor_support.html) · [Hardware blanks](floor_support_stock.csv) · [FreeCAD](floor_support.FCStd) · [Verification](floor_support_validation.md)
