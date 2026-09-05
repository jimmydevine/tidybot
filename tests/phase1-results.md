# Phase 1 — Port Bench Results

Record every coupon revision here, including failures. A failed coupon is the point of
the exercise; an undocumented one wastes the print.

Procedure: [docs/PHASE1_TEST_PLAN.md](../docs/PHASE1_TEST_PLAN.md)

---

## Rev A — spec 0.2.0

**Printed:** _(date)_
**Material:** PETG, 0.25 mm layer, 4 perimeters, 40 % gyroid
**Post protrusion measured:** _(3 values, target 18.0 ± 0.1 mm)_
**Flange gap when seated:** _(4 points around the rim, target 1.0 ± 0.15 mm)_

| Test | Target | Measured | Pass? |
|---|---|---|---|
| T1 mate reliability | 50/50, gap 1.0 ± 0.15 | | |
| T2 keying at 120° | impossible | | |
| T2 keying at 240° | impossible | | |
| T3 capture, lateral | ≥ 3 mm | | |
| T3 capture, yaw | ≥ 1° | | |
| T4 static pull | 200 N for 60 s | | |
| T4 failure mode | PETG bearing before pin shear | | |
| T5 contamination, dust | 50/50 | | |
| T5 contamination, wet | 50/50, drains clear < 30 s | | |
| T6 cycle life | T1 + T3 hold at 500 | | |

**Observations:**

**Parameter changes for Rev B:**
