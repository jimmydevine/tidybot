# =============================================================================
#  TidyBot CAD regeneration
# =============================================================================
#  Every printable part is generated from a Python script, so the whole fleet
#  can be regenerated from one edit to the port spec. That is the entire point
#  of the parametric approach -- use it.
#
#      make check    validate the port geometry (run this FIRST, it is cheap)
#      make coupon   Phase 1 bench coupons
#      make report   print derived port dimensions + BOM
#      make all      everything
#      make clean    remove generated STL/STEP
# =============================================================================

# Use '>' instead of tabs for recipe lines (GNU Make 3.82+).
.RECIPEPREFIX = >

#  FreeCAD headless binary. Override with:  make FREECAD=/path/to/freecadcmd
#
#  NOTE: the official AppImage does NOT provide a working headless entry point
#  from the outside -- '--console' drops into an interactive shell that never
#  exits, and there is no argv0 dispatch, so a symlink to the AppImage launches
#  the GUI. Extract it once and use the inner binary:
#
#      cd ~/Applications
#      ./FreeCAD_x.y.z-x86_64.AppImage --appimage-extract
#      mv squashfs-root FreeCAD-x.y.z
#      ln -sf ~/Applications/FreeCAD-x.y.z/usr/bin/freecadcmd ~/.local/bin/
#
FREECAD ?= $(shell command -v freecadcmd 2>/dev/null \
             || command -v freecad.cmd 2>/dev/null \
             || command -v FreeCADCmd 2>/dev/null \
             || ls -1 $(HOME)/Applications/FreeCAD-*/usr/bin/freecadcmd 2>/dev/null | head -1)
PYTHON  := python3

ifeq ($(FREECAD),)
$(warning FreeCAD headless binary not found -- 'make check'/'coupon' will fail.)
$(warning See the extraction note at the top of this Makefile, or set FREECAD=)
endif

.PHONY: all check coupon report clean

all: check coupon

# Cheap geometry validation. Always run before committing a spec change --
# it catches over-constraint and bottoming-out without burning a print.
check:
> @cd tests && $(FREECAD) check_port_mate.py 2>&1 | grep -vE '^FreeCAD |^\(C\)|free and open|snap-specific|QThreadStorage'

coupon: check
> @cd tests && $(FREECAD) generate_port_coupon.py 2>&1 | grep -E 'coupon_|EXCEEDS|spec'

# Runs under plain CPython -- no FreeCAD needed.
report:
> @cd lib && $(PYTHON) tidybot_port.py

clean:
> @find . -name '*.stl' -delete -o -name '*.step' -delete -o -name '*.FCBak' -delete
> @echo "cleaned generated geometry"
