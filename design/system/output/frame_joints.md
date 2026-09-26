# Revision G — core frame and joint candidate

**This pass establishes a more explicit load path, not a claimed weight saving.** The nominal metal frame changes from a 145 g allowance to 159.1 g including mounting hardware (+14.1 g). The 160 g printed trays/ribs, 130 g locks and all floor-frame/carrier allowances remain. These are estimates, not fabricated or proof-tested parts.

## Construction and load path

Use four 18 mm slices of 1 × 1.5 × 0.125 inch rectangular 6061-T6 tube at the existing [14/261, 14/261] mm coupling centers. Each slice has two horizontal faces joined by two continuous metal walls. Opposed module studs load steel sliding locks against the inside faces; the walls connect the upper and lower interfaces. Printed guides locate sliders and equipment; they are not the primary axial connection between modules.

Use a 20 × 18 × 2 mm steel slider with 8 mm travel through the open tube ends. Front and rear locks on the left release toward −X; right locks release toward +X. The shorter blank contains a 5 mm capture opening connected to a 9.5 mm entry opening and remains inside the 275 mm body during release. Tube internal depth is 19.05 mm, leaving 0.525 mm nominal clearance per side. An 18 × 12 × 2 mm metal bearing pad holds each slider clear of the tube corner radii even when the 0.5 mm draw gap closes.

With an assumed 3.175 mm inside radius, the loaded slider corner has 0.276 mm radial clearance and the pad has 0.350 mm clearance to the curved region. This is a radius/tolerance screen, not verified stock. The reference CAD uses sharp tube walls; actual profile radii must be checked. The existing 130 g lock allowance already includes seats: each mechanism retains 16.25 g, including its roughly 5.7 g steel blank and 1.2 g gross aluminum pad. No weight credit is taken for the shorter slider blank. Pad keepers, printed end retainers/actuation guides, wear liners, pawls, springs, fastening and sensed travel must fit the remaining allowance or increase the ledger. The slot geometry is not a completed latch.

Ground envelope remains 275 × 275 × 179.1 mm, including the full modeled slider stroke. The 38.1 mm tube height moves the top seat from 123 to 124.1 mm; LiDAR and upper core allocations rise 1.1 mm. Preserve the 180 mm overall limit. Sliders release only at a supported station, with motion/power inhibited. Manufacturing tolerance and station actuator access still need validation.

Four 12.7 × 1.5875 mm aluminum strips stand on edge between the corner blocks: two 255 mm and two 235 mm lengths. Four 12.7 mm angle clips connect the side strips to the tube blocks. The front/rear strips lap the inside faces of the tube walls. Reserve 24 M3 screw/nut/washer sets: two per direct rail end, four per angle clip. Flat joint faces and through fasteners avoid a precision-machined central frame. Confirm head clearance, hole layout, tool access and stock radii before release.

Stock can be cut by the supplier, or with a suitable metal-cutting saw and vise. The tube only needs crosscuts and drilled entry/mounting holes; no longitudinal milling, welding or sheet-metal brake is assumed. A countersink is needed where outward screw heads would use the side clearance. Tool ownership and exact cutting/drilling method should be settled at fabrication release, not by ordering a test harness now.

