# =============================================================================
#  TidyBot -- Phase 1 bench coupon geometry  (spec 0.2.0)
# =============================================================================
#  The TB-Port halves plus fixture holes. Not part of any robot -- see
#  docs/PHASE1_TEST_PLAN.md.
#
#  Lives in lib/ so BOTH the generator and the validator import the same
#  shapes. The validator must check the artifact that actually gets printed,
#  not an idealised port nobody prints. In v0.1 that distinction hid a bug
#  that removed every kinematic ball socket from the printed part.
# =============================================================================

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tidybot_port import (PORT, derived, attach,        # noqa: E402
                          module_port_parts, base_port_parts)

FIX_HOLE   = 5.5     # M5, fixture bolts and pull-test spreader
FIX_BC     = 120.0   # clear of the posts at Ø100
FIX_ANGLES = (60.0, 130.0, 180.0, 300.0)


def _fc():
    import Part
    import FreeCAD as App
    return Part, App


def _fixture_holes(body, z_top, thk):
    """M5 holes through the port plate, clear of every working feature."""
    Part, App = _fc()
    for a in FIX_ANGLES:
        r = FIX_BC / 2.0
        x = r * math.cos(math.radians(a))
        y = r * math.sin(math.radians(a))
        body = body.cut(Part.makeCylinder(
            FIX_HOLE / 2.0, thk + 2.0,
            App.Vector(x, y, z_top - thk - 1.0), App.Vector(0, 0, 1)))
    return body


def build_module_coupon():
    """Module-side coupon: plate, three tapered posts, connector cone.

    Routed through attach() so a host body can never back-fill the port's
    recesses -- the v0.1 failure.
    """
    Part, App = _fc()
    plate = Part.makeCylinder(PORT["PLATE_DIA"] / 2.0, PORT["PLATE_THK"],
                              App.Vector(0, 0, -PORT["PLATE_THK"]), App.Vector(0, 0, 1))
    body = attach(plate, module_port_parts())
    return _fixture_holes(body, 0.0, PORT["PLATE_THK"])


def build_base_coupon():
    """Base-side coupon: plate, three sockets, cone recess, drains, gasket groove."""
    Part, App = _fc()
    d = derived()
    depth = d["RECEPTACLE_DEPTH"] + PORT["PLATE_THK"]
    plate = Part.makeCylinder(PORT["PLATE_DIA"] / 2.0, depth,
                              App.Vector(0, 0, -depth), App.Vector(0, 0, 1))
    body = attach(plate, base_port_parts())
    return _fixture_holes(body, -depth + PORT["PLATE_THK"], PORT["PLATE_THK"])
