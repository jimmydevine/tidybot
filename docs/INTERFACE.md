# TidyBot Port Specification — "TB-Port"

**Spec version: 0.1.0 (DRAFT — not yet bench-validated)**

This is the single most important document in the project. Every module ever built
must satisfy it. Change it deliberately, bump the version, and regenerate all CAD.

Machine-readable source of truth for dimensions: `cad/lib/tidybot_port.py` (`PORT` dict).
This document explains *why*; the Python file is *what*. If they disagree, the Python
file wins and this document is stale — fix it.

---

## 0. Terminology

| Term | Meaning |
|---|---|
| **Male half** | The half with the protruding boss. Lives on **modules**. |
| **Female half** | The half with the bore. Lives on the **base** (and on the docking station rack). |
| **Mate axis** | +Z. Modules always approach along the base's Z axis. |
| **Seated** | Kinematic balls in their vees, latch engaged, contacts made. |
| **Descriptor** | The CAN message a module sends on attach describing itself. |

Convention: the base carries female halves (top and bottom). Modules carry male halves.
A pass-through module (e.g. a drive sled) has a male half up and a female half down.

---

## 1. Mechanical

### 1.1 Design intent

Three jobs are handled by three separate features. Do not let them blur together:

1. **Capture** — a conical funnel absorbs gross misalignment from the docking approach.
2. **Location** — a 3-ball / 3-vee kinematic coupling exactly constrains all 6 DOF.
3. **Retention** — a ball-detent latch holds the halves together along Z.

Precision comes from **steel hardware**, never from printed plastic surfaces
(see [ADR 0005](decisions/0005-print-constraints-taz6.md)). Printed plastic is bulk
and alignment only.

### 1.2 Capture envelope

| Parameter | Value | Notes |
|---|---|---|
| Lateral capture | **±8.0 mm** | At the funnel mouth |
| Angular capture | **±5°** | Tilt about X or Y |
| Funnel half-angle | 35° from axis | Shallow enough to self-centre, steep enough to stay short |
| Funnel mouth Ø | 66.4 mm | = bore Ø + 2 × lateral capture |

The docking station adds its own coarse funnel for the base as a whole. Total system
capture = station funnel + port funnel; the port does **not** have to absorb raw
navigation error on its own. Phase 4 measures the actual docking repeatability
distribution, and that measurement is what validates or resizes this number.

### 1.3 Kinematic coupling (location)

Classic Maxwell coupling: three Ø8 mm steel balls on the male flange, each seating
into a radial vee on the female flange. Each vee is formed by **two Ø3 mm steel dowel
pins** lying across a printed pocket — steel-on-steel line contact from cheap hardware,
which is the whole trick for getting precision off a 0.5 mm nozzle.

| Parameter | Value |
|---|---|
| Ball Ø | 8.0 mm (chrome steel bearing balls) |
| Ball bolt circle | Ø70.0 mm, at 90° / 210° / 330° |
| Ball protrusion above male flange | 3.0 mm |
| Ball retention | Ø8.2 × 5.0 mm flat-bottom bore, epoxy |
| Vee dowel Ø | 3.0 mm |
| Vee dowel spacing | 7.0 mm (tangential) |
| Nominal flange gap when seated | 1.0 mm |

The 1.0 mm flange gap is deliberate: **the balls carry the load, not the plastic faces.**
If the flanges touch, the coupling is over-constrained and repeatability is gone.

Ball / dowel geometry is derived trigonometrically in `tidybot_port.py` — change the ball
or dowel size and the pocket depths recompute themselves.

### 1.4 Retention (latch)

A ball-detent latch, mechanically equivalent to a scaled-up pneumatic quick-coupler.

- Male boss carries a circumferential groove (Ø46 root, semicircular, 2.0 mm deep)
  16 mm up from the flange face.
- Female bore carries 3 × Ø6 mm steel balls in radial through-holes at 120°.
- A collar around the female bore backs the balls inward. Collar retracted → balls free
  → module releases.

**The latch is fail-secure.** Springs hold it engaged; energy is required to *release*.
A power loss or firmware crash must never drop a module.

**The release actuator lives on the base, never on modules.** The base has two ports, so
you pay for two actuators once. Modules stay 100 % passive — no motors, no latch
electronics, no reason a module can't cost $30. This is the decision that determines
whether you end up with six modules or two. See [ADR 0001](decisions/0001-locomotion-in-base.md)
for the same reasoning applied to drivetrains.

v0.1 bench coupons ship with a plain slip-on collar (hand-operated). Powered collar
actuation is v0.2, after the coupling itself is validated.

### 1.5 Keying

The 3-fold symmetry of the coupling means a module could seat in any of three
orientations. A single Ø5 mm dowel pin on the boss end face at a known clock angle,
with a clearance-fit hole opposite, forces one orientation. It is a *key*, not a
locating feature — it must stay clearance-fit so it never fights the kinematic coupling.