[Tube stock reference](https://www.onlinemetals.com/en/buy/aluminum/1-x-1-5-x-0-125-aluminum-rectangle-tube-6061-t6-extruded/pid/14469). This is a catalog dimensional reference, not verified delivered stock. [Hydro alloy data](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf) lists 240 MPa minimum yield for its 6061-T6 extrusions. The model uses project screening limits of 120 MPa bending, 80 MPa shear and an approximate 69 GPa elastic modulus; these are not certification allowables or proof that other tempers are equivalent.

## Mechanical screens

Keep the inherited 600 N factored axial requirement. Check 150 N per corner with four-way sharing and 300 N with two-way sharing. The latter screens unequal load; it does not permit a robot to lift with missing/unlocked joints. Do not multiply the already factored 600 N by the separate equipment acceleration again.

For flange bending, treat a 10 mm effective strip as simply supported between the tube walls with a central load: I = b t³ / 12, σ = F L t / (8 I), δ = F L³ / (48 E I). This excludes drilled-hole stress concentrations, corner radii, load introduction, prying, wear and fatigue. It compares candidate sections; it does not qualify the joint.

| Tube wall | 300 N flange stress | Bending screen |
|---|---:|---|
| 1.587 mm | 396.9 MPa | Fail |
| 2.000 mm | 240.8 MPa | Fail |
| 2.381 mm | 163.8 MPa | Fail |
| 3.175 mm | 85.0 MPa | Pass |

The independent rail check applies the core/cartridge/cells at 3 g, shared across two rails, over a 247 mm support span: 44.4 MPa and 0.52 mm. This screens the equipment support only; the 600 N module load travels through the corner blocks. Torsion and joint stiffness still require analysis/test.

The average shear screen over the aluminum remaining beside the 9.5 mm entry hole is 11.1 MPa at 300 N, below the 80 MPa project screen. This does not calculate notch stress, pull-through, prying or fatigue. The steel slider/pawl and supplied mushroom head must be checked separately.

## Packaging changes and preserved functions

The Pi bay and board shift 2 mm left to clear the right front slider. The fixed pack-protection bay shifts 3 mm inward to clear the side rail. The F carrier front stiffener is trimmed 3 mm at its left end, retaining its previous mass allowance. Rear left bin/tank and filter-bay edges move to x = 29 mm to clear the rear sliders. Their opposite edges stay fixed; the filter element shifts 2 mm and retains its full 141 × 76 × 20 mm allocation. The sofa bin becomes 1 mm taller. No sensor, converter, wheel, roller, water/debris load or energy reserve is removed.

Capacity screen: inset each chamber box by 3 mm walls, then reserve 15% for non-storage features. This is a declared packaging assumption; later baffles, seals, ports and evacuation geometry must still fit without reducing the targets.

| Module | After wall/reserve screen | Required usable target |
|---|---:|---:|
| vacuum | 600 mL | 500 mL |
| mop | 355 mL | 350 mL |
| low | 309 mL | 300 mL |

## Power-carrier integration result

A straight shared upper front bridge at [27, 83.5, 65] mm, 221 × 1.5 × 20 mm, initially intersects the controller bay and sofa feed-drive bay. G clears the route: separate the RoboClaw and full-size supervisor board allocations, moving the supervisor 1 mm right/4 mm forward, and move the full sofa feed-drive bay 5 mm forward. No PCB or actuator allocation is shrunk. The F carrier stock is excluded from the bridge collision test because it would be replaced.

| Bottom | F obstruction | G obstruction, excluding replaced carrier |
|---|---|---|
| vacuum | drive_control | None |
| mop | drive_control | None |
| low | drive_control, extension_drive | None |

The bridge route is now available, but its attachments to the fixed suspension pivots and the caster-support structure are not yet designed. Keep the 225 g bottom frame and complete F carrier in the carried mass. Do not build both overlapping carrier systems or credit support removal until the replacement load path, insulation and fasteners are complete. The bridge is a checked replacement envelope, not an installed zero-mass part.

## Complete carried estimates

| Loaded configuration | F | G candidate |
|---|---:|---:|
| vacuum + cap | 4763 g | 4777 g |
| mop + cap | 4477 g | 4491 g |
| low + cap | 5042 g | 5056 g |
| Airborne duster + quad | 5003 g | 5017 g |

Duster static limiting-rotor thrust/weight becomes 1.997:1. This remains effectively at the 2:1 threshold within modeling uncertainty; the frame study does not qualify flight or select a battery.

Model and CAD checks cover the new stock allocations, slider positions, core withdrawal past the F power hardware and downward battery extraction. The full station motion, latch retention, optical coverage, production shell, cables, fastener protrusion, wet-floor behavior and installed thrust remain unverified. Keep F as the comparison record; G is a candidate mechanical revision with a changed top seat.

[Design note](../../../docs/FRAME_JOINT_DESIGN.md) · [Frame drawing](frame_joints.svg) · [FreeCAD](frame_joints.FCStd) · [STEP](frame_joints.step)
