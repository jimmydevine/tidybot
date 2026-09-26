# Automatic battery cartridges and station charging

**S follow-up:** [shared core supports and fixed receiver](CORE_SUPPORT.md) adds
material geometry, two retracting tongue references and a downward-clearance
check. It retains the entire 140 g cartridge tare and 753 g cell reference.
Cartridge shoulders, positive latch pawls, electrical contacts and tolerance
qualification remain incomplete; the exchange requirements below still apply.

Revision B, 2026-09-13. The owner requires automatic battery exchange, with
multiple packs kept charged at the stations. This is now part of the system
architecture. Battery voltage, capacity and cell selection remain open.
This is a mechanism and electrical design allocation, not a fabrication release.

The [revision E airborne duster](AIRBORNE_DUSTING.md) uses the same cartridge and
supported-core exchange. Its station first captures the wheel-less robot on a
landing shuttle and removes the boom as needed; the prior cabinet/battery CAD
does not yet implement that added launch/landing and tool-handling path.

The [resident sofa attachment](SOFA_ATTACHMENT.md) adds one extension nest,
one vacant normal-head nest and a supported external head-exchange apron at
each floor station. Park the extension and restore the normal head before
flight or entering a bay sized for the ordinary robot. The 615 mm stowed
combination and the new head shuttle are not accommodated by the earlier
cabinet CAD; station access and support paths need integration. Neither
resident extension travels between floors.

## Configuration and inventory

The robot carries one removable battery cartridge in the middle electronics
core. Every bottom and top uses that same interface. Each floor station initially
has **two spare cartridges and four rack bays**: two resident packs, a vacancy to
receive the returning pack, and a recovery vacancy. Across two floors that is
**five packs total**, including the one on the robot. These are planning quantities,
not an order or a guarantee of uninterrupted cleaning.

Extra rack bays are useful even with only two resident packs. The station can
deposit the depleted cartridge before collecting a replacement and retain a
failed cartridge without immediately blocking every exchange. A fault still
reduces available stock and may stop a mission. An ordinary spare bay is not a
qualified thermal containment compartment.

The controller targets both resident spares READY while the station is enabled.
READY means charging has terminated and cell voltage/balance, temperature,
identity and task capability pass their limits. Charging is not a continuous
trickle. Recheck before reserving a pack; track health, delivered capacity and
cycles. An optional long-idle storage mode can be added without changing the
normal charged-spare requirement. Its voltage must follow the selected cells.

All cartridges share guides, retention and electrical/interface definitions.
Different cell counts, chemistries or current capabilities are not automatically
interchangeable: physical keying and electronically checked pack profiles prevent
an incompatible pack from energizing the robot or entering the wrong charge mode.
The existing 6S and 8S entries remain comparison cases, not an approved mixed fleet.

## Cartridge and robot changes

Keep the existing **180 × 66 × 55 mm** battery allocation at robot
[44,86,66]. The allocation now includes a rigid carrier, positive retention and
an interface end, rather than just a loosely restrained hobby pack.

| Allocation | Size mm | Minimum corner mm | Purpose |
|---|---|---|---|
| Complete cartridge/receiver | 180 × 66 × 55 | [44,86,66] | Guided removal downward |
| Bare cell-pack pocket | 158 × 62 × 53 | [46,88,67] | Cells plus unresolved internal lead/padding clearances |
| Interface end | 16 × 62 × 53 | [206,88,67] | Cell monitor, ID, fuse and recessed contacts |
| Auxiliary dock logic supply | 35 × 60 × 20 | [45,90,124] | Dedicated dock supply and reverse-blocking source handover |

The 6S bare pack fits the cell pocket numerically; the rotated 8S example also
fits numerically but has only 1 mm total width allowance. **Neither installed
cartridge is qualified.** Connector volume, cable bends, insulation, padding,
swelling allowance and actual pack tolerances can invalidate either fit. The
16 mm interface end is a reservation, not evidence that the eventual high-current
connector/protection parts fit. A different pack or rearranged bay may be needed.

Use replaceable printed guide liners and a cartridge shell with a purchased
metal load path at the retaining shoulders. The station supports the cartridge
before a cam releases a spring-engaged latch. Guides and hard stops carry
handling loads; electrical contacts do not carry cartridge weight. Recess both
power poles, key orientation, provide a gripper feature, and verify both full
insertion and latch engagement independently. Contact wipe and mating force
remain connector-selection inputs. Current through the mating power contacts is zero before separation.

