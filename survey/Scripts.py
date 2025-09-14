# extract_updating_trees.py
from bs4 import BeautifulSoup
from pathlib import Path
import csv

INPUT = Path("an_updating_trees.html")
OUTDIR = Path("updating_trees")
OUTDIR.mkdir(parents=True, exist_ok=True)

def wrap(svg_str: str) -> str:
    return (
        "<!DOCTYPE html>\n<html>\n<head><meta charset='utf-8'></head>\n"
        f"<body>\n{svg_str}\n</body>\n</html>\n"
    )

html = INPUT.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

rows = []
count = 0
for idx, sec in enumerate(soup.select("section.tree-table"), start=1):
    svgs = sec.find_all("svg")
    if len(svgs) < 2:
        # still record what we saw for debugging
        rows.append({
            "tree_index": idx,
            "section_id": sec.get("id", ""),
            "svgs_in_section": len(svgs),
            "file_a": "",
            "file_b": "",
        })
        continue

    a_name = f"Tree_{idx}a.html"
    b_name = f"Tree_{idx}r.html"
    (OUTDIR / a_name).write_text(wrap(str(svgs[-2])), encoding="utf-8")
    (OUTDIR / b_name).write_text(wrap(str(svgs[-1])), encoding="utf-8")
    rows.append({
        "tree_index": idx,
        "section_id": sec.get("id", ""),
        "svgs_in_section": len(svgs),
        "file_a": a_name,
        "file_b": b_name,
    })
    count += 2

with open(OUTDIR / "manifest.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

print(f"Done. Wrote {count} SVG snippet files to {OUTDIR}/ and a manifest.csv")
