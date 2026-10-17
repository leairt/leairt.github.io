"""Validate the portfolio pages and copy only their dependencies to dist/client."""

import argparse
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist" / "client"
PAGES = ("index.html", "projects/index.html", "projects/3d-reconstruction/index.html", "projects/slavuj/index.html", "projects/artist-classification/index.html", "projects/bomgerman/index.html", "projects/clp/index.html")
CSS_URL = re.compile(r'''url\(\s*(?:"([^"]*)"|'([^']*)'|([^)]*))\s*\)''')


class References(HTMLParser):
    """Read asset references and fragment targets without external dependencies."""

    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if not value:
                continue
            if key in ("href", "src", "poster"):
                self.links.append(value)
            elif key == "id":
                if value in self.ids:
                    raise ValueError(f"Duplicate HTML id: {value}")
                self.ids.add(value)


def collect():
    """Return reachable source files, rejecting missing assets and broken anchors."""
    pending = list(PAGES)
    visited = set()
    targets = {}
    fragments = []

    while pending:
        relative = pending.pop()
        if relative in visited:
            continue
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(f"Missing site asset: {relative}")
        visited.add(relative)
        if source.suffix not in (".html", ".css"):
            continue

        content = source.read_text(encoding="utf-8")
        if source.suffix == ".html":
            parser = References()
            parser.feed(content)
            links = parser.links
            targets[relative] = parser.ids
        else:
            links = [next(part for part in match if part) for match in CSS_URL.findall(content)]

        for link in links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            target = (ROOT / path.lstrip("/")) if path.startswith("/") else source.parent / path
            if not path:
                target = source
            elif target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if not target.is_relative_to(ROOT):
                raise ValueError(f"Reference outside the site: {relative} -> {link}")
            dependency = str(target.relative_to(ROOT))
            pending.append(dependency)
            if url.fragment and target.suffix == ".html":
                fragments.append((relative, dependency, unquote(url.fragment)))

    for source, target, fragment in fragments:
        if fragment not in targets.get(target, set()):
            raise ValueError(f"Broken anchor: {source} -> {target}#{fragment}")
    return sorted(visited)


def build():
    files = collect()
    staging = OUTPUT.parent / ".client-build"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    for relative in files:
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    staging.rename(OUTPUT)
    size = sum((ROOT / name).stat().st_size for name in files) / 1024 / 1024
    print(f"Built {len(files)} files ({size:.1f} MB). All local assets and anchors resolved.")
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate without writing build output")
    parser.add_argument("--list", action="store_true", help="List all required website files")
    args = parser.parse_args()
    if args.list:
        print("\n".join(collect()))
    elif args.check:
        print(f"Validated {len(collect())} files; all local assets and anchors resolved.")
    else:
        build()
