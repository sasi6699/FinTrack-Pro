from PIL import Image, ImageDraw, ImageFont


OUTPUT = "design/FinTrack_Pro_Use_Case_Diagram.png"
WIDTH, HEIGHT = 3600, 2400

BACKGROUND = "#FFFFFF"
INK = "#111827"
MUTED = "#475569"
BOUNDARY = "#334155"
AUTH = "#DCEBFF"
DASHBOARD = "#E7F0FF"
TRANSACTIONS = "#F2E8FF"
BUDGET = "#E1F6EC"
ANALYTICS = "#FFF1D8"
REPORTS = "#E0F7F7"
SETTINGS = "#FCE7F3"


def font(size, bold=False):
    name = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
    return ImageFont.truetype(name, size)


image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(image)

title_font = font(58, True)
subtitle_font = font(31)
boundary_font = font(36, True)
use_case_font = font(29, True)
relationship_font = font(24, True)
note_font = font(23)


def centered_text(box, text, text_font, fill=INK):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=text_font)
    x = (left + right - (bbox[2] - bbox[0])) / 2
    y = (top + bottom - (bbox[3] - bbox[1])) / 2 - 2
    draw.text((x, y), text, font=text_font, fill=fill)


def ellipse(name, center, size, fill):
    cx, cy = center
    width, height = size
    box = (cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2)
    draw.ellipse(box, fill=fill, outline=INK, width=4)
    centered_text(box, name, use_case_font)
    return box


def actor(x, y):
    draw.ellipse((x - 31, y - 170, x + 31, y - 108), outline=INK, width=5)
    draw.line((x, y - 108, x, y + 26), fill=INK, width=5)
    draw.line((x - 76, y - 60, x + 76, y - 60), fill=INK, width=5)
    draw.line((x, y + 26, x - 70, y + 122), fill=INK, width=5)
    draw.line((x, y + 26, x + 70, y + 122), fill=INK, width=5)
    centered_text((x - 70, y + 145, x + 70, y + 190), "User", font(30, True))


def dashed_line(start, end, dash=18, gap=12, width=3):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    distance = (dx * dx + dy * dy) ** .5
    if not distance:
        return
    ux, uy = dx / distance, dy / distance
    cursor = 0
    while cursor < distance:
        stop = min(cursor + dash, distance)
        draw.line((x1 + ux * cursor, y1 + uy * cursor, x1 + ux * stop, y1 + uy * stop), fill=INK, width=width)
        cursor += dash + gap


def arrowhead(tip, direction, size=15):
    dx, dy = direction
    length = (dx * dx + dy * dy) ** .5
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base_x = tip[0] - ux * size
    base_y = tip[1] - uy * size
    draw.polygon(
        [tip, (base_x + px * size * .6, base_y + py * size * .6), (base_x - px * size * .6, base_y - py * size * .6)],
        fill=INK,
    )


def include_or_extend(start, end, stereotype, label_pos):
    dashed_line(start, end)
    arrowhead(end, (end[0] - start[0], end[1] - start[1]))
    x, y = label_pos
    label_box = draw.textbbox((0, 0), stereotype, font=relationship_font)
    draw.rounded_rectangle((x - 8, y - 5, x + label_box[2] + 8, y + label_box[3] + 5), radius=5, fill=BACKGROUND)
    draw.text((x, y), stereotype, font=relationship_font, fill=INK)


# Header
centered_text((0, 45, WIDTH, 125), "UML Use Case Diagram", title_font)
centered_text((0, 130, WIDTH, 182), "FinTrack Pro – Smart Personal Finance Dashboard", subtitle_font, MUTED)

# System boundary and actor
boundary_box = (430, 240, 3430, 2200)
draw.rounded_rectangle(boundary_box, radius=18, outline=BOUNDARY, width=5)
draw.rectangle((470, 216, 1660, 272), fill=BACKGROUND)
draw.text((500, 220), "FinTrack Pro – Smart Personal Finance Dashboard", font=boundary_font, fill=INK)
actor(190, 1120)

# Use cases
register = ellipse("Register", (760, 470), (420, 122), AUTH)
login = ellipse("Login", (760, 670), (420, 122), AUTH)
logout = ellipse("Logout", (760, 870), (420, 122), AUTH)
notifications = ellipse("Configure Notifications", (760, 1070), (510, 122), SETTINGS)

dashboard = ellipse("View Dashboard", (1410, 470), (480, 122), DASHBOARD)
budget = ellipse("Manage Budget", (1410, 850), (480, 122), BUDGET)
budget_progress = ellipse("View Budget Progress", (1410, 1055), (590, 122), BUDGET)
analytics = ellipse("View Analytics", (1410, 1430), (480, 122), ANALYTICS)
filters = ellipse("Filter Analytics", (1410, 1635), (480, 122), ANALYTICS)

transactions = ellipse("Manage Transactions", (2140, 470), (560, 122), TRANSACTIONS)
add = ellipse("Add Transaction", (2140, 700), (500, 122), TRANSACTIONS)
edit = ellipse("Edit Transaction", (2140, 900), (500, 122), TRANSACTIONS)
delete = ellipse("Delete Transaction", (2140, 1100), (500, 122), TRANSACTIONS)
search = ellipse("Search Transactions", (2140, 1300), (560, 122), TRANSACTIONS)

reports = ellipse("Generate Reports", (2870, 760), (520, 122), REPORTS)
export = ellipse("Export Reports\n(CSV, Excel, PDF)", (2870, 1035), (580, 155), REPORTS)

# Actor associations to the major user goals
actor_x, actor_y = 266, 1060
major_centers = [(550, 470), (550, 670), (550, 870), (550, 1070), (1170, 470), (1860, 470), (1170, 850), (1170, 1430), (2610, 760)]
for end in major_centers:
    draw.line((actor_x, actor_y, end[0], end[1]), fill=INK, width=3)

# UML relationships: only mandatory or optional behavior shown.
include_or_extend((1410, 911), (1410, 994), "<<include>>", (1470, 934))
include_or_extend((2140, 639), (2140, 531), "<<extend>>", (2245, 580))
include_or_extend((2140, 839), (2140, 531), "<<extend>>", (2245, 710))
include_or_extend((2140, 1039), (2140, 531), "<<extend>>", (2245, 910))
include_or_extend((2140, 1239), (2140, 531), "<<extend>>", (2245, 1110))
include_or_extend((1410, 1574), (1410, 1491), "<<extend>>", (1470, 1514))
include_or_extend((2870, 957), (2870, 821), "<<extend>>", (2970, 876))

# Footer note
draw.line((500, 2245, 3380, 2245), fill="#CBD5E1", width=2)
centered_text((500, 2260, 3380, 2310), "Scope: implemented Streamlit user-facing functionality only", note_font, MUTED)

image.save(OUTPUT, "PNG", dpi=(300, 300))
