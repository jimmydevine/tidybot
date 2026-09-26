# 0004. Two ports (top and bottom); sensors use an accessory rail

**Status:** Accepted
**Date:** 2026-08-22

## Context

How many TB-Ports does the base carry, and where? Front/side/rear ports were considered,
with additional sensors as the motivating use case.

## Decision

**Two ports: one top, one bottom.** Both are the female half, sharing the identical spec.

Sensors do **not** get a port. The base perimeter carries a non-structural **accessory
rail**: an M3 mounting grid plus a small connector stub providing +5 V, CAN H, CAN L
and ground.

## Consequences

- Bottom port: floor tools (vacuum, mop, sweeper) and, if the pass-through sled route in
  [ADR 0001](0001-locomotion-in-base.md) is taken, drive sleds.
- Top port: cargo tray, dusting arm, camera mast, battery extender, drone pad.
- Two ports means two latch actuators total, forever — the cost of the actuator-in-base
  rule stays bounded no matter how many modules exist.
- Sensors keep the thing that actually matters (power and CAN, so they still enumerate on
  the bus) without paying for a kinematic coupling, a fail-secure latch, an actuator, and
  an 8 kg load path they will never use. An automated swap interface is the wrong tool
  for something that gets bolted on once and left there.
- Cost: a sensor on the accessory rail cannot be swapped by the docking station. Accepted
  — nothing in the roadmap wants that.
- Adding a third TB-Port later is a **minor** spec change (additive, no mechanical break),
  so this is a cheap decision to revisit if a real need appears.

## Alternatives considered

- **Four ports (top, bottom, front, rear).** Rejected: doubles the actuator count and the
  structural complexity of the base to serve a use case (sensors) that doesn't need any
  of a port's expensive properties.
- **A smaller "port lite" spec for sensors.** Rejected: a second mechanical standard to
  maintain, version and keep compatible, when a bolt pattern and a connector do the job.
