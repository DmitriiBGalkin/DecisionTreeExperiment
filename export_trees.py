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
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load lexicon module from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.Lexicon


def find_browser() -> Path:
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


def extract_svg(rendered_html: str, source_path: Path) -> str:
    """
    The tree files are full HTML documents, but the pair page should only embed
    the actual <svg>...</svg>. Embedding full HTML inside another HTML document
    can create unpredictable spacing.
    """
    match = re.search(
        r"<svg\b.*?</svg>",
        rendered_html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        raise ValueError(f"No SVG found in {source_path}")

    svg = match.group(0)

    # Normalize common lowercase SVG attributes from your files.
    svg = re.sub(r"\bviewbox=", "viewBox=", svg, flags=re.IGNORECASE)
    svg = re.sub(
        r"\bpreserveaspectratio=",
        "preserveAspectRatio=",
        svg,
        flags=re.IGNORECASE,
    )

    return svg


def discover_pairs():
    pairs = {}

    for path in UPDATING_DIR.glob("Tree_*[ar].html"):
        match = re.fullmatch(r"Tree_(\d+)([ar])\.html", path.name)
        if not match:
            continue

        idx = int(match.group(1))
        side = match.group(2)

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
        <h2>D</h2>
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
            f"--print-to-pdf={str(pdf_file)}",
            html_file.as_uri(),
        ],
        check=True,
    )


def crop_png_bottom_whitespace(
    png_file: Path,
    tolerance: int = 6,
    bottom_padding: int = 16,
):
    """
    Chrome screenshots capture the full viewport height. This removes the empty
    background area below the rendered page content.
    """
    try:
        from PIL import Image
    except ImportError as exc:
        raise ImportError(
            "PNG cropping requires Pillow. Install it with: pip install pillow"
        ) from exc

    with Image.open(png_file) as image:
        rgb = image.convert("RGB")
        width, height = rgb.size
        pixels = rgb.load()

        # The bottom-left pixel should be the page background color.
        background = pixels[0, height - 1]

        def differs_from_background(pixel) -> bool:
            return any(abs(pixel[i] - background[i]) > tolerance for i in range(3))

        crop_bottom = height

        for y in range(height - 1, -1, -1):
            row_has_content = any(
                differs_from_background(pixels[x, y])
                for x in range(width)
            )

            if row_has_content:
                crop_bottom = min(height, y + 1 + bottom_padding)
                break

        if crop_bottom < height:
            cropped = image.crop((0, 0, width, crop_bottom))

            # Save through a temporary file to avoid Windows file-locking issues.
            tmp_file = png_file.with_suffix(".tmp.png")
            cropped.save(tmp_file)
            tmp_file.replace(png_file)

            print(f"cropped PNG: {png_file.name} {width}x{height} -> {width}x{crop_bottom}")


def export_png(
    browser: Path,
    html_file: Path,
    png_file: Path,
    png_scale: float = 2.0,
):
    """
    Export a high-resolution PNG.

    --window-size controls the CSS layout size.
    --force-device-scale-factor controls the output pixel density.

    For example:
      window-size 1800x900 and scale 2 gives about 3600px wide output.
      window-size 1800x900 and scale 3 gives about 5400px wide output.
    """
    if png_file.exists():
        png_file.unlink()

    subprocess.run(
        [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--force-device-scale-factor={png_scale}",
            "--window-size=1800,900",
            f"--screenshot={str(png_file)}",
            html_file.as_uri(),
        ],
        check=True,
    )

    if not png_file.exists():
        raise RuntimeError(f"PNG was not created: {png_file}")

    crop_png_bottom_whitespace(png_file)


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

    parser.add_argument(
        "--png-scale",
        type=float,
        default=2.0,
        help="PNG resolution scale factor. Use 1, 2, or 3. Default: 2.",
    )

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
        a_rendered = render_template(a_path, context)
        r_rendered = render_template(r_path, context)

        a_svg = extract_svg(a_rendered, a_path)
        r_svg = extract_svg(r_rendered, r_path)

        html = pair_html(idx, a_svg, r_svg, args.lang)

        html_file = outdir / f"Tree_{idx:02d}_pair.html"
        html_file.write_text(html, encoding="utf-8")

        if "pdf" in args.format:
            if browser is None:
                raise RuntimeError("Browser was not initialized.")
            export_pdf(browser, html_file, outdir / f"Tree_{idx:02d}_pair.pdf")

        if "png" in args.format:
            if browser is None:
                raise RuntimeError("Browser was not initialized.")
            export_png(
                browser,
                html_file,
                outdir / f"Tree_{idx:02d}_pair.png",
                png_scale=args.png_scale,
            )

        print(f"done: Tree {idx}")

    print(f"written to: {outdir}")


if __name__ == "__main__":
    main()