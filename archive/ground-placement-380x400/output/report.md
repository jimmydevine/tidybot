# Vacuum-head clearance study

**Layout only; not for fabrication.**

Source measurements: `config/owned_parts.json`. Proposed allowances: `config/vacuum_head_layout.json`.

| Roller pair | Study width | Study depth | Roof reference | Fin-envelope gap | Panel span with proposed overlap |
|---|---:|---:|---:|---:|---:|
| 10 inch pair | 324 mm | 72 mm | 35 mm | 2 mm | 177 mm |
| 7.25 inch pair | 254.15 mm | 72 mm | 35 mm | 2 mm | 142.07 mm |

All footprint dimensions include a provisional 40 mm drive bay. Motor/transmission selection may change its dimensions.

Width = roller length + 2 × (wall + end-support bay + axial clearance) + drive bay.
Depth = roller diameter + center distance + 2 × (wall + front/rear clearance).
Roof reference = roller diameter + top clearance + roof thickness, with fin envelopes tangent to the floor.

- All allowances are designer proposals; roller and filter dimensions come from owned_parts.json.
- 30mm center spacing gives a 2mm gap between 28mm maximum fin envelopes. This is an unpowered clearance starting point, not an established cleaning setting.
- Roller fin envelopes are tangent to the floor in this study; contact compression and compliant mounting remain to design.
- The 40mm drive bay is a reservation without a selected motor or transmission. Its depth and height may grow.
- Roller end fittings are not modeled. The entire reported end-to-end length is represented with the maximum fin diameter for preliminary packaging.
- The filter is drawn separately, not installed in the roller cassette. Its exact pull-tab location is unknown.
- Cassette roof height excludes any extra intake plenum, duct, drive protrusion, fastener or latch. It is not the height of the complete powered head.
- The midpoint split and overlap describe panel spans only; joint fasteners, bearing alignment and strength are not designed.

The table assumes a midpoint panel split with a 15 mm overlap. This does not establish a structurally adequate joint.

The separate filter body is 136 × 76 × 14 mm. Its approximate 19 mm local depth assumes the tab rise is additional to the body; exact placement and grip/extraction clearance remain open.

No new owner question is needed for this envelope study. Detailed end fittings, drive selection, airflow, service routes and the full core/vacuum layout remain work to do.
