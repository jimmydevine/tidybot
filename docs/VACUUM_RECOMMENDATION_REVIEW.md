# Vacuum recommendation based on the cleaning requirements

2026-09-13, revised after the owner's hair-priority clarification.
**Hair pickup is the primary objective; preventing hair accumulation on the
roller and its ends takes priority over simpler roller mechanics. Investigate
the Dreame TriCut first, alongside a serious comparison with brushes that shed
hair without cutting it.** The plain Roborock single rubber roller is now a
fallback. This is a change in investigation priority, not a final brush selection.
Retain the S7/S8 washable-filter candidate and provisional BIQU blower kit.
The ordered drivetrain, three-section architecture, automatic servicing and
275 × 275 × 180 mm limits remain in effect.

This is an engineering recommendation among the candidates reviewed, not proof
of superior pickup or a completed mechanical fit. Manufacturer claims for an
entire commercial robot do not establish the performance of its replacement
roller in our custom head. No new order or printable mount follows from this
review alone.

The [cassette and comparison plan](VACUUM_CASSETTE_PLAN.md) defines the next work:
compare TriCut with a matching Dreame plain roller in one head where compatible,
and make the complete head replaceable for other brush mechanisms.

**Order update, 2026-09-13:** the owner has ordered rollers, filters and the
blower kit. These remain unverified development components until received and
integrated; exact variants/quantities have not been reported. The
[current build plan](VACUUM_MODULE_NEXT_PASS.md) is the active work sequence.

## How the criteria change the choice

| Criterion | Consequence for this robot |
|---|---|
| Wood and tile, three heavily shedding dogs | First maximize hair delivered into the bin; then minimize retained hair, jams and manual detangling over repeated cleaning. A clean roller that leaves hair on the floor fails the primary objective. Carpet agitation is not a requirement. |
| Installed size and mass | Count the head, drive, bearings, floor-following movement, bin, filter holder, plenums and wiring. Neither roller length nor bare filter size proves fit. |
| Serviceability | Prevent accumulation as well as making it accessible. Make the roller and both ends accessible without removing the core. Make the bin and filter removable separately; routine filter washing can occur during the accepted manual servicing interval. |
| Replacement sourcing | Specify an OEM family and model reference, with replaceable printed end/filter adapters. Verify aftermarket alternatives individually rather than assigning OEM properties to an unknown kit. |
| Power and airflow | Choose the blower against total clean and loaded resistance. A filter rating does not specify pressure loss, and one roller does not by itself guarantee lower total energy use. |
| Automated operation | Preserve jam detection, bounded clearing attempts, bin evacuation and filter-presence detection. Automatic emptying does not eliminate filter or roller-end maintenance. |

## Roller comparison and recommendation

| Candidate | Evidence and tradeoff | Recommendation |
|---|---|---|
| Dreame TriCut replacement brush | Rubber brush with a built-in hair cutter; listed at 200.6 × 45.1 × 45.1 mm, 200 g and $49.99. These are supplier references, not an installed drawing or verified bare mass. Published brush-swap testing supports further investigation. | **First integration candidate.** Preserve the purchased cutter assembly; establish its end restraint, actuation and drive requirements before designing the mount. Not yet proven best for this robot. |
| Matching Dreame plain rubber brush, L40 Ultra / X40 Ultra compatibility family | Both OEM listings name the same host robots. Exact end parts and guard clearances still need verification. | **First comparison control.** Seek a roller-only swap in the TriCut cassette before building a second mechanism. See the cassette plan for source and sample cost. |
| Dreame HyperStream DuoBrush / Roborock DuoDivide | Different architectures intended to move hair off the rollers. Whole-robot testing gives a credible reason to compare them with cutting. Their supports, drive arrangement and suction opening must be integrated as a system. | **Serious competing approach.** Obtain the exact replacement assembly and interface information before choosing a family; do not treat these two systems as interchangeable. |
| Roborock single all-rubber main brush, S7/Q7 Max/Qrevo family | Finned rubber roller with removable caps/end bearing and documented maintenance. Fewer roller supports and no counter-rotation transmission. Exact drive load and mounting dimensions are unpublished in the reviewed sources. | **Fallback/reference.** Simpler mechanics alone no longer justify making this the leading choice. |
| iRobot 4639309 e/i/j complementary rubber pair | Available OEM replacements and brush-care instructions. Our short owned pair's 184.15 × 28 mm dimensions do not establish 4639309 geometry. | Retained comparison. Ownership alone does not establish pickup or resistance to hair accumulation. |

