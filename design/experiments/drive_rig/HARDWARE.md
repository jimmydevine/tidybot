# Rolling rig hardware and purchase status

**Received: two HiLetgo AS5600 boards**, per owner report on 2026-09-07.
An included 4 × 2 mm magnet is also received; total magnet count is unconfirmed.
Two B-G431B-ESC1 boards remain ordered with receipt unreported.
The earlier ST estimate was later in the week; actual paid prices are unknown.
**Remaining planning allowance: $171.00 before shipping/tax**, before
deducting any additional supplies already owned or ordered. Received encoders, bundled magnets and purchased controllers
are excluded from this remaining allowance.

The current complete-path planning reference total is **$260.86 before shipping/tax**.
It includes all listed
purchase allowances and consumable/media allowances, assuming reuse of the
owned motors, wheels, caster, Pi, battery, wattmeter, scale and tools. It is
not a purchase receipt. Only **$89.86** uses observed manufacturer prices;
the remaining **$171.00** uses explicitly labeled allowances. Regional
availability, taxes, minimum packs and shipping can change the total. A full
filament spool, if needed, costs more than the filament consumption allowance.
There is no dedicated force stand or precision scale purchase.

| Qty | Item | Reference/allowance USD | Status | Price basis |
|---:|---|---:|---|---|
| 2 | ST B-G431B-ESC1 integrated MCU and three-phase driver | $77.96 | purchased awaiting delivery | manufacturer storefront 2026-09-06; reference only not purchase receipt |
| 2 | HiLetgo AS5600 module B09KGWC1PT, 23 x 23 mm | $11.90 | received | historical Adafruit manufacturer reference 2026-09-06; not ordered-board price |
| 1 | Pololu D24V50F5 5 V regulator | $35.00 | proposed purchase | allowance not live quote |
| 2 | USB-A to Micro-B data cables 20-30 cm | $8.00 | proposed purchase | allowance |
| 1 | USB-C 5 V power pigtail rated at least 3 A | $6.00 | proposed purchase | allowance |
| 3 | XT60 mating connector pairs with insulating covers | $6.00 | proposed purchase | allowance |
| 3 | Inline blade fuse holders and 5 A plus 1 A fuses | $9.00 | proposed purchase | allowance |
| 1 | Latching motor-power switch rated at least 5 A at 24 V DC | $7.00 | proposed purchase | allowance |
| 1 | 1-8S LiPo balance-plug cell voltage alarm | $5.00 | proposed purchase | allowance |
| 1 | 18 AWG power and 24-26 AWG signal wire plus heat shrink and insulated splices | $10.00 | proposed purchase | allowance |
| 2 | Four-wire encoder leads 100-150 mm; termination pending board pinout | $3.00 | proposed purchase | allowance |
| 1 | M2 screw and washer assortment including 6 mm pan-head screws | $7.00 | proposed purchase | allowance |
| 1 | M3 nuts washers and screws assortment | $12.00 | proposed purchase | allowance |
| 1 | M2.5 Pi and M3 controller/encoder spacers with insulating washers | $10.00 | proposed purchase | allowance |
| 1 | 15 mm hook-and-loop battery and ballast straps plus small cable ties | $6.00 | proposed purchase | allowance |
| 1 | Thin nonconductive padding mounting tape and small adhesive supply | $5.00 | proposed purchase | allowance |
| 1 | Small-probe contact thermometer | $20.00 | proposed purchase | allowance model not selected |
| 1 | PETG filament floor tape and labeled ballast bags | $12.00 | inventory check | allowance consumption |
| 1 | Pi microSD card and cooling allowance | $10.00 | inventory check | allowance |

The [CSV](hardware.csv) includes source links, quantities, owned items, wiring
notes and every allowance. Controller selection is the purchased ST path,
not interchangeable with the owned aircraft ESC or a brushed H-bridge.

Selected controllers and proposed supporting electronics:

- [ST B-G431B-ESC1](https://estore.st.com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-discovery-kits/b-g431b-esc1.html):
  two purchased; $38.98 each is the earlier observed reference, not the receipt.
  Includes MCU, driver, current sensing and
  ST-LINK programmer, so no separate ESP32, PWM board, current-sense shield or
  servo tester is required. Small-pad soldering and custom firmware are required.
- [HiLetgo AS5600 module](https://www.amazon.com/dp/B09KGWC1PT): two received;
  owner reports 23 × 23 mm, 16 × 16 mm hole centers, 4 mm holes and centered chip.
  Hold further encoder support prints pending the retention redesign. The $5.95 each retained in the planning
  table is the historical Adafruit reference, not the HiLetgo purchase price.
- **Included HiLetgo magnet, 4 × 2 mm**, owner-measured: no separate magnet
  purchase allowance. The rig needs two; total received count is unconfirmed.
  Both the rigid-fit holder and tape trial are retired; the tape version enters
  but wobbles and lacks reach. Evaluate the owner's [metal-rod proposal](ENCODER_METAL_ROD.md)
  before moving the encoder. No rod diameter tolerance, cut length, retention
  method or cap geometry is released. Existing magnets/boards are candidates
  for reuse; magnetic field and mechanical alignment must be verified.
- [Pololu D24V50F5](https://www.pololu.com/product/2851): one; $35 allowance,
  not an observed price. It supplies the Pi; the motor controllers use the fused
  3S bus. Check regulator temperature and Pi rail voltage under actual USB load.

Fastener quantities for the modeled assembly (buy an assortment with spares):

| Location | Fasteners/spacers |
|---|---|
| Stationary motor faces | 8 × M2 × 6 pan head; nominal 2 mm engagement through 4 mm plate |
| Wheels | Existing M2 fasteners if suitable; otherwise select from assortment after measuring actual hub stack and clearance |
| Motor feet | 8 × M3 × 25, washers and nuts |
| Encoder carrier feet | 4 × M3 × 20, washers and nuts |
| Sensor boards | 8 × M3 × 12 screws/nuts (nylon preferred), 8 × 3 mm M3 insulating spacers, 16 insulating M3 washers; verify component clearance/full nut engagement; adjust spacers for actual sensor gap |
| Caster to riser | 2 × M3 × 14, washers and nuts; inspect ball/housing clearance |
| Caster riser to deck | 4 × M3 × 50 through bolts, washers and nuts |
| Ballast shelf | 4 × M3 × 60 through bolts, washers and nuts; 4 printed 42 mm columns |
| Pi | 4 × 10 mm M2.5 female spacers; 4 × 8 mm and 4 × 6 mm screws; verify spacer threads before tightening |
| Two controller carriers | 8 × 10 mm M3 female spacers; 16 × M3 × 8 screws with washers; board retention by edge pads/light ties |

No threaded inserts, machined hubs, new shafts or separate wheel bearings are
required. The small contact thermometer is a $20 allowance, not a selected SKU.
Regulator/switch/connector physical fit and actual stock still need checking
when choosing vendors. AS5600s and an included magnet are received; ST controllers are ordered.

See [ENCODER_MOUNT.md](ENCODER_MOUNT.md) for the first HiLetgo carrier fit and
per-board hardware. M3 replaces the earlier M2.5 sensor mounting hardware.

See [preparation before arrival](PREPARATION.md) for the remaining order checklist,
fit prints and measurement blanks. See the [assembly and test instructions](README.md) for wire routing, initial
fuse choices, low-current commissioning and the remaining firmware work.
