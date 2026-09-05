# Phase 1 — Port Bench Test Plan

**Goal:** answer the five open questions in [INTERFACE.md §5](INTERFACE.md) before any
real module is designed.

**This phase builds no robot.** It builds three printed parts and a small pile of steel.
That is deliberate: the coupler is the one component every future module depends on, and
it is far cheaper to iterate as a 110 mm coupon than as part of a chassis.

---

## 1. Parts

```
make -C cad all
```

Produces in `cad/tests/`:

| Part | Print time (est.) | Orientation |
|---|---|---|
| `coupon_port_male` | ~2.5 h | As generated, boss up |
| `coupon_port_female` | ~3 h | As generated, bore up |
| `coupon_latch_collar` | ~1 h | As generated |

TAZ 6, PETG, 0.5 mm nozzle, 0.25 mm layers, 4 perimeters, 40 % gyroid, **no supports**.

## 2. Hardware

Run `make -C cad report` for the generated BOM. Per coupon pair:

| Qty | Item | Notes |
|---|---|---|
| 3 | Ø8 mm chrome steel bearing balls | Kinematic coupling, epoxy into male flange |
| 6 | Ø3 × 30 mm hardened dowel pins | Vee grooves, female flange |
| 3 | Ø6 mm chrome steel bearing balls | Latch detent |
| 1 | Ø5 × 16 mm dowel pin | Key, press into male boss |
| 4 | M5 × 20 bolts | Fixture mounting |
| 1 | M8 eye bolt | Pull test |

Also needed: dial indicator (0.01 mm), luggage scale or spring gauge to 15 kg, feeler
gauges, digital calipers, epoxy.

## 3. Reading the parts

Before assembling, orient yourself. Nothing here is decorative — every hole has a job.

### Male coupon (`coupon_port_male`)

A flat 110 mm plate with a Ø50 × 22 mm boss standing up in the middle.

**The Ø90 flange is flush with the plate top, not a raised disc** — so don't look for a
protruding ring. The flange face *is* the plate's top surface.

| What you see | Ø | Where | What goes in it |
|---|---|---|---|
| 4 corner holes | 5.5 | plate corners | M5 bolts → test fixture |
| **3 sockets in the flat face** | **8.2 × 5 deep** | **Ø70 circle, at 90° / 210° / 330°** | **Ø8 steel balls, epoxy** |
| Boss | 50 × 22 tall | centre | inserts into the female bore |
| Groove around the boss | 2 deep | 16 mm up the boss | the female's Ø6 detent balls |
| Big centre hole | 20 | through everything | wiring harness |
| Small hole in boss end face | 4.9 | Ø36 circle, at 180° | Ø5 dowel, press fit — the key |
| Rectangular recess in boss end face | 24 × 10 × 1.6 | Ø36 circle, at 0° | contact pad PCB |
| Hole near one plate edge | 8.5 | offset from centre | M8 eye bolt, for the T3 pull test |

**The three Ø8.2 sockets are the ones that matter.** They are the kinematic coupling —
the entire reason this project uses steel instead of printed surfaces.

### Female coupon (`coupon_port_female`)

A 110 mm plate with a Ø90 × 31 mm cylinder on top. The mating face is the **top** of that
cylinder, facing up, with the bore going down into it.

| What you see | Ø | Where | What goes in it |
|---|---|---|---|
| 4 corner holes | 5.5 | plate corners | M5 bolts → test fixture |
| Tapered mouth → straight bore | 66.4 → 50.4 | centre | receives the male boss |
| **3 rectangular pockets in the top face** | — | **Ø70 circle, at 90° / 210° / 330°** | — |
| **2 cross-holes per pocket** | **3.1** | running radially, 7 mm apart | **Ø3 dowel pins — 6 total** |
| 3 radial holes through the outer wall | 6.2 | 15 mm down, at 30° / 150° / 270° | Ø6 detent balls |
| Small hole deep in the bore | 5.3 | Ø36 circle, at 180° | clearance for the key — stays loose |
| Rectangular pocket at the bore floor | 25 × 11 | Ø36 circle, at 0° | pogo pin block |
| Large hole near one plate edge | 25 | offset | finger grip, for 500 mate cycles |
| Centre hole | 20 | through | wiring harness |

