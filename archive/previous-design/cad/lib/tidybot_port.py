# =============================================================================
#  TidyBot -- TB-Port interface geometry  (SPEC VERSION 0.2.0)
# =============================================================================
#  THE authoritative definition of the module interface. Every module imports
#  this file. Nothing anywhere else may re-declare a port dimension.
#
#  Architecture: three identical tapered steel posts per face, retained by
#  cross pins in double shear, with all electricals in a sealed central
#  connector. Rationale: docs/decisions/0006-tri-post-coupling.md
#  Prose spec: docs/INTERFACE.md
#
#  Supersedes the 0.1.0 boss-and-bore geometry (git tag / commit 2c18923).
#
#  The PORT dict and derived() import under plain CPython -- no FreeCAD --
#  so firmware and test tooling read the same numbers:
#      python3 -c "from tidybot_port import PORT; print(PORT['POST_DIA'])"
#
#  COORDINATE CONVENTION -- both halves are built in their natural PRINT
#  orientation, features growing +Z off the bed:
#
#      module_port_parts()  plate z = -PLATE_THK..0, posts and cone grow +Z
#      base_port_parts()    face at z = 0, body grows -Z, sockets open upward
#
#  To mate, the base half is flipped and lifted by FLANGE_GAP.
# =============================================================================

import itertools
import math

SPEC_VERSION = "0.2.0"

# ----------------------------------------------------------------------------
#  PARAMETERS -- the interface. Changing anything here is a spec change:
#  bump SPEC_VERSION, update docs/INTERFACE.md, run `make -C cad check`.
# ----------------------------------------------------------------------------
PORT = dict(
    SPEC_VERSION      = SPEC_VERSION,

    # --- Overall footprint --------------------------------------------------
    PLATE_DIA         = 130.0,
    PLATE_THK         = 6.0,

    # --- Posts: 3, IDENTICAL, unequally spaced ------------------------------
    #  The 5 deg asymmetry at 235 is the keying feature. It makes a wrong
    #  orientation miss by ~4.4 mm against a 0.2 mm clearance -- mechanically
    #  impossible rather than merely discouraged. Keep the posts identical:
    #  one dowel size, one socket, one lip seal, one reamer, one spare.
    POST_ANGLES       = (0.0, 120.0, 235.0),
    POST_BC           = 100.0,   # bolt circle dia -> r = 50
    POST_DIA          = 10.0,
    POST_TIP_DIA      = 6.0,     # taper does the capture, on the post
    POST_TAPER_ANGLE  = 30.0,    # from the post axis; steeper = capture without length
    POST_LEN          = 18.0,    # protrusion from the module face
    POST_EMBED        = 12.0,    # pressed into the module plate + boss
    POST_BORE_DIA     = 9.90,    # light interference for a Ø10 rod in PETG
    POST_BOSS_DIA     = 18.0,    # boss behind the plate, so 12 mm of grip exists
    SOCKET_CLEARANCE  = 0.20,    # diametral

    # --- Retention: circumferential groove + one rotating lock plate -------
    #  A groove is a single lathe op -- or a round file against a rod spun in
    #  a drill. A cross-hole needs a V-block and a centre punch, and in
    #  hardened stock it needs carbide or EDM. Same double shear either way.
    #  The lock plate carries a KEYHOLE per post: the wide mouth lets the post
    #  through, then ~10 deg of rotation slides the throat into the groove.
    #  One plate replaces three pins AND the cam plate that drove them.
    GROOVE_Z          = 9.0,     # groove centre, above the module face
    GROOVE_ROOT_DIA   = 7.0,
    GROOVE_WIDTH      = 3.4,     # lock plate thickness + clearance
    LOCK_PLATE_THK    = 3.0,
    LOCK_OPEN_DIA     = 10.4,    # keyhole mouth -- the post passes through
    LOCK_CAPTURE_DIA  = 7.2,     # keyhole throat -- captures the groove

    # --- Central connector cone: engages FIRST, kills lateral error ---------
    #  It sits at r = 0, so yaw cannot displace it. That is the whole point:
    #  cone kills lateral, posts kill yaw. One feature, one job.
    CONE_BASE_DIA     = 40.0,
    CONE_TIP_DIA      = 30.0,
    CONE_LEN          = 22.0,    # > POST_LEN + 3 so it lands well before the posts
    CONE_CLEARANCE    = 0.30,
    CONTACT_COUNT     = 8,
    CONTACT_W         = 22.0,
    CONTACT_L         = 10.0,
    CONTACT_DEPTH     = 1.6,
    CONTACT_POGO_DEPTH= 6.0,
    CONTACT_STROKE_MAX= 4.0,     # the pogo travel a buyable block actually has

    # --- Sealing and drainage (ADR 0006, section on contamination) ----------
    GASKET_BC         = 118.0,   # groove on the BASE half; one gasket, not N
    GASKET_W          = 4.0,
    GASKET_H          = 2.0,
    DRAIN_DIA         = 4.0,     # from each socket floor, out the SIDE wall
    LIP_SEAL_W        = 1.5,

    FLANGE_GAP        = 1.0,     # designed air gap; steel carries the load
)

