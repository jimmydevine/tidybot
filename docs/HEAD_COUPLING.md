# Removable vacuum head coupling — P candidate

**R correction:** the [integrated-head withdrawal check](INTEGRATED_HEAD.md)
found that the former Y79 carrier risers/end shoes overlapped N's wheel
envelopes. They now start at Y72.5; risers occupy Z60–66 and shoes Z59.5–64.5.
P's own CAD checks now include N stock and wheel envelopes. The carrier retains
its 70 g allocation; the small end-shoe joints still require detailed fastening
and load checks.

**Q follow-up:** the [passive-head comparison](PASSIVE_HEAD.md) supplies constrained
slide/pivot kinematics and includes N drivetrain solids in its fit check. It
finds that the guide placement requires head-frame rework and that a separate
dock-only passive mechanism offers only 22–25 g conditional saving. Friction
and release away from a station remain unresolved. Keep the lift allowance and
integrate the supports with the existing frame; P's totals are unchanged.

This develops the [O resident sofa extension](SOFA_ATTACHMENT.md) into a
dimensioned removable carrier, air connection and electrical interface.
The ordinary powered head and the floor-supported extension use the same body
receiver. One extension stays at each floor station; restore the ordinary head
before flight. The carrier remains fixed relative to the chassis while the
ordinary cleaning head follows the floor beneath it.

**This is a local interface candidate, with reviewable solids and calculations.
It is not a completed mechanism or a release to print/order parts.** The
carrier-to-head suspension, latch guides, mating-face supports and station
shuttle are still incomplete. There is no new demonstrated weight saving.

[Interactive withdrawal](../design/system/output/head_coupling.html) ·
[Annotated drawing](../design/system/output/head_coupling.svg) ·
[Calculations](../design/system/output/head_coupling.md) ·
[Mass rows](../design/system/output/head_coupling_mass.csv) ·
[Inputs](../config/head_coupling.json) ·
[CAD checks](../design/system/output/head_coupling_cad_checks.json)

| Review state | FreeCAD | STEP |
|---|---|---|
| Seated, locks engaged | [Assembly](../design/system/output/head_coupling_0.FCStd) | [Assembly](../design/system/output/head_coupling_0.step) |
| Supported, keys retracted, withdrawn 120 mm | [Assembly](../design/system/output/head_coupling_120.FCStd) | [Assembly](../design/system/output/head_coupling_120.step) |

## Carrier and retention

Two 1.5 mm steel cheeks slide onto four captured 4 mm guide sleeves, two per
side. Slots open at the rear so forward withdrawal releases them. The left
closed slot end sets insertion depth; the right end has 0.5 mm relief.
An aluminum 12 × 12 × 1 mm tube spans the cheeks behind the moving head.
Small end shoes and fasteners still need detailed joints; the air/connector
flanges currently appear as unsupported placement solids in CAD.

The proposed positive locks use two short cylindrical screw heads as keys.
Each nominal M2 socket head is 3.8 mm diameter and 2 mm long. On the left,
it spans X23.2–25.2 mm: 1.0 mm inside the removable cheek and 0.7 mm inside
the fixed steel receiver, across the 0.3 mm running gap. **The receiver bore
must carry the load; the small threaded shank only operates the key.** A
station fork pulls a captive nut/washer outward by 3 mm, leaving 0.5 mm
clearance from the cheek. Springs engage the keys without an onboard motor.

This is a hardware concept, not an approved screw selection. Only 0.5 mm
receiver engagement remains after the assumed ±0.2 mm axial variation.
Actual head chamfers, tolerances, bearing wear, spring preload, captive guides,
pull hardware and independent lock sensing must be resolved. If reliable
engagement cannot be established, change the key geometry before fabrication.
Do not interpret the simplified screw-head cylinder as a supplier drawing.

The local fore-aft screen assigns about 79 N to one lock, including high
mating preload. Calculated shear/bearing stresses are required capacities,
not allowable values or proof of a qualified joint. Detailed load transfer,
fastener pull-through, torsion, shock and fatigue remain open. The core is
lifted through its main module interface; this head coupling retains the head
and is not a lifting point for the entire robot.

## Air and electrical mating

The air passage is 32 × 22 mm. A replaceable 3 mm face gasket compresses to
2 mm; its 34 × 24 mm opening starts outside the passage so there is no intended
seal edge in the hair stream. Foam grade, inward deformation and leakage are
unqualified. The moving head retains 25 mm nominal active flex length before
the carrier flange. Floor-following motion belongs in that flex, leaving the
exchange seal stationary while cleaning.

P moves the body air flange to Y96–99 mm and the fixed duct front to Y104 mm.
It raises the H front bridge 1.5 mm to clear the new tube; bridge attachments
need reintegration. These are local changes in the P export. Earlier O/M/N
exports retain their original geometry for comparison.

