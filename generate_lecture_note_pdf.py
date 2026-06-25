from pathlib import Path
import argparse
from datetime import datetime
import os
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parent
DEFAULT_SRC = ROOT / "class-notes-first-three-methods.md"
DEFAULT_DST = ROOT / "class-notes-first-three-methods.pdf"


def format_inline(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleCenter",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="H2Note",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="H3Note",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyNote",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletNote",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        leftIndent=14,
        firstLineIndent=-8,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="NumNote",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="FigureCaption",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="TitlePageCourse",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        spaceAfter=20,
    )
)
styles.add(
    ParagraphStyle(
        name="TitlePageTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="TitlePageMeta",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="TitlePageInstitution",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        spaceAfter=6,
    )
)


def build_image(image_path: Path) -> Image:
    reader = ImageReader(str(image_path))
    width_px, height_px = reader.getSize()
    max_width = A4[0] - 4 * cm
    max_height = 10 * cm
    scale = min(max_width / width_px, max_height / height_px)
    image = Image(str(image_path), width=width_px * scale, height=height_px * scale)
    image.hAlign = "CENTER"
    return image


def build_story(lines: list[str]):
    story = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()

        if not stripped:
            story.append(Spacer(1, 6))
            index += 1
            continue

        if stripped == "---":
            story.append(Spacer(1, 10))
            index += 1
            continue

        if stripped.startswith("# "):
            story.append(Paragraph(format_inline(stripped[2:]), styles["TitleCenter"]))
            index += 1
            continue

        if stripped.startswith("## "):
            story.append(Paragraph(format_inline(stripped[3:]), styles["H2Note"]))
            index += 1
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(format_inline(stripped[4:]), styles["H3Note"]))
            index += 1
            continue

        image_match = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if image_match:
            image_path = ROOT / image_match.group(2)
            story.append(build_image(image_path))
            story.append(Spacer(1, 6))
            index += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                row = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                table_lines.append(row)
                index += 1
            if len(table_lines) >= 2:
                data = table_lines[:1] + table_lines[2:]
                table = Table(data, repeatRows=1)
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E2F3")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                            ("FONTSIZE", (0, 0), (-1, -1), 9),
                            ("LEADING", (0, 0), (-1, -1), 12),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
                            ("LEFTPADDING", (0, 0), (-1, -1), 6),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                            ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        ]
                    )
                )
                story.append(table)
                story.append(Spacer(1, 8))
            continue

        bullet_match = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet_match:
            story.append(Paragraph("&bull; " + format_inline(bullet_match.group(1)), styles["BulletNote"]))
            index += 1
            continue

        num_match = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if num_match:
            story.append(Paragraph(f"{num_match.group(1)}. " + format_inline(num_match.group(2)), styles["NumNote"]))
            index += 1
            continue

        if stripped.startswith("*Figure ") and stripped.endswith("*"):
            story.append(Paragraph(format_inline(stripped[1:-1]), styles["FigureCaption"]))
            index += 1
            continue

        story.append(Paragraph(format_inline(stripped), styles["BodyNote"]))
        index += 1

    return story


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a PDF from a Markdown lecture note with embedded figures.")
    parser.add_argument("src", nargs="?", default=str(DEFAULT_SRC), help="Source Markdown file")
    parser.add_argument("dst", nargs="?", default=str(DEFAULT_DST), help="Output PDF file")
    parser.add_argument("--course-name", default="Decision Theory and Application", help="Course name shown on the title page")
    parser.add_argument("--lecturer-name", default="Dr. Ir. Ahmad Perwira Mulia MSc", help="Lecturer name shown on the title page")
    parser.add_argument("--date-text", default="Semester B, 2026", help="Date shown on the title page")
    parser.add_argument("--institution-name", default="Civil Engineering Post Graduate Programs, Fakultas Teknik, Universitas Sumatera Utara", help="Institution name shown on the title page")
    parser.add_argument("--faculty-name", default="", help="Optional faculty or department line shown on the title page")
    parser.add_argument("--no-title-page", action="store_true", help="Generate the PDF without a title page")
    return parser.parse_args()


def derive_note_title(src: Path) -> str:
    stem = src.stem.replace("-", " ").strip()
    if "slide ready" in stem:
        return "Slide-Ready Lecture Note"
    if stem.startswith("class notes"):
        return "Lecture Note"
    return "Lecture Note"


def build_title_page(
    course_name: str,
    note_title: str,
    lecturer_name: str,
    date_text: str,
    institution_name: str,
    faculty_name: str,
):
    story = [
        Spacer(1, 5 * cm),
        Paragraph(format_inline(course_name), styles["TitlePageCourse"]),
        Paragraph(format_inline(note_title), styles["TitlePageTitle"]),
        Spacer(1, 1 * cm),
        Paragraph(format_inline(institution_name), styles["TitlePageInstitution"]),
    ]
    if faculty_name.strip():
        story.append(Paragraph(format_inline(faculty_name), styles["TitlePageInstitution"]))
    story.extend([
        Spacer(1, 0.3 * cm),
        Paragraph(format_inline(lecturer_name), styles["TitlePageMeta"]),
        Paragraph(format_inline(date_text), styles["TitlePageMeta"]),
        PageBreak(),
    ])
    return story


def main() -> None:
    args = parse_args()
    src = Path(args.src)
    dst = Path(args.dst)
    if not src.is_absolute():
        src = ROOT / src
    if not dst.is_absolute():
        dst = ROOT / dst

    lines = src.read_text(encoding="utf-8").splitlines()
    story = []
    if not args.no_title_page:
        story.extend(
            build_title_page(
                args.course_name,
                derive_note_title(src),
                args.lecturer_name,
                args.date_text,
                args.institution_name,
                args.faculty_name,
            )
        )
    story.extend(build_story(lines))
    temp_dst = dst.with_name(f"{dst.stem}.tmp{dst.suffix}")
    document = SimpleDocTemplate(
        str(temp_dst),
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    document.build(story)
    try:
        os.replace(temp_dst, dst)
        print(dst)
    except PermissionError:
        fallback_dst = dst.with_name(f"{dst.stem}-updated{dst.suffix}")
        os.replace(temp_dst, fallback_dst)
        print(fallback_dst)


if __name__ == "__main__":
    main()