# The posts are structural, but they are still metal bridging the base to
# every module. Bond them to chassis ground on BOTH sides -- do not leave
# them floating. A vacuum generates serious static, and a floating metal
# assembly will accumulate it and dump it into the connector at the worst
# moment. Bonded, the posts engage before the contacts close, so they become
# a first-mate / last-break ground that bleeds charge before the signal pins
# ever touch: the same trick as long ground pins in a D-sub.
#
# Materials. Stainless, not mild steel: the posts sit exposed whenever a
# module is off, on a machine that mops. Rust would SWELL a Ø10 post in a
# Ø10.2 socket and bind it, shed abrasive particles into a joint that mates
# 500 times, and stain whatever it touched.
#
# Buy 303 if you are cutting the taper and groove yourself -- it is the
# free-machining grade. 304/316/A2 are common as dowel stock but gummy, and
# they work-harden: dwell with a file and the surface hardens under you.
# The yield figure below is the conservative austenitic value, so the margins
# hold whichever grade you end up with.
#
# CONSTRAINT: every part is either 3D printed in plastic or bought off the
# shelf. Nothing here may require a custom steel part to be made. The lock
# plate is therefore PRINTED -- 15x margin in PETG, and plastic against steel
# cannot gall, so the alloy question disappears with it.
MATERIAL = dict(
    STEEL_YIELD_MPA   = 205.0,   # 304/316/A2 austenitic, conservative
    PETG_YIELD_MPA    = 45.0,    # tensile; compressive is higher
    PETG_COMP_MPA     = 50.0,
    LOCK_PLATE_IS_PRINTED = True,
)

# Design loads -- ADR 0007. Not geometry, but every margin below refers to them.
LOAD = dict(
    AXIAL_TOP_N       = 192.0,   # 3-stack flight, top port
    AXIAL_BOTTOM_N    = 59.0,
    MOMENT_NM         = 4.0,
)


