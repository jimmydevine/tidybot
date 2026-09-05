# TidyBot Port Specification — "TB-Port"

**Spec version: 0.2.0 (DRAFT — not yet bench-validated)**

The single most important document in the project. Every module ever built must satisfy
it. Change it deliberately, bump the version, and regenerate all CAD.

Machine-readable source of truth: [`cad/lib/tidybot_port.py`](../cad/lib/tidybot_port.py)
(`PORT` and `LOAD`). This document explains *why*; the Python file is *what*. If they
disagree, the Python file wins and this document is stale — fix it.

Architecture rationale: [ADR 0006](decisions/0006-tri-post-coupling.md).
Structural context: [ADR 0007](decisions/0007-coaxial-ports-tension-path.md).

Supersedes 0.1.0 (boss-and-bore), retained at commit `2c18923`.

---

## 0. Notation

| Symbol | Means |
|---|---|
| `Ø` | diameter, in millimetres — **not** degrees |
| `°` | degrees of angle |

So "3 × Ø10 posts on a Ø100 circle at 0° / 120° / 235°" is three ten-millimetre posts,
arranged on a hundred-millimetre circle, at those three clock positions.

Convention: the **base** (middle section) carries sockets on both faces. **Modules**
carry posts. Every port is identical — one spec, both ports, any module either way up.

---

## 1. The four jobs

The port must **capture** a module arriving misaligned, **locate** it repeatably,
**retain** it against flight loads, and **connect** power and data. Each job is done by
one feature, and no feature does two:

| Job | Feature | Where |
|---|---|---|
| Capture, lateral | connector cone | centre, r = 0 |
| Capture, yaw | post tapers | r = 50 |
| Locate | posts in sockets | r = 50 |
| Retain | groove + lock plate, double shear | r = 50 |
| Connect | central connector | centre |
| Key | post asymmetry | r = 50 |

---

## 2. Mechanical

### 2.1 Posts — three, identical, unequally spaced

| Parameter | Value |
|---|---|
| Count | 3 |
| Angles | **0° / 120° / 235°** |
| Bolt circle | Ø100 (r = 50) |
| Post Ø | 10.0, tapering to 6.0 |
| Taper | 30° from axis, 3.46 mm long → 2.0 mm capture |
| Protrusion | 18.0 |
| Embedded | 12.0, pressed into a Ø9.90 bore |
| Stock | **Ø10 × 30 stainless rod, grade 303** |
| Socket | Ø10.2 × 20.0 deep |

**Steel, not printed.** The posts are steel rod pressed into the plate, never printed
features. The locking pin bears *inside* the post's cross-hole; in printed PETG that hole
crushes and every margin quoted here becomes fiction. Mild steel rather than hardened
dowel — the cross-hole has to be drilled, and a 123× shear margin makes hardness pointless.

**Three, not four.** A rigid body has six degrees of freedom and each post in a socket
removes two. Three is exactly determinate; four is over-constrained by two, and in
printed plastic one post lands first while the rest fight it — the joint rocks or jams.

**Identical, not graduated.** Sizing them Ø10/Ø8/Ø6 would also key the joint, but the
smallest post would set the rating and you would make, stock, ream, seal and replace
three parts instead of one.

**235°, not 240°.** That 5° asymmetry is the keying feature — see §5.

**The taper is the funnel.** Because it rides on the post rather than sitting in the
base, capture costs **zero receptacle depth**. This is the only geometry considered where
that is true.

### 2.2 Socket angles are the mirror

The two faces meet each other, so they are mirror images: a module post at angle *a*
finds a base socket at *−a*. Sockets therefore sit at **0° / 240° / 125°**.

With the old symmetric layout this was invisible, because the set mirrors onto itself.
The asymmetric layout makes it real, and getting it backwards means nothing mates at all.
`derived()` computes `SOCKET_ANGLES`; never hand-enter them.

### 2.3 Retention — groove and one rotating lock plate

Each post carries a circumferential groove. A single plate inside the base carries a
**keyhole per post**: the wide mouth passes the post, then about 10° of rotation slides
the narrow throat into the groove, locking all three at once.

