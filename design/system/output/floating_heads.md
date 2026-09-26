# M — floating-head integration

Packaging and mechanism requirements; not fabrication CAD or a purchase release

The previous static layout does not reserve working head movement. M adds an ideal floor-following model, separate moving-head mass and a revised clearance proposal. This is the space/load contract for the next detailed mount, not a finished suspension.

| Module | Nominal loaded planning mass | Wheel shims L / R | Working retraction | Net head force | Drive-wheel normal load |
|---|---:|---:|---:|---:|---:|
| vacuum | 5.316 kg | 3.50–3.00 mm | 2.42–3.69 mm | 1.92–3.89 N | 40.45–45.45 N |
| mop | 4.954 kg | 3.50–2.75 mm | -0.23–0.14 mm | 6.29–9.36 N | 29.53–33.10 N |

Each module is calibrated once with its head raised and reference contents. Work sweeps use all L contents, 24 caster headings, three head-spring rate cases and ±1 N parasitic-load cases. Nominal K hardware and nominal wheel springs are used; this does not resolve L spring manufacturing sensitivity.

| Module | Old moving/fixed conflict pairs | Proposed conflict pairs | Static conflicts | Raised minimum clearance | Max height + 2 mm |
|---|---:|---:|---:|---:|---:|
| vacuum | 13 | 0 | 0 | 10.47 mm | 176.01 mm |
| mop | 8 | 0 | 0 | 14.52 mm | 177.55 mm |

## vacuum conflicts and mass

Earlier pairs: [['vac_head', 'G_bottom_supervisor'], ['vac_head', 'H_left_rail'], ['vac_head', 'H_right_rail'], ['vac_head', 'blower_driver'], ['vac_head', 'drive_control'], ['vac_head', 'front_camera'], ['vac_head_drive', 'G_lock_0_bottom'], ['vac_head_drive', 'H_left_rail'], ['vac_head_drive', 'H_shelf_rib'], ['vac_head_drive', 'cincon_reference'], ['vac_head_drive', 'clamp_resistor_reference'], ['vac_head_drive', 'floor_front_stiffener'], ['vac_head_drive', 'floor_shelf_left']]
Proposed pairs: []
Changed static pairs: []
Moving dry head: 512.0 g. Added mount/lift/riser allowance: 174.0 g; original allowances retained, no speculative saving. Signed preload at reference height: -2.02 N (negative means counterbalance upward).

## mop conflicts and mass

Earlier pairs: [['mop_drive', 'H_inner_rail_0'], ['mop_drive', 'H_left_cap'], ['mop_drive', 'H_left_cheek_inner'], ['mop_drive', 'I_lidar_mount'], ['mop_drive', 'battery_bay'], ['mop_drive', 'lidar'], ['mop_pad', 'mop_lift'], ['mop_pad', 'mop_tank']]
Proposed pairs: []
Changed static pairs: []
Moving dry head: 282.0 g. Added mount/lift/riser allowance: 98.0 g; original allowances retained, no speculative saving. Signed preload at reference height: 4.74 N (negative means counterbalance upward).

## Interpretation

The whole vacuum cassette and its motor move together. Its dead weight already exceeds the 3 N trial contact target, so use adjustable upward counterbalance, not extra downward preload. The complete mop pad/drive float together while only the pad oscillates. Its 8 N trial target needs downward preload. Neither target establishes hair pickup, wet cleaning or traction performance.

A separately listed 0–5 N suction-force sensitivity increases gross brush/skid contact and possible drag. It does not automatically remove that same force from the wheels: with coincident pressure/contact resultants those external forces cancel in whole-robot vertical balance. The parasitic hose/guide load is modeled separately. Actual pressure footprint, moments, friction, head support reactions and brush deformation remain unknown.

M reserves −2…+10 mm working translation with ±1.5° pitch/roll, then a level 16 mm raised stop. The raised-clearance calculation is flat-floor only; it does not prove traversal of a 10 mm step. The working sweep is not every combination of wheel spring tolerances or obstacle contacts.

The layout requires elevated vacuum electronics and power shelf, a higher shared Pi/camera mounting position, an 18 mm higher mop tank and a 15 mm higher mop lift. The vacuum head is reduced to a 48 mm height reservation and its drive to 71 × 60 × 29 mm. The mop drive becomes 32 × 27 × 83 mm, farther rearward. These tightened allocations still require actual roller/motor/mount/belt/connector CAD; trimming an envelope does not prove the hardware fits it. The cap roof reservation rises 6 mm; the lidar remains the tallest part.

Guide, gimbal, equalizer, lift latch and riser geometry are not included in the clearance pass. Their mass allowances are included. The ideal floor-following model does not demonstrate that a particular guide supplies its motion without binding. Retain the L 10 mm raised anti-tip requirement. No STL is released.

[Design and mechanism requirements](../../../docs/FLOATING_HEAD_DESIGN.md) · [Interactive review](floating_heads.html) · [Input data](../../../config/floating_heads.json)