# ----------------------------------------------------------------------------
#  DERIVED GEOMETRY + GUARDS
#  Everything here is solved from the parameters, so a parameter change
#  re-solves instead of silently invalidating a hand-entered number. The
#  guards refuse specs that cannot work -- v0.1 shipped three bugs that a
#  guard would have caught.
# ----------------------------------------------------------------------------
def derived(p=None):
    p = p or PORT
    d = {}

    # --- Post taper: the capture feature, riding on the post ---------------
    dr = (p["POST_DIA"] - p["POST_TIP_DIA"]) / 2.0
    if dr <= 0:
        raise ValueError("POST_TIP_DIA must be smaller than POST_DIA")
    d["POST_CAPTURE"]   = dr
    d["POST_TAPER_LEN"] = dr / math.tan(math.radians(p["POST_TAPER_ANGLE"]))

    d["SOCKET_DIA"]   = p["POST_DIA"] + p["SOCKET_CLEARANCE"]
    d["SOCKET_DEPTH"] = p["POST_LEN"] + 2.0

    # --- Cone: engages before the posts ------------------------------------
    d["CONE_CAPTURE"]      = (p["CONE_BASE_DIA"] - p["CONE_TIP_DIA"]) / 2.0
    d["CONE_RECESS_DEPTH"] = p["CONE_LEN"] + 1.0
    d["CONE_LEAD"]         = p["CONE_LEN"] - p["POST_LEN"]
    if d["CONE_LEAD"] < 3.0:
        raise ValueError(
            "Cone leads the posts by only %.1f mm. It must land first and settle "
            "the lateral error before any post enters, or the posts inherit a job "
            "they cannot do (see ADR 0006)." % d["CONE_LEAD"])

    # --- Receptacle depth and volume consumed ------------------------------
    d["RECEPTACLE_DEPTH"] = max(d["SOCKET_DEPTH"], d["CONE_RECESS_DEPTH"])
    v_sockets = 3 * math.pi * (d["SOCKET_DIA"] / 2.0) ** 2 * d["SOCKET_DEPTH"]
    r1, r2 = p["CONE_BASE_DIA"] / 2.0, p["CONE_TIP_DIA"] / 2.0
    v_cone = math.pi / 3.0 * d["CONE_RECESS_DEPTH"] * (r1*r1 + r1*r2 + r2*r2)
    d["VOL_SOCKETS"] = v_sockets
    d["VOL_CONE"]    = v_cone
    d["VOL_TOTAL"]   = v_sockets + v_cone

    # --- Post mounting: the posts are STEEL, pressed into the plate --------
    d["POST_TOTAL_LEN"] = p["POST_LEN"] + p["POST_EMBED"]
    d["BOSS_WALL"] = (p["POST_BOSS_DIA"] - p["POST_BORE_DIA"]) / 2.0
    if d["BOSS_WALL"] < 3.0:
        raise ValueError(
            "Only %.1f mm of wall around the post bore. A press fit will split it."
            % d["BOSS_WALL"])
    if p["POST_EMBED"] < p["POST_DIA"]:
        raise ValueError(
            "Post embedded only %.1f mm for a Ø%.1f post. Aim for at least one "
            "diameter of grip." % (p["POST_EMBED"], p["POST_DIA"]))

    # --- Mirror handedness -------------------------------------------------
    #  The two faces meet each other, so they are mirror images. A module post
    #  at angle a must find a base socket at -a. With the old symmetric
    #  0/120/240 layout this was invisible (the set mirrors onto itself); the
    #  asymmetric keying layout makes it real, and getting it wrong means
    #  nothing mates at all.
    d["SOCKET_ANGLES"] = tuple((-a) % 360.0 for a in p["POST_ANGLES"])

    # --- Keying: a wrong orientation must be physically impossible ---------
    r = p["POST_BC"] / 2.0
    A = [a % 360.0 for a in p["POST_ANGLES"]]
    worst = 1e9
    for phi in (120.0, 240.0):
        rot = [(a + phi) % 360.0 for a in A]
        best = 1e9
        for perm in itertools.permutations(rot):
            err = max(min(abs(x - a), 360.0 - abs(x - a)) for x, a in zip(perm, A))
            best = min(best, err)
        worst = min(worst, best)
    d["KEY_MISFIT_DEG"] = worst
    d["KEY_MISFIT_MM"]  = r * math.radians(worst)
    if d["KEY_MISFIT_MM"] < 5.0 * p["SOCKET_CLEARANCE"]:
        raise ValueError(
            "POST_ANGLES %s let the module mate in more than one orientation: a "
            "wrong orientation misses by only %.2f mm against %.2f mm of clearance. "
            "Break the symmetry (see ADR 0006)."
            % (p["POST_ANGLES"], d["KEY_MISFIT_MM"], p["SOCKET_CLEARANCE"]))

    # --- Load-centroid offset, the cost of that asymmetry ------------------
    cx = sum(math.cos(math.radians(a)) for a in A) / 3.0 * r
    cy = sum(math.sin(math.radians(a)) for a in A) / 3.0 * r
    d["CENTROID_OFFSET"] = math.hypot(cx, cy)
    d["LOAD_IMBALANCE_NM"] = LOAD["AXIAL_TOP_N"] * d["CENTROID_OFFSET"] / 1000.0

    # --- Do the contacts actually MEET? ------------------------------------
    #  Every other check asks whether parts clash. This one asks whether they
    #  touch -- the blind spot that let 0.1.0 ship a coupling whose balls
    #  never reached their dowels.
    pad = p["CONE_LEN"] - p["CONTACT_DEPTH"]
    floor = p["FLANGE_GAP"] + d["CONE_RECESS_DEPTH"]
    d["CONTACT_GAP"] = floor - pad
    if d["CONTACT_GAP"] > p["CONTACT_POGO_DEPTH"] + p["CONTACT_STROKE_MAX"]:
        raise ValueError(
            "Pogo pins would have to span %.2f mm, beyond a %.1f mm block with "
            "%.1f mm of stroke. The contacts would never close."
            % (d["CONTACT_GAP"], p["CONTACT_POGO_DEPTH"], p["CONTACT_STROKE_MAX"]))
    if d["CONTACT_GAP"] < 1.0:
        raise ValueError(
            "Only %.2f mm for the contacts. The pad would crash into the pogo "
            "block before the posts seat." % d["CONTACT_GAP"])

    # --- Groove and lock plate ---------------------------------------------
    d["GROOVE_DEPTH"] = (p["POST_DIA"] - p["GROOVE_ROOT_DIA"]) / 2.0
    d["LOCK_TRAVEL"]  = (p["LOCK_OPEN_DIA"] + p["LOCK_CAPTURE_DIA"]) / 2.0
    d["LOCK_ROT_DEG"] = math.degrees(d["LOCK_TRAVEL"] / (p["POST_BC"] / 2.0))
    d["LOCK_ENGAGE"]  = (p["POST_DIA"] - p["LOCK_CAPTURE_DIA"]) / 2.0

    if p["LOCK_OPEN_DIA"] <= p["POST_DIA"]:
        raise ValueError(
            "Keyhole mouth Ø%.2f will not pass a Ø%.2f post -- the module could "
            "never be inserted." % (p["LOCK_OPEN_DIA"], p["POST_DIA"]))
    if not (p["GROOVE_ROOT_DIA"] < p["LOCK_CAPTURE_DIA"] < p["POST_DIA"]):
        raise ValueError(
            "Keyhole throat Ø%.2f must sit between the groove root Ø%.2f and the "
            "post Ø%.2f: wider and it slips off, narrower and it jams on the root."
            % (p["LOCK_CAPTURE_DIA"], p["GROOVE_ROOT_DIA"], p["POST_DIA"]))
    if p["GROOVE_WIDTH"] <= p["LOCK_PLATE_THK"]:
        raise ValueError("Groove %.2f mm is not wider than the %.2f mm lock plate."
                         % (p["GROOVE_WIDTH"], p["LOCK_PLATE_THK"]))

    # The groove must sit in the post's cylindrical section, clear of the
    # taper, with the whole width above the base's mating face.
    g_top = p["GROOVE_Z"] + p["GROOVE_WIDTH"] / 2.0
    g_bot = p["GROOVE_Z"] - p["GROOVE_WIDTH"] / 2.0
    if g_top > p["POST_LEN"] - d["POST_TAPER_LEN"]:
        raise ValueError(
            "The groove reaches z=%.2f but the taper starts at %.2f. The lock "
            "plate would bear on a cone instead of a square shoulder."
            % (g_top, p["POST_LEN"] - d["POST_TAPER_LEN"]))
    d["GROOVE_COVER"] = g_bot - p["FLANGE_GAP"]
    if d["GROOVE_COVER"] < 3.0:
        raise ValueError(
            "Only %.2f mm between the groove and the mating face. The lock slot "
            "would break out of the base's face." % d["GROOVE_COVER"])

    # --- Margins: the lock plate is the load path --------------------------
    d["LOCK_BEARING_MM2"] = 0.5 * math.pi / 4.0 * (
        p["POST_DIA"] ** 2 - p["LOCK_CAPTURE_DIA"] ** 2)
    d["POST_NET_MM2"] = math.pi / 4.0 * p["GROOVE_ROOT_DIA"] ** 2
    d["LOCK_LOAD_N"]  = LOAD["AXIAL_TOP_N"] / 3.0
    d["LOCK_BEARING_MPA"] = d["LOCK_LOAD_N"] / d["LOCK_BEARING_MM2"]
    d["POST_TENSION_MPA"] = d["LOCK_LOAD_N"] / d["POST_NET_MM2"]
    y_plate = (MATERIAL["PETG_COMP_MPA"] if MATERIAL["LOCK_PLATE_IS_PRINTED"]
               else MATERIAL["STEEL_YIELD_MPA"])
    d["LOCK_MARGIN"] = y_plate / d["LOCK_BEARING_MPA"]
    d["POST_MARGIN"] = MATERIAL["STEEL_YIELD_MPA"] / d["POST_TENSION_MPA"]
    if d["LOCK_MARGIN"] < 10.0:
        raise ValueError("Lock plate bearing margin only %.1fx." % d["LOCK_MARGIN"])
    return d


