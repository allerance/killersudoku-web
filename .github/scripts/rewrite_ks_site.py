#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path

ROOT = Path(".").resolve()


def copy_src(src: Path) -> None:
    for child in ROOT.iterdir():
        if child.name in {".git", ".github"}:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    for child in src.iterdir():
        if child.name in {".git", ".github"}:
            continue
        dest = ROOT / child.name
        if child.is_dir():
            shutil.copytree(child, dest)
        else:
            shutil.copy2(child, dest)


def rewrite() -> None:
    (ROOT / "CNAME").write_text("killersudoku.arcadewick.com\n")

    p = ROOT / "404.html"
    if p.exists():
        p.write_text(p.read_text().replace("/arcadewick-web", "/killersudoku-web"))

    idx = ROOT / "index.html"
    html = idx.read_text()
    old = '  <base href="/">\n'
    new = (
        "  <script>\n"
        "  document.write('<base href=\"' + (location.pathname.indexOf('/killersudoku-web') === 0 ? '/killersudoku-web/' : '/') + '\">');\n"
        "  </script>\n"
    )
    if old in html:
        idx.write_text(html.replace(old, new, 1))

    (ROOT / "README.md").write_text(
        "Static GitHub Pages host for Arcadewick Killer Sudoku.\n"
        "\n"
        "- Play: http://killersudoku.arcadewick.com\n"
        "- github.io: https://allerance.github.io/killersudoku-web/\n"
        "- Compiled web output only. Flutter source stays in the private allerance/arcadewick repo.\n"
        "\n"
        "Pages: deploy from branch main, folder /. Do not Enforce HTTPS until a certificate exists.\n"
        "\n"
        "DNS (GoDaddy): CNAME host killersudoku → allerance.github.io\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy-from", required=True)
    args = parser.parse_args()
    src = Path(args.copy_from).resolve()
    if not (src / "main.dart.js").is_file():
        raise SystemExit(f"missing main.dart.js in {src}")
    copy_src(src)
    rewrite()
    cname = (ROOT / "CNAME").read_text().strip()
    if cname != "killersudoku.arcadewick.com":
        raise SystemExit(f"bad CNAME: {cname!r}")
    if not (ROOT / "main.dart.js").is_file():
        raise SystemExit("missing main.dart.js after copy")


if __name__ == "__main__":
    main()
