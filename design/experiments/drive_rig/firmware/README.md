# USB-only ST controller diagnostic

This program checks a B-G431B-ESC1's USB serial link and an optional AS5600 sensor.
It has **no motor-drive commands, PWM generation, FOC, alignment or calibration**.
Use it with the **battery and all motor phase wires disconnected**. Keep the
ST-LINK daughterboard attached. USB supplies the MCU for these checks, as
described in [ST UM2516, sections 5.3 and 6.1](https://www.st.com/content/ccc/resource/technical/document/user_manual/group1/86/3f/45/e0/12/18/47/85/DM00564746/files/DM00564746.pdf/jcr%3Acontent/translations/en.DM00564746.pdf).

## Build on the development computer

From the repository root (the local environment is already installed in this
workspace; the first two commands are for another computer):

```sh
python3 -m venv .venv-drive-rig
.venv-drive-rig/bin/python -m pip install platformio==6.1.18
export PLATFORMIO_CORE_DIR=/tmp/tidybot-platformio
.venv-drive-rig/bin/pio run -d design/experiments/drive_rig/firmware
```

The platform is pinned to `ststm32@20.0.0`; the verified resolved Arduino package
is `framework-arduinoststm32@4.30000.0` (core 3.0.0), with GCC 12.3.1. No motor or
third-party sensor library is required. The framework supplies Wire and serial.
See [PlatformIO's board configuration](https://docs.platformio.org/en/latest/boards/ststm32/disco_b_g431b_esc1.html).

**Build checked on 2026-09-06:** 31,100 bytes flash, 1,780 bytes static RAM.
This includes neither a hardware run nor measured stack/heap high-water usage.
The boards have not arrived. USB operation, field readings and electrical
outputs remain to be checked on the actual hardware. No upload was performed.

## First USB check after delivery

1. Disconnect battery, motor leads and external circuits. Place one intact board
   on a nonconductive surface and connect its ST-LINK Micro-B port by a data cable.
   Flash only one ST board at a time so the programming target is unambiguous.
2. Run the following from the repository root, using the same environment as
   the build. Upload replaces the application on the motor-control MCU; it does
   not intentionally modify the attached ST-LINK firmware.

```sh
export PLATFORMIO_CORE_DIR=/tmp/tidybot-platformio
.venv-drive-rig/bin/pio run -d design/experiments/drive_rig/firmware -t upload
.venv-drive-rig/bin/pio device list
.venv-drive-rig/bin/pio device monitor -p /dev/ttyACM0 -b 115200
```

Choose the enumerated port rather than assuming `/dev/ttyACM0` belongs to this
board. On Linux, USB programming and serial access may need the appropriate
[PlatformIO udev rules and user permissions](https://docs.platformio.org/en/latest/core/installation/udev-rules.html).
Close the monitor with Ctrl-C. A later monitor command can add `--filter log2file`
to retain observations; keep such logs separate from measured driving runs.

3. Expect newline-delimited JSON containing firmware `tidybot-usb-diag-0.1`, a
   24-hex-character `board_id`, increasing `uptime_ms`, and `motor_drive:false`.
   Without a sensor, expect `i2c_ok:false`, `field_ok:false`, and null angle/field
   flags. These are expected states, not sample results already measured.
4. Label this board L or R and save its ID. Repeat with the other board. Later
   both can connect to the Pi, but `/dev/ttyACM` numbers can change with enumeration;
   associate sides using the observed board IDs/USB identities.

## Optional encoder check, still USB only

Remove USB power before soldering or changing connections. Identify the delivered
board revision and check its schematic through the
[ST product documentation](https://www.st.com/en/evaluation-tools/b-g431b-esc1.html).
The J8 sensor connector includes a **5 V supply pad**, which is not the proposed
sensor supply below. Locate and measure the correct 3.3 V rail first.

The ordered encoder is the [HiLetgo module](https://www.amazon.com/dp/B09KGWC1PT),
reported as 23 × 23 mm. Its listing calls the supply **VCC, 3.3 V**. The table
below is retained as the earlier Adafruit reference; verify actual module labels,
supply configuration and pullups before applying it to the HiLetgo board.

| Earlier Adafruit AS5600 #6357 reference | ST board connection |
|---|---|
| VIN | Verified 3.3 V rail |
| GND | Controller ground |
| SDA | PB7, J8 B+/H2 signal path |
| SCL | PB8, J8 Z+/H3 signal path |
| OUT / other unused signals | Leave unconnected |

Each encoder uses its own controller's local I2C bus at address 0x36 and 100 kHz.
Use short leads and verify the signal idle voltage stays at 3.3 V. The board's
Hall/encoder input network and the breakout's pullups must work together; a
compiled pin map does not establish electrical communication. Inspect wiring
and the revision's series resistors/pullups if `i2c_ok` stays false; do not remove
components based only on a generic board example. The
[STM32duino board pin definitions](https://github.com/stm32duino/Arduino_Core_STM32/blob/3.0.0/variants/STM32G4xx/G431C%286-8-B%29U_G441CBU/variant_B_G431B_ESC1.h)
and its peripheral map provide the software pin assignment.

With a centered diametric magnet fitted, reconnect USB and turn the wheel
**slowly by hand** through complete revolutions. The program reads status 0x0B
and the 12-bit raw angle at 0x0C–0x0D. `field_ok` requires detection and neither
the weak nor strong flag, following
[Adafruit's AS5600 register implementation](https://github.com/adafruit/Adafruit_AS5600/blob/main/Adafruit_AS5600.cpp).
Raw counts range 0–4095 and wrap once per revolution; the direction depends on
assembly orientation. Log smooth changes, repeatability and field status over
the whole revolution. A valid field flag alone does not establish angular
accuracy or absence of distortion from the motor magnets.

Failed reads emit `i2c_ok:false` and null angle/field flags, never a retained
previous angle. A readable sensor with invalid magnetic field still exposes its
raw count but marks `field_ok:false`; do not treat that count as valid feedback.
Reporting targets 10 Hz, not a real-time guarantee. Wire timeouts or USB delays
can slow reports. This is not a velocity measurement or a motion watchdog.

## Output behavior and remaining work

The program holds PA8/PC13, PA9/PA12 and PA10/PB15 low as GPIOs from setup onward.
These are this board's six gate-input pins. The
[L6387E driver](https://www.st.com/resource/en/datasheet/l6387e.pdf) has outputs
in phase with its inputs. The program does not configure switching timers and
does not interpret received serial bytes. This does not control behavior during
reset, before flashing or under other firmware: keep bus and motor disconnected
throughout this diagnostic procedure.

Motor driving will be a separate firmware stage with sensored commutation,
calibrated phase-current measurements, measured motor parameters, limited
alignment, speed ramps and tested fault handling. The rig remains
`powered_release: false` until that commissioning is complete.
