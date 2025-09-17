#!/usr/bin/env python3
"""
Shift selected SVG coordinates by dx/dy based on numeric ranges.

Changes vs previous version:
- Per-attribute shifting: for <line>, x1/x2/y1/y2 are tested independently.
  If only x2 matches the X filter, only x2 is shifted by DX, etc.
- Optional per-endpoint lock: if REQUIRE_BOTH_AXES_FOR_ENDPOINTS is True and you
  set both X and Y filters, a line endpoint (x1,y1) or (x2,y2) will shift only
  if BOTH that endpoint's X and Y satisfy their respective filters.

Supported attributes:
- X-like: x, cx, x1, x2
- Y-like: y, cy, y1, y2

Target file structure:
- An HTML file with a single <svg>...</svg> block inside.
"""

from __future__ import annotations
import re
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET

# =========================
# CONFIG — EDIT THESE
# =========================

INPUT_FILE  = Path("updating_trees/Tree_20r.html")
OUTPUT_FILE = Path("updating_trees/Tree_20r.html")  # set same as INPUT_FILE to overwrite
MAKE_BACKUP = True  # if overwriting INPUT_FILE, keep a .bak

# Coordinate filters (set to None to disable a bound)
# Example: 100 < x < 500 and y > 100
X_MIN = 1400.0
X_MAX = 1800.0
Y_MIN = 100.0
Y_MAX = None

# Inclusive/exclusive bounds (False => strict > / <)
INCLUSIVE_BOUNDS = False

# Per-endpoint lock for <line> when BOTH X and Y filters are set:
# - False (default): test and shift each attribute independently (x1, x2, y1, y2).
# - True: for lines, treat (x1,y1) and (x2,y2) as endpoints; require BOTH axes
#         of an endpoint to match before shifting that endpoint's coords.
REQUIRE_BOTH_AXES_FOR_ENDPOINTS = False

# Shift amounts
DX = 50.0
DY = 0.0

# Number formatting
WRITE_DECIMALS = 6

# =========================
# END CONFIG
# =========================

ATTRS_X = ("x", "cx", "x1", "x2")
ATTRS_Y = ("y", "cy", "y1", "y2")

SVG_BLOCK_RE = re.compile(r"<svg\b[^>]*>.*?</svg>", re.IGNORECASE | re.DOTALL)

def format_like(original: str, new_value: float) -> str:
    orig = original.strip()
    if re.fullmatch(r"-?\d+", orig):
        if abs(new_value - round(new_value)) < 10**-(WRITE_DECIMALS):
            return str(int(round(new_value)))
    s = f"{new_value:.{WRITE_DECIMALS}f}".rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s

def try_float(s: str) -> float | None:
    try:
        return float(s)
    except Exception:
        return None

def in_range(val: float, lo: float | None, hi: float | None, inclusive: bool) -> bool:
    if lo is not None:
        if inclusive:
            if val < lo:
                return False
        else:
            if val <= lo:
                return False
    if hi is not None:
        if inclusive:
            if val > hi:
                return False
        else:
            if val >= hi:
                return False
    return True

def get_local_name(tag: str) -> str:
    # Strip namespace: "{ns}local" -> "local"
    if tag.startswith("{"):
        return tag.rsplit("}", 1)[1]
    return tag

