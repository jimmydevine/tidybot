# TidyBot — Requirements & Budgets

**Status: v0.1 draft.** Numbers marked *(estimate)* are starting points to be replaced
with measurements. Numbers marked *(constraint)* come from physics or hardware and are
not negotiable without changing the hardware.

---

## 1. What TidyBot is

A modular household robot: one mobile base carrying compute, sensing, power and drive,
plus interchangeable tool modules that attach above and below it. A docking station
charges the base and swaps its modules unattended.

## 2. What TidyBot is not (v1)

Scope discipline — these are explicitly out, so they can't quietly creep in:

- Not a manipulator platform. No arm in v1.
- Not multi-floor autonomous. Stairs are Phase 6 research.
- Not outdoor-rated.
- Not a security/telepresence device. Cameras only if a module needs them.

---

## 3. Mass budget *(estimate)*

Mass matters more than it looks: it sets motor torque, battery size, floor protection,
and whether a person can pick the thing up one-handed.

| Item | Target | Notes |
|---|---|---|
| Base structure (printed) | 900 g | Frame + panels |
| Battery (6S ~6 Ah Li-ion) | 900 g | 18650 or 21700 pack |
| Drive (2 × motor, gearbox, wheels, caster) | 700 g | |
| Compute + LiDAR + IMU + PDB | 500 g | |
| Fasteners, wiring, ports | 400 g | Always underestimated |
| **Base total** | **3.4 kg** | |
| Typical tool module | 0.5–1.5 kg | |
| **System, loaded** | **≤ 5.5 kg** | Above this, drive and floor protection get expensive |

## 4. Power budget *(estimate)*

| Load | Continuous | Peak |
|---|---|---|
| Compute (SBC + LiDAR) | 12 W | 20 W |
| Drive | 25 W | 90 W (stall-limited) |
| Base overhead | 5 W | 8 W |
| Bottom port allowance | 150 W | 250 W |
| Top port allowance | 40 W | 80 W |
| **Worst case** | **232 W** | **448 W** |

At 24 V that worst case is 9.7 A continuous — comfortable for 14 AWG and a 15 A fuse.
The same load at 12 V would be 19.3 A, which is a materially more expensive robot.
That comparison is the entire argument in [ADR 0002](decisions/0002-bus-voltage-24v.md).

**Runtime target:** 60 min vacuuming, 90 min light duty. 6S 6 Ah ≈ 130 Wh; at ~180 W
average vacuuming that is ~43 min, so **either the pack grows to ~9 Ah or the runtime
target comes down.** Flagging this now rather than discovering it in Phase 3.

## 5. Physical envelope *(constraint — TAZ 6)*

Build volume 280 × 280 × 250 mm, 0.5 mm nozzle. See [ADR 0005](decisions/0005-print-constraints-taz6.md).

| Parameter | Value |
|---|---|
| Base diameter | ≤ 250 mm (single-piece printable) |
| Base height, no modules | ≤ 120 mm |
| Max single printed part | 250 × 250 × 230 mm |
| Min reliable wall | 1.5 mm (3 × 0.5 mm) |
| Min reliable feature | 2.0 mm |
| Default material | PETG |

250 mm is narrower than a typical robot vacuum (320–350 mm), which costs some
coverage per pass. Accepted: single-piece printability is worth more than a wider
sweep, and a wider *tool* can still overhang the base.

## 6. Performance targets

| Metric | Target | Verified in |
|---|---|---|
| Port mate success, hand | 50/50 | Phase 1 |
| Port repeatability | < 0.1 mm | Phase 1 |
| Port play under load | < 0.3 mm | Phase 1 |
| Navigation position error | < 50 mm | Phase 2 |
| Autonomous dock success | 50/50 | Phase 4 |
| Dock repeatability | to be measured | Phase 4 |
| Unattended swap success | 20/20, zero drops | Phase 5 |

Phase 4's dock repeatability has no target on purpose. It is a **measurement that feeds
the Phase 5 design**, and picking a number now would just be a guess that later
constrains the swapper for no reason.

## 7. Safety requirements *(constraint)*

1. Latch is fail-secure. Loss of power must not release a module.
2. PRESENCE loss while moving → immediate stop.
3. A module drawing more than its declared power gets shed within 100 ms.
4. Battery: per-cell monitoring, fused main bus, charge only while docked.
5. No pinch points reachable during a swap while the robot is powered.
6. The station must fail safe with a module half-swapped — hold it, don't drop it.

## 8. Software stack

- ROS 2 (current LTS) on the base SBC.
- Nav2 for navigation, slam_toolbox for mapping.
- Per-module MCU firmware on CAN.
- A hot-plug manager that maps descriptors → ROS 2 lifecycle nodes.
- MQTT / Home Assistant discovery from Phase 2, not bolted on later.

## 9. Cost targets *(estimate)*

| Item | Target |
|---|---|
| Base, all-in | $350 |
| Tool module | $40–80 |
| Docking station | $200 |

Module cost is a **design driver, not an outcome.** It is the direct consequence of
keeping modules passive — no drive, no latch actuator, no battery. If a module design
creeps past ~$100, something belonging in the base has leaked into it.