The three pockets pair with the three sockets on the male. **A ball drops into a pocket
and rests on the two dowels** spanning it — that is the vee. Steel ball on steel pins,
line contact, no printed surface involved.

### Collar (`coupon_latch_collar`)

A plain ring that slides down over the female cylinder to trap the detent balls inward.
Lift it to release. Hand-operated in v0.1; powered actuation comes later.

---

## 4. Assembly

1. Epoxy the three Ø8 balls into the three Ø8.2 sockets on the male plate's flat face. **Check protrusion is
   3.0 ± 0.1 mm on all three** before the epoxy cures — this directly sets coupling
   repeatability, and it is the one dimension that cannot be fixed afterwards.
2. Slide the six Ø3 dowels into the female vee channels. They should be a slip fit,
   retained by the printed walls. If loose, a dab of epoxy at one end only.
3. Press the Ø5 key pin into the male boss.
4. Drop the three Ø6 detent balls into the female radial holes; fit the collar.

## 5. Tests

Record every result in `tests/phase1-results.md`. **Write down failures**; a coupon that
fails is more informative than one that passes.

### T1 — Repeatability (answers Q4)
Mount the female to the fixture. Dial indicator against the male plate rim.
Mate and demate **50 times**, recording the indicator each time.

- **Pass:** σ < 0.05 mm, total spread < 0.1 mm.
- Ball protrusion inconsistency is the most likely culprit if this fails.

### T2 — Capture envelope (answers Q2)
Offset the male progressively from centre and lower it in, hands off, under its own
weight. Find the largest offset that still seats.

- **Pass:** ≥ 8 mm lateral, ≥ 5° angular.
- If short, the funnel needs a shallower angle (and more length — check `ENGAGEMENT`
  stays ≥ 6 mm; `derived()` will refuse a spec that violates this).

### T3 — Static pull (answers Q3)
Eye bolt in the male plate, female fixed, collar locked. Load progressively to 8 kg.

- **Pass:** holds 8 kg for 60 s, no permanent deformation, no cam-out.
- If the detent cams out, deepen `DETENT_DEPTH` or increase collar backing stiffness.

### T4 — Moment stiffness (answers Q1)
Seated and latched, apply a 4 N·m moment (e.g. 4 kg at 100 mm). Measure flange rim
deflection.

- **Pass:** < 0.3 mm, fully recovered on release.
- If the flange faces contact under load, the 1.0 mm gap is too small — but be careful:
  increasing the gap reduces detent engagement. Prefer stiffening the flange first.

### T5 — Cycle life (answers Q5)
500 mate/demate cycles. Inspect ball sockets, vee dowels and the detent groove every 100.

- **Pass:** repeatability from T1 still within spec at cycle 500; no socket elongation,
  no groove wear through.
- Socket wear here is the trigger for a metal insert in v0.2.

## 6. Exit criteria

Phase 1 is complete when **T1–T5 all pass on the same coupon pair**, results are recorded,
and any resulting parameter changes are:

1. made in `cad/lib/tidybot_port.py`,
2. validated with `make -C cad check`,
3. reflected in `INTERFACE.md` with `SPEC_VERSION` bumped,
4. re-verified by a fresh print.

Only then does `SPEC_VERSION` go to **1.0.0**, and only then does module design start.

## 7. Expect to iterate

Two to four coupon revisions is normal and is not a sign anything has gone wrong. The
whole reason this phase exists is to absorb that iteration in 3-hour prints rather than
in a chassis. Budget two to three weeks of evenings.
