# M validation record

2026-09-14. Design calculations and allocation CAD only; no physical validation.

- System suite: **116 tests passed**, including nine new checks for mass partition, rigid transforms, virtual work, water placement, coupled equilibrium, suction accounting, raised contact and regression of earlier conflicts.
- Calculated **1,512 working and 168 raised cases**. Positive wheel/caster support, no wheel-stop contact, head travel within the proposed operating range and height plus 2 mm reserve below 180 mm in those cases.
- **28 geometry poses per module**; mop pad tested at both oscillation endpoints. Old layout exposes 13 vacuum / 8 mop moving/fixed conflict pairs; the M allocation proposal has zero sampled pairs and zero changed-static allocation overlaps.
- FreeCAD 1.1.3: four FCStd and four STEP scenes, **424 valid source shapes**. Fixed context exported as edges; moving allocations as solids. This validates allocation geometry construction, not actual hardware fit or STEP round-trip topology.
- Node DOM-stub check: **72 slider/module combinations** rendered without invalid numeric values. Generated raised-vacuum SVG rendered with QtSvg and visually inspected. This is not a full browser accessibility or interaction test.
- Local links in the M design document and report checked.

Limits: guide/pivot/latch/lift/risers absent from the geometry; actual narrowed brush/drive stacks, cable/flex-duct motion, local head moments, traction and step crossing unqualified. The L wheel-spring tolerance failures remain unresolved. The ideal head pose has no proven guide kinematics. New mechanism masses are allowances, not CAD-derived values. Shared-core changes require later sofa/duster integration.

## Input/output fingerprints

| File | SHA-256 |
|---|---|
| config/floating_heads.json | 390829fbcd8cb1bcaa96f27a11dab5aafaa19960d8f1c55546b54c06f461f931 |
| design/system/floating_heads.py | 806a70c039c8e6cd2bb5d36b5bfe580eaa6099efaa19a4dab9370838015ed45c |
| design/system/test_floating_heads.py | 9627c98176808517eb6115d68684ecfdf46820e42c0949f4325b23f2fcd0225d |
| design/system/export_floating_heads_freecad.py | 315503101189831ae19a27bbba996291cbfbd78c50f77d8d1266ab8d79dabe22 |
| design/system/floating_heads_viewer.html | 6e8f5806d1d09e3cf09528a88074bea176ace37226bfdfb4525285d2b43dd39c |
| design/system/output/floating_heads.json | cd08027cf5b8f92f05cba78807b2a9576f4d7f66408940a6a41dc722456acddc |
