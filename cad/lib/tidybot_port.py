# =============================================================================
#  TidyBot -- TB-Port interface geometry  (SPEC VERSION 0.1.0)
# =============================================================================
#  THE authoritative definition of the module interface. Every module in the
#  project imports this file and calls male_port() or female_port(). Nothing
#  anywhere else may re-declare a port dimension.
#
#  Prose rationale for these numbers: docs/INTERFACE.md
#
#  Usage from a FreeCAD generator script:
#      import sys, os
#      sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
#      from tidybot_port import PORT, male_port, female_port
#
#  The PORT dict and derived() are importable with plain CPython (no FreeCAD),
#  so firmware and test tooling can read the same numbers:
#      python3 -c "from tidybot_port import PORT; print(PORT['BOSS_DIA'])"
#
#  COORDINATE CONVENTION -- both halves are built in their natural PRINT
#  orientation, features growing +Z off the bed:
#
#      male_port()   flange body z = -FLANGE_THK .. 0, boss grows +Z (boss up)
#      female_port() flange face at z = 0, body grows -Z, bore opens upward
#
#  To mate, one half is flipped. Both print as-generated with no supports.
# =============================================================================

import math

SPEC_VERSION = "0.1.0"

# ----------------------------------------------------------------------------
#  PARAMETERS -- the interface. Changing anything here is a spec change:
#  bump SPEC_VERSION, update docs/INTERFACE.md, and `make all` to regenerate.
# ----------------------------------------------------------------------------
PORT = dict(
    SPEC_VERSION      = SPEC_VERSION,

    # --- Flange (the outer disc that carries the kinematic coupling) --------
    FLANGE_DIA        = 90.0,
    FLANGE_THK        = 8.0,

    # --- Boss / bore (coarse alignment + latch) -----------------------------
    BOSS_DIA          = 50.0,
    BOSS_LEN          = 22.0,
    BORE_CLEARANCE    = 0.40,   # diametral: bore = BOSS_DIA + this
    TIP_CHAMFER       = 2.0,    # lead-in on the boss tip

    # --- Capture funnel ------------------------------------------------------
    CAPTURE_LATERAL   = 8.0,    # mm of lateral misalignment absorbed
    FUNNEL_ANGLE      = 35.0,   # degrees from the mate axis

    # --- Kinematic coupling (3 balls into 3 dowel-pin vees) ------------------
    KC_BALL_DIA       = 8.0,
    KC_DOWEL_DIA      = 3.0,
    KC_DOWEL_SPACING  = 7.0,    # tangential centre-to-centre of the vee pair
    KC_BOLT_CIRCLE    = 70.0,
    KC_ANGLES         = (90.0, 210.0, 330.0),
    KC_PROTRUSION     = 3.0,    # ball height above the male flange face
    KC_SOCKET_DIA     = 8.2,    # epoxy socket in the male flange
    FLANGE_GAP        = 1.0,    # designed air gap when seated -- the balls
                                # carry the load, NOT the plastic faces

    # --- Latch (ball detent) -------------------------------------------------
    DETENT_Z          = 16.0,   # groove centre, above the male flange face
    DETENT_DEPTH      = 2.0,    # radial depth of the groove
    DETENT_BALL_DIA   = 6.0,
    DETENT_ANGLES     = (30.0, 150.0, 270.0),

    # --- Keying (defeats the coupling's 3-fold symmetry) --------------------
    KEY_DIA           = 5.0,
    KEY_BC            = 36.0,   # on the boss end face
    KEY_ANGLE         = 180.0,
    KEY_PROTRUSION    = 6.0,    # engages BEFORE the electrical contacts

    # --- Electrical contacts (on the boss end face, recessed & protected) ----
    CONTACT_BC        = 36.0,
    CONTACT_ANGLE     = 0.0,
    CONTACT_W         = 24.0,   # 8 pins @ 2.54 mm + margin
    CONTACT_L         = 10.0,
    CONTACT_DEPTH     = 1.6,    # pad PCB recess on the male half
    CONTACT_POGO_DEPTH= 6.0,    # pogo block pocket on the female half

    # --- Services ------------------------------------------------------------
    WIRE_BORE_DIA     = 20.0,   # central pass-through for the harness
)


