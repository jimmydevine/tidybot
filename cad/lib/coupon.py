# =============================================================================
#  TidyBot -- Phase 1 bench coupon geometry
# =============================================================================
#  A TB-Port half welded onto a plain square plate with a grip hole, fixture
#  bolt holes and a load-test hole. Not part of any robot -- see
#  docs/PHASE1_TEST_PLAN.md.
#
#  Lives in lib/ rather than tests/ so that BOTH the generator and the
#  validator import the same geometry. The validator must check the artifact
#  that actually gets printed, not an idealised port that no one prints.
# =============================================================================

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tidybot_port import (PORT, derived, attach,          # noqa: E402
                          male_port_parts, female_port_parts)

PLATE       = 110.0   # square, comfortably inside the 250 mm TAZ 6 limit
PLATE_THK   = 6.0
GRIP_HOLE   = 25.0    # finger hole, so 50 mate cycles by hand aren't miserable
LOAD_HOLE   = 8.5     # M8 eye bolt, for hanging the 8 kg static load test
CORNER_HOLE = 5.5     # M5, bolts the coupon to a test fixture


def _fc():
    import Part
    import FreeCAD as App
    return Part, App


def _plate(z_top):
    """Square plate with its top face at z_top, growing downward."""
    Part, App = _fc()
    p = Part.makeBox(PLATE, PLATE, PLATE_THK,
                     App.Vector(-PLATE / 2.0, -PLATE / 2.0, z_top - PLATE_THK))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = p.cut(Part.makeCylinder(
                CORNER_HOLE / 2.0, PLATE_THK + 2.0,
                App.Vector(sx * (PLATE / 2.0 - 8.0), sy * (PLATE / 2.0 - 8.0),
                           z_top - PLATE_THK - 1.0), App.Vector(0, 0, 1)))
    return p


def build_male():
    """Male coupon: port boss up, plate below.

    The plate occupies z = -PLATE_THK..0, which is exactly where the kinematic
    ball sockets are. attach() fuses the plate first and re-cuts the sockets
    afterwards; a plain fuse() would fill them in.
    """
    Part, App = _fc()
    body = attach(_plate(0.0), male_port_parts())
    # Eye-bolt hole for the pull test, clear of the harness bore
    body = body.cut(Part.makeCylinder(
        LOAD_HOLE / 2.0, PLATE_THK + 2.0,
        App.Vector(0, PLATE / 2.0 - 12.0, -PORT["FLANGE_THK"] - PLATE_THK - 1.0),
        App.Vector(0, 0, 1)))
    return body


def build_female():
    """Female coupon: bore opening up, plate below.

    The plate sits entirely below the port body, so it does not overlap the
    vee pockets -- but it is routed through attach() anyway so the two coupons
    cannot drift apart in behaviour.
    """
    Part, App = _fc()
    d = derived()
    z_top = -(d["BORE_DEPTH"] + PORT["FLANGE_THK"])
    body = attach(_plate(z_top), female_port_parts())
    body = body.cut(Part.makeCylinder(
        GRIP_HOLE / 2.0, PLATE_THK + 2.0,
        App.Vector(0, PLATE / 2.0 - 22.0, z_top - PLATE_THK - 1.0),
        App.Vector(0, 0, 1)))
    return body
