#!/usr/bin/env python3
"""Converte o relatorio Markdown em um PDF editorial com ReportLab."""

from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "relatorio_tecnico.md"
OUTPUT = ROOT / "reports" / "relatorio_tecnico.pdf"

NAVY = colors.HexColor("#123047")
TEAL = colors.HexColor("#0F766E")
ORANGE = colors.HexColor("#EA580C")
RED = colors.HexColor("#B91C1C")
SLATE = colors.HexColor("#475569")
LIGHT = colors.HexColor("#E7F3F1")
PALE_ORANGE = colors.HexColor("#FFF3E8")
GRID = colors.HexColor("#CBD5E1")
WHITE = colors.white


def register_fonts() -> None:
    base = Path("/usr/share/fonts/truetype/dejavu")
    pdfmetrics.registerFont(TTFont("DejaVu", base / "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", base / "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Oblique", base / "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVuMono", base / "DejaVuSansMono.ttf"))
    pdfmetrics.registerFontFamily(
        "DejaVu",
        normal="DejaVu",
        bold="DejaVu-Bold",
        italic="DejaVu-Oblique",
        boldItalic="DejaVu-Bold",
    )


def make_styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=sample["Title"],
            fontName="DejaVu-Bold",
            fontSize=27,
            leading=32,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=12,
        ),
        "cover_subtitle": ParagraphStyle(
            "CoverSubtitle",
            fontName="DejaVu",
            fontSize=15,
            leading=21,
            textColor=TEAL,
            spaceAfter=10,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta",
            fontName="DejaVu",
            fontSize=10,
            leading=16,
            textColor=SLATE,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=sample["Heading1"],
            fontName="DejaVu-Bold",
            fontSize=17,
            leading=21,
            textColor=NAVY,
            spaceBefore=16,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=sample["Heading2"],
            fontName="DejaVu-Bold",
            fontSize=12,
            leading=16,
            textColor=TEAL,
            spaceBefore=11,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=sample["BodyText"],
            fontName="DejaVu",
            fontSize=9.25,
            leading=13.4,
            textColor=colors.HexColor("#1F2937"),
            alignment=TA_LEFT,
            spaceAfter=6.5,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="DejaVu",
            fontSize=9.1,
            leading=13,
            textColor=colors.HexColor("#1F2937"),
        ),
        "callout": ParagraphStyle(
            "Callout",
            fontName="DejaVu",
            fontSize=9,
            leading=13,
            textColor=NAVY,
            backColor=PALE_ORANGE,
            borderColor=ORANGE,
            borderWidth=0.8,
            borderPadding=10,
            spaceBefore=6,
            spaceAfter=10,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName="DejaVu-Oblique",
            fontSize=7.5,
            leading=10,
            textColor=SLATE,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            fontName="DejaVu-Bold",
            fontSize=7.2,
            leading=9.3,
            textColor=WHITE,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            fontName="DejaVu",
            fontSize=7.1,
            leading=9.3,
            textColor=colors.HexColor("#1F2937"),
        ),
    }


def inline_markup(text: str) -> str:
    value = html.escape(text.strip())
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`(.+?)`", r'<font name="DejaVuMono" size="8">\1</font>', value)
    value = re.sub(
        r"(https?://[^\s<]+)",
        r'<link href="\1" color="#0F766E">\1</link>',
        value,
    )
    return value


def image_flowable(relative_path: str, caption: str, max_width: float) -> list:
    path = (SOURCE.parent / relative_path).resolve()
    if not path.exists():
        return [Paragraph(f"Figura não encontrada: {html.escape(relative_path)}", STYLES["callout"])]
    with PILImage.open(path) as bitmap:
        width, height = bitmap.size
    ratio = min(max_width / width, 10.5 * cm / height)
    graphic = Image(str(path), width=width * ratio, height=height * ratio)
    graphic.hAlign = "CENTER"
    return [graphic, Paragraph(caption, STYLES["caption"])]


