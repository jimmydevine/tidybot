# TidyBot

A modular household robot. One mobile base carrying compute, sensing, power and drive,
plus interchangeable tool modules that attach above and below it. A docking station
charges the base and swaps its modules unattended.

## Where to start

| Document | What it is |
|---|---|
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phases and exit criteria. **Read this first.** |
| [docs/INTERFACE.md](docs/INTERFACE.md) | The TB-Port spec. The single most important document here. |
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Mass, power, envelope and cost budgets |
| [docs/decisions/](docs/decisions/) | Architecture Decision Records — *why* things are the way they are |
| [docs/PHASE1_TEST_PLAN.md](docs/PHASE1_TEST_PLAN.md) | What to build and measure next |

## The central idea

For a modular robot, **the interface spec is the project.** Every module ever built is
downstream of it. Get the port right and modules can be designed independently, in any
order, for years. Get it wrong and you find out on module #4, when fixing it means
reprinting everything.

So the port is Phase 1, and it is bench-tested as a 110 mm coupon before any robot exists.

Two rules follow from that and shape everything else:

- **Modules are passive.** No drive, no latch actuator, no battery. Motors, actuators and
  intelligence live in the base, which you build once. This is what keeps a tool module
  at $40 instead of $200 — and that cost difference is what decides whether you end up
  with six modules or two.
- **Precision comes from steel, not plastic.** Printed parts are bulk and rough
  alignment. Bearing balls and dowel pins do the locating. See
  [ADR 0005](docs/decisions/0005-print-constraints-taz6.md).

## CAD

Parts are generated from parametric Python, headless, via FreeCAD. The port geometry
exists in exactly one place — [cad/lib/tidybot_port.py](cad/lib/tidybot_port.py) — and
every module imports it, so a spec change regenerates the whole fleet.

```sh
make -C cad report    # derived dimensions + BOM (plain python3, no FreeCAD needed)
make -C cad check     # validate the port geometry -- cheap, run it first
make -C cad coupon    # generate the Phase 1 bench coupons
make -C cad all       # check + coupon
```

### Headless FreeCAD

`make` needs FreeCAD's **headless** binary. It searches `PATH` for `freecadcmd`,
`freecad.cmd` or `FreeCADCmd`, then falls back to `~/Applications/FreeCAD-*/usr/bin/freecadcmd`.
Override with `make FREECAD=/path/to/freecadcmd`.

The official **AppImage has no usable headless entry point from the outside**:
`--console` drops into an interactive shell that never exits, and there is no argv0
dispatch, so symlinking the AppImage just launches the GUI. Extract it once and use the
binary inside:

```sh
cd ~/Applications
./FreeCAD_1.1.3-x86_64.AppImage --appimage-extract
mv squashfs-root FreeCAD-1.1.3
ln -sf ~/Applications/FreeCAD-1.1.3/usr/bin/freecadcmd ~/.local/bin/
```

The GUI is only for *inspecting* results — open the generated `.step` files. The model
lives in the generator scripts, not in any `.FCStd`.

### One rule when building modules

To put a port on a module body, use `attach()` — never `body.fuse(male_port())`:

```python
from tidybot_port import attach, male_port_parts
part = attach(my_module_body, male_port_parts())
```

`male_port()` returns a *finished* solid. Fusing a body onto it unions material straight
back into the kinematic ball sockets — silently, with no error, producing a part that
looks right and cannot work. `attach()` fuses the additive geometry first and re-applies
the cuts last. This already bit the Phase 1 coupon once.

`make check` is a real regression test, not a formality. It asserts the property the
coupling depends on — that when seated, the two printed halves never touch, so all load
passes through steel. It also catches bottoming-out, insufficient engagement after the
capture funnel, and parts that exceed the TAZ 6 build volume.

## Hardware context

Printer: LulzBot TAZ 6, 280 × 280 × 250 mm, **0.5 mm nozzle**. That nozzle is the binding
mechanical constraint on the whole project and is why precision surfaces are steel.
Design rules: [ADR 0005](docs/decisions/0005-print-constraints-taz6.md).

## Status

Phase 0 complete. Phase 1 (port bench validation) is next — nothing else should be
designed until `SPEC_VERSION` reaches 1.0.0.
