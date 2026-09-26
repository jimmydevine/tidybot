# I — height and caster mounting

A C1 lidar candidate and revised caster mounting space pass the sampled packaging screens while preserving H’s 10 mm bump and 2.5 mm candidate droop. This is an overlay; G remains the complete mass baseline. No print, order or flight release.

## Suspension height

Lidar nominal top: **174.8 mm**. The 2 mm project reserve is added after solving support attitude; it is not yet a tolerance stack. Each bottom uses its own geometry, including the raised components and a conservative cap-height bound.

| Bottom | A1 sampled max | C1 sampled max | C1 + 2 mm reserve | 180 mm screen |
|---|---:|---:|---:|---|
| vacuum | 181.813 | 177.348 | 179.348 | Pass |
| mop | 181.813 | 177.348 | 179.348 | Pass |
| low | 181.876 | 177.348 | 179.348 | Pass |

The three-support model uses spherical drive-wheel proxies and an ideal caster contact point. It samples independent wheel travel and swivel headings, then refines around each maximum. It does not establish a continuous extremum, spring equilibrium, threshold traversal, loaded tire shape or body clearances on irregular floors. Full travel remains a mechanical design candidate.

## Lidar and lift connector

C1 reference: 55.6 × 55.6 × 41.3 mm, 110 g, four M2.5 holes on a 43 mm square; screw insertion ≤4 mm. The manufacturer drawing gives ±0.2 mm dimensional tolerance. The mount reserves 64 × 64 × 9.4 mm above the core; screws and rail attachments are still to detail. Bare sensor is 60 g lighter than the 170 g A1 reference. These are reference specifications, not measurements of supplied hardware. [SLAMTEC drawing, rev1.1, pp15/18](https://files.seeedstudio.com/wiki/SLAMRadar/SLAMTEC_rplidar_datasheet_C1M1_en.pdf).

C1 is a candidate replacement, not an equivalent-specification claim: 5000 samples/s and a typical 10 Hz sweep, versus the A1 reference’s 8000 samples/s and 5.5 Hz. C1’s nominal 0.72° spacing is about 38 mm at 3 m; keep the near-obstacle sensors, camera and cliff sensing. Mapping and dog/furniture detection still need validation. [C1 manufacturer page](https://www.slamtec.com/en/c1), [A1 specification](https://www.slamtec.com/en/lidar/a1spec).

The C1 electrical reference uses 5 V, 230 mA typical running and 800 mA typical startup; reserve startup headroom rather than sizing only to 1.15 W. Use its 3.3 V UART at 460800 baud with a supported driver. Keep existing power budgets until integrated measurements. [Manufacturer electrical tables, pp13–14](https://files.seeedstudio.com/wiki/SLAMRadar/SLAMTEC_rplidar_datasheet_C1M1_en.pdf).

The existing lift-connector reservation rotates from 78 × 32 × 35 to 78 × 35 × 32 mm and moves to [193, 88, 122.5] mm. Its volume is preserved. This leaves 1.5 mm above pack protection and 2.1 mm below the entire rotating optical enclosure (1.9 mm after the sensor drawing tolerance). The nominal beam is at z=163.3 mm. All four mechanical seats stay at z=124.1 mm; the connector carrier, cap opening, top-module mating route and harness must be revised to this location.

The old A1 cannot simply move downward enough: battery top is 121 mm; lowering its 124.1 mm base by the needed several millimetres consumes the mounting clearance. C1 with the old tall port also fails the unobstructed-window screen. The new geometry therefore depends on both the lidar and connector layout changes. Do not cover the optical enclosure with an unqualified transparent shroud. This pass checks the ground cap; lift-frame visibility remains open.

## Caster stack

Use S70-8x15 / 8 (EAN 4031582322040, 0007193200) as the fitting candidate. TENTE specifies M8 × 15, 6 mm added height and 20 g. It replaces the unsupported 2.5 mm fitting assumption. Confirm the exact pairing with 5940UAP050L51-8 before ordering. [TENTE fitting datasheet](https://e-shop.tente.fr/uploads/document/s7/s70-8x15-8-67e1849d480db980470763.pdf).

| Feature | z above reference floor |
|---|---:|
| Bare caster | 50.5 mm |
| Fitting shoulder / plate underside | 56.5 mm |
| 3 mm plate top | 59.5 mm |
| Reserved washer / nut tops | 61.1 / 69.1 mm |
| Full uncut threaded stem tip | 71.5 mm |
| Equipment underside | 74.0 mm |

Reserve a 24 mm diameter service pocket above the plate. The uncut stem, not the nut, sets the top at 71.5 mm, leaving 2.5 mm overhead. Washer ≤1.6 mm and locking nut ≤8 mm are fastener procurement limits; there is 2.4 mm nominal thread beyond that stack. Verify actual tolerances, locking engagement, tool access with equipment removed and fitting shoulder width before release.

The upper nut only retains the fitting to our plate. It does not establish retention of the caster on the fitting’s plug end during lifting. Manufacturer confirmation of that joint or a positively captive replacement remains required. The rolling load rating is not a pull-out rating. No modification of the caster’s plastic body is proposed.

Including the taller ground-to-plate moment arm, the gross 40 × 3 mm saddle screens at 80.8 MPa and 0.346 mm deflection under H's 100 N vertical / 25 N fore-aft case. These remain strip-beam estimates with a rigid root; the bolted angles and holes are not qualified.

## Nearby equipment

Raise the vacuum bin bridge floor from 62 to 74 mm, keeping its top at 94 mm. A flat chamber floor avoids a new hair-catching pocket. Raise the entire blower/plenum and its exhaust by 10 mm in vacuum/sofa bottoms, and the mop pump by 8 mm. Their revised undersides are 74 mm. The mop tank, sofa bin, filter, cleaning head and wheel travel stay at their existing allocations. Duct transitions and pump hoses must follow these changes.

| Bottom | Internal volume after 15% reserve | Required target |
|---|---:|---:|
| vacuum | 0.542 L | 0.50 L |
| mop | 0.355 L | 0.35 L |
| low | 0.309 L | 0.30 L |

These are conservative separate inner-box screens with 3 mm walls; seals, baffles and evacuation still need detailed validation. No cleaning-capacity reduction below the existing targets is credited.

## Mass and outstanding work

Bare lidar delta: -60 g. Add a provisional 18 g mount reserve. Caster installation reserve rises to 142 g including 20 g for unresolved secondary retention; this is +30 g relative to G. The illustrative combined delta is only **-12 g**, before completing the H support assembly. It is not a new complete robot mass or a flight-endurance improvement.

Next detail the moving motor trays, spring cups, travel stops, wheel-drop switches and rail/seat joints. Resolve caster retention and exact connector mating before fabrication. Complete cable routes, mount tolerances and the actual cap shell before declaring the full envelope verified.

The interactive HTML and FreeCAD/STEP files are review artifacts. Bay outlines are allocations; mounting geometry is not fabrication-ready.
