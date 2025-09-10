from pathlib import Path
import re

# Which inline SVG tags to clean up
SHAPE_TAGS = r"(?:rect|ellipse|circle|path|polygon|polyline)"
TAG_RE = re.compile(rf"(<(?:{SHAPE_TAGS})\b)([^>]*?)(/?>)", re.IGNORECASE | re.DOTALL)

# style="...": capture value (single or double quotes)
STYLE_ATTR_RE = re.compile(r'style\s*=\s*"([^"]*)"|style\s*=\s*\'([^\']*)\'', re.IGNORECASE)
# generic attribute stripper
def strip_attr(attrs: str, name: str) -> str:
    return re.sub(rf'\s+{name}\s*=\s*"[^"]*"|\s+{name}\s*=\s*\'[^\']*\'', "", attrs, flags=re.IGNORECASE)

def parse_style(style_text: str) -> list[tuple[str, str]]:
    """
    Parse a style string into a list of (prop_lower, value_stripped) in order encountered.
    Ignores empty items; keeps raw value (case/spacing preserved except ends).
    """
    result = []
    for chunk in style_text.split(";"):
        if not chunk.strip():
            continue
        if ":" not in chunk:
            continue
        prop, val = chunk.split(":", 1)
        prop = prop.strip().lower()
        val = val.strip()
        result.append((prop, val))
    return result

def merge_styles(style_values: list[str]) -> str:
    """
    Merge multiple style attribute values. Later declarations override earlier ones (CSS behavior).
    Keeps property order by last occurrence.
    """
    order = []
    seen = set()
    merged = {}
    for s in style_values:
        for prop, val in parse_style(s):
            merged[prop] = val
            if prop in seen:
                # move prop to the end of order
                order = [p for p in order if p != prop]
            else:
                seen.add(prop)
            order.append(prop)
    if not order:
        return ""
    return "; ".join(f"{p}: {merged[p]}" for p in order) + ";"

def fix_shapes(html: str) -> tuple[str, int]:
    """
    For each shape tag:
      - remove duplicate style attributes, merge them into one
      - remove any fill="..." attribute, rely on style's fill
      - ensure self-closing '/>' if it was '/ >' or '>'
    """
    fixes = 0

    def repl(m):
        nonlocal fixes
        open_tag, attrs, end = m.groups()

        # collect all style values
        style_vals = [g for g in STYLE_ATTR_RE.findall(attrs)]
        style_vals = [a or b for (a, b) in style_vals]  # flatten tuple groups

        if not style_vals and 'fill=' not in attrs.lower():
            # no duplicate style and no fill attr -> nothing to do
            return m.group(0)

        # remove all style and any fill attrs
        attrs = strip_attr(attrs, "style")
        attrs = strip_attr(attrs, "fill")

        # merge styles if any
        merged_style = merge_styles(style_vals)

        # insert back single style if non-empty
        if merged_style:
            attrs = (attrs + f' style="{merged_style}"').rstrip()

        # spacing tidy
        attrs = (" " + attrs.strip()) if attrs.strip() else ""

        # normalize closing to '/>'
        end_norm = "/>" if end.strip() in (">", "/>", "/ >") else "/>"

        fixes += 1
        return f"{open_tag}{attrs} {end_norm}"

    return TAG_RE.sub(repl, html), fixes

def main():
    script_dir = Path(__file__).resolve().parent
    trees_dir = script_dir / "Trees"  # adjust if your structure differs

    if not trees_dir.exists():
        print(f'Folder not found: "{trees_dir}"')
        return

    html_files = sorted(trees_dir.glob("*.html"))
    if not html_files:
        print(f'No .html files found in "{trees_dir}"')
        return

    total_files = 0
    total_fixes = 0
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        fixed, n = fix_shapes(text)
        if n > 0:
            f.write_text(fixed, encoding="utf-8")
            print(f"Fixed {f.name}: {n} tag(s)")
            total_files += 1
            total_fixes += n
        else:
            print(f"No issues in {f.name}")

    print(f"\nDone. Files fixed: {total_files}/{len(html_files)} | Tags corrected: {total_fixes}")

if __name__ == "__main__":
    main()
