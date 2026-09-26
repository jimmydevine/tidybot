# Removable head coupling — P candidate

The carrier slides forward out of four captured guide studs. Two spring-engaged cap-head keys prevent withdrawal; a supported dock tool retracts both. Each key bridges the removable cheek and a fixed steel receiver bore, so retention does not depend on bending a small threaded shank. Normal-head floor following is downstream of this fixed carrier. The extension connects the same carrier to its own supported hitch.

**Candidate status:** interface geometry and electrical contract; not a fabrication release or completed head suspension. O/M complete mass estimates remain unchanged.

## Mass ownership

| Scope | Detailed nominal / reserved | Existing allocation |
|---|---:|---:|
| Body interface, including still-allowed latch/contact details | 93.84 g | 93.84 g |
| Removable fixed carrier and mating half | 67.27 g | 70 g |
| Unfinished normal-head compliance | 35 g reserved | Within prior M mount |
| Existing normal-head lift | 62 g retained | Prior M lift |

The 70 g carrier allocation combines O's 15 g adapter and 55 g of M's 90 g mount. That leaves **35 g for unresolved normal-head compliance**. The combined carried allowance remains 260.84 g, exactly the previous 260.84 g. This is a scope assignment, not a demonstrated weight reduction. If the remaining mechanism exceeds its allocation, redesign the shared head/frame before claiming budget closure.

Transfer remains **5.275 kg / 4.5 kg**, requiring 775 g reduction. No extra saving from parking the lift/compliance or consolidating the extension adapter is booked until their installed geometry is complete.

## Mating and release

- Keep the 275 mm body width. Cheeks sit outside the side rails; a rear tube joins them below the power hardware. The candidate raises H_front_bridge 1.5 mm to clear that tube. Its attachment holes and full bridge joints require integration.
- Rear-open slots capture four 4 mm sleeves. Left closed slot end sets insertion depth; the right end has 0.5 mm relief to avoid two competing axial stops. The right side still requires a lateral float/shim strategy to accommodate rail spacing tolerances.
- Two nominal 3.8 mm diameter, 2 mm long M2 socket-head keys engage at Y76/Z70. At the left joint the head spans X23.2–25.2: 1.0 mm engagement in the removable cheek and 0.7 mm in the fixed receiver, across a 0.3 mm gap. A 3 mm outward stroke clears the cheek. The thin engagement, screw chamfers/tolerances, preload spring, captive pull nuts and guide need validation. The fixed receiver bore must carry the transverse load; the threaded shank only actuates the key.
- Dock support must carry the head and locate its floating portion level before release. The locks retain the carrier, not the free-moving brush body. Tool power must be isolated before the dock pulls the pins.
- Withdraw **120 mm** along negative Y before moving toward a storage nest. The rearmost mating face clears the body front by 21.8 mm. Robot plus withdrawing extension occupies **735 mm** before margins, separate from confirmed sofa space.

## Air joint

Move the fixed air flange rearward to Y96–99 and start the retained fixed duct at Y104, keeping its rear end unchanged. The removable flange ends at Y94; a 3 mm replaceable foam gasket compresses into the 2 mm gap. The clear bore stays 32 × 22 mm, and the gasket opening is 34 × 24 mm so its edges start outside the air passage. The actual gasket must resist inward deformation and release cleanly.

The working-head flex retains 25 mm nominal axial length (Y66–91). Its working/raised bend, compression, fatigue and hair passage remain unresolved. The seal is on the fixed carrier interface; floor-following motion belongs in the upstream flex. Avoid a sliding dirty-air O-ring through the hair stream.

At assumed gasket compression pressures of 10/25/50 kPa, seal forces are [5.3, 13.2, 26.4] N. Eight contacts add 9.4 N nominal. Combined nominal mating force is 22.6 N; the high screen including +30% contact-force sensitivity is 38.6 N. These foam values are design sensitivities, not a selected gasket specification.

