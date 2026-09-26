# Phase 1 — Port Bench Test Plan

**Spec 0.2.0 — three tapered posts with cross pins**

Answers the open questions in [INTERFACE.md §8](INTERFACE.md). **This phase builds no
robot.** It builds two printed parts and a small pile of steel, because the coupler is
the one component every future module depends on and it is far cheaper to iterate as a
130 mm coupon than as part of a chassis.

---

## 1. Parts

```sh
make -C cad all
```

Produces in `cad/tests/`:

| Part | Size | Volume | Print time (est.) |
|---|---|---|---|
| `coupon_module_face` | 130 × 130 × 34 | 96 cm³ | ~3 h |
| `coupon_base_face` | 130 × 130 × 31 | 375 cm³ | ~7 h |

TAZ 6, PETG, 0.5 mm nozzle, 0.25 mm layers, 4 perimeters, 40 % gyroid, **no supports**.
Print as generated — orientation is a spec, not a slicer setting ([ADR 0005](decisions/0005-print-constraints-taz6.md)).

## 2. Hardware

`make -C cad report` prints the generated BOM. Per coupon pair:

| Qty | Item | Notes |
|---|---|---|
| 3 | **Ø10 × 30 stainless rod, 303** | Posts — see machining below |
| 1 | **Lock plate, 3 mm, 3 keyholes** | Steel or laser-cut; `coupon_lock_plate` |
| 3 | Ø10 lip seal / wiper | Socket mouths |
| 1 | TPU O-ring, Ø118 × 2 | Perimeter gasket, seats in the base groove |
| 8 | M5 × 20 bolts | Fixture and pull-test spreader |

### Machining the posts

Each Ø10 × 30 rod needs three operations:

1. **Turn one end** to Ø6 over 3.5 mm, at 30° from the axis. This is the capture taper.
2. **Cut a Ø7 groove, 3.4 mm wide**, centred 9 mm from the shoulder — the shoulder being
   where the post meets the plate, 12 mm from the *unturned* end. The lock plate seats in
   this groove and bears on its upper shoulder.
3. **Press 12 mm into the plate**, into a Ø9.90 bore. Leaves 18 mm proud.

**Stainless, grade 303.** The posts are exposed whenever a module is off, on a robot that
mops — mild steel would rust, and rust swells enough to bind a Ø10 post in a Ø10.2 socket.
Buy **303** specifically: it is the free-machining grade. 304, 316 and A2 are common as
dowel stock but work-harden under a file, and once the surface hardens nothing cuts it.

Use a different alloy for the lock plate — austenitic stainless galls against itself.

**A groove, not a cross-hole.** This is deliberate and it is the reason the part is
makeable by hand. A cross-hole through a round bar needs a V-block and a centre punch or
the drill walks off the crown; in hardened stock it wants carbide or EDM. A groove is one
lathe op — or a round file held against the rod while it spins in a drill press.

Both features can be cut that way: chuck the rod, spin it, apply a file. The taper is
capture and the groove is a shoulder; neither is a precision surface.

That also re-opens the **buy** route. Ground locating pins with tapered or bullet noses
are a catalogue item (Misumi, Carr Lane, Jergens and similar). Previously they were a dead
end because you still had to drill hardened steel; with a groove instead, adding one to a
bought pin — or specifying it — is straightforward.

Also needed: dial indicator (0.01 mm), spring gauge to 25 kg, feeler gauges, calipers,
fine dust (flour or dry cement), and water with a drop of detergent.

## 3. Reading the parts

### Module coupon (`coupon_module_face`)

A Ø130 disc with a central cone and three bores for the steel posts. **The posts are not
printed** — they are steel, pressed into those bores (ADR 0005: printed plastic is bulk
and rough alignment; anything that locates or takes load is steel). Each bore has a Ø18
boss behind the plate to give 12 mm of grip.

| What you see | Ø | Where | What it does |
|---|---|---|---|
| 4 holes near the rim | 5.5 | Ø120 circle | M5 fixture bolts |
| **3 bores with bosses behind** | 9.90 | **Ø100 circle at 0° / 120° / 235°** | press-fit steel posts |
| (posts, once fitted) | 10 → 6 | standing 18 mm proud | locate, retain, key |
| Groove in each post | 7.0 root × 3.4 wide | centred 9 mm up | the lock plate seats here |
| Big central cone | 40 → 30 | centre, 22 tall | lands first, kills lateral error |
| Recess in the cone tip | 22 × 10 | | contact pad PCB |
| Bore up the cone axis | 16 | | harness |