# ----------------------------------------------------------------------------
#  FREECAD GEOMETRY  (imported lazily; module stays CPython-importable)
# ----------------------------------------------------------------------------
def _fc():
    import Part
    import FreeCAD as App
    return Part, App


def _polar(radius, angle_deg):
    a = math.radians(angle_deg)
    return radius * math.cos(a), radius * math.sin(a)


def _rotated(shape, angle_deg):
    _, App = _fc()
    s = shape.copy()
    s.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle_deg)
    return s


def module_port_parts(p=None):
    """Male half, on every module: (additive_solid, [cut_tools]).

    Plate at z = -PLATE_THK..0; three tapered posts and the connector cone
    grow +Z. Prints as generated, features up, no supports.

    Use attach() -- never host.fuse(module_port()) -- when putting this on a
    module body. Fusing over a finished port back-fills its recesses.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    cuts = []

    body = Part.makeCylinder(p["PLATE_DIA"] / 2.0, p["PLATE_THK"],
                             App.Vector(0, 0, -p["PLATE_THK"]), Z)

    # --- mounting for three identical STEEL posts --------------------------
    #  The posts are steel dowels, NOT printed. ADR 0005: precision and load
    #  surfaces are steel; printed plastic is bulk and rough alignment only.
    #  The pin bears inside the post's cross-hole, so that hole has to be in
    #  metal or it crushes and every margin on this port is fiction.
    for ang in p["POST_ANGLES"]:
        x, y = _polar(p["POST_BC"] / 2.0, ang)
        # boss behind the plate, giving POST_EMBED of grip
        body = body.fuse(Part.makeCylinder(
            p["POST_BOSS_DIA"] / 2.0, p["POST_EMBED"] - p["PLATE_THK"],
            App.Vector(x, y, -p["POST_EMBED"]), Z))
        # press-fit bore for the dowel
        cuts.append(Part.makeCylinder(
            p["POST_BORE_DIA"] / 2.0, p["POST_EMBED"] + 0.1,
            App.Vector(x, y, -p["POST_EMBED"]), Z))

    # --- central connector cone: lands first, kills lateral error ----------
    body = body.fuse(Part.makeCone(
        p["CONE_BASE_DIA"] / 2.0, p["CONE_TIP_DIA"] / 2.0, p["CONE_LEN"],
        App.Vector(0, 0, 0), Z))
    # contact pad PCB recess in the cone tip
    cuts.append(Part.makeBox(
        p["CONTACT_W"], p["CONTACT_L"], p["CONTACT_DEPTH"] + 0.1,
        App.Vector(-p["CONTACT_W"] / 2.0, -p["CONTACT_L"] / 2.0,
                   p["CONE_LEN"] - p["CONTACT_DEPTH"])))
    # harness bore up the cone axis
    cuts.append(Part.makeCylinder(
        8.0, p["CONE_LEN"] + p["PLATE_THK"] + 2.0,
        App.Vector(0, 0, -p["PLATE_THK"] - 1.0), Z))
    return body, cuts


def steel_post(p=None, angle=0.0):
    """One post, as hardware: a Ø10 steel rod with a turned taper and a
    drilled cross-hole, positioned as it sits when pressed into the module.

    Modelled explicitly so the checks can verify the steel, not just the
    plastic around it. v0.1's checks passed on a coupling whose steel could
    never touch.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    x, y = _polar(p["POST_BC"] / 2.0, angle)
    straight = p["POST_LEN"] - d["POST_TAPER_LEN"]

    post = Part.makeCylinder(p["POST_DIA"] / 2.0, p["POST_EMBED"] + straight,
                             App.Vector(x, y, -p["POST_EMBED"]), Z)
    post = post.fuse(Part.makeCone(
        p["POST_DIA"] / 2.0, p["POST_TIP_DIA"] / 2.0, d["POST_TAPER_LEN"],
        App.Vector(x, y, straight), Z))
    # circumferential groove -- a single lathe op, or a round file against
    # the rod spun in a drill. The lock plate seats in here.
    ring = Part.makeCylinder(p["POST_DIA"] / 2.0 + 1.0, p["GROOVE_WIDTH"],
                             App.Vector(x, y, p["GROOVE_Z"] - p["GROOVE_WIDTH"] / 2.0), Z)
    ring = ring.cut(Part.makeCylinder(
        p["GROOVE_ROOT_DIA"] / 2.0, p["GROOVE_WIDTH"] + 0.2,
        App.Vector(x, y, p["GROOVE_Z"] - p["GROOVE_WIDTH"] / 2.0 - 0.1), Z))
    post = post.cut(ring)
    return post


