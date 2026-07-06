#!/usr/bin/env python3
"""Render one or more site pages (with their images/videos) to a single PDF.

Uses headless Chromium (Playwright) so CSS Grid/Flexbox/aspect-ratio render
exactly as in a browser, then concatenates the per-page PDFs with pypdf.

<video> elements can't play inside a PDF, so each one is swapped for a still
frame (captured at t=0) before printing.

Usage:
    python scripts/html_to_pdf.py page1.html page2.html -o combined.pdf
    python scripts/html_to_pdf.py projects/*.html -o all-projects.pdf

Requires: pip install playwright pypdf && playwright install chromium
"""
import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfWriter

VIDEO_TO_FRAME_JS = """
async () => {
  const videos = Array.from(document.querySelectorAll('video'));
  for (const video of videos) {
    try {
      if (video.readyState < 2) {
        await new Promise((resolve) => {
          video.addEventListener('loadeddata', resolve, { once: true });
          setTimeout(resolve, 3000);
        });
      }
      video.currentTime = 0;
      await new Promise((resolve) => setTimeout(resolve, 150));
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || video.clientWidth || 640;
      canvas.height = video.videoHeight || video.clientHeight || 480;
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
      const img = document.createElement('img');
      img.src = canvas.toDataURL('image/jpeg', 0.85);
      img.style.width = '100%';
      img.style.height = '100%';
      img.style.objectFit = video.style.objectFit || 'contain';
      img.className = video.className;
      video.replaceWith(img);
    } catch (e) {
      // leave the video element in place if we couldn't capture a frame
    }
  }
}
"""

HIDE_NAV_CSS = """
nav, header nav, .navbar { display: none !important; }
"""


def render_page_to_pdf(page, html_path: Path, out_pdf: Path, hide_nav: bool) -> None:
    url = html_path.resolve().as_uri()
    page.goto(url, wait_until="networkidle")
    page.evaluate(VIDEO_TO_FRAME_JS)
    if hide_nav:
        page.add_style_tag(content=HIDE_NAV_CSS)
    page.emulate_media(media="print")
    page.pdf(
        path=str(out_pdf),
        format="A4",
        print_background=True,
        margin={"top": "12mm", "bottom": "12mm", "left": "10mm", "right": "10mm"},
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html_files", nargs="+", help="HTML files to render, in the order they should appear")
    parser.add_argument("-o", "--output", required=True, help="Path for the combined output PDF")
    parser.add_argument("--keep-nav", action="store_true", help="Keep the site nav bar in the PDF (hidden by default)")
    args = parser.parse_args()

    html_paths = [Path(p) for p in args.html_files]
    missing = [p for p in html_paths if not p.exists()]
    if missing:
        for p in missing:
            print(f"NOT FOUND: {p}", file=sys.stderr)
        return 1

    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            for html_path in html_paths:
                tmp_pdf = Path(tmp) / (html_path.stem + ".pdf")
                print(f"Rendering {html_path} ...")
                render_page_to_pdf(page, html_path, tmp_pdf, hide_nav=not args.keep_nav)
                writer.append(str(tmp_pdf))
        browser.close()

    with open(out_path, "wb") as f:
        writer.write(f)
    print(f"Saved: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