Eight spring contacts mate separately from the air seal. The reference is
Mill-Max **0860-0-15-20-82-14-11-0**, using its November 2022 sheet: 9.957 mm
free height, 2.286 mm maximum stroke, 120 gf nominal force and 7.2 A derated
current. This establishes a documented envelope and preload reference; it
does not qualify a complete connector bank. [Manufacturer datasheet hosted
by Mouser](https://www.mouser.com/catalog/specsheets/Mill-Max_0860-0-15-20-82-14-11-0.pdf).

| Coordinate row, increasing X: 178 / 186 / 194 / 202 mm | Contact 1 | Contact 2 | Contact 3 | Contact 4 |
|---|---|---|---|---|
| Z54 mm | 12 V tool | Power return | 5 V logic | Logic return |
| Z60 mm | CAN H | CAN L | Hardware enable | ID/presence |

Use replaceable hard-gold target pads, a protected 12 V tool branch (4 A
candidate) and a separately limited 5 V logic supply (0.25 A candidate).
There is one contact per power conductor. The proposed tool current limit
still needs validation against starting and pickup loads. The two power
contacts alone can dissipate 0.64 W at 4 A using the catalog maximum resistance;
thermal performance, wiring, inrush and dust protection remain checks.

The tool has local driver-enable gating, encoder acquisition and a CAN
interface. The reserved small PCB/IO mass is not a completed controller design.
Use a dedicated bottom-to-tool CAN segment with termination at its two ends;
the existing core bus must not receive an accidental third terminator.
The MCU/bus implementation still needs selection and integration.

All contacts have equal length: there is no ground-first sequence. Mechanically
guide the tool before contact. Mate and separate with both tool and logic
supplies isolated. After seating and both locks are independently confirmed,
enable limited logic power, check tool identity/communication, then enable
driver power. Provide a local enable pull-down, unpowered high-impedance bus,
watchdog timeout and current monitoring. This is an electrical/control contract,
not implemented or tested firmware. No cryptographic authentication is implied.

## Supported exchange and station space

1. Reserve this floor's extension nest and an empty normal-head nest. Capture
   the robot on the apron; support the fixed carrier and the floating head
   independently at the exchange datum. Confirm telescope retracted for return.
2. Stop wheel, roller and blower drives. Isolate both connector supplies and
   confirm the tool is supported before the station retracts both keys.
3. Withdraw the supported carrier **120 mm forward**, then transfer it to its
   nest. The rearmost mating face ends 21.8 mm ahead of the body front.
4. Present the replacement tool on its support, guide it to the insertion
   datum and release the station actuators so the spring keys engage.
5. Confirm seating and both locks, check identity on limited logic power, then
   enable tool power. Release supports only after successful validation.
6. On incomplete insertion, power loss or inconsistent sensors, retain station
   support and inhibit drives. Recovery must preserve physical support; do not
   assume a partly inserted key has retained the head.

The 120 mm stroke supersedes O's provisional 100 mm **for this P geometry**.
With the extension withdrawing, robot and extension occupy **735 mm in length
before margins**. Nests, shuttle routing, release actuators and recovery access
require additional station space. The user's approximate 650 mm sofa approach
and 1 m nearby turning space remain recorded; neither confirms station space.
No additional home measurement is needed until a complete station layout makes
that request concrete.

## Mass ownership and next design gate

| Scope | P nominal / allowance | What it replaces |
|---|---:|---|
| Body interface | 93.84 g, partly allowances | O body interface, unchanged |
| Removable fixed carrier and mating half | 67.27 g itemized; 70 g allocated | O adapter 15 g + 55 g of M mount |
| Unfinished head compliance | 35 g remaining | Remainder of M 90 g mount |
| Existing head lift | 62 g retained | M lift allowance, unchanged |
| Combined budget | **260.84 g** | Exactly the prior combined budget |

The itemized carrier includes unresolved installation allowances; 67.27 g is
not a weighed assembly or a full CAD-volume total. Only about 2.16 g remains
within its proposed allocation. The **35 g remaining for compliance is a tight,
unproven target**. The 135 g head frame and 75 g common plumbing scopes also
remain booked. Reconcile their physical parts while completing the linkage,
flex and mating supports; do not delete whole allowances for partial overlap.

O's complete transfer estimate remains **5.275 kg with 300 g debris**, including
core and installed battery, excluding cap and lift. It still requires **775 g
reduction** to meet the 4.5 kg maximum. No mass credit is taken for removing
more hardware with the normal head during sofa work, or for consolidating the
extension's own adapter, until those assemblies are physically partitioned.

The next design gate is the shared carrier/head support: complete its joints,
compliance, flex, key guides and flange/PCB supports within the combined budget.
Compare a passive retained head and station-operated capture with the current
powered-lift allowance. Preserve threshold travel, cleaning contact, automatic
exchange and flight retention. If those functions cannot fit the allocation,
simplify the head/frame together before adding more mechanisms or ordering.

## Verification and reproduction

The local CAD check finds 39 valid interface solids, no material intersections
with the checked context, no intersections at 105 sampled head positions and
no withdrawal intersections at 121 positions spaced 1 mm apart. The minimum
sampled head clearance is approximately **1.05 mm**. These use rotated head
envelopes, not a continuous motion proof or actual detailed roller geometry.

The checks include modified M/H allocations and local carrier/receiver solids.
They do not cover every new N motor-support solid, full fastener access, latch
housings/springs, flange/PCB brackets, suspension joints, flexible services,
complete dock movement or manufacturing tolerances. Context exports are
wireframes; orange tool and teal body parts are solids. Colors are viewer
dependent. No STL files are released by this study.

```sh
python3 design/system/head_coupling.py
python3 design/system/head_coupling_viewer.py
freecadcmd design/system/export_head_coupling_freecad.py
python3 -m unittest discover -s design/system -p 'test_head_coupling.py' -q
```

The CAD JSON includes a source fingerprint across model inputs and Python
sources. Regenerate it after changes before relying on the recorded clearances.
At the original P review, all 146 system-model tests passed. The interactive viewer
also passed travel, key-release and reset checks. Automated tests cover mass
accounting, tolerance and release calculations,
and consistency with the exported local geometry. They do not test the
unimplemented hardware or control sequence.