Cell monitoring, identification, temperature sensing and a pack-side fuse travel
with every cartridge. The core retains its main switched discharge bus, current
shunt and precharge circuit. Rack charging must work with the cartridge removed
from the core; it cannot depend on a cell monitor left inside the robot.

The BQ76952 remains a possible monitor/controller basis with cell voltage,
temperature and balancing functions. It is not a finished cartridge BMS or a
qualified high-current switch assembly.
[TI BQ76952](https://www.ti.com/product/BQ76952).

The existing flight branch allocation of 150 A continuous and 320 A short must
be checked through **every** series element, including the new cartridge contact,
fuse and fixed switching stage. Those are design allocations, not ratings of the
parts drawn here. Charging uses independently controlled lower-current contacts.
Do not parallel charged and discharged packs or use small signal contacts for
propulsion current. Detailed precharge, discharge-isolation and charge-isolation
schematics are still required.

The added carried allowances are:

| Hardware | Low / nominal / high g |
|---|---:|
| Cartridge shell, monitor/ID, fuse, contacts and internal wiring | 85 / 140 / 220 |
| Fixed receiver, latch, switches and contact support | 30 / 50 / 85 |
| Auxiliary dock-power regulator, source OR and connection | 25 / 45 / 75 |
| **Added to previous robot budget** | **140 / 235 / 380** |

For budget bookkeeping these rows are included once in the core hardware
subtotal; the bare cell pack is still a separate row. Each spare has its own
140 g nominal cartridge tare, but does not duplicate the fixed core receiver or
dock supply. The 753 g comparison pack becomes an **893 g loaded cartridge**;
two stored spares add 1.786 kg per station, outside the flying mass.

The updated nominal vacuum robot is **4.676 kg on the floor** and **8.257 kg with
the octo top**. Its modeled hover rises to about **2.45 kW**, and the illustrative
transfer/departure energy allocation rises to **68.6 Wh**. Ground power inputs
remain assumed task loads; unchanged floor runtime does not demonstrate that
added weight has zero effect on actual consumption. See the regenerated
[budget](../design/system/output/system_budget.md).

## Mechanical exchange route

The middle battery is bounded by wheel/power hardware at its sides, LiDAR above,
and the working bottom below. The initial automatic route therefore uses the
existing module exchanger: **support the core, remove and park the bottom, then
withdraw the cartridge downward**. A battery-only visit temporarily removes the
same bottom and reinstalls it. This is slower than a dedicated side drawer but
retains the fixed body envelope and avoids adding a second full handling robot.

The station may first park the cap/lift top as in the existing core-lift sequence.
It raises the core by 300 mm, placing the cartridge underside at station z=376.
The shared bottom picker gains a battery adapter with positive capture; its Z
mechanism must reach this underside. The previous bottom-only transfer position
is not enough. Support the cartridge, release it, and lower **100 mm** to
z=276, with its top at z=331 before horizontal travel.

The battery rack reserves [880,250,375] to [1160,890,535], above the right-hand
bottom storage positions and below the parked lift top. Four cartridge shelf
reservations are 190 × 90 × 65 mm at [908,y,390], with y=270,420,570,720. The
enclosure includes shelf/contact space; chargers use the existing electrical bay.
Keep the battery enclosure dry and separate from mop wash and tank plumbing.
Compartment temperature sensing, ventilation and fault isolation need detailed
design; these boxes are not demonstrated fire barriers.

A proposed handling route withdraws below the held core, moves rearward to a
y=950 waypoint, shifts into the right-side aisle, then raises to the rack level
and approaches a shelf. At rack height keep the cartridge minimum x at least
750 mm to clear the held core, whose maximum x is 737.5 mm. The reverse route
returns the new cartridge. This is a route allocation only: gripper projection,
gantry crossmembers, cable chains, shelf entry and recovery motions still need
a full swept-volume check.

The model checks downward cartridge sweep against fixed core allocations, rack
placement against static station allocations, and shelf containment/separation.
It deliberately excludes the already removed bottom from the withdrawal check.
The cabinet remains **1200 × 1800 × 1500 mm** at this allocation stage.
Allow **two minutes as an initial exchange-time target**, including handling;
there is no measured cycle time yet.

## Power handover and operating sequence

The station supplies a protected **24 V / 60 W logic umbilical** to the core.
A dedicated converter and reverse-blocking source selection feed the 5 V logic
rail, with a 40 W delivered allocation. The LiDAR, Pi and supervisor can remain
live while the main cartridge is disconnected. Wheels, tools and flight remain
disabled. The station input never backfeeds an empty battery connector.

This avoids adding a second onboard battery solely for exchange. It is not a
promise of survival through a station mains failure: passive supports must hold
the robot and cartridge if all power is lost, and the job state must recover
after a reboot. Verify handover voltage droop under the actual peripheral load
before claiming uninterrupted Pi operation.

1. Reserve a compatible READY cartridge and a receiving vacancy before docking.
   Keep enough onboard energy to return and dock; retain flight landing reserves.
2. Dock, mechanically capture the core, establish auxiliary logic power and verify
   its power-good state. Save mission/pack inventory state.
3. Disable and isolate propulsion/tools. Verify pack current near zero and the
   relevant bus discharged; park the top and bottom as required for access.
4. Capture the old cartridge, release its latch, withdraw, and deposit it in the
   reserved receiving shelf. Record identity and occupancy from physical sensing.
5. Retrieve the reserved replacement, seat it to its hard stops, latch, and verify
   identity, orientation, cell/temperature limits and both engagement sensors.
6. Precharge the robot bus; verify voltage rise, then enable the protected supply.
   Check source handover before withdrawing auxiliary station power.
7. Reinstall and verify the bottom/top, weigh the complete robot if preparing to
   fly, and resume the saved cleaning job. Release supports last.
8. Assess the returned pack, cool if necessary, balance-charge within its own
   limits, terminate charge and mark READY only after verification.

An interrupted exchange leaves loads disabled and supported. Inventory after a
restart comes from pack IDs and presence sensors, not only the last saved slot
map. Failure to seat/latch, unexpected current, an incompatible ID, or no ready
replacement keeps the robot docked. A battery fault must not cause the station
to automatically insert that pack into another device to retry it.

## Charging throughput and availability

Reserve four individually controlled charge channels, with **180 W total charger
input shared across them**, rather than 180 W per bay. Current and voltage limits,
cell supervision and isolation are per pack. No battery outputs are paralleled.
The BQ25756 is a possible programmable CC/CV charge-controller basis; it requires
an external power stage, control and protection. It is not a complete four-bay
charger. [TI BQ25756](https://www.ti.com/product/BQ25756).

The station's 280 W DC supply must also cover handling, its controller, rack
electronics and up to 60 W robot logic input. Budget instantaneous loads and
reduce/pause charging during large handling or drying loads. The shared charge
allocation cannot be multiplied by the number of shelves. The model assumes
90% charging conversion efficiency and 80% charging availability, giving a
**129.6 W average energy ceiling into cells**. Neither percentage is measured;
pack current limits and charge taper may reduce delivery further.

At the current 116 W vacuum load this leaves about 14 W of average energy
margin. Under-sofa vacuuming at 122 W leaves only 8 W. Sustained no-wait operation
is plausible under these assumptions, but has little margin for long pauses,
higher measured cleaning power or extended balancing. Larger/more chargers are
station-side options; they do not require carrying a larger battery.

Independently, enough packs must be in rotation to cover each depleted pack's
recovery time. With equal packs and ignoring the short exchange interval:

`minimum local packs = 1 + ceil(recovery time / robot run time)`

Recovery includes cooling, power-sharing delays, CC/CV taper and balancing.
Two station spares plus the robot's pack give roughly **96 minutes** to recover
each returned pack during 48-minute vacuum runs. A 90-minute recovery fits this
allocation; a 120-minute recovery needs four local packs or scheduled waiting.
Adding packs only buffers an energy deficit; it cannot fix insufficient sustained
charger throughput. A 1C/5.2 A example gives an ideal 48-minute constant-current
lower bound to replace 80% capacity, before taper/cooling. This is arithmetic,
not authorization to charge the eventual pack at that rate.

For flight, reserve a compatible charged pack at the destination as well as
an arrival slot and landing energy. Pack exchange reduces charging delays after
landing; it does not extend one airborne sortie or reduce its peak current.
Repeated flight energy must be included separately in station scheduling. At
2.45 kW hover versus at most 162 W charge delivery while enabled, continuous
flying cannot be sustained by this station charge allocation.

The remaining releases are the cartridge/connector drawing, installed pack fit,
retention and electrical schematics, thermal/charge behavior, handover testing,
full station handling geometry and recovery firmware. No new purchases or
fabrication are required to adopt this architecture.
