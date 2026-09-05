# =============================================================================
#  TidyBot -- PHASE 1 BENCH COUPON EXPORTER  (spec 0.2.0)
# =============================================================================
#  Geometry lives in cad/lib/coupon.py so the validator checks the same
#  shapes. This file only exports them.
#
#      freecadcmd generate_port_coupon.py       (or: make -C cad coupon)
#
#  Prints as generated -- no supports, no rotation in the slicer. Print
#  orientation is a spec, not a slicer setting (ADR 0005).
#
#  TAZ 6, 0.5 mm nozzle, PETG: 0.25 mm layers, 4 perimeters, 40% gyroid.
# =============================================================================

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "lib"))

from tidybot_port import PORT, derived, lock_plate            # noqa: E402
from coupon import build_module_coupon, build_base_coupon     # noqa: E402

OUT = _HERE


def _say(msg):
    print(msg)
    sys.stdout.flush()


def export(shape, name):
    shape.exportStl(os.path.join(OUT, name + ".stl"))
    shape.exportStep(os.path.join(OUT, name + ".step"))
    bb = shape.BoundBox
    _say("  %-24s %6.1f x %6.1f x %6.1f mm   %6.1f cm3"
         % (name, bb.XLength, bb.YLength, bb.ZLength, shape.Volume / 1000.0))
    if max(bb.XLength, bb.YLength) > 250.0 or bb.ZLength > 230.0:
        _say("  !! EXCEEDS TAZ 6 BUILD VOLUME -- see ADR 0005")


def main():
    d = derived()
    _say("TidyBot Phase 1 coupon -- TB-Port spec %s" % PORT["SPEC_VERSION"])
    _say("  posts at %s deg, sockets at %s deg (mirrored)"
         % ("/".join("%.0f" % a for a in PORT["POST_ANGLES"]),
            "/".join("%.0f" % a for a in d["SOCKET_ANGLES"])))
    export(build_module_coupon(), "coupon_module_face")
    export(build_base_coupon(),   "coupon_base_face")
    export(lock_plate(),          "coupon_lock_plate")
    _say("  (lock plate: steel or laser-cut for T4; a printed one is fine for T1-T3)")
    _say("\nAssembly + test procedure: docs/PHASE1_TEST_PLAN.md")
    _say("Steel BOM:                 make -C cad report")


main()