def printed_post(p=None):
    """One post as a PRINTABLE part, standing on its embedded end.

    Phase 1 does not need steel. A printed post carries the flight load with
    27x margin; what it gives up is precision (a Ø10 printed at a 0.5 mm
    nozzle lands around +/-0.15 mm, so socket clearance opens to ~0.40 mm)
    and wear life. T1, T2, T3 and T5 all still mean something. Only T4's
    200 N pull and T6's 500 cycles want real steel.

    Printed standing: the groove and taper come out as clean revolved
    features, and layer adhesion is loaded in tension at 13x even derated --
    so orientation is not the constraint here.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    straight = p["POST_LEN"] - d["POST_TAPER_LEN"]

    post = Part.makeCylinder(p["POST_DIA"] / 2.0, p["POST_EMBED"] + straight,
                             App.Vector(0, 0, 0), Z)
    post = post.fuse(Part.makeCone(
        p["POST_DIA"] / 2.0, p["POST_TIP_DIA"] / 2.0, d["POST_TAPER_LEN"],
        App.Vector(0, 0, p["POST_EMBED"] + straight), Z))
    ring = Part.makeCylinder(p["POST_DIA"] / 2.0 + 1.0, p["GROOVE_WIDTH"],
                             App.Vector(0, 0, p["POST_EMBED"] + p["GROOVE_Z"]
                                        - p["GROOVE_WIDTH"] / 2.0), Z)
    ring = ring.cut(Part.makeCylinder(
        p["GROOVE_ROOT_DIA"] / 2.0, p["GROOVE_WIDTH"] + 0.2,
        App.Vector(0, 0, p["POST_EMBED"] + p["GROOVE_Z"]
                   - p["GROOVE_WIDTH"] / 2.0 - 0.1), Z))
    return post.cut(ring)


def lock_plate(p=None, rotation=None):
    """The retention mechanism: ONE plate carrying a keyhole per post.

    The wide mouth of each keyhole passes the post; ~10 deg of rotation
    slides the narrow throat into the post's groove, locking all three at
    once. Replaces three loose pins and the cam plate that drove them.

    rotation=None  -> locked position
    rotation=0     -> open position (posts pass freely)

    Lives entirely inside the sealed base: nothing that moves ever sees the
    room, which is the property that matters on a robot that mops.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    if rotation is None:
        rotation = d["LOCK_ROT_DEG"]
    r = p["POST_BC"] / 2.0

    z0 = p["GROOVE_Z"] - p["LOCK_PLATE_THK"] / 2.0
    plate = Part.makeCylinder(r + 14.0, p["LOCK_PLATE_THK"], App.Vector(0, 0, z0), Z)
    plate = plate.cut(Part.makeCylinder(r - 14.0, p["LOCK_PLATE_THK"] + 2.0,
                                        App.Vector(0, 0, z0 - 1.0), Z))

    for ang in p["POST_ANGLES"]:
        # In the plate's own frame: mouth at the post angle, throat behind it
        # by the lock rotation, so rotating forward brings the throat home.
        a_open = ang
        a_cap = ang - d["LOCK_ROT_DEG"]
        ox, oy = _polar(r, a_open)
        cx, cy = _polar(r, a_cap)
        plate = plate.cut(Part.makeCylinder(
            p["LOCK_OPEN_DIA"] / 2.0, p["LOCK_PLATE_THK"] + 2.0,
            App.Vector(ox, oy, z0 - 1.0), Z))
        plate = plate.cut(Part.makeCylinder(
            p["LOCK_CAPTURE_DIA"] / 2.0, p["LOCK_PLATE_THK"] + 2.0,
            App.Vector(cx, cy, z0 - 1.0), Z))
        # the slot joining mouth to throat
        mx, my = (ox + cx) / 2.0, (oy + cy) / 2.0
        span = math.hypot(ox - cx, oy - cy)
        slot = Part.makeBox(span, p["LOCK_CAPTURE_DIA"], p["LOCK_PLATE_THK"] + 2.0,
                            App.Vector(-span / 2.0, -p["LOCK_CAPTURE_DIA"] / 2.0, z0 - 1.0))
        slot.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1),
                    math.degrees(math.atan2(oy - cy, ox - cx)))
        slot.translate(App.Vector(mx, my, 0))
        plate = plate.cut(slot)

    return _rotated(plate, rotation)


