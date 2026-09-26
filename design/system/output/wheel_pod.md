# J wheel-pod mechanism study

Candidate mechanism, not fabrication or purchase release

Complete G mass remains unchanged. These are calculated nominal dimensions and candidate parts; no physical load test is claimed.

## Shaft, motor and wheel stack

Left tire X=2…26 mm; mirrored right tire ends at 273 mm. Motor plate X=24…26 mm sits inside the wheel recess.
Shaft/hub nominal axial overlap 8.50 mm; motor boss to hub back 1.50 mm. Proposed flush M3×6 screws enter the gearbox 4 mm, below its 6 mm maximum. Stock bracket holes are not countersunk.

## Pivot and spring

| Pin | Calculated bending | Preliminary screen |
|---|---:|---|
| 6 mm | 211.5 MPa | Fail |
| 8 mm | 89.2 MPa | Pass |

Bearings at X=44/88 mm leave room for two internal collars. The 8×80 mm steel pin weighs 31.57 g per side before tolerances. Collar clearance diameter is 22.4 mm, including the clamp screw.

At full bump the stop lever is 26.34 mm, rather than its nominal 32 mm. Re-solving equilibrium across preload settings gives a maximum stop force of 218.5 N. The weakest-preload case matters; the largest spring force alone does not bound pivot load.

Spring sourcing target: 5 N/mm, free length 32.5 mm, OD≤10 mm, ID≥7 mm, solid height≤13.5 mm. Across 1638 sampled travel/preload combinations, installed length is 15.76–26.99 mm and force reaches 83.7 N.
Minimum telescope overlap 2.01 mm; guide end gap 1.26 mm; spring solid-height clearance 2.26 mm. Dimensional screen: pass. This does not verify a spring SKU, fatigue, friction or print fit.

Shims lower the upper rocker fork by 0–6 mm. At nominal travel, this supports 13–25 N per wheel. Shims are a setup adjustment for each bottom module; automatic attachment exchange does not adjust them.

| Bottom | Left shim range | Right shim range | In range |
|---|---:|---:|---|
| vacuum | 4.60–5.03 mm | 2.96–3.38 mm | True |
| mop | 1.53–2.61 mm | 0.23–1.31 mm | True |
| low | 5.60–6.02 mm | 2.29–3.10 mm | False |

Those ranges use G nominal mass/CG and caster headings, not revised pod mass or payload uncertainty. Recalculate after the installed mass ledger closes.

## Stop targets and remaining work

Moving bump-contact point at nominal Y/Z=113.00/54.59 mm reaches the fixed Z=62 mm plane at +10 mm wheel travel. A positive droop retainer must stop at −2.5 mm. These point targets are not connected hardware.

Finish the metal/printed load path, cap-to-frame fastening, spring SKU and cups, hard-stop strike surfaces, droop capture, wheel-drop switch, cable loop and bushing housing process. Raw printed bores are not precision bearing housings. Motor output-shaft radial capacity and hub clamp strength remain unverified. Caster retention from I also remains open.

## Sources

- [motor](https://www.pololu.com/product/4846)
- [motor drawing](https://www.pololu.com/file/0J1634/25d-metal-gearmotor-dimension-diagram.pdf)
- [bracket](https://www.pololu.com/product/2676)
- [bracket drawing](https://www.pololu.com/file/0J825/2676-bracket-dimensions.pdf)
- [collar](https://www.ruland.com/mcl-8-a.html)
- [bushing](https://www.igus.com/iglide-ibh/sleeve-bearings/product-details/iglide-g1-m?artnr=G1SM-0810-10)
- [wheel](https://www.gobilda.com/hogback-traction-wheel-72mm-diameter-50a-durometer/)
- [hub](https://www.gobilda.com/1309-series-sonic-hub-4mm-bore/)
