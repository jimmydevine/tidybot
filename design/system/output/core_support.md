# S — shared core equipment supports and battery receiver

A pair of equipment bridges uses the existing G frame to support the battery receiver and lightweight equipment trays. The main frame, module locks, battery cartridge, protection and all electronics remain. This pass replaces only the former 160 g core-print allowance and 50 g fixed receiver allowance.

**Review candidate, not a fabrication release.** The contact/latch completion, several equipment mounts, fasteners and cooling guides remain explicit allowances.

## Core audit

The current core, including its removable cartridge tare but excluding battery cells, is **1347.1 g**. The existing metal frame and frame fasteners account for **159.1 g** and remain untouched.

| Core item | Current mass |
|---|---:|
| Core-fixed SLAMTEC RPLIDAR A1 | 170.0 g |
| Core PETG ribs, equipment trays and ducts | 160.0 g |
| Removable cartridge shell, cell monitor/ID/temperature, fuse and recessed contacts | 140.0 g |
| Eight core-side captive sliding locks, seats, springs and detection | 130.0 g |
| Core wiring, connector halves, fuse, charge and service access | 125.0 g |
| OAK-D S2 USB stereo camera and bracket | 106.0 g |
| Raspberry Pi 5, active cooler and microSD | 82.0 g |
| Core switched discharge bus, current shunt, precharge and protection power stage | 80.0 g |
| Fixed battery guide, positive latch, presence switches and floating contact support | 50.0 g |
| Station logic-power input, 24 V to 5 V regulator, source OR and hold-up capacitors | 45.0 g |
| Six near-field ToF boards, windows and core IMU allowance | 32.0 g |
| 5 V regulator and carrier, 40 W design allocation | 25.0 g |
| ESP32-DevKitC plus CAN transceiver and hardware watchdog | 20.0 g |
| Stop switch, buzzer, status LEDs and guard contacts | 15.0 g |
| core interface F | 8.0 g |

The 140 g removable cartridge contains 65 g shell/restraint, 35 g monitor/ID and 40 g fuse/contacts/wiring. All 140 g stays. Cells remain 753 g, 6S/5.2 Ah, 115.44 Wh nominal. No voltage, capacity, discharge capability, sensor or automation change is credited. The 170 g lidar row remains even though I has a smaller C1 placement candidate; this study does not accept that earlier performance trade.

## Installed replacement scope

| Item | Mass |
|---|---:|
| Previous core prints + fixed receiver | 210.00 g |
| Modeled material | 66.33 g |
| Remaining hardware and completion allowance | 88.00 g |
| Complete local candidate | 154.33 g |
| Conditional saving | 55.67 g |

| Part | Mass | Basis |
|---|---:|---|
| equipment_bridge_front | 14.52 g | Dimensioned material; attachment holes and supplied radii not credited |
| front_left_frame_clip | 0.24 g | Gross angle-clip material; supplied bend radius and two-plane fasteners remain to detail |
| front_right_frame_clip | 0.24 g | Gross angle-clip material; supplied bend radius and two-plane fasteners remain to detail |
| equipment_bridge_rear | 14.52 g | Dimensioned material; attachment holes and supplied radii not credited |
| rear_left_frame_clip | 0.24 g | Gross angle-clip material; supplied bend radius and two-plane fasteners remain to detail |
| rear_right_frame_clip | 0.24 g | Gross angle-clip material; supplied bend radius and two-plane fasteners remain to detail |
| left_receiver_end | 4.05 g | 1 mm receiver side web with central opening and latch slot; cartridge shoulder is in retained shell/restraint scope |
| left_front_receiver_tab | 0.09 g | Receiver-to-bridge tab material; radiused bend/joint and fastener access remain unresolved |
| left_rear_receiver_tab | 0.09 g | Receiver-to-bridge tab material; radiused bend/joint and fastener access remain unresolved |
| left_guide_liner_0 | 0.16 g | Replaceable guide strip; nominal 0.2 mm clearance to retained cartridge outline, tolerance not qualified |
| left_guide_liner_1 | 0.16 g | Replaceable guide strip; nominal 0.2 mm clearance to retained cartridge outline, tolerance not qualified |
| left_battery_tongue | 0.53 g | Closed-position tongue material; pawl, spring, guide and sensing retained in completion rows. Opens outward by 3 mm |
| right_receiver_end | 4.05 g | 1 mm receiver side web with central opening and latch slot; cartridge shoulder is in retained shell/restraint scope |
| right_front_receiver_tab | 0.09 g | Receiver-to-bridge tab material; radiused bend/joint and fastener access remain unresolved |
| right_rear_receiver_tab | 0.09 g | Receiver-to-bridge tab material; radiused bend/joint and fastener access remain unresolved |
| right_guide_liner_0 | 0.16 g | Replaceable guide strip; nominal 0.2 mm clearance to retained cartridge outline, tolerance not qualified |
| right_guide_liner_1 | 0.16 g | Replaceable guide strip; nominal 0.2 mm clearance to retained cartridge outline, tolerance not qualified |
| right_battery_tongue | 0.53 g | Closed-position tongue material; pawl, spring, guide and sensing retained in completion rows. Opens outward by 3 mm |
| pi_tray | 7.59 g | Open printed tray with outside ribs and raised rear attachment tabs; local relief clears floor shelf stiffener without changing that bottom part |
| supervisor_tray | 5.35 g | Printed shelf and outside wall tied to left G rail; board fasteners separate |
| power_board_shelf | 8.49 g | Insulated shelf below protection bay; upright mounting and dielectric isolation retained in remaining mounts allowance |
| logic_buck_tray | 0.59 g | Open logic tray; standoffs/rail attachments remain in equipment mounting allowance |
| dock_power_tray | 0.70 g | Open logic tray; standoffs/rail attachments remain in equipment mounting allowance |
| lidar_tray | 3.41 g | Ring plate inside I mount reservation; legs and exact fasteners remain in mounting allowance |
| frame_and_equipment_fasteners | 14.00 g | Installation allowance for beam clips, carrier fasteners, inserts and load spreaders; exact lengths and holes unresolved |
| receiver_latch_completion | 15.00 g | Latch guides, positive pawls, springs, two position sensors and associated hardware; two modeled tongues are counted separately |
| receiver_contact_support | 6.00 g | Fixed floating contact support and insulation; core-side power wiring stays in core_harness and cartridge contacts stay in battery_cartridge |
| remaining_equipment_mounts | 28.00 g | Camera, six near-sensor mounts, status hardware mounting, power-board mounting and port supports not detailed by this pass |
| cooling_guides_and_wire_restraints | 10.00 g | Short air guides, edge protection, cable clips and isolation; electrical harness/cooler hardware remains separate |
| completion_reserve | 15.00 g | Unassigned completion reserve inside the replacement scope; not fabricated material |