| | |
|---|---|
| Groove | Ø7.0 root, 3.4 mm wide, 1.50 mm deep |
| Keyhole | Ø10.4 mouth → Ø7.2 throat |
| Lock motion | 8.8 mm tangential = **10.1°** of plate rotation |
| Shoulder engagement | 1.40 mm radial |
| Lock plate bearing | 3.38 MPa (**74×** in mild steel) |
| Post net section | 1.66 MPa (**150×**) |
| Material below the slot | 6.30 mm |

**Why a groove and not a cross-hole.** Both give double shear and both are strong enough
many times over. But a cross-hole through a round bar needs a V-block and a centre punch
or the drill wanders, and in hardened stock it needs carbide or EDM — which ruled out
buying ready-made ground locating pins, the one off-the-shelf route that solves the taper.
A groove is a single lathe op, or a round file against the rod spun in a drill press.

**One plate replaces three pins and the cam plate that would have driven them.** It lives
entirely inside the sealed base, so nothing that moves ever sees the room.

### 2.3b Materials — stainless, and which grade

The posts sit **exposed whenever a module is off**, on a machine that mops. Mild steel
would rust, and rust here is not cosmetic: it **swells**, and a rusted Ø10 post binds in a
Ø10.2 socket. It also sheds abrasive particles into a joint that mates 500 times, and
stains whatever the module touches.

| Grade | Yield | Lock plate margin | Post margin | Notes |
|---|---|---|---|---|
| 303 stainless | 240 MPa | 71× | 145× | **Free-machining. Buy this.** |
| 304 / 316 / A2 | 205 MPa | 61× | 123× | Common dowel stock; work-hardens |

Margins are quoted at the conservative 205 MPa so they hold whichever grade turns up.

**Buy 303 if you are cutting the taper and groove yourself.** It is the free-machining
grade, with sulphur added. 304, 316 and the A2/A4 fastener grades are gummy and
work-harden — dwell with a file and the surface hardens under you, after which nothing
cuts.

**Make the lock plate a different alloy from the posts.** Austenitic stainless galls
badly against itself under load. The risk here is modest, because the plate rotates while
the joint is *unloaded* — you lock, then fly — and galling needs sliding under load. But
flight vibration is micro-motion at full load, and a different alloy is free insurance.

### 2.4 Connector cone — the primary alignment feature

| Parameter | Value |
|---|---|
| Ø | 40 → 30 |
| Length | 22.0 (leads the posts by 4.0 mm) |
| Capture | 5.0 mm lateral |

The cone lands **before** any post enters. It sits at r = 0, where yaw cannot displace
it, so it kills lateral error while being blind to rotation. The posts then have only
yaw left to absorb.

That decomposition is the whole design. Asking the posts to do both needs 14.2 mm of
capture against a 2.0 mm taper — it fails. Split the job and they need 0.74 mm.

### 2.5 Load rating

| Load | Value | From |
|---|---|---|
| Axial, top port | **192 N** | 3-stack flight, ADR 0007 |
| Axial, bottom port | 59 N | |
| Moment | 4.0 N·m | |
| Flange gap when seated | 1.0 mm | steel carries the load, never the plastic |

---

## 3. Electrical

**All eight contacts live in the central connector**, inside the cone, behind the
perimeter gasket. The posts carry load only.

Two reasons. A pin bears on its post to transmit load, so they are a single node — the
posts cannot furnish eight circuits. And this robot mops: energised posts, exposed
whenever a module is off, are a bridged supply waiting for a puddle.

Keeping the signals central also keeps **CAN H and CAN L a genuine twisted pair**. On
posts 160 mm apart they would be a loop antenna beside three motors — exactly what
[ADR 0003](decisions/0003-can-bus.md) chose CAN to avoid.

### 3.1 Bonding — the posts are grounded, not floating

The posts carry no signal, but they are still metal bridging the base to every module, and
**floating metal on a machine that generates static is a bad default.** A vacuum builds
serious charge; a floating assembly will accumulate it and dump it into the connector at
the worst possible moment.

Bond the posts to chassis ground on **both** sides. That turns a hazard into a feature:
the posts engage several millimetres before the contacts close, so they become a
**first-mate / last-break ground** that bleeds charge before any signal pin touches — the
same trick as the long ground pins in a D-sub.

Keep the galvanic couple inside the stainless family. 303 against 304 is a negligible
driving voltage; aluminium or plated steel in the wet zone is not.