def table_flowable(rows: list[list[str]], available_width: float) -> Table:
    columns = len(rows[0])
    weights = []
    for column_index in range(columns):
        longest = max(len(row[column_index]) for row in rows)
        weights.append(min(max(longest, 8), 36))
    total = sum(weights)
    widths = [available_width * weight / total for weight in weights]
    formatted = []
    for row_index, row in enumerate(rows):
        style = STYLES["table_header"] if row_index == 0 else STYLES["table_cell"]
        formatted.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(formatted, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, GRID),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def parse_markdown(lines: list[str], available_width: float) -> list:
    story: list = []
    paragraph_buffer: list[str] = []
    bullet_buffer: list[str] = []
    table_buffer: list[list[str]] = []

    def flush_paragraph() -> None:
        if paragraph_buffer:
            story.append(Paragraph(inline_markup(" ".join(paragraph_buffer)), STYLES["body"]))
            paragraph_buffer.clear()

    def flush_bullets() -> None:
        if bullet_buffer:
            items = [
                ListItem(Paragraph(inline_markup(item), STYLES["bullet"]), leftIndent=10)
                for item in bullet_buffer
            ]
            story.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    start="circle",
                    leftIndent=16,
                    bulletFontName="DejaVu",
                    bulletFontSize=7,
                    spaceAfter=7,
                )
            )
            bullet_buffer.clear()

    def flush_table() -> None:
        if table_buffer:
            if len(table_buffer) >= 2 and all(set(cell) <= {"-", ":", " "} for cell in table_buffer[1]):
                del table_buffer[1]
            story.append(table_flowable(table_buffer, available_width))
            story.append(Spacer(1, 7))
            table_buffer.clear()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_bullets()
            table_buffer.append([cell.strip() for cell in line.strip("|").split("|")])
            continue
        flush_table()
        if not line.strip():
            flush_paragraph()
            flush_bullets()
            continue
        image_match = re.fullmatch(r"!\[(.+?)\]\((.+?)\)", line.strip())
        if image_match:
            flush_paragraph()
            flush_bullets()
            story.extend(image_flowable(image_match.group(2), image_match.group(1), available_width))
        elif line.startswith("### "):
            flush_paragraph()
            flush_bullets()
            story.append(Paragraph(inline_markup(line[4:]), STYLES["h2"]))
        elif line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            story.append(Paragraph(inline_markup(line[3:]), STYLES["h1"]))
            story.append(HRFlowable(width="100%", thickness=1.2, color=TEAL, spaceAfter=4))
        elif line.startswith("> "):
            flush_paragraph()
            flush_bullets()
            story.append(Paragraph(inline_markup(line[2:]), STYLES["callout"]))
        elif line.startswith("- "):
            flush_paragraph()
            bullet_buffer.append(line[2:])
        elif re.match(r"^\d+\. ", line):
            flush_paragraph()
            bullet_buffer.append(line)
        else:
            flush_bullets()
            paragraph_buffer.append(line.strip())
    flush_paragraph()
    flush_bullets()
    flush_table()
    return story


def draw_page(canvas, doc) -> None:
    width, height = A4
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#D7E3E8"))
        canvas.setLineWidth(0.6)
        canvas.line(1.6 * cm, height - 1.25 * cm, width - 1.6 * cm, height - 1.25 * cm)
        canvas.setFont("DejaVu-Bold", 7.5)
        canvas.setFillColor(NAVY)
        canvas.drawString(1.6 * cm, height - 0.95 * cm, "TECH CHALLENGE | FASE 3")
        canvas.setFont("DejaVu", 7.5)
        canvas.setFillColor(SLATE)
        canvas.drawRightString(width - 1.6 * cm, height - 0.95 * cm, "Alfabetizacao e inteligencia analitica")
        canvas.line(1.6 * cm, 1.15 * cm, width - 1.6 * cm, 1.15 * cm)
        canvas.drawString(1.6 * cm, 0.78 * cm, "Relatorio tecnico")
        canvas.drawRightString(width - 1.6 * cm, 0.78 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def build() -> None:
    register_fonts()
    global STYLES
    STYLES = make_styles()
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=1.65 * cm,
        rightMargin=1.65 * cm,
        topMargin=1.65 * cm,
        bottomMargin=1.55 * cm,
        title="Predicao e Inteligencia Analitica para Alfabetizacao no Brasil",
        author="Equipe do Tech Challenge",
        subject="Tech Challenge - Fase 3",
    )
    width, height = A4
    available_width = width - document.leftMargin - document.rightMargin

    story = [
        Spacer(1, 1.1 * cm),
        Paragraph("TECH CHALLENGE | FASE 3", STYLES["cover_meta"]),
        Spacer(1, 0.5 * cm),
        Paragraph("Predição e Inteligência Analítica para Alfabetização no Brasil", STYLES["cover_title"]),
        HRFlowable(width="35%", thickness=5, color=TEAL, hAlign="LEFT", spaceBefore=4, spaceAfter=14),
        Paragraph(
            "Uma solução reproduzível de Machine Learning para estimar risco e priorizar apoio territorial",
            STYLES["cover_subtitle"],
        ),
        Spacer(1, 1.2 * cm),
        Table(
            [
                [Paragraph("CURSO", STYLES["table_header"]), Paragraph("Pós-graduação em Inteligência Artificial", STYLES["table_cell"])],
                [Paragraph("EQUIPE", STYLES["table_header"]), Paragraph("[preencher nomes e RM]", STYLES["table_cell"])],
                [Paragraph("DATA", STYLES["table_header"]), Paragraph("[preencher]", STYLES["table_cell"])],
                [Paragraph("VERSÃO", STYLES["table_header"]), Paragraph("1.0 - metodologia e evidências consolidadas", STYLES["table_cell"])],
            ],
            colWidths=[3.0 * cm, available_width - 3.0 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), NAVY),
                    ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F8FAFC")),
                    ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            ),
        ),
        Spacer(1, 1.25 * cm),
        Paragraph(
            "NOTA DE INTEGRIDADE | Métricas preditivas não são simuladas. Os campos sinalizados no relatório serão preenchidos pela execução com a exportação real do BigQuery.",
            STYLES["callout"],
        ),
        Spacer(1, 1.0 * cm),
        Paragraph(
            "Fontes: Inep, Base dos Dados e IBGE | Pipeline Python e BigQuery SQL",
            STYLES["cover_meta"],
        ),
        PageBreak(),
    ]

    source_lines = SOURCE.read_text(encoding="utf-8").splitlines()
    start = next(index for index, line in enumerate(source_lines) if line == "## Resumo executivo")
    story.extend(parse_markdown(source_lines[start:], available_width))
    document.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    print(f"PDF criado: {OUTPUT}")


if __name__ == "__main__":
    build()
