# Fixed drive-mount comparison — N

This is a lighter construction candidate, not an adopted drivetrain. Removing independent wheel suspension transfers floor-following requirements to the cleaning head. M cannot be carried forward unchanged.

| Complete carried assembly | M | N comparison | Potential reduction |
|---|---:|---:|---:|
| vacuum | 5.316 kg | 5.086 kg | 230.0 g |
| mop | 4.954 kg | 4.724 kg | 230.0 g |

Same battery, contents, cap, motors, wheels, caster, head mechanisms and frame budgets. The cap is included; the lift top is not. No head-mechanism savings or overlap credits are taken. The potential reduction remains conditional on head redesign and complete joint checks.

| Local replacement item | Count | Total |
|---|---:|---:|
| motor support angles | 2 | 110.8 g |
| common crossmember | 1 | 42.0 g |
| rail cleats | 2 | 10.1 g |
| Pololu 2676 brackets | 2 | 17.0 g |
| motor M3x6 flush screws | 4 | 2.2 g |
| foot M3x12 screw washer locknut sets | 8 | 15.2 g |
| support M4x25 screw washers locknut sets | 4 | 16.8 g |
| beam M4x25 screw washers locknut sets | 2 | 8.0 g |
| rail M4x12 screw washers locknut sets | 4 | 10.8 g |
| beam horizontal compression sleeves | 4 | 4.1 g |
| beam vertical compression sleeves | 2 | 2.1 g |
| completion reserve | 1 | 20.0 g |

The 225 g bottom-frame budget remains. Nominal stock mass counts full sections, including the large-angle inside radius, without deducting holes. Fastener sets, compression sleeves and a 20 g completion reserve are explicit. Mass coordinates for stock/fasteners are approximate; CG is a planning value.

## Terrain consequence

| Module | Required head translation in sampled states | Pitch | Roll | Minimum support reaction |
|---|---:|---:|---:|---:|
| vacuum | -8.4 to 10.0 mm | 5.22° | 2.32° | 4.2 N |
| mop | -6.0 to 10.0 mm | 5.22° | 2.32° | 6.4 N |

M allows -2 to +10 mm translation and ±1.5° tilt. Its motion envelope fails the rigid-chassis comparison. These samples represent 4/10 mm horizontal levels and eight caster headings. A finite head straddling a vertical edge, backing down a step, body clearance, impact, wet traction and changing head spring/contact forces are not validated by positive support reactions.

## Drive and structure screens

- vacuum: flat demand 0.077 N·m per motor; conservative continuous screen 0.392 N·m. At a 10 mm sharp edge, worst driven-wheel initiation torque 0.613 N·m; caster-climb friction coefficient requirement up to 0.18. Current-limited screen 0.780 N·m; intermittent gearbox screen 0.785 N·m.
- mop: flat demand 0.118 N·m per motor; conservative continuous screen 0.392 N·m. At a 10 mm sharp edge, worst driven-wheel initiation torque 0.475 N·m; caster-climb friction coefficient requirement up to 0.64. Current-limited screen 0.780 N·m; intermittent gearbox screen 0.785 N·m.

The retained 150 N vertical and ±25 N fore-aft per-wheel structural cases give 98.6 MPa at the angle strip (120 MPa screen), and 30.8 MPa for the crossmember bound (55 MPa screen). Beam deflection bound 0.211 mm; twist bound 0.09°. These are local section checks, not complete mechanical qualification.

The motor-to-beam joint screen assumes two 1,250 N bolt preloads and friction coefficient 0.15. It is not a tightening instruction. Beam bending includes the couples from the outboard wheel positions; torsion assumes rotational restraint at the ends. Cleats/rails, washer seating, tube-hole net sections, load transfer into the full chassis, motor radial loading, tolerances and fatigue remain to resolve.

## Decision and next work

Continue with a passive, retained vacuum cassette sized for the calculated head motion, and compare its complete installed mass against M. Keep the rigid-mount option conditional until that cassette fits and wet 10 mm crossings have a credible traction margin. The current candidate reduces mass by about 230 g; it does not solve the whole-robot weight problem. Retain the previous suspension geometry as the fallback.

The mop's nominal CG is Y=139.5 mm. At the illustrative wet friction coefficient 0.35, the caster-climb calculation requires Y ≤ 126.2 mm: approximately 13.3 mm forward. Investigate front-mounted water storage or a mop-specific axle location. This is a placement target, not a credited mass reduction or an assertion that those parts fit. Suspension alone does not remove a rear-heavy caster's climb load.

No new order or print follows from this comparison. The metal pieces require cut stock, trimmed angle legs, drilled holes and deburring; precision compression spacers or supplier-cut spacers are needed. No mill/lathe is assumed. Confirm cutting capability or use supplier processing before fabrication.

## Sources

- [angle](https://www.onlinemetals.com/en/buy/aluminum/2-x-2-x-0-1875-aluminum-angle-6061-t6-extruded-structural/pid/988)
- [tube](https://www.onlinemetals.com/en/buy/aluminum/0-5-x-0-063-aluminum-square-tube-6063-t52-extruded/pid/20685)
- [tube properties](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6063.pdf)
- [motor bracket](https://www.pololu.com/product/2676)
- [motor guidance](https://www.pololu.com/file/0J1829/pololu-25d-metal-gearmotors.pdf)

[Geometry and limitations](../../../docs/FIXED_DRIVE_COMPARISON.md) · [Mass correction](../../../docs/MASS_OPTIMIZATION_REVIEW.md)
