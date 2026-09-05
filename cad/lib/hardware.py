# =============================================================================
#  TidyBot -- shared hardware dimensions
# =============================================================================
#  Every off-the-shelf metal part used in the project, in one place. Import this
#  rather than typing a hole diameter into a model, so that a change to (say)
#  insert hole tolerance propagates everywhere on the next regen.
#
#  All dimensions in mm. Clearances assume PETG on a 0.5 mm nozzle; see
#  docs/decisions/0005-print-constraints-taz6.md.
# =============================================================================

# --- M3 heat-set inserts (the standard fastener everywhere on this project) ---
M3_INSERT_HOLE_DIA   = 4.0    # for a standard M3 brass heat-set insert
M3_INSERT_DEPTH      = 6.0    # boss must be at least this deep
M3_CLEAR_HOLE_DIA    = 3.4    # M3 screw passes freely
M3_HEAD_DIA          = 6.0    # socket-head cap screw
M3_HEAD_DEPTH        = 3.2    # counterbore depth

M4_INSERT_HOLE_DIA   = 5.6
M4_CLEAR_HOLE_DIA    = 4.5

# --- Bearing balls (chrome steel, widely available in mixed packs) ------------
BALL_8_DIA           = 8.0    # kinematic coupling ball
BALL_8_SOCKET_DIA    = 8.2    # flat-bottom bore, retained with epoxy
BALL_6_DIA           = 6.0    # latch detent ball
BALL_6_BORE_DIA      = 6.2    # radial through-hole in the female bore wall

# --- Dowel pins (hardened steel, h6 ground) ----------------------------------
DOWEL_3_DIA          = 3.0    # forms the kinematic vee grooves
DOWEL_3_CHANNEL_DIA  = 3.1    # printed channel: slip fit, retained by geometry
DOWEL_5_DIA          = 5.0    # keying pin
DOWEL_5_PRESS_DIA    = 4.9    # press fit into the male half
DOWEL_5_CLEAR_DIA    = 5.3    # clearance in the female half -- MUST stay loose,
                              # the key must never fight the kinematic coupling

# --- Generic print clearances -------------------------------------------------
FIT_SLIP             = 0.40   # parts that must slide (boss in bore)
FIT_CLOSE            = 0.20   # located but removable
FIT_PRESS            = -0.10  # interference

MIN_WALL             = 1.5    # 3 x 0.5 mm nozzle
MIN_FEATURE          = 2.0