# ----------------------------------------------------------------------------
#  DERIVED GEOMETRY
#  The vee-groove depths follow from ball and dowel size by trigonometry, so
#  changing KC_BALL_DIA or KC_DOWEL_SPACING re-solves the pockets automatically
#  instead of silently invalidating a hand-entered depth.
# ----------------------------------------------------------------------------
def derived(p=None):
    p = p or PORT
    d = {}

    r_ball  = p["KC_BALL_DIA"] / 2.0
    r_dowel = p["KC_DOWEL_DIA"] / 2.0
    half_sp = p["KC_DOWEL_SPACING"] / 2.0

    # A ball resting on two parallel dowels: its centre sits this far above the
    # plane containing the two dowel axes.
    contact = r_ball + r_dowel
    if half_sp >= contact:
        raise ValueError(
            "KC_DOWEL_SPACING (%.2f) is too wide for a %.1f mm ball -- the ball "
            "would fall through between the dowels." % (p["KC_DOWEL_SPACING"], p["KC_BALL_DIA"])
        )
    d["KC_BALL_ABOVE_DOWELS"] = math.sqrt(contact**2 - half_sp**2)

    # In the FEMALE local frame (flange face z = 0, body growing -Z):
    #   seated ball centre sits FLANGE_GAP below the male face, which is
    #   KC_PROTRUSION above it -> ball centre is this far below the female face.
    d["KC_BALL_CENTRE_Z"] = -(p["KC_PROTRUSION"] - p["FLANGE_GAP"])
    d["KC_DOWEL_AXIS_Z"]  = d["KC_BALL_CENTRE_Z"] - d["KC_BALL_ABOVE_DOWELS"]

    # Pocket floor must clear the bottom of the seated ball, or the plastic
    # takes the load instead of the steel and the coupling is meaningless.
    ball_bottom = d["KC_BALL_CENTRE_Z"] - r_ball
    d["KC_POCKET_DEPTH"] = abs(ball_bottom) + 1.0

    # Bore and funnel
    d["BORE_DIA"]     = p["BOSS_DIA"] + p["BORE_CLEARANCE"]
    d["FUNNEL_MOUTH"] = d["BORE_DIA"] + 2.0 * p["CAPTURE_LATERAL"]
    d["FUNNEL_DEPTH"] = p["CAPTURE_LATERAL"] / math.tan(math.radians(p["FUNNEL_ANGLE"]))
    d["BORE_DEPTH"]   = p["BOSS_LEN"] - p["FLANGE_GAP"] + 2.0
    # Air below the seated boss tip. Must stay positive, or the boss bottoms
    # out on the bore floor and the kinematic coupling never seats.
    d["TIP_CLEARANCE"] = d["BORE_DEPTH"] - p["BOSS_LEN"] + p["FLANGE_GAP"]

    # Parallel (non-funnel) engagement length -- the part that actually resists
    # tilt. If this goes small, the funnel is eating the joint's stiffness.
    d["ENGAGEMENT"] = d["BORE_DEPTH"] - d["FUNNEL_DEPTH"]
    if d["ENGAGEMENT"] < 6.0:
        raise ValueError(
            "Only %.1f mm of parallel engagement left after the funnel. Increase "
            "BOSS_LEN, steepen FUNNEL_ANGLE, or reduce CAPTURE_LATERAL."
            % d["ENGAGEMENT"]
        )

    # Detent ball centre height in the female frame
    d["DETENT_Z_FEMALE"] = -(p["DETENT_Z"] - p["FLANGE_GAP"])
    return d


# ----------------------------------------------------------------------------
#  FREECAD GEOMETRY
#  Imported lazily so this module stays usable under plain CPython.
# ----------------------------------------------------------------------------
def _fc():
    import Part
    import FreeCAD as App
    return Part, App


