# =============================================================================
#  TidyBot -- PHASE 1 BENCH COUPON EXPORTER
# =============================================================================
#  Geometry lives in cad/lib/coupon.py so the validator can check the same
#  shapes. This file only exports them.
#
#      freecadcmd generate_port_coupon.py       (or: make -C cad coupon)
#
#  Prints as generated -- no supports, no rotation in the slicer. Print
#  orientation is a spec, not a slicer setting (ADR 0005).
#
#  Suggested slicer settings (TAZ 6, 0.5 mm nozzle, PETG):
#      layer 0.25 mm | 4 perimeters | 40% gyroid | no supports
# =============================================================================

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "lib"))

from tidybot_port import PORT, latch_collar          # noqa: E402
from coupon import build_male, build_female          # noqa: E402

OUT = _HERE


def _say(msg):
    print(msg)
    sys.stdout.flush()


def export(shape, name):
    shape.exportStl(os.path.join(OUT, name + ".stl"))
    shape.exportStep(os.path.join(OUT, name + ".step"))
    bb = shape.BoundBox
    _say("  %-22s %6.1f x %6.1f x %6.1f mm"
         % (name, bb.XLength, bb.YLength, bb.ZLength))
    if max(bb.XLength, bb.YLength) > 250.0 or bb.ZLength > 230.0:
        _say("  !! EXCEEDS TAZ 6 BUILD VOLUME -- see ADR 0005")


def main():
    _say("TidyBot Phase 1 coupon -- TB-Port spec %s" % PORT["SPEC_VERSION"])
    export(build_male(),   "coupon_port_male")
    export(build_female(), "coupon_port_female")
    export(latch_collar(), "coupon_latch_collar")
    _say("\nAssembly + test procedure: docs/PHASE1_TEST_PLAN.md")
    _say("Steel BOM:                 make -C cad report")


main()
