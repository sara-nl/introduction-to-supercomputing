#!/usr/bin/env python3
"""Fail a deck build when a slide overflows or shrinks body text.

The check runs after the PDF exists. It fails the build when:

- the TeX log reports an Overfull \\hbox or Overfull \\vbox
- the log says a font shape was missing and a fallback was used
- any text span draws outside the page
- any text span is below the deck's minimum size, unless that size is
  listed in the allow file
- with --reference, a figure is under 70% of its original area, its
  centre has moved by more than 10% of the page, or source credits are
  stacked away from their images. A 960x540 full-slide raster is skipped.

The minimum is 14bp on a 540bp-tall deck and scales with the page
height, so a deck authored on a smaller canvas keeps its own scale.
Sizes already used before the 2026-10-25 restack belong in the allow
file. A new size under the minimum, such as 13bp prose on a 15.9bp
deck, fails.
"""

from __future__ import annotations

import argparse
import re
import sys

OVERFULL = re.compile(r"^Overfull \\[hv]box", re.M)
FONT_FALLBACK = re.compile(
    r"Font shape `.+` undefined|Some font shapes were not available|font substitution",
    re.I,
)


def allow_sizes(path: str | None) -> list[float]:
    if not path:
        return []
    sizes = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.split("#", 1)[0].strip()
            if line:
                sizes.append(float(line))
    return sizes


def allowed(size: float, sizes: list[float], tolerance: float) -> bool:
    return any(abs(size - item) <= tolerance for item in sizes)


def figure_boxes(page) -> list[tuple[float, float, float, float]]:
    """Photo and logo boxes. A full-slide raster is a page dump, not a figure."""
    width, height = page.rect.width, page.rect.height
    boxes = []
    for info in page.get_image_info():
        x0, y0, x1, y1 = info["bbox"]
        if (x1 - x0) >= width * 0.90 and (y1 - y0) >= height * 0.85:
            continue
        boxes.append((x0, y0, x1, y1))
    return boxes


def stacked_credits(page, index: int) -> list[str]:
    """A column of 'source' links that sits away from the photos."""
    width, height = page.rect.width, page.rect.height
    links = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            text = "".join(span["text"] for span in line["spans"]).strip().lower()
            if text in {"source", "_source_"}:
                links.append(line["bbox"])
    if len(links) < 3:
        return []
    pictures = figure_boxes(page)
    problems = []
    used = set()
    for i, box in enumerate(links):
        if i in used:
            continue
        cluster = [box]
        used.add(i)
        for j, other in enumerate(links):
            if j in used:
                continue
            if abs(other[0] - box[0]) <= 40:
                cluster.append(other)
                used.add(j)
        if len(cluster) < 3:
            continue
        top = min(item[1] for item in cluster)
        bottom = max(item[3] for item in cluster)
        if bottom - top < height * 0.18:
            continue
        away = 0
        for item in cluster:
            cx = (item[0] + item[2]) / 2
            cy = (item[1] + item[3]) / 2
            near = False
            for pic in pictures:
                if pic[0] - 8 <= cx <= pic[2] + 8 and pic[1] - 12 <= cy <= pic[3] + height * 0.08:
                    near = True
                    break
            if not near:
                away += 1
        if away == len(cluster):
            problems.append(
                f"p{index}: {len(cluster)} source credits are stacked away from their images"
            )
    return problems


def compare_figures(doc, reference: str) -> list[str]:
    import pymupdf

    original = pymupdf.open(reference)
    problems = []
    if original.page_count != doc.page_count:
        problems.append(
            f"page count {doc.page_count} does not match the original {original.page_count}"
        )
    for index, (new, old) in enumerate(zip(doc, original), 1):
        width, height = new.rect.width, new.rect.height
        fresh = figure_boxes(new)
        used = set()
        for box in figure_boxes(old):
            cx = (box[0] + box[2]) / 2
            cy = (box[1] + box[3]) / 2
            area = max((box[2] - box[0]) * (box[3] - box[1]), 1)
            best = None
            best_at = None
            for i, candidate in enumerate(fresh):
                if i in used:
                    continue
                dx = abs((candidate[0] + candidate[2]) / 2 - cx)
                dy = abs((candidate[1] + candidate[3]) / 2 - cy)
                score = dx + dy
                if best is None or score < best:
                    best = score
                    best_at = i
            if best_at is None:
                problems.append(f"p{index}: a figure from the original is missing")
                continue
            used.add(best_at)
            got = fresh[best_at]
            got_area = (got[2] - got[0]) * (got[3] - got[1])
            dx = abs((got[0] + got[2]) / 2 - cx)
            dy = abs((got[1] + got[3]) / 2 - cy)
            if got_area < area * 0.70:
                problems.append(
                    f"p{index}: a figure is {got_area / area:.0%} of its original area"
                )
            if dx > width * 0.10 or dy > height * 0.10:
                problems.append(
                    f"p{index}: a figure moved by more than 10% of the page"
                )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--log")
    parser.add_argument("--allow")
    parser.add_argument("--min-size", type=float, default=14.0)
    parser.add_argument("--reference-height", type=float, default=540.0)
    parser.add_argument("--edge", type=float, default=1.5,
                        help="how far past the page edge ink may go, in bp")
    parser.add_argument("--tolerance", type=float, default=0.45)
    parser.add_argument("--reference",
                        help="original PDF; figures must keep its area and place")
    args = parser.parse_args()

    problems: list[str] = []
    if args.log:
        try:
            log = open(args.log, encoding="utf-8", errors="replace").read()
        except FileNotFoundError:
            log = ""
            problems.append(f"log not found: {args.log}")
        for match in OVERFULL.finditer(log):
            line = log[match.start():].splitlines()[0]
            problems.append(f"overfull box: {line}")
        for match in FONT_FALLBACK.finditer(log):
            line = log[match.start():].splitlines()[0]
            problems.append(f"font fallback: {line}")

    import pymupdf

    sizes = allow_sizes(args.allow)
    doc = pymupdf.open(args.pdf)
    for index, page in enumerate(doc, 1):
        width, height = page.rect.width, page.rect.height
        floor = args.min_size * (height / args.reference_height)
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"]
                    if not text.strip():
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    size = float(span["size"])
                    if (
                        x0 < -args.edge
                        or y0 < -args.edge
                        or x1 > width + args.edge
                        or y1 > height + args.edge
                    ):
                        problems.append(
                            f"p{index}: text past the page edge "
                            f"({size:.2f}bp, {span['font']}) {text[:80]!r}"
                        )
                    elif x0 < width * 0.25 and x1 > width - 8 and (x1 - x0) > width * 0.55:
                        problems.append(
                            f"p{index}: line runs from the left margin to the page edge "
                            f"({size:.2f}bp, {span['font']}) {text[:80]!r}"
                        )
                    if size + 1e-6 < floor and not allowed(size, sizes, args.tolerance):
                        problems.append(
                            f"p{index}: text {size:.2f}bp is below {floor:.2f}bp "
                            f"and not in the allow list ({span['font']}) {text[:80]!r}"
                        )
            problems.extend(stacked_credits(page, index))

    if args.reference:
        problems.extend(compare_figures(doc, args.reference))

    if problems:
        print(f"{args.pdf}: {len(problems)} slide gate failure(s)", file=sys.stderr)
        for item in problems:
            print(f"  {item}", file=sys.stderr)
        return 1
    print(f"{args.pdf}: slide gate passed ({doc.page_count} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
