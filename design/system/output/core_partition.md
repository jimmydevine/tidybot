# Revision F — core and floor-power partition

Dimensioned candidate, not a fabrication release. C/E inputs remain the comparison baseline. All figures are estimates; no component has been weighed or tested in this revision.

| Loaded configuration | Before | F candidate | Change |
|---|---:|---:|---:|
| vacuum + cap | 4676 g | 4763 g | +87 g |
| mop + cap | 4580 g | 4477 g | -103 g |
| low + cap | 4955 g | 5042 g | +87 g |
| vacuum + four-propeller lift | 7027 g | 7114 g | +87 g |
| mop + four-propeller lift | 6931 g | 6828 g | -103 g |
| low + four-propeller lift | 7306 g | 7393 g | +87 g |
| Airborne duster + four-propeller lift | 5249 g | 5003 g | -246 g |

Same battery cells, bin/water loads, cleaning hardware, sensors, guards and mission reserves in every comparison. The 140 g battery cartridge tare remains booked under core; cells are additional.

## What moves and what is added

- 190 g blower converter/cooling assembly moves to suction bottoms.
- 24 g drive converter and 40 g braking assembly move to driven bottoms.
- Core retains computing, all sensors, 5 V conversion, pack protection, battery receiver, frame and locks.
- Additional core interface allowance: 8 g. Fixed core falls from 1,439 to 1,193 g; including cartridge tare, 1,579 to 1,333 g.
- Each floor bottom adds 52.9 g of stock plus 10 g carrier fasteners and 16 g interface/wiring allowance: 78.9 g installed addition beyond relocated electronics.
- Existing 190 g converter installation and original harness/frame allowances are retained. No credit is taken for their potentially redundant supports. Mop currently shares the carrier footprint; trimming its unused left shelf is a later opportunity.

## Layout and exchange

The bottom-owned power shelf occupies the old front-left converter space. Its main outline is 115 × 70 × 1 mm aluminum with a 34 × 17 mm front-right notch and a small left mounting tab. The shelf is at z = 86 mm. A 2 mm lower foot plate at z = 12 mm and three 72 mm tube/rod posts support it; 2 × 8 mm edge strips stiffen the shelf. The full dimension list is in core_partition.json and the CAD reference.

Cut sheet/strip stock and drill holes; no machined block or bent-sheet tooling is assumed. This pass specifies stock envelopes and mass, not drilling templates: plate joints, anti-rotation, insulation, tolerances and attachment of the lower plate to the shared bottom frame still need design and load checks. The narrow post spacing requires lateral-stiffness validation. Hole removal is not credited in stock mass.

Core 5 V board moves to [11, 93, 126] mm above the left MCU. Reserve a 34 × 47 × 14 mm bay and a local cap roof above z = 138 mm. Overall LiDAR height remains below 180 mm. Braking capacitor/control move behind y = 30 mm; the core camera occupies y ≤ 28 mm. The shelf notch preserves that upward removal path.

Automatic checks cover static functional allocations and the upward core sweep against the new bottom power hardware. They do not validate complete station handling, connector float, cables, fastener heads, contoured shells or moving suspension/tool mechanisms.

## Electrical interface

F_RAW6S supplies switched raw 18–25.2 V and protected 5 V logic to the bottom. At the 240 W raw-branch allocation, worst-case modeled current is 13.33 A. Reserve contacts capable of 20 A continuously after thermal derating. This is a contact requirement, not a selected connector or fuse setting. The lift power trunk remains separate.

The preceding keyed 12/24/5 V interface is incompatible. Give F_RAW6S a different physical key and ID; a software label alone does not prevent misconnection. Core protection/precharge remains upstream; local converters start disabled and run only after seating, all four bottom locks, identity, voltage, temperature and watchdog checks. Keep locks engaged during braking, disable converters, isolate and discharge the raw branch, then separate. Maintain core logic from dock power during exchange. The airborne duster uses the protected 5 V branch and keeps raw tool power disabled. The 18 V calculation boundary is not a recommended battery discharge cutoff.

The 12 V regenerative clamp stays downstream of the drive buck; it does not rely on the buck returning braking energy to the battery. Converter enable polarity, capacitance/precharge, branch protection, CAN grounding, connector cycle life and fault responses remain implementation work.

Moving converters gives no modeled efficiency benefit. Floor load/efficiency assumptions remain unchanged for comparison. Cincon specifies 87.5% full-load efficiency for CHB100W-24S24; the inherited model uses 90% for the 24 V rail, so actual duty efficiency and cooling still require verification. [Cincon datasheet](https://www.cincon.com/productdownload/Datasheet-CHB100W.pdf). The 12 V converter current capability depends on input voltage and cooling; headline current is not a guarantee across this 6S range. [Pololu D42V110F12](https://www.pololu.com/product/5677).

## Flight consequence

| Four-propeller airborne duster | Before | F candidate |
|---|---:|---:|
| Nominal mass | 5249 g | 5003 g |
| Modeled hover electrical power | 1734 W | 1626 W |
| Static thrust/weight, limiting rotor | 1.966:1 | 2.002:1 |
| local_dusting: cleaning energy ceiling | 74 s | 84 s |
| longer_dusting: cleaning energy ceiling | 20 s | 29 s |

Removing front power hardware moves the center of mass rearward; the flight calculation includes that unequal rotor loading. The nominal 2.002:1 result only just crosses the 2:1 arithmetic screen; the difference is far smaller than the design uncertainty and does not establish an adequate flight margin. These are energy/static screens using the same source thrust curve and guard assumptions, not achieved endurance or qualified flight. Upper mass bounds, contact dynamics and installed continuous thrust remain unresolved. Vacuum/sofa transfer loads retain their converters and increase with support hardware; the mop omits blower conversion and becomes lighter.

## Next design work

Resolve the shared bottom/core frame load paths and joints next. That will determine whether the extra shelf supports can be integrated into material already budgeted, and whether the common 305 g printed/metal core structure can be reduced. Preserve the current mass additions until actual replacement geometry supports a deduction. No new purchase or print is needed for this allocation review.

[Design context](../../../docs/CORE_POWER_PARTITION.md) · [Interactive views](core_partition.html) · [FreeCAD](core_partition.FCStd) · [STEP](core_partition.step)
