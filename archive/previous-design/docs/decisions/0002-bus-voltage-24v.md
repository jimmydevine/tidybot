# 0002. 24 V nominal DC bus

**Status:** Accepted
**Date:** 2026-08-22

## Context

A single DC bus crosses every port and feeds everything from a 5 V MCU to a vacuum
impeller. The voltage choice sets wire gauge, connector current rating, MOSFET
selection, and how much heat ends up inside a plastic robot.

## Decision

**24 V nominal**, from a 6S Li-ion pack (25.2 V full, 18.0 V empty). Modules buck their
own logic rails locally; the bus carries 24 V and ground only.

## Consequences

- Worst-case load (~232 W, see REQUIREMENTS.md) is **9.7 A at 24 V** versus **19.3 A at
  12 V**. That halving is the whole argument: 14 AWG and a 15 A fuse instead of 10 AWG
  and 20 A contacts, and roughly a quarter of the I²R loss in the port contacts — which
  matters because those contacts are small, and heat there is what kills them.
- Vacuum impellers are happier at 24 V; higher-voltage BLDC options are cheap and common.
- 6S is well supported by hobby BMS and charger hardware.
- Cost: every module needs its own buck converter (~$2 and a bit of board space). This
  is a deliberate trade — a local buck per module is cheaper than a second bus wire pair
  across every port, and it keeps switching noise local to the module that makes it.
- 18.0 V at empty is still comfortably above what a buck needs for a clean 5 V rail, so
  behaviour doesn't degrade near end-of-charge.

## Alternatives considered

- **12 V.** Rejected on current: doubles conductor and contact requirements for the same
  power, at the exact place (a small blind-mate connector) where that is most expensive.
- **48 V.** Rejected as overkill at this power level and needlessly close to voltages
  that complicate safety and component selection in a printed household device.
- **Dual bus (24 V power + 5 V logic across the port).** Partially adopted: a low-current
  +5 V aux pin exists, but only to boot a module's MCU for discovery *before* the main
  bus is enabled. It is not a general logic supply.
