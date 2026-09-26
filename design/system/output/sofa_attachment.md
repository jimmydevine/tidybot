# Floor-resident sofa attachment comparison

**Preferred architecture to develop:** exchange the complete ordinary powered head for an external, floor-supported sofa extension. Share the vacuum drivetrain, bin, filter, blower, core and battery. Keep one extension on each floor. The extension is never part of the transfer-flight load.

This is a feasibility candidate. N remains conditional, and the automatic head interface is new work; the existing manual M3 cassette mount cannot perform this exchange. No new printable parts or purchase list are released.

## Complete carried mass at maximum modeled contents

| Configuration | Nominal mass | Meaning |
|---|---:|---|
| N vacuum before head-exchange hardware | 5.166 kg | Transfer assembly, no cap/lift |
| O vacuum ready for transfer | 5.275 kg | Core, battery, normal head and permanent exchange hardware; no extension/cap/lift |
| O ordinary floor vacuum | 5.345 kg | Same configuration with cap |
| O sofa cleaning on floor | 6.102 kg | With cap and one extension; normal head parked |
| One detached extension | 1.254 kg | Own cart, telescope, head, feed/lift hardware and interfaces |

All vacuum rows use 300 g debris in the existing shared bin. Transfer is **775 g above the 4.5 kg limit**. This architecture does not fix the underlying vacuum/core mass deficit. At usual 150 g debris, O transfer is 5.125 kg.

The flight increment is 93.84 g of body interface plus 15 g on the normal head, totaling **108.84 g**. The 482 g known head hardware and its new adapter stay in the nest during sofa work. Full existing M mount/lift/riser and N support allowances remain counted; overlapping scopes are not credited before a detailed replacement exists.

Extension estimate interval: 0.862 / 1.254 / 1.911 kg (low/nominal/high planning values, not statistical bounds). Whole-robot upper mass remains undefined because N has no upper replacement estimate. 2 resident extensions total 2.508 kg of inventory; only one attaches at a time, and zero fly. Station racks/shuttles are additional stationary hardware, outside these carried masses.

## Space and reach

| Quantity | Nominal reservation |
|---|---:|
| Ordinary rigid body and wheels | 275 × 275 × 180 mm |
| With extension retracted | 275 × 615 × 180 mm |
| Telescope travel | 1000 mm |
| Maximum leading-edge reach beyond sofa front | 980 mm versus 914.4 mm depth |
| Under-sofa working head / guide height | 38 / 40 mm |
| Straight floor space in front of sofa | 635 mm before clearance margin |
| Ideal stowed turning sweep | 912 mm diameter before clearance margin |
| One extension parking nest target | 270 × 450 × 140 mm |

The ordinary body remains inside the owner limit. The removable extension uses the explicit exception for extensions. Six 245 mm stages with 45 mm overlap give 1000 mm travel. Here the main body is 360 mm from the sofa front; the stowed head is only 20 mm away. These are different distances. Do not reuse the old internal-telescope model’s 80 mm body standoff or 335 mm stowed outline.

Working head/guide must lower before entering the 50 mm gap. Raising 12 mm gives a 52 mm guide envelope, too tall for that gap. The feed drive stays outside the sofa. Reach is axial and measured to the leading edge; the suction-mouth position is unfinished. Full stroke extends 66 mm past the nominal sofa back, so limit the commanded stroke for rear walls/obstructions. Sofa legs and underside obstructions may leave areas inaccessible; mapping and coverage checks remain necessary.

The telescope cannot simply occupy its old position within the ordinary vacuum. Nominal conflicts: vac_head, vac_flex, vac_duct, vac_bin_front. Move it outside the body, on its own supports. Receiver plate/air-face reservation intersections: []. That limited screen does not validate the moving receiver, latch, wiring, withdrawal path or finished joints.

## Airflow screen

| Assumed flow | Telescope + added coupler/link loss | Coupler K sensitivity |
|---|---:|---:|
| 0 L/s | 0 Pa | 0–0 Pa |
| 2 L/s | 59 Pa | 54–69 Pa |
| 3.6 L/s | 191 Pa | 175–223 Pa |
| 6 L/s | 530 Pa | 486–619 Pa |

Smooth-duct Darcy/minor-loss calculation inherited from the system model, with 150 mm extra 32 × 22 mm link. It excludes the head, common duct/bin/filter, joint leakage and hair blockage; it is not a blower operating point or a pickup prediction. The smallest telescope bore is only 31 × 19 mm (589 mm²). Flush seals and a cleanable path matter, and representative dog-hair clumps may force a larger bore or a different guide/hose arrangement.

Use one common air connection at a time. Park the roller cassette and insert the extension outlet, so the blower does not draw through an unused floor opening. Do not add an uncounted tee/diverter. Retain the common flex/duct and add the tool-side compliant link across the articulated hitch.

## What remains to resolve

- Complete the receiver, positive locks, tool-support/load path, electrical contacts and air seals together. Preserve the ordinary head’s floor following; a rigid latch cannot replace its compliance.
- Specify an articulated, yaw-constrained cart connection and floor support. Check retracted/extended balance, wet-floor traction, turning and all 4–10 mm thresholds. Existing wheel-drive results are not validation for the roughly 6.1 kg sofa configuration.
- Complete telescope guides, seal clearances, feed-strip routing, lift, wiring, obstruction detection and retrieval. Existing function masses are retained estimates, not finished mechanisms.
- Allocate a supported external tool-exchange apron at each station. The 615 mm combination cannot be assumed to fit the old 275 mm robot bay. Parking-nest dimensions alone do not specify the entire station footprint.
- Establish blower operating flow with the actual filter, head, link and staged duct. Preserve hair pickup before claiming battery endurance. Shared battery powers the attachment; feed/lift and added drag remain to validate. No additional carried battery is assumed.
- Reduce the ordinary vacuum/core mass to the 4.5 kg transfer budget including its completed quick-change interface.

## Confirmed room space and receiver follow-up

The owner answered **yes** to approximately 650 mm of clear floor in front of each sofa and 1 m of nearby turning space. The nominal envelope leaves only 15 mm of front-space difference and about 88 mm across the turning diameter; these rough figures are not measured operating margins. Sofa legs, navigation tolerances and station-apron space still need their own layout checks.

The original receiver-plate reservations intersected head envelopes in 74 sampled head/plate pairs. The same plates now sit at minimum corners [24.5,40,68] and [249,40,68] mm, against the outer faces of the existing side rails. They have no envelope intersections across 105 sampled terrain/raised poses, with a minimum sampled box gap of 2.86 mm. Plate stock and complete carried-mass accounting are unchanged.

A level, supported 100 mm forward withdrawal of the normal head/motor boxes has 0 intersections against the checked fixed allocations and receiver/air-face reservations. Their rear edges end 34 mm ahead of the body front. This establishes a candidate straight shuttle direction, not a finished automatic head exchange. Dock-located support, removable adapter/compliance, positive locks, connector engagement and air-flex disconnection remain to detail.

For the extension, the same proposed withdrawal clears its reserved air-face tail by 16.5 mm ahead of the body, while robot plus tool occupy 715 mm longitudinally before margins. This is a station handling envelope, separate from the confirmed sofa approach space. The extension adapter/hitch withdrawal geometry remains incomplete.

[Architecture and automatic sequence](../../../docs/SOFA_ATTACHMENT.md) · [Receiver drawing](sofa_head_receiver.svg) · [Interactive layout](sofa_attachment.html) · [Incremental hardware ledger](sofa_attachment_mass.csv) · [Inputs](../../../config/sofa_attachment.json)