**Note the posts are not evenly spaced.** 0°, 120°, 235° — the 5° offset at the third
post is deliberate and is what forces one orientation.

### Base coupon (`coupon_base_face`)

A Ø130 × 31 block with the sockets opening upward.

| What you see | Ø | Where | What goes in it |
|---|---|---|---|
| 4 holes near the rim | 5.5 | Ø120 circle | M5 fixture bolts |
| **3 sockets** | 10.2 × 20 deep | **Ø100 circle at 0° / 240° / 125°** | the posts |
| Chamfer at each socket mouth | | | meets the post taper |
| Flat cavity across each socket | 3.4 mm tall | 8 mm down | the lock plate sweeps through |
| Angled hole from each socket floor | 4 | exits the **side wall** | drain |
| Central cone recess | 40.3 → 30.3 × 25 | centre | the connector cone |
| Annular groove on the face | Ø118 × 4 wide | | perimeter gasket |

**The socket angles are the mirror of the post angles** (0/240/125 against 0/120/235),
because the two faces meet. This is correct, not a typo.

## 4. Assembly

1. Press the three machined posts into the module coupon, tapered end out. **Check
   protrusion is 18.0 ± 0.1 mm on all three**, and that all three grooves sit at the same
   height — the lock plate is one rigid part and cannot accommodate a post that sits proud.
2. Fit the lip seals into the base socket mouths.
3. Seat the TPU O-ring in the base's perimeter groove.
4. Fit the lock plate in its cavity. Rotating it ~10° moves all three posts from open to
   locked at once. Leave it open for T1–T3.

## 5. Tests

Record everything in [`tests/phase1-results.md`](../tests/phase1-results.md). **Write
down failures** — a coupon that fails is more informative than one that passes.

### T1 — Mate reliability (answers Q1, Q4)
Fifty mates by hand, dropped in under their own weight, no guiding.

- **Pass:** 50/50 seat fully with the flange gap closed to 1.0 ± 0.15 mm all round.
- Any partial seat or rock is a failure, not a retry.

### T2 — Keying
Attempt to mate at 120° and 240°.

- **Pass:** both are physically impossible; the module sits visibly proud and cannot be
  pushed home.
- The checks predict 4.36 mm of misfit. Measure the actual standoff.

### T3 — Capture envelope (answers Q2)
Offset the module progressively and lower it hands-off. Find the largest lateral offset
and yaw angle that still seats.

- **Pass:** ≥ 3 mm lateral, ≥ 1° yaw. The cascade only asks for 0.3 mm and 0.5°, so this
  is a wide margin by design.
- If short, the cone taper is the thing to lengthen — not the posts.

### T4 — Static pull (answers Q5)
Pins home, M5 spreader on the fixture holes, load axially.

- **Pass:** holds **200 N** for 60 s, no permanent deformation, lock plate does not spread.
- Then load to failure and record the mode. The calculation says the PETG bearing yields
  long before the pin shears; confirm that, because it is the assumption every margin on
  this port rests on.

### T5 — Contamination (answers Q3)
The test v0.1 never had. Fifty mates with fine dust worked into the sockets and posts,
then fifty more with the joint wetted.

- **Pass:** still 50/50 seating; drains clear standing water within 30 s; no dust packed
  into a socket floor that a wipe cannot clear.
- Inspect the lip seals at 25 and 50 cycles.

### T6 — Cycle life
500 mates. Re-run T1 and T3 at 100, 250 and 500.

- **Pass:** T1 still 50/50 and T3 still within spec at cycle 500; socket bores not worn
  beyond 10.4 mm.

## 6. Exit criteria

Phase 1 is complete when **T1–T6 all pass on the same coupon pair**, results are
recorded, and any resulting parameter changes are:

1. made in `cad/lib/tidybot_port.py`,
2. validated with `make -C cad check`,
3. reflected in `INTERFACE.md` with `SPEC_VERSION` bumped,
4. re-verified by a fresh print.

Only then does `SPEC_VERSION` go to **1.0.0**, and only then does module design start.

## 7. Expect to iterate

Two to four coupon revisions is normal and is not a sign anything has gone wrong. That is
the whole reason this phase exists — to absorb the iteration in 3-hour prints rather than
in a chassis. Budget two to three weeks of evenings.

The base coupon is a 7-hour print. If you are iterating only the module side, reprint just
that one — the base geometry changes far less often.