## Electrical interface

Use eight protected spring contacts against replaceable hard-gold target pads. Contacts mate along Y, separately from the dirty-air seal, at X178/186/194/202 and Z54/60. Set the body-board front at Y107 and pad face at Y98.186. Locator engagement precedes contact. All pins have equal length: do not claim ground-first sequencing. Keep both supplies off while mating. After seating and both locks are confirmed, enable limited logic power for ID/communication checks, then enable tool driver power.

| Front-view row | Pin 1 | Pin 2 | Pin 3 | Pin 4 |
|---|---|---|---|---|
| Z54, left to right | 12 V tool | Power return | 5 V logic | Logic return |
| Z60, left to right | CAN H | CAN L | Hardware enable | ID/presence |

Use a fused/current-limited 12 V branch (4 A candidate) and 5 V logic (0.25 A candidate). Identify the tool on limited logic power before enabling its driver supply. The normal roller reference has a 5 A stall extrapolation, so motor current limiting and pickup/starting torque still need validation; a 4 A branch is not permission to stall it. Local CAN controller/driver-enable gating, encoder acquisition and an ID resistor are part of the carrier electronics allowance. No Pi timing dependency or direct motor phases cross this connector.

Provide unpowered high-impedance CAN behavior, local pull-down of enable, a heartbeat timeout and current/voltage monitoring. Terminate the short bottom-to-tool CAN segment at its two ends; do not add a third terminator to the core bus. Use a dedicated bus segment or controller interface that actually supports this topology. No firmware/PCB is released here.

The reference contact is Mill-Max **0860-0-15-20-82-14-11-0**. Its November 2022 manufacturer sheet gives 9.957 mm free height, 2.286 mm maximum stroke, 20 mΩ maximum contact resistance and 7.2 A derated current. At the proposed 4 A tool limit the two power contacts contribute up to 0.16 V drop and 0.64 W total. Individual-contact catalog limits do not qualify the assembled bank. [Manufacturer datasheet](https://www.mouser.com/catalog/specsheets/Mill-Max_0860-0-15-20-82-14-11-0.pdf).

Proposed compression is 1.143 mm. Including ±0.3 mm stack tolerance and high-load calculated beam deflection gives 0.71–1.58 mm, within the listed stroke. Confirm spring force, plated-pad wear, dust protection, PCB mounting and thermal behavior. The earlier April 2022 copy contains inconsistent stroke/derating entries and is not used.

[Roller motor reference](https://www.pololu.com/product/4842/specs) · [Feed motor reference](https://www.pololu.com/product/4845/specs) · [Existing motor driver reference](https://www.pololu.com/product/2997/specs)

## Local load screen

With 78.6 N assigned to a single lock (40 N fore-aft plus high mating preload), required key shear is 6.9 MPa, cheek bearing 20.7 MPa, fixed receiver bearing 29.6 MPa and simple rear-edge tear-out stress 5.3 MPa. Minimum engagement after ±0.2 mm axial variation is only 0.5 mm. Check actual cap chamfers/hardness and bearing length before using this key concept. These numbers do not qualify the purchased screw, engagement tolerances, support housing or the thin rail joint.

The ideal tube calculation gives 0.18 mm at a 50 N central vertical load and 0.08 mm under nominal mating force. Connections and torsion are excluded; no head/robot lifting certification follows. Gasket compression including the high-load beam movement and stack allowance spans 19–48% and needs a compatible material/force curve.

The CAD checks solids and sampled head positions, not the unfinished active flex, all fastener heads or continuous threshold motion. See the generated CAD check JSON for every remaining overlap rather than assuming the study passed.

[Design record](../../../docs/HEAD_COUPLING.md) · [Interactive coupling](head_coupling.html) · [Drawing](head_coupling.svg) · [Mass rows](head_coupling_mass.csv) · [CAD checks](head_coupling_cad_checks.json)
