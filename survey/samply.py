"""
Generate tree HTML files named tree_2a.html, tree_2r.html, ..., tree_21a.html, tree_21r.html
into a folder called 'updated_trees'.

It uses 'Tree_Question.html' as a template (must be in the same folder as this script).
"""

from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    out_dir = base_dir / "updated_trees"
    out_dir.mkdir(parents=True, exist_ok=True)

    template_path = base_dir / "Tree_Question.html"
    if not template_path.exists():
        raise FileNotFoundError("Tree_Question.html not found in the script folder")

    template = template_path.read_text(encoding="utf-8")

    for n in range(2, 22):  # 2 to 21 inclusive
        for suffix in ("a", "r"):
            fname = f"tree_{n}{suffix}.html"
            (out_dir / fname).write_text(template, encoding="utf-8")

    print(f"Created {len(list(out_dir.iterdir()))} files in {out_dir.resolve()}")

if __name__ == "__main__":
    main()
