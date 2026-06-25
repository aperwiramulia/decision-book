from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "application-figures"
OUT_DIR.mkdir(exist_ok=True)


def load_font(size: int, bold: bool = False):
    candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = load_font(44, bold=True)
SUBTITLE_FONT = load_font(28, bold=True)
TEXT_FONT = load_font(24)
SMALL_FONT = load_font(20)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped_text(draw, text, xy, font, fill, max_width, line_gap=8):
    x, y = xy
    lines = wrap_text(draw, text, font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        box = draw.textbbox((x, y), line, font=font)
        y = box[3] + line_gap
    return y


def quadrant_image(title: str, output: Path, quadrants: list[tuple[str, str, str]]):
    image = Image.new("RGB", (1600, 1100), "white")
    draw = ImageDraw.Draw(image)

    draw.text((80, 40), title, font=TITLE_FONT, fill="#17324d")
    draw.text((80, 100), "Illustrative classification of the example used in the lecture note", font=SMALL_FONT, fill="#506070")

    left = 120
    top = 200
    box_w = 620
    box_h = 320
    gap = 40
    colors = ["#f8d7da", "#d1ecf1", "#fff3cd", "#d4edda"]
    headings = [(left, top), (left + box_w + gap, top), (left, top + box_h + gap), (left + box_w + gap, top + box_h + gap)]

    draw.line((left + box_w + gap / 2, top - 40, left + box_w + gap / 2, top + 2 * box_h + gap + 20), fill="#7a8a99", width=3)
    draw.line((left - 30, top + box_h + gap / 2, left + 2 * box_w + gap + 30, top + box_h + gap / 2), fill="#7a8a99", width=3)
    draw.text((50, top + box_h - 10), "More urgent", font=SMALL_FONT, fill="#445566")
    draw.text((50, top + box_h + 70), "Less urgent", font=SMALL_FONT, fill="#445566")
    draw.text((left + 150, top - 90), "More important", font=SMALL_FONT, fill="#445566")
    draw.text((left + box_w + gap + 160, top - 90), "Less important", font=SMALL_FONT, fill="#445566")

    for index, (heading, body, note) in enumerate(quadrants):
        x, y = headings[index]
        draw.rounded_rectangle((x, y, x + box_w, y + box_h), radius=24, fill=colors[index], outline="#8393a1", width=3)
        draw.text((x + 24, y + 18), heading, font=SUBTITLE_FONT, fill="#17324d")
        next_y = draw_wrapped_text(draw, body, (x + 24, y + 70), TEXT_FONT, "#1f1f1f", box_w - 48)
        draw_wrapped_text(draw, note, (x + 24, next_y + 12), SMALL_FONT, "#4d5b68", box_w - 48)

    image.save(output)


def swot_image(output: Path):
    image = Image.new("RGB", (1600, 1100), "white")
    draw = ImageDraw.Draw(image)
    draw.text((80, 40), "SWOT Application: Student Snack Business", font=TITLE_FONT, fill="#17324d")
    draw.text((80, 100), "A simple visual summary of the classroom example", font=SMALL_FONT, fill="#506070")

    left = 120
    top = 200
    box_w = 620
    box_h = 320
    gap = 40
    colors = ["#d4edda", "#f8d7da", "#d1ecf1", "#fff3cd"]
    labels = [
        ("Strengths", "Strong social media promotion\nFriends can become first customers", "Internal advantages that help launch the business"),
        ("Weaknesses", "Limited capital\nLittle inventory management experience", "Internal limits that need to be controlled"),
        ("Opportunities", "High evening snack demand on campus\nEasy ordering through campus groups", "External conditions that can be used for growth"),
        ("Threats", "Existing sellers already have loyal buyers\nIngredient prices may increase", "External risks that can reduce performance"),
    ]
    positions = [(left, top), (left + box_w + gap, top), (left, top + box_h + gap), (left + box_w + gap, top + box_h + gap)]

    for (title, body, note), (x, y), color in zip(labels, positions, colors):
        draw.rounded_rectangle((x, y, x + box_w, y + box_h), radius=24, fill=color, outline="#8393a1", width=3)
        draw.text((x + 24, y + 18), title, font=SUBTITLE_FONT, fill="#17324d")
        next_y = draw_wrapped_text(draw, body, (x + 24, y + 78), TEXT_FONT, "#1f1f1f", box_w - 48)
        draw_wrapped_text(draw, note, (x + 24, next_y + 12), SMALL_FONT, "#4d5b68", box_w - 48)

    image.save(output)


def bcg_image(output: Path):
    image = Image.new("RGB", (1600, 1100), "white")
    draw = ImageDraw.Draw(image)
    draw.text((80, 40), "BCG Application: School Cooperative Products", font=TITLE_FONT, fill="#17324d")
    draw.text((80, 100), "Illustrative positioning of the four products used in the example", font=SMALL_FONT, fill="#506070")

    origin_x = 220
    origin_y = 880
    width = 1120
    height = 620
    draw.line((origin_x, origin_y, origin_x + width, origin_y), fill="#445566", width=4)
    draw.line((origin_x, origin_y, origin_x, origin_y - height), fill="#445566", width=4)
    draw.text((origin_x + width - 120, origin_y + 20), "Relative market share", font=SMALL_FONT, fill="#445566")
    draw.text((60, origin_y - height - 20), "Market growth", font=SMALL_FONT, fill="#445566")

    mid_x = origin_x + width / 2
    mid_y = origin_y - height / 2
    draw.line((mid_x, origin_y, mid_x, origin_y - height), fill="#93a1ad", width=2)
    draw.line((origin_x, mid_y, origin_x + width, mid_y), fill="#93a1ad", width=2)

    draw.text((origin_x + 120, origin_y - height - 60), "High growth", font=SMALL_FONT, fill="#445566")
    draw.text((origin_x + 120, origin_y + 20), "Low growth", font=SMALL_FONT, fill="#445566")
    draw.text((origin_x - 40, origin_y - 40), "Low share", font=SMALL_FONT, fill="#445566")
    draw.text((origin_x + width - 160, origin_y - 40), "High share", font=SMALL_FONT, fill="#445566")

    draw.text((origin_x + 150, origin_y - height + 20), "Question Marks", font=SUBTITLE_FONT, fill="#17324d")
    draw.text((mid_x + 120, origin_y - height + 20), "Stars", font=SUBTITLE_FONT, fill="#17324d")
    draw.text((origin_x + 180, mid_y + 20), "Dogs", font=SUBTITLE_FONT, fill="#17324d")
    draw.text((mid_x + 90, mid_y + 20), "Cash Cows", font=SUBTITLE_FONT, fill="#17324d")

    products = [
        ("School hoodies", origin_x + 240, origin_y - 470, "#f39c12"),
        ("Reusable tumblers", origin_x + 860, origin_y - 500, "#2ecc71"),
        ("Printed phone charms", origin_x + 300, origin_y - 180, "#e74c3c"),
        ("Bottled water", origin_x + 870, origin_y - 160, "#3498db"),
    ]
    for label, x, y, color in products:
        draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill=color, outline="#17324d", width=3)
        draw_wrapped_text(draw, label, (x + 40, y - 14), SMALL_FONT, "#1f1f1f", 220, line_gap=4)

    image.save(output)


def main():
    quadrant_image(
        "Eisenhower Application: Student Weekly Tasks",
        OUT_DIR / "eisenhower-student-application.png",
        [
            ("Important + Urgent", "Submit assignment due tonight", "Complete immediately to avoid penalty."),
            ("Urgent + Not Important", "Reply to classroom message", "Handle quickly so it does not interrupt important work."),
            ("Important + Not Urgent", "Prepare for next week's midterm\nMeet the project group", "Schedule these tasks early because they support long-term performance."),
            ("Not Urgent + Not Important", "Watch random videos online", "Reduce or postpone this activity during study time."),
        ],
    )
    swot_image(OUT_DIR / "swot-student-business-application.png")
    bcg_image(OUT_DIR / "bcg-school-coop-application.png")
    print(OUT_DIR)


if __name__ == "__main__":
    main()