def base_port_parts(p=None):
    """Female half, on the base: (additive_solid, [cut_tools]).

    Face at z = 0, body grows -Z, sockets open upward. Prints as generated.
    Every socket drains out the SIDE wall -- never into the electronics.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    cuts = []

    depth = d["RECEPTACLE_DEPTH"] + p["PLATE_THK"]
    body = Part.makeCylinder(p["PLATE_DIA"] / 2.0, depth,
                             App.Vector(0, 0, -depth), Z)

    for ang in d["SOCKET_ANGLES"]:
        x, y = _polar(p["POST_BC"] / 2.0, ang)
        # socket
        cuts.append(Part.makeCylinder(
            d["SOCKET_DIA"] / 2.0, d["SOCKET_DEPTH"] + 0.1,
            App.Vector(x, y, -d["SOCKET_DEPTH"]), Z))
        # lead-in chamfer at the socket mouth, so the taper meets a taper
        cuts.append(Part.makeCone(
            d["SOCKET_DIA"] / 2.0 + 1.2, d["SOCKET_DIA"] / 2.0, 1.2,
            App.Vector(x, y, -1.2), Z))
        ux, uy = _polar(1.0, ang)
        # cavity for the lock plate to sweep through, at the groove height
        z_lock = -(p["GROOVE_Z"] - p["FLANGE_GAP"])
        sweep = 2.0 * d["LOCK_TRAVEL"] + p["POST_DIA"] + 6.0
        slot = Part.makeBox(sweep, p["POST_DIA"] + 8.0, p["GROOVE_WIDTH"],
                            App.Vector(-sweep / 2.0, -(p["POST_DIA"] + 8.0) / 2.0,
                                       z_lock - p["GROOVE_WIDTH"] / 2.0))
        slot.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), ang + 90.0)
        slot.translate(App.Vector(x, y, 0.0))
        cuts.append(slot)
        # drain: socket floor -> out through the side wall
        cuts.append(Part.makeCylinder(
            p["DRAIN_DIA"] / 2.0, p["PLATE_DIA"],
            App.Vector(x, y, -d["SOCKET_DEPTH"] + p["DRAIN_DIA"] / 2.0),
            App.Vector(ux, uy, -0.15)))

    # --- connector cone recess --------------------------------------------
    cc = p["CONE_CLEARANCE"]
    cuts.append(Part.makeCone(
        (p["CONE_BASE_DIA"] + cc) / 2.0, (p["CONE_TIP_DIA"] + cc) / 2.0,
        p["CONE_LEN"], App.Vector(0, 0, 0), App.Vector(0, 0, -1)))
    cuts.append(Part.makeCylinder(
        (p["CONE_TIP_DIA"] + cc) / 2.0, d["CONE_RECESS_DEPTH"] - p["CONE_LEN"] + 0.1,
        App.Vector(0, 0, -d["CONE_RECESS_DEPTH"]), Z))
    # pogo block pocket at the cone floor
    cuts.append(Part.makeBox(
        p["CONTACT_W"] + 1.0, p["CONTACT_L"] + 1.0, p["CONTACT_POGO_DEPTH"],
        App.Vector(-(p["CONTACT_W"] + 1.0) / 2.0, -(p["CONTACT_L"] + 1.0) / 2.0,
                   -d["CONE_RECESS_DEPTH"] - p["CONTACT_POGO_DEPTH"] + 0.1)))
    # harness bore
    cuts.append(Part.makeCylinder(
        8.0, depth + 2.0, App.Vector(0, 0, -depth - 1.0), Z))

    # --- perimeter gasket groove: one gasket on the base, not N on modules -
    go = Part.makeCylinder((p["GASKET_BC"] + p["GASKET_W"]) / 2.0,
                           p["GASKET_H"] + 0.1, App.Vector(0, 0, -p["GASKET_H"]), Z)
    gi = Part.makeCylinder((p["GASKET_BC"] - p["GASKET_W"]) / 2.0,
                           p["GASKET_H"] + 0.3, App.Vector(0, 0, -p["GASKET_H"] - 0.1), Z)
    cuts.append(go.cut(gi))
    return body, cuts


def _resolve(parts):
    body, cuts = parts
    for c in cuts:
        body = body.cut(c)
    return body


def module_port(p=None):
    """Male half as a standalone finished solid. Do NOT fuse a host onto it."""
    return _resolve(module_port_parts(p))


def base_port(p=None):
    """Female half as a standalone finished solid. Do NOT fuse a host onto it."""
    return _resolve(base_port_parts(p))


def attach(host, parts):
    """Fuse a port onto a host body with the correct cut ordering.

    ALWAYS use this instead of host.fuse(module_port()). Fusing a host over a
    finished port back-fills its recesses -- silently, with no error. This
    exact bug shipped in v0.1 and removed all three ball sockets.
    """
    body, cuts = parts
    out = host.fuse(body)
    for c in cuts:
        out = out.cut(c)
    return out


def report(p=None):
    """Derived geometry, margins and BOM. Runs under plain python3."""
    p = p or PORT
    d = derived(p)
    print("TB-Port spec %s  --  three tapered posts, groove + lock plate" % p["SPEC_VERSION"])
    print("\nGEOMETRY")
    print("  post                  3 x Ø%.1f, identical, at %s deg"
          % (p["POST_DIA"], "/".join("%.0f" % a for a in p["POST_ANGLES"])))
    print("  post bolt circle      Ø%.0f  (r = %.0f)" % (p["POST_BC"], p["POST_BC"] / 2))
    print("  base sockets at       %s deg  (mirror of the posts -- the faces meet)"
          % "/".join("%.0f" % a for a in d["SOCKET_ANGLES"]))
    print("  taper                 %.2f mm long -> %.2f mm capture, on the post"
          % (d["POST_TAPER_LEN"], d["POST_CAPTURE"]))
    print("  socket                Ø%.2f x %.1f deep" % (d["SOCKET_DIA"], d["SOCKET_DEPTH"]))
    print("  post is STEEL         Ø%.1f x %.0f rod, %.0f embedded + %.0f proud"
          % (p["POST_DIA"], d["POST_TOTAL_LEN"], p["POST_EMBED"], p["POST_LEN"]))
    print("  press bore            Ø%.2f, %.1f mm boss wall" % (p["POST_BORE_DIA"], d["BOSS_WALL"]))
    print("  cone                  Ø%.0f->Ø%.0f x %.0f, leads the posts by %.0f mm"
          % (p["CONE_BASE_DIA"], p["CONE_TIP_DIA"], p["CONE_LEN"], d["CONE_LEAD"]))
    print("  receptacle depth      %.1f mm  (the cone is the deepest feature)"
          % d["RECEPTACLE_DEPTH"])
    print("  groove cover          %.2f mm of base material below the lock slot"
          % d["GROOVE_COVER"])
    print("  contact gap           %.2f mm for the pogo pins to span"
          % d["CONTACT_GAP"])
    print("\nVOLUME CONSUMED IN THE BASE")
    print("  3 post sockets        %6.0f mm3" % d["VOL_SOCKETS"])
    print("  connector cone        %6.0f mm3" % d["VOL_CONE"])
    print("  total                 %6.0f mm3   (bayonet alternative: ~69,979)"
          % d["VOL_TOTAL"])
    print("\nKEYING")
    print("  wrong orientation misses by %.1f deg = %.2f mm at r=%.0f"
          % (d["KEY_MISFIT_DEG"], d["KEY_MISFIT_MM"], p["POST_BC"] / 2))
    print("  socket clearance %.2f mm -> a wall, not a tight fit" % p["SOCKET_CLEARANCE"])
    print("  cost: centroid %.2f mm off axis = %.2f N*m imbalance"
          % (d["CENTROID_OFFSET"], d["LOAD_IMBALANCE_NM"]))
    print("\nRETENTION -- groove + one rotating lock plate")
    print("  groove                Ø%.1f root, %.1f wide, %.2f mm deep"
          % (p["GROOVE_ROOT_DIA"], p["GROOVE_WIDTH"], d["GROOVE_DEPTH"]))
    print("  keyhole               Ø%.1f mouth -> Ø%.1f throat"
          % (p["LOCK_OPEN_DIA"], p["LOCK_CAPTURE_DIA"]))
    print("  lock motion           %.1f mm tangential = %.1f deg of plate rotation"
          % (d["LOCK_TRAVEL"], d["LOCK_ROT_DEG"]))
    print("  shoulder engagement   %.2f mm of radial overlap" % d["LOCK_ENGAGE"])

    print("\nMARGINS (top port, %.0f N flight load, %.0f N per post)"
          % (LOAD["AXIAL_TOP_N"], d["LOCK_LOAD_N"]))
    print("  lock plate bearing    %.2f MPa -> %.0fx (%s)"
          % (d["LOCK_BEARING_MPA"], d["LOCK_MARGIN"],
             "PRINTED PETG" if MATERIAL["LOCK_PLATE_IS_PRINTED"] else "stainless"))
    print("  post net section      %.2f MPa -> %.0fx" % (d["POST_TENSION_MPA"], d["POST_MARGIN"]))
    print("\nBILL OF MATERIALS per mated pair")
    print("  3 x Ø%.0f x %.0f post" % (p["POST_DIA"], d["POST_TOTAL_LEN"]))
    print("        PHASE 1: print them. %.0fx margin, and only T4/T6 need steel."
          % (MATERIAL["PETG_YIELD_MPA"] / d["POST_TENSION_MPA"]))
    print("        LATER:   stainless 303, if you can get the two features cut.")
    print("        - turn one end to Ø%.0f over %.1f mm at %.0f deg  (the capture taper)"
          % (p["POST_TIP_DIA"], d["POST_TAPER_LEN"], p["POST_TAPER_ANGLE"]))
    print("        - cut a Ø%.0f groove, %.1f wide, centred %.0f mm above the shoulder"
          % (p["GROOVE_ROOT_DIA"], p["GROOVE_WIDTH"], p["GROOVE_Z"]))
    print("        - press %.0f mm into the plate (bore Ø%.2f)"
          % (p["POST_EMBED"], p["POST_BORE_DIA"]))
    print("        NOTE: 303 is the free-machining grade -- buy that if you are")
    print("              cutting the taper yourself. 304/316/A2 are common as")
    print("              dowel stock but work-harden under a file.")
    print("              Both features are one lathe op, or a file against the")
    print("              rod spun in a drill. No cross-hole, no V-block.")
    print("  1 x lock plate, %.0f mm, 3 keyholes  -- PRINTED, not steel"
          % p["LOCK_PLATE_THK"])
    print("        %.1fx margin in PETG, and plastic on steel cannot gall."
          % d["LOCK_MARGIN"])
    print("  3 x lip seal, %.1f mm            (socket mouths)" % p["LIP_SEAL_W"])
    print("  1 x TPU O-ring, Ø%.0f x %.0f       (perimeter gasket, on the base)"
          % (p["GASKET_BC"], p["GASKET_H"]))
    print("  1 x %d-way pogo block + mating pad PCB  (central connector)" % p["CONTACT_COUNT"])


if __name__ == "__main__":
    report()
