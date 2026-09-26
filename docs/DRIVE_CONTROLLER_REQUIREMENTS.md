# Wheel-drive controller selection

2026-09-06. Shopping criteria for the **BDUAV 2204-260KV rolling rig** and possible
reuse in the final wheeled bottom. The final motor choice remains open. These
criteria do not select a lift ESC or restart propulsion testing.

Prefer a **sensored FOC brushless motor controller** with local speed regulation.
FOC means field-oriented control; sensored means rotor position is measured and
used to control the motor. Both hardware interfaces and firmware support must be
established. A generic "FOC" or "30A" label does not establish these capabilities.

This list mixes required functions, integration preferences and performance that
must be measured on the actual motor. An MCU or current shunt alone does not
establish working firmware or accurate sub-amp current control. See the
[controller alternatives and installed-cost comparison](DRIVE_CONTROLLER_OPTIONS.md)
for candidates with existing servo firmware. None is yet validated with our BDUAV
motors; the ST proposal is a development platform, not a completed drive system.

## Shopping checklist

| Item | Requirement or preference |
|---|---|
| Motor type and quantity | Three-phase BLDC/PMSM; two independent motor channels, either two single-motor boards or one dual-motor controller. A brushed H-bridge does not substitute. |
| Supply | Required: operation throughout the usable 3S range, including 12.6 V fully charged and the chosen low-voltage cutoff. Preferred for possible 4S reuse: explicitly rated for 16.8 V plus braking/transient headroom; a documented operating maximum of 24 V or more is a useful search filter. This does not select 4S. A 24 V maximum does not support a full 6S pack at 25.2 V. |
| Low-speed operation | Starts under load from rest in either direction, creeps for docking, and regulates through at least 100 mechanical RPM as a proposed screening target. Normal cleaning with 60 mm wheels is approximately 48–80 RPM. Manufacturer high-speed or electrical-RPM limits are different quantities. |
| Direction and braking | Forward and reverse commanded during operation, controlled deceleration and configurable speed/acceleration limits. A setup-only direction reversal is insufficient. Verify supply behavior during regenerative braking. |
| Rotor feedback | Rotor-angle feedback supported by the actual firmware, either an onboard encoder or a supported external sensor. The current rig proposes AS5600 over I2C; an onboard or different external encoder is possible with revised wiring/mounts. A Hall-only RC-car input does not directly accept an AS5600 I2C connection. |
| Motor current control | Preferred for reusable hardware: measured phase-current control with an adjustable limit that works below 1 A. Approximately 0.1 A or finer setting increments are a screening preference, not a safe motor setting or proof of measurement accuracy. Verify sensing accuracy/noise at the intended low currents. Battery-current telemetry and a large board-overcurrent trip are different features. |
| Current capacity | Final required continuous and peak phase current are **TBD**. No basis yet to require 30 A, 40 A or 80 A. Check the real continuous rating under enclosure cooling, not only a propeller-cooled burst figure. Controller capacity is not permission to put that current through the motor. |
| Local controller | Prefer an integrated MCU with supported firmware/programming tools. A separate MCU plus driver is acceptable if the full BOM includes it. The Linux Pi issues commands/logs; the local MCU runs the fast motor loops. |
| Host connection | USB serial or documented 3.3 V UART preferred. CAN is possible with an appropriate Pi interface. PWM commands can work if the local board implements speed regulation and stopping; PWM alone does not provide telemetry. |
| Stops and faults | Disabled at boot; configurable command timeout (rig target at most 250 ms), encoder-fault handling, undervoltage and thermal handling, and a means to disable the power stage. System firmware must stop the other motor when one side faults. Board temperature sensing does not measure motor winding temperature. |
| Documentation and fit | Exact board revision, schematic/pinout, supported motor/sensor combinations, firmware and example configuration. Include connector access, wiring, encoder, MCU, programmer, cooling and power hardware in the installed size, mass and cost. |
| Availability and substitution | Owner preference added 2026-09-06: favor established distributors or ordinary retailers and avoid dependence on a manufacturer-direct purchase. Record exact revisions and procurement sources; document and test substitutes before calling them interchangeable. Availability does not waive motor-control or current-protection requirements. |

SimpleFOC distinguishes voltage control, model-estimated current and measured
current control. Its FOC current mode needs current-sensing hardware, and its
fast control loop runs locally at typically well above 1 kHz.
[Torque-control documentation](https://docs.simplefoc.com/torque_control)
Its [AS5600 interface](https://docs.simplefoc.com/magnetic_sensor_i2c) uses I2C.
The rig's two fixed-address AS5600 sensors currently connect to separate local
controller buses. A dual-controller design must resolve that address conflict.

## Lower-cost test option

A simpler encoder-based gimbal driver using voltage-mode FOC could be useful for
the BDUAV test if measured winding resistance and conservative voltage/thermal
limits support it. Current-sensing hardware is not inherent in every FOC design.
That option would require a revised commissioning plan; it would not provide the
same measured current limiting as the preferred reusable controller. The actual
BDUAV resistance remains unknown, and the conflicting ML2206B sheet is not a
substitute. Do not apply this fallback to the low-resistance iFlight motors using
the same limits. [Control-mode tradeoffs](https://docs.simplefoc.com/torque_control)

## Listing terms to check

- "Bidirectional DShot" describes command and telemetry communication; it does
  not by itself promise forward/reverse motor rotation.
  [Betaflight explanation](https://betaflight.com/docs/wiki/guides/current/DSHOT-RPM-Filtering)
- "Sensored" may mean a particular Hall-sensor interface. Check the actual
  connector, signal type and firmware before choosing an encoder.
- "FOC driver" or "SimpleFOC-compatible" may describe only a power-stage board.
  Check whether the MCU, current sensing and firmware are included.
- "30 A continuous" is neither a minimum needed here nor a small-motor current
  setting. An oversized sensing range may require extra attention to low-current
  resolution and calibration.

Useful search terms: **sensored FOC BLDC controller external encoder current
control 3S**, or **SimpleFOC controller integrated MCU current sensing**.

The [B-G431B-ESC1](https://www.st.com/en/evaluation-tools/b-g431b-esc1.html) is one
candidate because it includes an MCU, three-phase stage, sensor support and
current shunts. It still needs external encoders, custom sensored firmware and
verification of low-current control with the BDUAV motors. Its published 40 A
peak was tested with propeller-forced cooling; it is not our enclosed rating.
Alternatives should be compared against this checklist and the
[complete rig hardware proposal](../design/experiments/drive_rig/HARDWARE.md).

If the final robot uses brushed gearmotors, choose an appropriate H-bridge drive
instead. Passing this checklist establishes a candidate, not proven motor torque,
bearing life, thermal performance or automatic-cleaning suitability.