The sum includes unions only once and subtracts modeled openings at solid material density. This is not a slicer/weighed result. The cartridge hardware, G frame/fasteners, eight locks, 125 g harness, 80 g main power stage, logic converters and all other masses stay in their original rows. R’s tentative head saving is not stacked onto this candidate.

## Complete non-lift mass at maximum modeled contents

| Configuration | Current | With S only | Budget | Candidate over / under |
|---|---:|---:|---:|---:|
| N_mop | 4.704 kg | 4.648 kg | 4.500 kg | +148 g |
| O_vacuum | 5.275 kg | 5.219 kg | 4.500 kg | +719 g |
| G_E_air_dust | 2.611 kg | 2.555 kg | 3.500 kg | -945 g |

Duster numbers are a mass projection only: the shared core layout still needs integration with its older E tool layout. Vacuum and mop packaging checks do not establish duster compatibility. Whole-assembly upper uncertainty remains undefined for N/O, and no saving is booked.

## Mechanical demand screens

Two 266.825 mm spans carry a conservative **2100.1 g** baseline core-plus-cells load at 3 g. Each takes **30.89 N**, producing **48.29 MPa** bending stress and **0.654 mm** deflection in the simply supported strip model. Screen result: **pass** against project limits of 120 MPa / 1 mm.
The bridge uses the existing 12.7 × 1.5875 mm strip reference on edge. Grade/temper and actual stock still need confirmation. Elastic modulus 69 GPa and density 2.7 g/cm³ are engineering assumptions. Hydro’s 6061 sheet supports the reference alloy context, not the joint design or other stock tempers. [Hydro alloy reference](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf).
A separate 100 N cartridge retention case shared by two tongues asks for **50 N each**, **4.17 MPa** average shoulder bearing and **19.69 MPa** nominal tongue bending stress. These are capacity demands, not proof of a supplied latch, shell or fastener. Both latches must be sensed locked. Spring closure alone is not positive retention; completing the pawls remains required.
The G corner frame retains the full 600 N inter-module requirement. The cartridge and component bridges do not carry that load instead. Weak-axis and torsional stiffness, fastening, sheet bend radii, local stress and durability remain open.

## Exchange and limits

The station supports the core and removes the bottom before cartridge extraction. It supports the cartridge, verifies zero power-contact current, then retracts both tongues 3 mm. The cartridge goes down 100 mm. The printed guide strips remain on the core, while the cartridge metal shoulders travel with the retained shell. The 0.2 mm nominal side-guide gap is not a tolerance-qualified fit.
The 158 × 62 × 53 mm cell pocket and 16 × 62 × 53 mm electrical interface-end reservation remain protected. Neither validates an installed 150 A contact/fuse/BMS stack or soft-pack swelling clearance. The main battery interface is still unfinished; weight cannot be removed from its 140 g allowance on that basis.

See core_support_cad_checks.json for scoped intersections, upward core removal and downward cartridge clearance. Nominal non-overlap is not tolerance or deflection approval, and wire sweeps are not yet modeled.

The remaining system deficit requires additional concrete work on the bottom chassis and power-carrier supports, followed by bin/air-path construction. Further shaving of small common-core pieces alone will not close it.