def process_svg(svg_xml: str) -> tuple[str, int, int]:
    root = ET.fromstring(svg_xml)
    ns_match = re.match(r"\{(.*)\}", root.tag)
    if ns_match:
        ET.register_namespace('', ns_match.group(1))

    # Counters = number of individual attributes shifted
    shifted_x_attrs = 0
    shifted_y_attrs = 0

    # Axis filter presence
    have_x_filter = (X_MIN is not None) or (X_MAX is not None)
    have_y_filter = (Y_MIN is not None) or (Y_MAX is not None)

    def match_x(v): return in_range(v, X_MIN, X_MAX, INCLUSIVE_BOUNDS)
    def match_y(v): return in_range(v, Y_MIN, Y_MAX, INCLUSIVE_BOUNDS)

    for elem in root.iter():
        tag = get_local_name(elem.tag)

        # Helper to shift a single attribute if its current value matches
        def maybe_shift_attr(attr: str, delta: float, matcher, axis: str) -> bool:
            if attr not in elem.attrib:
                return False
            v_str = elem.attrib[attr]
            v = try_float(v_str)
            if v is None:
                return False
            # If no filter on this axis but we are shifting that axis, treat as eligible
            if ((axis == "x" and not have_x_filter and DX != 0) or
                (axis == "y" and not have_y_filter and DY != 0) or
                matcher(v)):
                new_v = v + delta
                elem.set(attr, format_like(v_str, new_v))
                return True
            return False

        # Special handling for <line> to support per-endpoint logic
        if tag == "line":
            # Read existing coords (if present and numeric)
            coords = {}
            for a in ("x1","y1","x2","y2"):
                v = try_float(elem.attrib.get(a, ""))
                coords[a] = v

            # If per-endpoint lock is ON and both axis filters exist, decide per endpoint
            if REQUIRE_BOTH_AXES_FOR_ENDPOINTS and have_x_filter and have_y_filter:
                # Endpoint 1
                e1_x_ok = (coords["x1"] is not None and match_x(coords["x1"]))
                e1_y_ok = (coords["y1"] is not None and match_y(coords["y1"]))
                if e1_x_ok and e1_y_ok:
                    if DX and coords["x1"] is not None:
                        elem.set("x1", format_like(elem.attrib["x1"], coords["x1"] + DX))
                        shifted_x_attrs += 1
                    if DY and coords["y1"] is not None:
                        elem.set("y1", format_like(elem.attrib["y1"], coords["y1"] + DY))
                        shifted_y_attrs += 1
                # Endpoint 2
                e2_x_ok = (coords["x2"] is not None and match_x(coords["x2"]))
                e2_y_ok = (coords["y2"] is not None and match_y(coords["y2"]))
                if e2_x_ok and e2_y_ok:
                    if DX and coords["x2"] is not None:
                        elem.set("x2", format_like(elem.attrib["x2"], coords["x2"] + DX))
                        shifted_x_attrs += 1
                    if DY and coords["y2"] is not None:
                        elem.set("y2", format_like(elem.attrib["y2"], coords["y2"] + DY))
                        shifted_y_attrs += 1
            else:
                # Independent per-attribute matching (your requested behavior)
                if DX:
                    if maybe_shift_attr("x1", DX, match_x, "x"): shifted_x_attrs += 1
                    if maybe_shift_attr("x2", DX, match_x, "x"): shifted_x_attrs += 1
                if DY:
                    if maybe_shift_attr("y1", DY, match_y, "y"): shifted_y_attrs += 1
                    if maybe_shift_attr("y2", DY, match_y, "y"): shifted_y_attrs += 1

            continue  # done with <line>

        # Generic elements (ellipse, rect, text, etc.) — per-attribute shifting
        if DX:
            for a in ATTRS_X:
                if maybe_shift_attr(a, DX, match_x, "x"):
                    shifted_x_attrs += 1
        if DY:
            for a in ATTRS_Y:
                if maybe_shift_attr(a, DY, match_y, "y"):
                    shifted_y_attrs += 1

    new_svg = ET.tostring(root, encoding="unicode")
    return new_svg, shifted_x_attrs, shifted_y_attrs

def main():
    html_text = INPUT_FILE.read_text(encoding="utf-8")

    m = SVG_BLOCK_RE.search(html_text)
    if not m:
        raise SystemExit("No <svg>...</svg> block found in the input file.")

    svg_block = m.group(0)
    new_svg_block, count_x_attrs, count_y_attrs = process_svg(svg_block)

    # Replace the old SVG with the new one
    new_html = html_text[:m.start()] + new_svg_block + html_text[m.end():]

    # Write out
    if OUTPUT_FILE.resolve() == INPUT_FILE.resolve():
        if MAKE_BACKUP:
            backup = INPUT_FILE.with_suffix(INPUT_FILE.suffix + ".bak")
            shutil.copyfile(INPUT_FILE, backup)
        OUTPUT_FILE.write_text(new_html, encoding="utf-8")
        print(f"Updated in place: {INPUT_FILE}")
    else:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(new_html, encoding="utf-8")
        print(f"Wrote: {OUTPUT_FILE}")

    print(f"Attributes shifted on X-axis: {count_x_attrs}")
    print(f"Attributes shifted on Y-axis: {count_y_attrs}")

if __name__ == "__main__":
    main()
