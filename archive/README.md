# Archived design work

The earlier project was moved into [previous-design/](previous-design/) on 2026-09-05
so the active repository contains the current three-section design and its example
configuration. This material is historical reference, not current requirements.

A later snapshot of the [380 × 400 mm ground placement](ground-placement-380x400/README.md)
preserves the layout superseded by the owner's 275 × 275 × 180 mm size limits.

| Location | Archived material |
|---|---|
| [Project README](previous-design/README.md) | README snapshot from before cleanup, including the earlier design and build instructions |
| [CAD](previous-design/cad/) | TB-Port generators, hardware helpers, Makefile, test coupons and existing generated geometry |
| [Documents](previous-design/docs/) | Earlier requirements, roadmap, interface, coupling study, test plan and architecture decisions |
| [Tests](previous-design/tests/) | Phase 1 bench-results template |
| `previous-design/firmware/`, `previous-design/ros2_ws/` | Existing empty development scaffolding, preserved locally |

The working copies were moved, including uncommitted CAD edits. Relative directory
structure is preserved. Links from the README snapshot to current design documents
have been adjusted for its new location. Other archived file contents are unchanged.

Run historical commands from `archive/previous-design/`, or use a path such as:

```sh
make -C archive/previous-design/cad report
```

The former `.gitignore` and `.gitattributes` are scoped inside `previous-design/`.
Generated geometry and Python caches remain present locally and ignored, as before;
moving them does not make them tracked release artifacts. Git does not track empty
directories, so the empty firmware/ROS scaffolding will not appear in a fresh clone.

Return to the [current project](../README.md) for active design work.
