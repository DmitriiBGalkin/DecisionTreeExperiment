from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
from pathlib import Path

from django.template import Context, Engine


ROOT = Path(__file__).resolve().parent
UPDATING_DIR = ROOT / "survey" / "updating_trees"

LEXICON_FILES = {
    "en": ROOT / "survey" / "lexicon_en.py",
    "de": ROOT / "survey" / "lexicon_de.py",
}


def load_lexicon(lang: str):
    path = LEXICON_FILES[lang]
    spec = importlib.util.spec_from_file_location(f"lexicon_{lang}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Lexicon


def find_browser():
    candidates = [
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("Could not find Edge or Chrome.")


def render_template(path: Path, context_dict: dict) -> str:
    source = path.read_text(encoding="utf-8")
    engine = Engine(debug=False)
    template = engine.from_string(source)
    return template.render(Context(context_dict)).strip()


def discover_pairs():
    pairs = {}
    for path in UPDATING_DIR.glob("Tree_*[ar].html"):
        m = re.fullmatch(r"Tree_(\d+)([ar])\.html", path.name)
        if not m:
            continue
        idx = int(m.group(1))
        side = m.group(2)
        pairs.setdefault(idx, {})[side] = path

    ordered = []
    for idx in sorted(pairs):
        if "a" in pairs[idx] and "r" in pairs[idx]:
            ordered.append((idx, pairs[idx]["a"], pairs[idx]["r"]))
    return ordered


def pair_html(idx: int, a_svg: str, r_svg: str, lang: str) -> str:
    title = f"Tree {idx}" if lang == "en" else f"Baum {idx}"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
:root {{
  --tree-root-fill: #fff4cc;
  --tree-assets-fill: #fff4cc;
  --tree-denied-fill: #D3D3D3;
  --tree-approved-fill: #D3D3D3;
  --tree-stroke: #000;
  --tree-stroke-w: 2;
  --tree-text: #000;
}}

html, body {{
  margin: 0;
  padding: 0;
  background: #f7f7f7;
  font-family: Arial, sans-serif;
  color: #111827;
}}

.page {{
  padding: 24px;
}}

h1 {{
  font-size: 24px;
  margin: 0 0 16px;
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
  background: #fff;
}}

.grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}}

.card {{
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px;
  box-sizing: border-box;
}}

.card h2 {{
  margin: 0 0 10px;
  font-size: 16px;
  text-align: center;
}}

svg {{
  display: block;
  width: 100%;
  height: auto;
  background: white;
}}

@page {{
  margin: 12mm;
}}
</style>
</head>
<body>
  <div class="page">
    <h1>{title}</h1>
    <div class="grid">
      <section class="card">
        <h2>A</h2>
        {a_svg}
      </section>
      <section class="card">
        <h2>R</h2>
        {r_svg}
      </section>
    </div>
  </div>
</body>
</html>
"""


def export_pdf(browser: Path, html_file: Path, pdf_file: Path):
    subprocess.run(
        [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            html_file.as_uri(),
        ],
        check=True,
    )


def export_png(browser: Path, html_file: Path, png_file: Path):
    subprocess.run(
        [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--window-size=1800,900",
            f"--screenshot={png_file}",
            html_file.as_uri(),
        ],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["en", "de"], default="en")
    parser.add_argument(
        "--format",
        nargs="+",
        choices=["html", "pdf", "png"],
        default=["html"],
    )
    parser.add_argument("--outdir", default="updating_tree_exports")
    args = parser.parse_args()

    lexicon = load_lexicon(args.lang)
    pairs = discover_pairs()
    outdir = ROOT / args.outdir / args.lang
    outdir.mkdir(parents=True, exist_ok=True)

    browser = None
    if "pdf" in args.format or "png" in args.format:
        browser = find_browser()

    context = {
        "Lexicon": lexicon,
        "which_language": {
            "en": args.lang == "en",
            "de": args.lang == "de",
        },
        "en": args.lang == "en",
        "de": args.lang == "de",
    }

    for idx, a_path, r_path in pairs:
        a_svg = render_template(a_path, context)
        r_svg = render_template(r_path, context)
        html = pair_html(idx, a_svg, r_svg, args.lang)

        html_file = outdir / f"Tree_{idx:02d}_pair.html"
        html_file.write_text(html, encoding="utf-8")

        if "pdf" in args.format:
            export_pdf(browser, html_file, outdir / f"Tree_{idx:02d}_pair.pdf")

        if "png" in args.format:
            export_png(browser, html_file, outdir / f"Tree_{idx:02d}_pair.png")

        print(f"done: Tree {idx}")

    print(f"written to: {outdir}")


if __name__ == "__main__":
    main()