def _polar(radius, angle_deg):
    a = math.radians(angle_deg)
    return radius * math.cos(a), radius * math.sin(a)


def _rotated(shape, angle_deg):
    """Copy a shape and spin it about Z. Copy first -- rotate() mutates."""
    _, App = _fc()
    s = shape.copy()
    s.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle_deg)
    return s


def male_port_parts(p=None):
    """Return (additive_solid, [cut_tools]) for the male half.

    Use this -- not male_port() -- whenever the port is fused onto a larger
    body. Fuse the additive solid FIRST, subtract the cut tools LAST.

    Fusing a host body over an already-finished port back-fills its ball
    sockets and recesses with solid material, silently and with no error.
    attach() below does the ordering for you.
    """
    Part, App = _fc()
    p = p or PORT
    Z = App.Vector(0, 0, 1)
    O = App.Vector(0, 0, 0)
    tip = p["BOSS_LEN"]
    cuts = []

    # --- additive ---------------------------------------------------------
    flange = Part.makeCylinder(p["FLANGE_DIA"] / 2.0, p["FLANGE_THK"],
                               App.Vector(0, 0, -p["FLANGE_THK"]), Z)
    boss = Part.makeCylinder(p["BOSS_DIA"] / 2.0, p["BOSS_LEN"], O, Z)
    body = flange.fuse(boss)

    # --- subtractive ------------------------------------------------------
    # Lead-in chamfer on the boss tip
    ch = p["TIP_CHAMFER"]
    ring = Part.makeCylinder(p["BOSS_DIA"] / 2.0 + 1.0, ch + 0.1,
                             App.Vector(0, 0, tip - ch), Z)
    cone = Part.makeCone(p["BOSS_DIA"] / 2.0 - ch, p["BOSS_DIA"] / 2.0, ch,
                         App.Vector(0, 0, tip - ch), Z)
    cuts.append(ring.cut(cone))

    # Latch detent groove
    cuts.append(Part.makeTorus(p["BOSS_DIA"] / 2.0, p["DETENT_DEPTH"],
                               App.Vector(0, 0, p["DETENT_Z"]), Z))

    # Kinematic coupling ball sockets (flat-bottom, balls epoxied in).
    # These sit in the flange face -- exactly the region a host body overlaps,
    # which is why cut ordering matters.
    socket_depth = p["KC_BALL_DIA"] - p["KC_PROTRUSION"]
    for ang in p["KC_ANGLES"]:
        x, y = _polar(p["KC_BOLT_CIRCLE"] / 2.0, ang)
        cuts.append(Part.makeCylinder(
            p["KC_SOCKET_DIA"] / 2.0, socket_depth + 0.5,
            App.Vector(x, y, -socket_depth), Z))

    # Keying pin bore (Ø5 dowel pressed in, protruding past the tip)
    kx, ky = _polar(p["KEY_BC"] / 2.0, p["KEY_ANGLE"])
    cuts.append(Part.makeCylinder(4.9 / 2.0, 10.0,
                                  App.Vector(kx, ky, tip - 10.0), Z))

    # Contact pad PCB recess on the boss end face
    cx, cy = _polar(p["CONTACT_BC"] / 2.0, p["CONTACT_ANGLE"])
    cuts.append(Part.makeBox(
        p["CONTACT_W"], p["CONTACT_L"], p["CONTACT_DEPTH"] + 0.1,
        App.Vector(cx - p["CONTACT_W"] / 2.0, cy - p["CONTACT_L"] / 2.0,
                   tip - p["CONTACT_DEPTH"])))

    # Central harness pass-through
    cuts.append(Part.makeCylinder(
        p["WIRE_BORE_DIA"] / 2.0, p["FLANGE_THK"] + p["BOSS_LEN"] + 2.0,
        App.Vector(0, 0, -p["FLANGE_THK"] - 1.0), Z))
    return body, cuts


