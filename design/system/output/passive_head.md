# Passive vacuum head — Q comparison

Kinematic and force comparison, not a finished mount or fabrication release

Two independent vertical slides carry spherical head pivots. A short drop link places each pivot 20 mm below its carriage. The left pivot locates the head laterally; the right provides 1 mm axial float. The head can translate, roll and pitch without forcing a rigid crossbar to slide crookedly.

## Motion and force results

- Required carriage centers: 27.11–50.00 mm. Tolerance-adjusted limits: 25.50–60.50 mm; smallest travel margin 1.61 mm.
- Pitch 5.22°, roll 2.32°; right-side geometric float 0.173 mm. After 0.5 mm spacing tolerance, 0.327 mm remains from the 1 mm float allocation.
- Nominal moving head 498.4 g. Target normal force 3.5 N needs unequal upward spring preloads: 1.17 N left / 0.22 N right. The motor-side mass is not centered.
- Nominal spring model: 2.98–4.02 N net contact. Including rate/preload variation and ±1 N parasitic force: 1.60–5.31 N; with 0–5 N suction: 1.60–10.31 N. These are assumptions, not measured bounds.
- Station capture uses 16 mm raised clearance and carriage Z56 mm. Passive end stops alone do not provide the proposed raised flight capture.

## Whole local replacement scope

| Item | Quantity | Total | Basis |
|---|---:|---:|---|
| rails | 2 | 18.6 g | catalog_length |
| carriages | 2 | 3.4 g | catalog |
| spherical_bearings | 2 | 1.0 g | catalog_reference |
| rail_backings_and_carrier_tabs | 2 | 8.0 g | allowance |
| drop_links_and_bearing_cages | 2 | 8.0 g | allowance |
| pivot_pins_and_retainers | 2 | 4.0 g | allowance |
| mounting_fasteners | 1 | 5.0 g | allowance |
| counterbalance_springs_and_anchors | 1 | 3.0 g | allowance |
| end_stops_and_pitch_stops | 1 | 4.0 g | allowance |
| dock_set_capture_hooks | 1 | 10.0 g | allowance |
| capture_sensors_and_harness | 1 | 4.0 g | allowance |
| completion_reserve | 1 | 6.0 g | allowance |

Total **75.0 g**, including 52.0 g of unfinished allowances. Compare against **97 g** (remaining P compliance plus M lift), giving a conditional 22.0 g reduction. The 70 g carrier, old head frame and plumbing stay counted.

Current transfer remains **5.275 kg**. If the whole Q scope is completed at this mass and meets its functions, the hypothetical total is 5.253 kg, still 753 g over 4.5 kg. No reduction is booked.

## Pitch stability and edge climbing

| Net contact | Drag | Required floor resultant Y | Stop couple needed |
|---:|---:|---:|---:|
| 3.50 N | -1.5 N | 29.5 mm | 0.0 N·mm |
| 3.50 N | 0.0 N | 38.1 mm | 0.0 N·mm |
| 3.50 N | 1.5 N | 46.7 mm | 0.0 N·mm |
| 2.98 N | -1.5 N | 29.4 mm | 0.0 N·mm |
| 2.98 N | 0.0 N | 39.5 mm | 0.0 N·mm |
| 2.98 N | 1.5 N | 49.6 mm | 0.0 N·mm |
| 1.60 N | -1.5 N | 29.0 mm | 0.0 N·mm |
| 1.60 N | 0.0 N | 47.8 mm | 0.0 N·mm |
| 1.60 N | 1.5 N | 66.5 mm | 23.2 N·mm |

The ideal front/rear support interval is Y20–52 mm. A resultant outside that interval means the freely pitching head cannot maintain both support rows: a pitch stop or different force/geometry is needed. Moving the pivot upward worsens this drag moment; the drop link prevents that unnecessary penalty. This is a level-body free-body screen, not a solved contact distribution on a step.

Two end skids have proposed front/back 13.5 mm rises over 14 mm runs. At a 10 mm edge they are intended to lead the hard housing. Wedge/friction sensitivity:

| Assumed friction | Push / normal-force ratio | Push at target contact | Push at high contact case |
|---:|---:|---:|---:|
| 0.10 | 1.18 | 4.1 N | 12.1 N |
| 0.20 | 1.44 | 5.0 N | 14.9 N |
| 0.35 | 1.98 | 6.9 N | 20.5 N |

This exposes an unresolved force cost. Guide drag, tire traction, contact transitions, edge shape and housing clearance need a coupled threshold check; the actuator cannot be deleted solely because an incline fits on paper.

Adding guide friction, the 20 mm drop-link moment, eccentric-force feedback and ±1 N services produces up to ±5.82 N in the conservative scalar screen. It gives 936 nonpositive-contact cases out of 1872, with net contact down to -3.23 N. A nonpositive result means the assumed floor-following state is not physically sustained; do not interpret it as negative floor pressure. These friction inputs are not measured limits.

A gravity-loaded variant removes the counterbalance springs: 72 g local scope, nominal 4.89 N contact and only 0.25 N residual in the high-friction screen. Its conditional 25 g saving is too small to justify deleting away-from-dock lift capability without validation. Prefer evaluating this simpler force arrangement within an integrated head-frame design, while retaining the powered-lift budget until the operating requirements close.

## Catalog references

The guide reference uses two 62 mm NS-01-17 rails (150 g/m) and two standard NW-02-17 carriages (1.7 g each, 20 mm long, 6 mm assembled profile). The manufacturer also describes preload and fixed/floating mounting; use a standard carriage here to avoid adding unnecessary preload. Exact short-rail holes and mounting-face fit need specification. [Guide catalog](https://www.igus.com/us/pdf/drylinn.pdf) · [Current carriage](https://www.igus.com/product/drylin-nw-2-17-j?artnr=NW-02-17).

The KGLM-03 historical pivot reference has a 3 mm bore, 10 mm OD and 6 mm width. Its specified precision shaft/housing fits are not achieved merely by printing a hole. A captured split housing and smooth pin need qualification, and the current LC successor must be checked separately. [Bearing dimensions](https://www.igus.com/us/pdf/igubal.pdf) · [Historical 0.5 g mass](https://www.igus.com/contentData/Product_Files/Download/pdf/2016%20igubal%20complete.pdf).

## Boundaries and next decision

- Horizontal support-plane samples, not a continuous sharp-step traversal.
- Pitch free-body is level only; guides and springs have unmeasured friction and moments.
- Mass includes unfinished joints, pins, springs, capture and supports as explicit allowances.
- Dock-set capture requires a receiving station to release the head. Arbitrary in-flight head positioning is not supplied.

[Design record](../../../docs/PASSIVE_HEAD.md) · [Interactive mechanism](passive_head.html) · [Local CAD check](passive_head_cad_checks.json) · [Mass rows](passive_head_mass.csv)
