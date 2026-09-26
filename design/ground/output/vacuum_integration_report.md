# Selected-component integration check

Date: 2026-09-13. **Placement only; not a fabrication release.**

28 root reservations, 18 nested references. Numerical conflicts: 0.

Axis-aligned reserved spaces only. Touching faces allowed. Structure, clearances inside bays, deformation, cables and mechanism paths need separate verification.

- Scanner top: 178 mm; rigid limit: 275 × 275 × 180 mm.
- Tire outer width: 271 mm. Body margin: 2 mm per side.
- Bin: 1.020 L gross; 0.838 L with 3 mm walls alone. Usable target 0.5–0.6 L remains unverified.
- Bottom projects 34 mm above its 86 mm mating plane; core projects 16 mm below it. A 60 mm station drop leaves 10 mm conservative vertical separation.
- Caster reference has 1 mm radial space inside its bay; final caster not selected.
- Converter minimum-length pins project 0.8 mm through the proposed PCB. Cooling and electrical layout are not qualified by this geometry check.

## Conditional service paths

| Path | Conflicts | Preconditions |
|---|---:|---|
| bin_service | 0 | Clean-air seal released and dirty inlet separated; real latch/rail construction unverified. |
| battery_service | 0 | Manual service; station capture withdrawn from path. |
| pi_service | 0 | Manual front tray extraction; connector disconnection and frame opening required. |
| head_service | 0 | Bottom supported above floor; head de-energized and screws/plug/flex joint released. Real flanges unmodeled. |

## Coordinates and evidence

| ID | Min x/y/z | Size x/y/z | Dimension basis |
|---|---|---|---|
| head | [22.5, 6, 0] | [230, 60, 50] | proposed reservation |
| roller | [37.2, 13.45, 0] | [200.6, 45.1, 45.1] | manufacturer listing; not verified rotating geometry |
| roller_drive | [28, 6, 50] | [74, 60, 24] | proposed reservation |
| brush_side | [2, 29, 0] | [18, 35, 65] | proposed reservation |
| wheel_left | [2, 72, 0] | [24, 73.3, 82] | proposed reservation |
| tire_left | [2, 72, 0] | [24, 72, 72] | manufacturer reference |
| mount_left | [26, 88, 18] | [80, 64, 46] | proposed reservation |
| motor_left | [26, 95.5, 23.5] | [69, 25, 25] | manufacturer reference |
| wheel_right | [249, 72, 0] | [24, 73.3, 82] | proposed reservation |
| tire_right | [249, 72, 0] | [24, 72, 72] | manufacturer reference |
| mount_right | [169, 88, 18] | [80, 64, 46] | proposed reservation |
| motor_right | [180, 95.5, 23.5] | [69, 25, 25] | manufacturer reference |
| flex_duct | [118.5, 66, 6] | [38, 26, 48] | proposed reservation |
| duct | [118.5, 92, 16] | [38, 70, 28] | proposed reservation |
| bin | [26, 162, 16] | [149, 107, 64] | proposed reservation |
| filter_chamber | [26, 166, 80] | [149, 103, 40] | proposed reservation |
| filter_allocation | [30, 177, 83] | [141, 76, 20] | proposed maximum allocation; not a part dimension |
| air_bridge | [175, 183, 103] | [17, 56, 17] | proposed reservation |
| caster | [192, 192, 0] | [80, 80, 60] | proposed reservation |
| blower_bay | [192, 170, 65] | [78, 100, 55] | proposed reservation |
| blower | [195, 175, 66] | [71, 70, 37.5] | manufacturer reference |
| blower_driver_bay | [108, 7, 62] | [44, 59, 24] | proposed reservation |
| blower_driver | [110, 11, 65] | [40, 50, 1.6] | manufacturer footprint; display thickness only |
| bottom_controls | [156, 7, 62] | [96, 59, 24] | proposed reservation |
| roboclaw | [160, 14, 66] | [48, 42, 17] | manufacturer reference; delivered revision unverified |
| bottom_mcu | [220, 9, 65] | [28, 55, 18] | proposed reservation |
| core_power | [28, 8, 88] | [96, 82, 30] | proposed reservation |
| pi_tray | [144, 8, 88] | [104, 83, 32] | proposed reservation |
| pi | [153, 20, 92] | [85, 56, 1.6] | manufacturer footprint; display thickness only |
| battery_tray | [10, 102, 88] | [164, 59, 32] | proposed reservation |
| battery | [19, 110, 92] | [135, 43, 22] | owner measured |
| boost_bay | [176, 92, 70] | [70, 70, 50] | proposed reservation |
| front_sensors | [126, 2, 88] | [16, 88, 30] | proposed reservation |
| pickup_left | [4, 36, 90] | [14, 54, 24] | proposed reservation |
| pickup_right | [257, 36, 90] | [14, 54, 24] | proposed reservation |
| joint_front_left | [4, 4, 80] | [20, 20, 16] | proposed reservation |
| joint_front_right | [252, 4, 80] | [20, 20, 16] | proposed reservation |
| joint_rear_left | [4, 248, 80] | [20, 20, 16] | proposed reservation |
| joint_rear_inboard | [176, 246, 80] | [14, 24, 16] | proposed reservation |
| lidar | [89, 96, 123] | [96.8, 70.3, 55] | manufacturer family reference |
| converter_carrier | [178, 95, 74.2] | [66, 64, 1.6] | proposed PCB outline; not routed |
| converter | [180.5, 98, 78] | [61, 57.9, 12.7] | manufacturer reference; working electrical baseline |
| converter_pad | [181, 98.5, 90.7] | [60, 56.9, 0.25] | manufacturer reference |
| converter_heatsink | [180.5, 97.95, 90.95] | [61, 58, 12.7] | manufacturer reference envelope; fins omitted |
| converter_fan | [191, 106.95, 105.65] | [40, 40, 12] | manufacturer extended dimensions with pads; cooling candidate |
| caster_sweep | [193, 193, 0] | [78, 78, 51] | manufacturer geometry reference only; not selected for purchase |

## Open design work

- Actual roller ends/cutter actuation and suitable drive within bay
- Actual filter seal and body within 141 × 76 × 20 mm allocation
- Serviceable hair-resistant caster SKU within 80 x 80 x 60 mm bay; 10 mm threshold behavior
- Wheel suspension/linkage and full shaft/plate/tire checks
- Cincon converter carrier, default-off interface, startup and cooling qualification
- Frame strength and narrow rear-inboard lock
- Cliff/bump sensor coverage and stopping distances
- Complete wiring cooling sealing and dirt evacuation
- Measured mass/CG incl caster trailing contact and empty/full bin
- Actual supply/driver revisions and blower system losses