def male_port(p=None):
    """Male half as a standalone finished solid.

    Flange body at z = -FLANGE_THK..0, boss growing +Z. Prints as generated,
    boss up, no supports.
    Requires: 3 x Ø8 balls (epoxy), 1 x Ø5 dowel (press), pad PCB.

    Do NOT fuse a host body onto the result -- use attach() instead.
    """
    return _resolve(male_port_parts(p))


def female_port_parts(p=None):
    """Return (additive_solid, [cut_tools]) for the female half.

    Same ordering rule as male_port_parts(): fuse additive first, cut last.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    cuts = []

    # --- additive ---------------------------------------------------------
    depth = d["BORE_DEPTH"] + p["FLANGE_THK"]
    body = Part.makeCylinder(p["FLANGE_DIA"] / 2.0, depth,
                             App.Vector(0, 0, -depth), Z)

    # --- subtractive ------------------------------------------------------
    # Bore + capture funnel
    cuts.append(Part.makeCylinder(
        d["BORE_DIA"] / 2.0, d["BORE_DEPTH"] + 0.1,
        App.Vector(0, 0, -d["BORE_DEPTH"]), Z))
    cuts.append(Part.makeCone(
        d["FUNNEL_MOUTH"] / 2.0, d["BORE_DIA"] / 2.0, d["FUNNEL_DEPTH"],
        App.Vector(0, 0, -d["FUNNEL_DEPTH"]), Z))

    # Kinematic vee pockets: a slot, crossed by two radial dowels the ball
    # rests on. The dowels are supported at both ends by the pocket walls.
    pk_d   = d["KC_POCKET_DEPTH"]
    pk_len = p["KC_BALL_DIA"] + 12.0
    pk_wid = p["KC_DOWEL_SPACING"] + p["KC_DOWEL_DIA"] + 6.0
    for ang in p["KC_ANGLES"]:
        r = p["KC_BOLT_CIRCLE"] / 2.0
        pocket = Part.makeBox(pk_len, pk_wid, pk_d + 0.1,
                              App.Vector(r - pk_len / 2.0, -pk_wid / 2.0, -pk_d))
        cuts.append(_rotated(pocket, ang))
        for side in (-1.0, 1.0):
            ch = Part.makeCylinder(
                p["KC_DOWEL_DIA"] / 2.0 + 0.05, pk_len + 14.0,
                App.Vector(r - pk_len / 2.0 - 7.0,
                           side * p["KC_DOWEL_SPACING"] / 2.0,
                           d["KC_DOWEL_AXIS_Z"]),
                App.Vector(1, 0, 0))
            cuts.append(_rotated(ch, ang))

    # Latch detent: radial through-holes for the Ø6 balls, backed by a collar
    for ang in p["DETENT_ANGLES"]:
        hole = Part.makeCylinder(
            p["DETENT_BALL_DIA"] / 2.0 + 0.1, p["FLANGE_DIA"],
            App.Vector(0, 0, d["DETENT_Z_FEMALE"]), App.Vector(1, 0, 0))
        cuts.append(_rotated(hole, ang))

    # Keying pin clearance -- deliberately loose
    kx, ky = _polar(p["KEY_BC"] / 2.0, p["KEY_ANGLE"])
    cuts.append(Part.makeCylinder(
        5.3 / 2.0, 12.0, App.Vector(kx, ky, -d["BORE_DEPTH"] - 6.0), Z))

    # Pogo pin block pocket
    cx, cy = _polar(p["CONTACT_BC"] / 2.0, p["CONTACT_ANGLE"])
    cuts.append(Part.makeBox(
        p["CONTACT_W"] + 1.0, p["CONTACT_L"] + 1.0, p["CONTACT_POGO_DEPTH"],
        App.Vector(cx - (p["CONTACT_W"] + 1.0) / 2.0,
                   cy - (p["CONTACT_L"] + 1.0) / 2.0,
                   -d["BORE_DEPTH"] - p["CONTACT_POGO_DEPTH"] + 0.1)))

    # Central harness pass-through
    cuts.append(Part.makeCylinder(
        p["WIRE_BORE_DIA"] / 2.0, depth + 2.0,
        App.Vector(0, 0, -depth - 1.0), Z))
    return body, cuts


def female_port(p=None):
    """Female half as a standalone finished solid.

    Flange face at z = 0, body growing -Z, bore opening upward. Prints as
    generated, bore up, no supports.
    Requires: 6 x Ø3 dowels (vees), 3 x Ø6 balls + collar (latch), pogo block.

    Do NOT fuse a host body onto the result -- use attach() instead.
    """
    return _resolve(female_port_parts(p))


def _resolve(parts):
    body, cuts = parts
    for c in cuts:
        body = body.cut(c)
    return body


def attach(host, parts):
    """Fuse a port onto a host body with the correct cut ordering.

    ALWAYS use this instead of host.fuse(male_port()). Fusing a host over a
    finished port back-fills its ball sockets with solid material -- no error,
    no warning, just a part that cannot work.
    """
    body, cuts = parts
    out = host.fuse(body)
    for c in cuts:
        out = out.cut(c)
    return out


def latch_collar(p=None):
    """v0.1 hand-operated collar: a plain ring that traps the detent balls.

    Slides down over the female flange to lock, lifts to release. Powered
    actuation is v0.2, deliberately deferred until the coupling is validated.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)

    h  = 16.0
    id_ = p["FLANGE_DIA"] + 0.6
    od  = id_ + 2 * 4.0
    ring = Part.makeCylinder(od / 2.0, h, App.Vector(0, 0, 0), Z)
    ring = ring.cut(Part.makeCylinder(id_ / 2.0, h + 2.0, App.Vector(0, 0, -1), Z))
    # Relief pockets so the balls can retract when the collar is lifted
    for ang in p["DETENT_ANGLES"]:
        pocket = Part.makeCylinder(
            p["DETENT_BALL_DIA"] / 2.0 + 0.6, 6.0,
            App.Vector(id_ / 2.0 - 1.0, 0, h - 4.0), App.Vector(1, 0, 0))
        ring = ring.cut(_rotated(pocket, ang))
    return ring


