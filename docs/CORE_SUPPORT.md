# Shared core supports and battery receiver — S

The current core is **1,347 g including cartridge tare**, before adding the
753 g battery cells. Much of it has a distinct function: sensors, computing,
power protection, wiring, module locks and the metal frame. The largest broad
construction allowance still open is the 160 g printed trays/ribs. The fixed
battery receiver has another 50 g allocation.

S replaces those two rows with equipment bridges, lightweight trays and a fixed
receiver supported from the existing frame. The candidate is approximately
**154 g against 210 g**, including unfinished hardware and reserve: about
**56 g conditional saving**. No saving is booked yet.

[Interactive structure and cartridge path](../design/system/output/core_support.html) ·
[Calculation and complete ledger](../design/system/output/core_support.md) ·
[Inputs](../config/core_support.json) ·
[CAD check scope](../design/system/output/core_support_cad_checks.json)

| Position | FreeCAD | STEP |
|---|---|---|
| Installed cartridge | [Assembly](../design/system/output/core_support_installed.FCStd) | [Assembly](../design/system/output/core_support_installed.step) |
| Cartridge lowered 100 mm | [Assembly](../design/system/output/core_support_withdrawn.FCStd) | [Assembly](../design/system/output/core_support_withdrawn.step) |

These are review models. The station gripper, several mounts and the complete
electrical/retention mechanism are not ready for fabrication.

Metal profiles can be supplier-cut; the receiver tabs need suitable purchased
angle stock or vendor forming. No sheet-metal brake, mill or new workshop tool
is assumed available. Exact stock and fabrication method remain to settle.

## Construction and ownership

Two 12.7 × 1.5875 mm aluminum strips stand on edge across the existing side
rails, at Y83.4125 and Y154.6. Their span is 266.825 mm. Small angle clips attach
them to the G frame. They support equipment and cartridge loads; the unchanged
G corner blocks and module locks retain the 600 N inter-module requirement.

The Pi gets an open ribbed tray supported between the existing front frame rail
and the new front bridge. A relief and raised rear tabs clear the floor-power
shelf stiffener. The core supervisor gets a separate shelf attached to the left
rail. Other modeled trays preserve the protection-board, logic-power and lidar
allocations; unfinished legs, fastening and mounting hardware stay in the ledger.

Two receiver side webs sit outside the original 180 × 66 × 55 mm cartridge
outline. Their openings reduce material while leaving the guide edges and latch
slots. A lower relief clears the N drive cleat. The rear bridge and its clips
clear the mop tank and vacuum blower without changing those component volumes.

Two modeled steel tongues retract outward 3 mm for downward battery exchange.
They require metal cartridge shoulders, positive locking pawls, release guides
and two lock sensors. The shoulders belong in the retained cartridge-shell
scope; the unmodeled fixed latch hardware is explicitly included in S. The
closed-tongue interference check demonstrates geometric obstruction to removal,
not strength or automatic-latch qualification.

The following remain fully counted:

- **140 g cartridge tare:** 65 g shell/restraint, 35 g monitor/ID, 40 g
  fuse/contacts/internal wiring.
- **753 g cells**, unchanged 6S/5.2 Ah reference and 115.44 Wh nominal energy.
- **159 g metal core frame/fasteners**, **130 g module locks**, **125 g core
  harness**, and **80 g main power protection**.
- All electronics, sensor masses, converters and dock-power handover hardware.

S does not claim a lighter battery chemistry, remove protection, reduce capacity,
or credit the earlier proposed lidar substitution. Its 88 g remaining allowance
includes fasteners, latch completion, contact support, other equipment mounts,
cooling/wire guides and a 15 g completion reserve. The geometry does not stand
in for those parts.

## Fit, exchange and mechanical limits

The checks cover new S material against vacuum and mop component allocations
and N drive supports, plus the protected cell and cartridge-interface-end
reservations. They check new core pieces moving upward 180 mm and the cartridge
moving downward 100 mm in 1 mm steps. Top and bottom modules are removed for
battery extraction; both tongues are released. Wiring, station grippers and
fastener protrusions are not included in these sweeps.

The side-guide gap is only **0.2 mm nominal**. It still needs a manufacturing,
wear, thermal and misalignment tolerance stack. The 158 × 62 × 53 mm cell pocket
and 16 × 62 × 53 mm interface-end reservation are unchanged, but neither proves
that a completed high-current cartridge fits. Several supports still use
unverified sheet bends/angle stock and unfinished fastening details.

The simple beam screen places the entire baseline core and cells at 3 g on two
bridges. It calculates approximately **48 MPa stress and 0.65 mm deflection**,
within the project's preliminary 120 MPa / 1 mm limits. End joints, torsion,
weak-axis loads, local holes, creep and equipment attachment still need checking.
That deflection also belongs in the eventual clearance stack; nominal CAD
clearance alone is insufficient.

The cartridge retention screen uses 100 N shared between two tongues. Both
latches must be engaged; the calculation is not permission to operate with one
unlocked. A station must support the cartridge before release, isolate battery
current before separating contacts, and verify reseating and both locks before
enabling the robot. Control implementation is still pending.

## Effect on the weight target

With S alone, the ordinary vacuum transfer estimate would move from **5.275 kg
to about 5.219 kg**, still approximately **719 g above** the 4.5 kg limit. The
mop would be about **4.648 kg**, approximately **148 g above**. R's tentative
head-frame saving is not added. The authoritative candidate totals remain
unchanged until the replacement is complete.

The duster gets a separate mass projection in the report, but its older E layout
has not been checked with this shared core geometry. No duster fit or new flight
performance claim follows from the arithmetic.

This comparison does not yet recalculate whole-robot CG, wet-floor wheel loads
or lift trim. Those must use the completed support and hardware mass locations.

The next substantial target is the **bottom chassis and floor-power carrier**:
the 225 g general frame remains alongside separately modeled drive supports and
power-carrier hardware. Develop one frame with those mounting/load paths, then
replace the complete overlapping scope once. Preserve the current battery,
bin/water capacities, wheel traction, cleaning performance and automatic exchange.
