# Wheel-drive controller alternatives

**2026-09-12 update:** the brushless comparisons below now concern an optional
experiment. The [ground robot recommendation](GROUND_COMPONENT_RECOMMENDATION.md)
uses geared brushed motors with integrated encoders and a RoboClaw controller.
The B-G431B-ESC1 path is not a prerequisite for that design.

Reviewed 2026-09-06 for the two BDUAV 2204-260KV motors and direct-drive 60 mm
wheels. **The owner has purchased two B-G431B-ESC1 boards for the rolling rig,**
expected later this week; receipt, actual paid price and exact arrival date are
not yet recorded. Proceed with the ST/external-encoder development path. The
comparisons below remain reference material for future substitutions. Final
robot suitability still depends on measured drive performance.

See the [pre-arrival preparation list](../design/experiments/drive_rig/PREPARATION.md)
for fit prints, remaining supplies and USB-only diagnostic firmware. No powered
motor commissioning has been completed.

The selected B-G431B-ESC1 development path requires external encoders, application
firmware and verification of current sensing at our small motor currents.
It should have been described as a development platform. The
[shopping checklist](DRIVE_CONTROLLER_REQUIREMENTS.md) includes both preferences
and physical acceptance tests; no alternative below has passed those tests on
our motors. An integrated encoder satisfies the rotor-feedback requirement and
can replace the proposed AS5600 with a revised carrier.

## Availability preference added 2026-09-06

The owner prefers broad retail/distributor availability over a dependency on
buying directly from mjbots. Prefer identifiable hardware revisions, documented
firmware and tested substitutes for an eventual open-source build. A marketplace
listing alone does not establish multiple supply sources or interchangeable
boards; two distributors also still depend on the original manufacturer.

