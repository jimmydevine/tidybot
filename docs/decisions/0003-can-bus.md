# 0003. CAN for the inter-module bus

**Status:** Accepted
**Date:** 2026-08-22

## Context

Modules must be discoverable, hot-pluggable, and able to talk to the base over a small
number of contacts, in an electrically noisy enclosure containing brushed and brushless
motors and a vacuum impeller.

## Decision

**CAN 2.0B at 500 kbit/s**, two contacts (CAN H / CAN L), linear topology with 120 Ω
termination at each end and ≤ 100 mm stubs.

Strongly prefer **Cyphal/CAN** (formerly UAVCAN) over a bespoke protocol.

## Consequences

- Differential signalling survives being run past motors. This is the deciding property.
- Multi-drop on two wires: adding a third or fourth port later costs no extra contacts.
- Hot-plug tolerant — a node joining or leaving a live bus is a normal, designed-for event.
- Transceivers are ~$1; every candidate MCU (STM32, ESP32, RP2040 + MCP2515) supports it.
- Cost: needs a real bus topology. Star wiring or long stubs will produce reflections and
  intermittent faults that are miserable to debug. This constrains internal wire routing
  and must be respected in the base's harness design.
- **Choose Cyphal vs. bespoke before writing Phase 3 firmware.** Cyphal brings node
  discovery, heartbeats and typed pub/sub already designed for exactly this problem.
  Cheap to adopt now; expensive to retrofit once several modules have shipped firmware.

## Alternatives considered

- **I²C.** Rejected: address collisions across independently-designed modules, no noise
  immunity, no hot-plug story, and short usable cable length. It would work on the bench
  and fail in the robot.
- **RS-485 / Modbus.** Workable, but no built-in arbitration or message identity, so a
  discovery and addressing layer would have to be invented anyway.
- **USB.** Rejected: host/device topology fits badly, and hubs plus hot-plug plus motor
  noise is a poor combination.
- **Ethernet.** Rejected: contact count, connector size, cost and power per module are
  all wrong at this scale.