Sources: [Roborock S7 design and qualified manufacturer comparisons](https://us.roborock.com/pages/roborock-s7),
[S7 maintenance manual](https://support.roborock.com/hc/en-us/article_attachments/900008254623),
[iRobot roller pair](https://www.irobot.com/en_US/dual-multi-surface-rubber-brushes-for-roomba-combo-and-roomba-e,-i,-and-j-series-and-roomba-combo-10-max/4639309.html),
[iRobot brush care](https://support.irobot.co.uk/articles/en_GB/Knowledge/2451),
[Dreame TriCut specifications](https://www.dreametech.com/products/anti-tangle-roller-brush).
Manufacturer testimonials and whole-robot suction figures are not comparative
roller test data.

Fallback replacement reference: **Roborock SDZS05RR**, identified by the
[manufacturer's Japanese accessory catalog](https://jp.roborock.com/pages/accessories)
for the single rubber brush family. The
[US replacement listing](https://us.roborock.com/products/s7-main-brush) is
**$22.99** and lists compatible Qrevo, Q7 Max and S7 variants. Regional SKUs and
revisions still need matching before publishing a universal mount. The catalog
also links an Amazon Japan purchase route; a US Amazon brush offer was not
verified in this review. This is a consumer spare, not a motor component with
complete engineering drawings.

### Why investigate cutting, and what the evidence does not establish

[Vacuum Wars' L40 Ultra test](https://vacuumwars.com/dreame-l40-review/)
reported substantially better hair-pickup and tangle results after replacing
the standard brush with TriCut in the same robot. That is useful evidence for
the accessory, although the site's hair-test method was then still developing.

Cutting is not a guarantee of the lowest wrap. In its
[L60 Ultra PE/FE comparison](https://vacuumwars.com/dreame-l60-ultra-pe-review/),
the tester reported 0% wrap for HyperStream and 7% for TriCut in a seven-inch
hair test. These were different complete robots, not a controlled brush swap.
Neither result establishes performance with the owner's mix of short undercoat,
longer fur and clumps on wood/tile, or maintenance over many cleaning cycles.

Roborock's [DuoDivide explanation](https://au.roborock.com/pages/roborock-qrevo-2-pro)
describes two brush arms feeding a central opening and a 10% speed difference.
This makes the drive and inlet part of the mechanism, not just mounting details.
Its zero-tangle claim is qualified by a controlled test using 0.1 g of hair at
specified lengths; it is not evidence of maintenance-free operation with three
dogs. This mechanism is distinct from Dreame's tapered HyperStream pair.

### Integration requirements before selecting the brush

1. **Specify the complete replaceable mechanism.** For TriCut, establish the
   exact regional part/revision, drive socket, stationary end restraint and how
   rotation actuates the cutter. The reviewed public sources do not provide a
   dimensioned interface, required RPM, torque or cutter load. Do not assume a
   freely rotating bearing at each end is sufficient, or invent a cam design.
   Prefer an intact commercial cutter over a custom blade mechanism.
2. **Check the entire head.** The listed 200.6 mm length leaves 74.4 mm within
   the 275 mm body width before drive, supports, walls and clearances. This is
   only a preliminary width allowance. The 45.1 mm listed cross-section is not
   the complete head height or a verified rotating diameter. Model the guard,
   floor seal, inlet, drive and compliance for 4–10 mm transitions together;
   resolve the full 180 mm robot height. The previous cassette is superseded.
3. **Protect the ends and dirt passage.** Provide accessible end shields and
   bearings, a broad route from pickup to bin and station evacuation, and filter
   protection that does not become a hair-catching screen. Review the side
   brush hub too. Cutting wrapped strands does not by itself prevent a clump
   from bridging a chute or packing around an axle.
4. **Design for controlled operation and servicing.** Keep cutter contact
   enclosed by the assembly and head; only intended cleaning surfaces contact
   the wood. Use a removable underside cover and default-off drive when it is
   removed. Detect a stalled brush through suitable speed/current feedback;
   automatic clearing direction must respect the cutter's verified mechanism.
   Include blade/roller replacement access, power, mass and noise in selection.

Evaluate the resulting cleaning module using repeatable loads of the actual
dog hair on wood/tile. Record hair delivered into the bin, left on the floor,
retained on the roller/ends, and trapped elsewhere separately. Repeat cycles
without manually clearing the roller between each pass, recording interventions,
jam events and service time. Include bin evacuation and a partly loaded filter.
Do not claim zero wrap from one pass, or infer good pickup from an empty roller.
This is application validation of the assembled module, not a new expensive
stand for characterizing unidentified parts.

## Filter comparison and recommendation

**Prefer one genuine Roborock S7/S8-family washable filter as the first candidate**,
with **SDLW05RR** as the regional model reference. The preference is based on
documented maintenance and filtration classification, not a demonstrated
pressure-drop or size advantage over the owned filter.

Roborock describes the S7 filter as **E11**, with a footnote stating third-party
testing to EN 1822-1:2009. Its manual specifies rinsing and at least 24 hours of
air drying before reuse. Keep a second dry filter off the robot for servicing.
This does not specify an H13 filter or establish the custom robot's assembled
filtration efficiency; leaks around the frame still matter.
[Manufacturer rating and test footnote](https://us.roborock.com/pages/roborock-s7),
[maintenance instructions](https://support.roborock.com/hc/en-us/article_attachments/900008254623).

| Candidate | Reason to consider | Missing evidence / decision |
|---|---|---|
| Roborock S7/S8 washable family | Published E11 claim for the S7 filter, explicit wash/dry procedure and identified replacements. | **Preferred candidate**, subject to exact seal geometry, installed volume and airflow compatibility. No clean/loaded pressure-loss curve was found. |
| iRobot 4643682 s-series family / owned compatible filter | Retained comparison; the owned frame is 136 × 76 × 14 mm with a raised tab. | No established pressure-loss advantage from the large frame alone. Owned media quality is unidentified; OEM properties cannot be assigned to it. |
| iRobot 4639161 e/i/j family | An OEM alternative for a different holder shape; manufacturer lists it for $36.99/three-pack. | Do not select it just to shrink the frame, or assume two in parallel outperform another element. No clean/loaded curve was found. |

[iRobot compact-filter information](https://www.irobot.com/en_US/high-efficiency-filter%2C-3-pack-for-roomba-combo-and-roomba-i%2C-e%2C-and-j-series/4639161.html).
The s-series source and owned dimensions remain in the earlier
[selection record](VACUUM_COMPONENT_SELECTION.md).

The [US Roborock filter listing](https://us.roborock.com/products/roborock-washable-filter-x2-for-roborock-s7-series)
is **$32.99/two-pack**. [Amazon ASIN B08XZHW5ZQ](https://www.amazon.com/dp/B08XZHW5ZQ)
also identifies this family (Filter-A); the retrieved page includes an offer
sold by Roborock Technology Co. Ltd and shipped by Amazon, alongside conflicting
availability text. Verify the selected variant and live offer before ordering.
Its 5.55 × 2.48 × 1.46 inch listing dimensions are not a dimensioned drawing of
one installed element; do not use them to print a holder. Neither a smaller
installed envelope nor greater active media area has been verified here.

Provide a broad, accessible hair baffle before the fine filter, a continuous
perimeter gasket, and a removable filter adapter with clean-air connections.
Reserve pressure taps to help assess loading in the assembled module. Do not
equate washable with wet-pickup capability: this remains a dry vacuum bottom,
separate from the mop bottom. Avoid adding a cyclone or a fine pre-screen without
justifying its space, resistance and servicing burden.

## Blower and fit consequences

Keep **BIQU Universal Turbo Kit V1.0 / 1060000677**, with WS7040-24-V200 blower
and matched driver, as the provisional suction choice. Its
[public documentation](https://global.bttwiki.com/Universal%20Turbo%20Kit.html)
and the existing [curve comparison](../design/ground/output/vacuum_airflow_comparison.svg)
are a stronger basis than the unidentified owned blower. The conflicting
published curves, 24 V power conversion, default-off control, installed size and
noise remain unresolved as recorded in the earlier selection. Replacing the
filter does not validate the hypothetical system curves.

**Why the BIQU package:** it is a documented retail bundle of the Wonsmart
blower, matched brushless driver, printer-control adapter and cables, with
reference models. It is a sourcing option, not a required robot subsystem or
an established suction upgrade over the equivalent Wonsmart blower/driver.
The [BIQU packaging and wiring documentation](https://global.bttwiki.com/Universal%20Turbo%20Kit.html)
distinguishes the motor driver from the adapter for a printer fan-control port.
Our local controller can potentially command the driver through an appropriate
electrical interface without that adapter; levels, enable behavior and wiring
remain to verify. The kit's printer intake filter does not replace our sealed
dust filter, and its printer mounts do not determine our robot mounting.

A separately sourced Wonsmart blower with its specified driver is acceptable.
Compare total delivered cost and repeatable availability of that pair with the
kit. Do not substitute a bare motor for a complete controlled assembly.
The [Wonsmart WS7040 product page](https://www.wonsmartmotor.com/24v-high-pressure-small-air-blower-product/)
contains conflicting external/internal-driver descriptions, so exact supplied
electronics and the applicable curve need confirmation. The conflicting curves
in the earlier study do not prove that the BIQU adapter improves suction.

The TriCut listing plus the filter two-pack totals **$82.98**, compared with
**$55.98** for the fallback plain roller and the same filter pack. Both exclude
blower, drive, supports, seals, housing and shipping. These are comparison costs,
not complete subassembly orders. Reuse follows suitability and compatibility.

Next integration uses these candidates to resolve the complete cassette and
air-path dimensions, motor/transmission, holder, bin, blower, converter and
service paths together. The previous top view remains a **superseded dual-roller
study**, and its height/width figures do not prove fit of this revision. Keep the
275 × 275 × 180 mm envelope fixed, changing arrangement or candidate components
if needed. Final pickup, hair accumulation, filter loading and evacuation need
checking on the assembled cleaning module; no separate costly characterization
rig is proposed.