### 1.6 Load rating (target, to be verified in Phase 1)

| Load | Target |
|---|---|
| Static axial (tension) | 8 kg |
| Moment about X/Y | 4 N·m |
| Play at flange rim, seated | < 0.3 mm |
| Mate/demate cycles before re-qualification | 500 |

---

## 2. Electrical

### 2.1 Power

**24 V nominal DC bus** (6S Li-ion: 25.2 V full, 18.0 V empty). See [ADR 0002](decisions/0002-bus-voltage-24v.md).

- Each module bucks its own logic rails locally. The bus carries 24 V and ground only.
- Per-port budget: **150 W continuous, 250 W peak (2 s)**. Enforced by the base with
  a current-sense shunt per port; a module exceeding its declared draw gets shed.
- Modules must declare peak draw in their descriptor. The base refuses to enable the
  bus for a module whose declared draw exceeds the remaining budget.
- Inrush: modules > 20 W must soft-start. An unlimited bulk-cap inrush will brown out
  the base's compute.

### 2.2 Contacts

Pogo pins on the **female** (base) half; flat gold pads on the **male** (module) half.
Pogos wear fastest, and there is exactly one base to service versus N modules.

Contacts sit on the **boss end face**, recessed inside the bore — protected from
debris, and they only engage in the last few mm of travel, after mechanical alignment
is already established.

| Pin | Function | Notes |
|---|---|---|
| 1, 2 | GND | Doubled for current |
| 3, 4 | +24 V bus | Doubled; switched by the base, off by default |
| 5 | +5 V aux | Always-on, ≤ 500 mA. Powers the module's MCU for discovery *before* the main bus is enabled. |
| 6 | CAN H | |
| 7 | CAN L | |
| 8 | PRESENCE | Pulled low by a link in the module. Continuously monitored. |

PRESENCE is a hard interlock, not a convenience: losing it mid-drive means a module is
detaching and the base must stop immediately.

The +5 V aux rail is what makes safe hot-plug work — the module boots, identifies
itself, and declares its power needs *before* anything switches 24 V into it.

### 2.3 Discovery sequence

1. Mechanical seat → PRESENCE goes low.
2. Base enables +5 V aux.
3. Module MCU boots, joins the CAN bus, publishes its **descriptor**.
4. Base validates the descriptor against the remaining power budget.
5. Base enables the 24 V bus for that port.
6. Base updates its kinematic/mass model and spins up the matching software stack.

---

## 3. Data

**CAN 2.0B, 500 kbit/s.** See [ADR 0003](decisions/0003-can-bus.md).

Strongly consider **Cyphal/CAN** (formerly UAVCAN) rather than a bespoke protocol — it
was designed for exactly this problem (node discovery, heartbeats, typed pub/sub,
hot-plug on a shared bus) and comes with tooling. Decide before writing firmware; this
is cheap to choose now and expensive to change in Phase 3.

Bus topology: linear, base at one end, 120 Ω termination at the base and at the
electrically-farthest port. Stub length from a port to the trunk ≤ 100 mm.

### 3.1 Module descriptor

Every module publishes this on attach. It is what turns "swappable parts" into a robot
that actually reconfigures itself:

| Field | Type | Why it matters |
|---|---|---|
| `module_type` | enum | Selects the software stack to launch |
| `hw_revision` | u8 | |
| `fw_version` | semver | |
| `port_spec_version` | semver | Base refuses incompatible majors |
| `serial` | u64 | Per-unit calibration lookup |
| `mass_g` | u32 | Feeds the drive controller and tip-over limits |
| `com_xyz_mm` | i16[3] | Relative to the port origin |
| `power_peak_w` | u16 | Validated against the remaining budget |
| `power_idle_w` | u16 | Runtime estimation |
| `capabilities` | bitfield | What the module can be asked to do |

`mass_g` and `com_xyz_mm` are not bookkeeping. They are how the base retunes itself
when you hang 1.5 kg of vacuum off the bottom port.

---

## 4. Compatibility policy

Semantic versioning on `port_spec_version`:

- **Patch** — tolerance or documentation changes. No re-print.
- **Minor** — additive, backwards compatible. Old modules still mate and function.
- **Major** — mechanical or pinout break. Old modules will not mate. Avoid at nearly
  any cost; if you take one, retrofit or retire every existing module in the same change.

The base logs the spec version of every module it sees and refuses a mismatched major.

---

## 5. Open questions for Phase 1

These are the things the bench coupon exists to answer. Do not design a real module
until they are closed:

1. Does the 1.0 mm flange gap survive real loads, or does it need a preload spring?
2. Is 8 mm lateral capture achievable with a 35° funnel, or does the funnel need to be
   shallower (and therefore longer)?
3. Does the detent groove at 2.0 mm depth hold 8 kg, or does it cam out?
4. What is the actual repeatability across 50 mate cycles?
5. Does the Ø8.2 epoxy ball socket survive 500 cycles in PETG, or does it need a
   metal insert?