**Do not use post continuity as a seating sense**, tempting as it is. A water bridge
across two posts would read as "seated" — a false positive on a flight-critical interlock,
in exactly the conditions the robot works in. Sense the lock plate's position instead, and
PRESENCE through the connector.

### 3.2 Contacts

The pogo pins span a **3.60 mm gap** at full seat, well inside a 6 mm block with 4 mm of
stroke. This is a spec, not an assumption — `derived()` refuses a geometry where the
contacts could never close, or where the pad would crash into the block before the posts
seat.

| Pin | Function |
|---|---|
| 1, 2 | GND |
| 3, 4 | +24 V, switched, off by default |
| 5 | +5 V aux, always on, ≤ 500 mA |
| 6, 7 | CAN H / CAN L |
| 8 | PRESENCE (hard interlock) |

Pogo pins on the base side, gold pads on the module side. Discovery sequence and the
module descriptor are unchanged from 0.1.0 — see §3.1 of the git history for that text,
reproduced below.

### 3.3 Discovery

1. Mechanical seat → PRESENCE low.
2. Base enables +5 V aux.
3. Module MCU boots, joins CAN, publishes its **descriptor**: type, hw/fw revision,
   `port_spec_version`, serial, `mass_g`, `com_xyz_mm`, `power_peak_w`, capabilities.
4. Base validates against the remaining power budget.
5. Base enables 24 V for that port.
6. Base updates its mass model and launches the module's software stack.

`mass_g` and `com_xyz_mm` are not bookkeeping — they are how the base retunes itself
when 1.5 kg of vacuum hangs off the bottom port, and how the rotor unit knows what it is
lifting.

---

## 4. Contamination

This robot vacuums and mops. Five rules, all applied:

1. **The mechanism never leaves the base.** Pins, cam plate and motor are sealed inside.
   What is exposed is solid steel posts and drained holes — nothing that can foul.
2. **Every socket drains out the side wall.** Never into the electronics.
3. **Lip seal at each socket mouth.** The post wipes itself clean on entry.
4. **Perimeter gasket** on the base half — one gasket, replaceable, rather than one per
   module.
5. **Contacts sealed** inside the gasketed cone.

---

## 5. Keying

Three posts at 120° would mate three ways. Moving one to **235°** makes the wrong
orientations miss by **4.36 mm** against 0.20 mm of clearance — a wall, not a tight fit.

The cost is a load centroid 1.45 mm off axis, worth 0.28 N·m of imbalance against a 20×
bearing margin. Negligible.

Orientation matters even though the posts carry no current: the connector's eight
contacts must land on their opposite numbers, and modules have a front — a vacuum's brush
roll faces the direction of travel.

Because the misfit is *angular*, it grows with radius, so a misaligned module cannot even
begin to enter. It sits proud and detectable rather than jamming halfway.

---

## 6. Alignment cascade

No single feature is heroic. Each stage handles only what the previous one left:

| Stage | Mechanism | Residual |
|---|---|---|
| 0 | navigation | 10 mm / 3° |
| 1 | dock vee rails guide the whole robot | 2 mm / 1° |
| 2 | compliant module cradle in the dock | 1 mm / 0.5° |
| 3 | connector cone | 0.3 mm |
| 4 | post tapers | 0.1 mm |

**Two of the five stages live in the docking station**, which puts the dock on the
critical path rather than in Phase 4.

Do not stagger the post lengths to make them engage in sequence. It moves the centre of
rotation onto the first post, so the second sees r·√3·θ instead of r·θ — 73% worse. The
first feature to engage must be the central one.

---

## 7. Compatibility

Semantic versioning on `port_spec_version`. **Patch:** tolerances and documentation.
**Minor:** additive, backwards compatible. **Major:** mechanical or pinout break — old
modules will not mate; retrofit or retire every one in the same change.

The base logs each module's spec version and refuses a mismatched major.

---

## 8. Open questions for Phase 1

1. Does 0.10 mm of radial socket clearance survive 500 cycles with dust present, or does
   it wear open?
2. Is 2.0 mm of post capture enough once the cone has done its job, or does the cascade's
   stage-3 residual exceed 0.3 mm in practice?
3. Do the lip seals survive 500 wipes, and do the drains actually clear standing water?
4. Does the cone bottom out on debris before the posts seat?
5. What is the real pull-out load of a Ø5 pin bearing on printed PETG, against the
   calculated 20× margin?
