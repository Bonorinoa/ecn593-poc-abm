#!/usr/bin/env python3
"""Build a standalone academic lecture-notes PDF from a JSON spec.

Designed for the ECN 593 short course. Uses Times New Roman (macOS
Supplemental fonts) so Greek and common math glyphs render.

Spec schema
-----------
{
  "lecture_number": 1,
  "title": "History Matching",
  "subtitle": "Ruling out worlds rather than fitting them",
  "running_header": "Lecture 1 · History Matching",
  "author": "ECN 593 short course notes (study draft, not a frozen specification)",
  "date": "August 2026",
  "abstract": "One or two paragraphs.",
  "elements": [
      {"type": "heading", "level": 1, "text": "Section title"},
      {"type": "heading", "level": 2, "text": "Subsection"},
      {"type": "paragraph", "text": "Body. Use <i>italics</i>, <b>bold</b>, <super>2</super>."},
      {"type": "bullet", "items": ["item one", "item two"]},
      {"type": "enum", "items": ["first", "second"]},
      {"type": "display", "text": "I(c) = (z − M(c))′ V<sup>−1</sup> (z − M(c))"},
      {"type": "callout", "title": "This is not", "text": "..."},
      {"type": "table", "caption": "Optional caption", "header": true,
       "rows": [["H1", "H2"], ["a", "b"]]},
      {"type": "pagebreak"}
  ]
}

Paragraph text is ReportLab XML. Escape literal < > & as &lt; &gt; &amp;.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
FONT_REG = FONT_DIR / "Times New Roman.ttf"
FONT_BOLD = FONT_DIR / "Times New Roman Bold.ttf"
FONT_ITAL = FONT_DIR / "Times New Roman Italic.ttf"
FONT_BI = FONT_DIR / "Times New Roman Bold Italic.ttf"

INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#444444")
RULE = colors.HexColor("#222222")
CALLOUT_BG = colors.HexColor("#f4f1ea")
CALLOUT_EDGE = colors.HexColor("#6b5344")
HEADER_RULE = colors.HexColor("#8a7358")
TABLE_HEAD = colors.HexColor("#ece6dc")
LIGHT_GRID = colors.HexColor("#b8b0a4")


def _register_fonts() -> str:
    if not FONT_REG.exists():
        raise FileNotFoundError(f"Missing body font: {FONT_REG}")
    pdfmetrics.registerFont(TTFont("TNRoman", str(FONT_REG)))
    pdfmetrics.registerFont(TTFont("TNRoman-Bold", str(FONT_BOLD)))
    pdfmetrics.registerFont(TTFont("TNRoman-Italic", str(FONT_ITAL)))
    pdfmetrics.registerFont(TTFont("TNRoman-BoldItalic", str(FONT_BI)))
    from reportlab.pdfbase.pdfmetrics import registerFontFamily

    registerFontFamily(
        "TNRoman",
        normal="TNRoman",
        bold="TNRoman-Bold",
        italic="TNRoman-Italic",
        boldItalic="TNRoman-BoldItalic",
    )
    return "TNRoman"


def _styles(font: str) -> dict:
    base = getSampleStyleSheet()
    s = {}
    s["title"] = ParagraphStyle(
        "LTitle",
        parent=base["Title"],
        fontName=f"{font}-Bold",
        fontSize=18,
        leading=22,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=6,
        tracking=0,
    )
    s["subtitle"] = ParagraphStyle(
        "LSubtitle",
        parent=base["Normal"],
        fontName=f"{font}-Italic",
        fontSize=12,
        leading=16,
        textColor=MUTED,
        spaceAfter=10,
    )
    s["meta"] = ParagraphStyle(
        "LMeta",
        parent=base["Normal"],
        fontName=font,
        fontSize=9.5,
        leading=13,
        textColor=MUTED,
        spaceAfter=4,
    )
    s["abstract_label"] = ParagraphStyle(
        "LAbsLab",
        parent=base["Normal"],
        fontName=f"{font}-Bold",
        fontSize=10,
        leading=13,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
    )
    s["abstract"] = ParagraphStyle(
        "LAbs",
        parent=base["Normal"],
        fontName=f"{font}-Italic",
        fontSize=10.5,
        leading=14.5,
        textColor=INK,
        alignment=TA_JUSTIFY,
        leftIndent=12,
        rightIndent=12,
        spaceAfter=12,
    )
    s["h1"] = ParagraphStyle(
        "LH1",
        parent=base["Heading1"],
        fontName=f"{font}-Bold",
        fontSize=13.5,
        leading=17,
        textColor=INK,
        spaceBefore=16,
        spaceAfter=8,
        borderPadding=0,
    )
    s["h2"] = ParagraphStyle(
        "LH2",
        parent=base["Heading2"],
        fontName=f"{font}-Bold",
        fontSize=11.5,
        leading=15,
        textColor=INK,
        spaceBefore=12,
        spaceAfter=6,
    )
    s["h3"] = ParagraphStyle(
        "LH3",
        parent=base["Heading3"],
        fontName=f"{font}-BoldItalic",
        fontSize=11,
        leading=14,
        textColor=INK,
        spaceBefore=10,
        spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "LBody",
        parent=base["Normal"],
        fontName=font,
        fontSize=10.5,
        leading=14.8,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    s["bullet"] = ParagraphStyle(
        "LBullet",
        parent=s["body"],
        leftIndent=16,
        spaceAfter=3,
        alignment=TA_LEFT,
    )
    s["display"] = ParagraphStyle(
        "LDisplay",
        parent=base["Normal"],
        fontName=f"{font}-Italic",
        fontSize=11,
        leading=16,
        textColor=INK,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8,
        leftIndent=18,
        rightIndent=18,
    )
    s["callout_title"] = ParagraphStyle(
        "LCallT",
        parent=base["Normal"],
        fontName=f"{font}-Bold",
        fontSize=9.5,
        leading=12,
        textColor=CALLOUT_EDGE,
        spaceAfter=3,
    )
    s["callout_body"] = ParagraphStyle(
        "LCallB",
        parent=base["Normal"],
        fontName=font,
        fontSize=10,
        leading=13.5,
        textColor=INK,
        alignment=TA_JUSTIFY,
    )
    s["caption"] = ParagraphStyle(
        "LCap",
        parent=base["Normal"],
        fontName=f"{font}-Italic",
        fontSize=9,
        leading=12,
        textColor=MUTED,
        spaceBefore=3,
        spaceAfter=10,
        alignment=TA_LEFT,
    )
    s["footer"] = ParagraphStyle(
        "LFoot",
        parent=base["Normal"],
        fontName=font,
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
    s["cell"] = ParagraphStyle(
        "LCell",
        parent=base["Normal"],
        fontName=font,
        fontSize=8.5,
        leading=11.5,
        textColor=INK,
    )
    s["cell_h"] = ParagraphStyle(
        "LCellH",
        parent=s["cell"],
        fontName=f"{font}-Bold",
    )
    s["ref"] = ParagraphStyle(
        "LRef",
        parent=base["Normal"],
        fontName=font,
        fontSize=9.5,
        leading=13,
        textColor=INK,
        leftIndent=16,
        firstLineIndent=-16,
        spaceAfter=5,
        alignment=TA_LEFT,
    )
    return s


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(str(text), style)


def _callout(title: str, text: str, styles: dict):
    inner = [
        _p(title, styles["callout_title"]),
        _p(text, styles["callout_body"]),
    ]
    tbl = Table([[inner]], colWidths=[6.3 * inch])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CALLOUT_BG),
                ("BOX", (0, 0), (-1, -1), 0.8, CALLOUT_EDGE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return KeepTogether([Spacer(1, 6), tbl, Spacer(1, 8)])


def _table(el: dict, styles: dict):
    raw = el.get("rows") or []
    if not raw:
        return []
    header = bool(el.get("header", True))
    formatted = []
    for i, row in enumerate(raw):
        st = styles["cell_h"] if (header and i == 0) else styles["cell"]
        formatted.append([_p(str(c), st) for c in row])
    n = max(len(r) for r in formatted)
    usable = 6.5 * inch
    col_w = [usable / n] * n
    tbl = Table(formatted, colWidths=col_w, repeatRows=1 if header else 0)
    cmd = [
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        cmd += [
            ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, RULE),
        ]
    tbl.setStyle(TableStyle(cmd))
    out = [tbl]
    if el.get("caption"):
        out.append(_p(el["caption"], styles["caption"]))
    else:
        out.append(Spacer(1, 8))
    return out


def build(spec: dict, out_path: str) -> dict:
    font = _register_fonts()
    styles = _styles(font)
    n = spec.get("lecture_number", "")
    title = spec.get("title", "Lecture")
    running = spec.get("running_header") or f"Lecture {n} · {title}"
    author = spec.get("author", "ECN 593 short course notes")
    date = spec.get("date", "August 2026")

    story = []
    kicker = f"ECN 593  ·  Applied project short course  ·  Lecture {n}"
    story.append(_p(kicker.upper(), styles["meta"]))
    story.append(
        HRFlowable(width="100%", thickness=1.2, color=HEADER_RULE, spaceAfter=10)
    )
    story.append(_p(title, styles["title"]))
    if spec.get("subtitle"):
        story.append(_p(spec["subtitle"], styles["subtitle"]))
    story.append(_p(f"{author}<br/>{date}", styles["meta"]))
    if spec.get("abstract"):
        story.append(_p("Abstract", styles["abstract_label"]))
        story.append(_p(spec["abstract"], styles["abstract"]))
        story.append(
            HRFlowable(width="100%", thickness=0.4, color=LIGHT_GRID, spaceAfter=8)
        )

    for el in spec.get("elements", []):
        et = el.get("type")
        if et == "heading":
            level = int(el.get("level", 1))
            key = {1: "h1", 2: "h2", 3: "h3"}.get(level, "h1")
            story.append(_p(el.get("text", ""), styles[key]))
        elif et == "paragraph":
            story.append(_p(el.get("text", ""), styles["body"]))
        elif et == "bullet":
            items = []
            for it in el.get("items", []):
                items.append(
                    ListItem(_p(it, styles["bullet"]), leftIndent=12, bulletColor=INK)
                )
            story.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    start="•",
                    leftIndent=18,
                    bulletFontName=font,
                    bulletFontSize=10,
                    spaceAfter=8,
                )
            )
        elif et == "enum":
            items = []
            for it in el.get("items", []):
                items.append(
                    ListItem(_p(it, styles["bullet"]), leftIndent=18, bulletColor=INK)
                )
            story.append(
                ListFlowable(
                    items,
                    bulletType="1",
                    leftIndent=22,
                    bulletFontName=font,
                    bulletFontSize=10,
                    spaceAfter=8,
                )
            )
        elif et == "display":
            story.append(_p(el.get("text", ""), styles["display"]))
        elif et == "callout":
            story.append(
                _callout(el.get("title", "Note"), el.get("text", ""), styles)
            )
        elif et == "table":
            story.extend(_table(el, styles))
        elif et == "ref":
            story.append(_p(el.get("text", ""), styles["ref"]))
        elif et == "pagebreak":
            story.append(PageBreak())
        elif et == "pre":
            story.append(
                Preformatted(
                    el.get("text", ""),
                    ParagraphStyle(
                        "LPre",
                        fontName="Courier",
                        fontSize=8.5,
                        leading=11,
                        textColor=INK,
                        spaceAfter=8,
                    ),
                )
            )
        else:
            print(f"warning: unknown element type {et!r}", file=sys.stderr)

    def _on_page(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(HEADER_RULE)
        canvas.setLineWidth(0.6)
        canvas.line(0.85 * inch, 10.45 * inch, 7.65 * inch, 10.45 * inch)
        canvas.setFont("TNRoman-Italic", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.85 * inch, 10.55 * inch, running[:90])
        canvas.drawRightString(7.65 * inch, 10.55 * inch, "study draft")
        canvas.line(0.85 * inch, 0.55 * inch, 7.65 * inch, 0.55 * inch)
        canvas.setFont("TNRoman", 8)
        canvas.drawCentredString(4.25 * inch, 0.38 * inch, f"{doc.page}")
        canvas.restoreState()

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.75 * inch,
        title=f"Lecture {n}: {title}",
        author=author,
        subject="ECN 593 applied project short course",
    )
    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return {"output": out_path, "elements": len(spec.get("elements", []))}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("spec")
    p.add_argument("-o", "--output", required=True)
    args = p.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    result = build(spec, args.output)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
