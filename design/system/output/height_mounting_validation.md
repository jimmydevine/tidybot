# I validation record — 2026-09-14

Status: candidate packaging study; no physical validation or fabrication release.

- `python3 design/system/height_mounting.py`: generated data, report and viewer.
  No changed-component or upper caster service-space conflicts across the three
  ground layouts. All existing bin/tank targets pass the volume screen.
- `python3 -m unittest discover -s design/system -p 'test_*.py' -q`:
  **82 tests passed**. New adverse cases restore the tall connector, lower each
  affected rear component, introduce a mop-only height obstruction and increase
  nut height. These demonstrate that the relevant failure checks trigger.
- Height sampling: 2,592 poses per bottom plus 225 local refinement poses per
  bottom. Independent wheel travel spans −2.5 to +10 mm; coarse caster headings
  use 5° increments. This is not continuous-envelope or contact-equilibrium proof.
- `freecadcmd design/system/export_height_mounting_freecad.py`:
  **356 valid shapes** across vacuum (122), mop (112) and sofa (122), with native
  FreeCAD and STEP exports. Native archive integrity checks passed. FreeCAD
  reported inability to write its user cache/preferences outside the workspace;
  the model exports completed and their archives are intact.
- Generated viewer JavaScript executed with Node and a minimal DOM harness for
  all three module selections, with previous-placement outlines on and off.
  No NaN/undefined geometry; the 179.35 mm reserved height is displayed.
- Extracted side and caster SVGs parsed/rendered with QtSvg and were visually
  inspected. A full browser interaction/layout check was not performed.
- All five input-file SHA-256 hashes match the generated data. Local review-file
  links were checked. Tracked diff whitespace check passed.

The C1 mechanical drawing, optical enclosure and mounting-hole pattern were
visually read from the manufacturer's revision 1.1 datasheet distributed by
Seeed. The current manufacturer download points to revision 1.2, but that endpoint
returned HTTP 403. Confirm the supplied revision before mounting-hole release.
The TENTE fitting datasheet supplies its M8 × 15 thread, 6 mm added height and
20 g mass; nut/washer/tool-space sizes remain procurement reservations.

Still open: exact caster/fitting pairing and pull-out retention, continuous
suspension envelope and tolerances, lidar support attachments, lift connector
mating/cables, moving motor trays, spring seats/stops and rail/seat joints.
The C1 substitution has not been validated for mapping performance or lift-frame
visibility. G complete mass estimates remain separate from provisional I deltas.