The strongest documented development route under this sourcing preference is
**B-G431B-ESC1 plus external encoders and application firmware such as SimpleFOC**.
Current listings exist at
[DigiKey](https://www.digikey.com/en/products/detail/stmicroelectronics/B-G431B-ESC1/10321670)
and [Mouser](https://www.mouser.ca/en/ProductDetail/STMicroelectronics/B-G431B-ESC1?qs=%252B6g0mu59x7KUfhaFDGurZQ%3D%3D),
both displaying stock when checked. This improves purchasing options, but does
not resolve the custom firmware, wiring or sub-amp performance checks discussed
above. No widely distributed, ready-configured equivalent to moteus has been
verified for the complete checklist.

The [HeelAooRC AM32 listing](https://www.amazon.com/dp/B0F677BT7X) is a candidate
for a lower-cost experiment using two single-motor ESCs. Its seller specifies
2–4S, 40 A maximum, a 5 V/2 A BEC and a programming converter. The exact hardware
revision and current-sensing capability remain unspecified. Its AM32 startup
behavior must be tested with the BDUAV motors; it has not qualified as an
encoder-based replacement. The
[AM32 crawler guidance](https://wiki.am32.ca/general/Crawler-Hardware-and-AM32.html)
explains the low-speed sensing and sine-mode limitations.

Controller-specific mounts and harnesses should remain replaceable. The planned
robot software should expose wheel commands and status separately from each
controller's communication protocol. These are design intentions; no new adapter
firmware, interchangeable electrical connector or alternative mount is released.

## Candidates with existing servo firmware

Prices are manufacturer listings, before shipping, tax and any checkout
surcharges. Current figures are controller capacity, not allowable BDUAV current.
The conflicting ML2206B/160KV purchase-page sheet remains unsuitable for setting
limits on motors marked BDUAV 2204-260KV.

| Candidate | Controller cost for two wheels | Useful features | Fit and integration limits |
|---|---:|---|---|
| [moteus-c1](https://mjbots.com/products/moteus-c1) | $138 ($69 each) | MCU, sensored FOC, onboard absolute encoder, included magnets, open Apache-2.0 firmware; 38 × 38 × 9 mm, 8.9 g each. Published continuous phase current is 5 A without added thermal management. | 10 V minimum input: stop the 3S rig with margin above this at the controllers under load. Supports a future 4S supply. Needs CAN-FD or UART host interface and revised printed carriers. Sub-amp sensing accuracy on these motors is unverified. |
| [ODrive Micro](https://shop.odriverobotics.com/products/odrive-micro) | $178 ($89 each) | MCU, servo firmware with torque/velocity/position control, onboard magnetic encoder; 32 × 32 × 7.5 mm, up to 3.5 A continuous. | Also has a 10 V input minimum and supports 4S. Needs host interface, suitable encoder/magnet installation and revised mounts. The proposed AS5600 I2C connection is not among its listed external encoder interfaces. USB plus motor power requires a USB isolator. |
| [Tinymovr M5.2](https://motionlayer.company/products/tinymovr-m5) | €196 (€98 each) | Compact controller aimed at small gimbal motors, existing FOC firmware, onboard encoder and included magnet; 29.5 × 29.5 mm, 8 g. | Its specified 12–38 V input makes it a poor choice for normal discharge of the owned 3S pack. Consider if we later select 4S. The manufacturer specifies motor resistance/inductance compatibility ranges; our actual values remain unknown. Needs host interface and revised mounts. |

These are alternatives for wheel control. Reuse in the final wheeled bottom is
conditional on the final motor's voltage/current, motor-parameter compatibility,
enclosure cooling and fault handling. They do not select the deferred lift ESCs.

## Moteus control package for comparison

| Item | Quantity | Extended price |
|---|---:|---:|
| [moteus-c1](https://mjbots.com/products/moteus-c1), with encoder, magnet and mating power connector | 2 | $138 |
| [mjcanfd-usb-1x](https://mjbots.com/products/mjcanfd-usb-1x), shared by both motors | 1 | $39 |
| [JST PH3 CAN cables](https://mjbots.com/products/jst-ph3-cable), listed 30 cm version; confirm routed lengths in revised CAD | 2 | $8 |
| [JST PH3 120-ohm terminator](https://mjbots.com/products/jst-ph3-can-fd-terminator), far end | 1 | $5 |
| USB-A to USB-C **data** cable, if none owned | 1 | $5–10 allowance |
| **Control and communication package** | | **$195–200** |

The $190 manufacturer-priced subtotal plus the USB-cable allowance is not the
whole rolling-rig cost. The existing rig still needs its Pi power regulator,
power distribution, fuses, motor-power stop, motor leads, insulation, fasteners
and prints. Included XT30 mating connectors need leads to the battery distribution;
they do not directly mate with the pack's XT60. Separate AS5600 boards, their
separately purchased magnets and ST USB cables would be removed from a revised
BOM if we use the onboard encoders.

The present $263.50 rig estimate contains $103.50 for the ST boards, external
encoders, magnets, encoder leads and USB cables. Substituting the package above
gives roughly **$355–360 before shipping/tax**, assuming all other existing allowances hold.
This is a planning comparison, not a revised order list: power leads, board
carriers and fasteners still need reconciliation with the new layout. It makes
the premium over the custom-firmware ST path visible.

The USB adapter connects the Pi to one CAN-FD bus, daisy-chained through the two
controllers. Enable termination at the adapter and put the additional terminator
at the far end. The adapter supports Linux SocketCAN as well as its serial
protocol. No separate motor-control MCU is needed. Python command/logging code
and system fault handling still need implementation.

## What remains to qualify moteus

- Use its existing [configuration controls](https://mjbots.github.io/moteus/reference/configuration/)
  for phase-current limit, velocity/acceleration limits and command timeout.
  These features reduce firmware development; they do not prove current accuracy
  below 1 A. Verify sensing noise, starting behavior and heating at conservative
  limits appropriate to the actual motor. Do not inherit the controller's maximum
  current as the motor setting.
- The [hardware specification](https://mjbots.github.io/moteus/reference/hardware/)
  gives 10 V minimum for c1. Choose a loaded-pack stopping threshold above this
  with allowance for sag; per-cell battery monitoring is still required. A 3S
  nominal voltage of 11.1 V alone does not establish full-discharge compatibility.
- Mount each controller so its onboard encoder faces the rotating bore's magnet,
  or use a supported external encoder. This needs a new printed carrier and
  clearance/field checks. Existing AS5600-carrier STLs are not a c1 mounting kit.
  The [encoder documentation](https://mjbots.github.io/moteus/reference/encoders/)
  describes both onboard and external options.
- Configure commissioning specifically for a small motor. The automatic
  [calibration procedure](https://mjbots.github.io/moteus/guides/calibration/)
  defaults to 7.5 W calibration power; that is not an established safe value for
  these BDUAV motors. Motor identification and controlled calibration come before
  a loaded run.
- Set and test the local timeout (rig target at most 250 ms), startup disable,
  encoder failures and the system response to one controller faulting. A local
  watchdog does not by itself implement stopping the other wheel. Retain the
  independent motor-power stop and evaluate braking against the actual battery
  and wiring arrangement.

## Costs and limitations of the other options

**ODrive Micro:** two boards plus the manufacturer's $37
[USB-CAN adapter](https://shop.odriverobotics.com/products/usb-can-adapter) and one
$14 [USB isolator](https://shop.odriverobotics.com/products/usb-isolator) for
sequential USB commissioning total **$229 before cables/harnesses**. The adapter
listing currently says sold out, so this is a reference package rather than an
immediately orderable set. A compatible alternative CAN interface is possible
but needs a specific wiring/software choice. The
[Micro datasheet](https://docs.odriverobotics.com/v/latest/hardware/micro-datasheet.html)
and product page require isolation if USB and DC input are connected together.
Its [motor-parameter guide](https://docs.odriverobotics.com/v/latest/articles/motor-parameters.html)
also needs checking against measured BDUAV parameters. Existing firmware is a
benefit; it does not eliminate small-motor qualification.

**Tinymovr M5.2:** the two boards alone cost €196; the
[CANine host adapter](https://motionlayer.company/products/canine) is listed from
€34.50 without its optional case, including one 20 cm JST-GH CAN cable. Add the
remaining CAN/power harnesses, USB lead and any required termination. This is
already at least €230.50 before those additions
and the supply change. The M5 page specifies 1–20 ohm motor resistance and
10 µH–10 mH inductance; establish measurement conventions before comparing them
with multimeter readings. Its 12 V minimum is why it is conditional here, despite
its focus on small gimbal motors.

No controller has been purchased, no new carrier has been released and no powered
test has been run. The existing CAD/BOM still describes the earlier ST/AS5600
proposal. The next implementation change, if using moteus, is to reconcile its
mechanical placement and the complete rig BOM before printing controller mounts.