def report(p=None):
    """Print the derived geometry. Run under plain python3 to sanity-check a
    parameter change before committing to an 8-hour print."""
    p = p or PORT
    d = derived(p)
    print("TB-Port spec %s" % p["SPEC_VERSION"])
    print("  bore                 Ø%.2f mm" % d["BORE_DIA"])
    print("  funnel mouth         Ø%.2f mm  (capture ±%.1f mm)"
          % (d["FUNNEL_MOUTH"], p["CAPTURE_LATERAL"]))
    print("  funnel depth          %.2f mm  @ %.0f deg" % (d["FUNNEL_DEPTH"], p["FUNNEL_ANGLE"]))
    print("  parallel engagement   %.2f mm" % d["ENGAGEMENT"])
    print("  tip clearance         %.2f mm" % d["TIP_CLEARANCE"])
    print("  ball above dowels     %.3f mm" % d["KC_BALL_ABOVE_DOWELS"])
    print("  vee dowel axis z      %.3f mm (female frame)" % d["KC_DOWEL_AXIS_Z"])
    print("  vee pocket depth      %.3f mm" % d["KC_POCKET_DEPTH"])
    print("  detent ball z         %.3f mm (female frame)" % d["DETENT_Z_FEMALE"])
    print("\nBill of materials per mated pair:")
    print("  3 x Ø%.0f bearing ball   (kinematic, epoxy into male flange)" % p["KC_BALL_DIA"])
    print("  6 x Ø%.0f dowel pin      (vee grooves, female flange)" % p["KC_DOWEL_DIA"])
    print("  3 x Ø%.0f bearing ball   (latch detent, female bore)" % p["DETENT_BALL_DIA"])
    print("  1 x Ø%.0f dowel pin      (key, press into male boss)" % p["KEY_DIA"])
    print("  1 x 8-way pogo block + mating pad PCB")


if __name__ == "__main__":
    report()
