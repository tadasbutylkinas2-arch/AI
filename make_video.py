from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageClip, concatenate_videoclips

W, H = 1280, 720
FPS = 24
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Colour palette
BG1   = (10,  10,  46)
BG2   = (13,  32,  96)
BLUE  = (0,   198, 255)
GREEN = (0,   230, 118)
WHITE = (255, 255, 255)
GREY  = (180, 180, 200)
TEAL  = (128, 203, 196)
DARK  = (30,  30,  80)

def gradient_bg(draw, w=W, h=H):
    for y in range(h):
        r = int(BG1[0] + (BG2[0]-BG1[0]) * y/h)
        g = int(BG1[1] + (BG2[1]-BG1[1]) * y/h)
        b = int(BG1[2] + (BG2[2]-BG1[2]) * y/h)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def fnt(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def centered_text(draw, text, y, size, color=WHITE, bold=True):
    font = fnt(size, bold)
    bbox = draw.textbbox((0,0), text, font=font)
    x = (W - (bbox[2]-bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]

def accent_line(draw, y):
    draw.rectangle([80, y, W-80, y+4], fill=BLUE)

def bullet_lines(draw, items, start_y, size=30, color=WHITE, bullet_color=GREEN):
    font_b = fnt(size, bold=True)
    font_r = fnt(size, bold=False)
    y = start_y
    for item in items:
        # bullet
        draw.text((120, y), "▶", font=font_b, fill=bullet_color)
        draw.text((160, y), item, font=font_r, fill=color)
        y += size + 18
    return y

def card_bg(draw, x1, y1, x2, y2):
    draw.rounded_rectangle([x1,y1,x2,y2], radius=16,
                            fill=(255,255,255,20), outline=BLUE, width=2)

# ── Slide builders ─────────────────────────────────────────────────────────

def slide_title():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient_bg(d)
    # decorative circles
    for cx,cy,r,op in [(900,150,200,25),(200,550,150,15),(1100,500,100,18)]:
        overlay = Image.new("RGBA",(W,H),(0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(*BLUE, op))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        d = ImageDraw.Draw(img)
    centered_text(d, "Isiorines atminties itaisai", 180, 58, color=BLUE)
    accent_line(d, 265)
    centered_text(d, "Isorines atminties itaisai", 180, 58, color=BLUE)
    # rewrite with proper text
    img2 = Image.new("RGB", (W, H))
    d2 = ImageDraw.Draw(img2)
    gradient_bg(d2)
    for cx,cy,r,op in [(900,150,200,25),(200,550,150,15),(1100,500,100,18)]:
        overlay = Image.new("RGBA",(W,H),(0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(*BLUE, op))
        img2 = Image.alpha_composite(img2.convert("RGBA"), overlay).convert("RGB")
        d2 = ImageDraw.Draw(img2)
    centered_text(d2, "Išorinės atminties įtaisai", 185, 56, color=BLUE)
    accent_line(d2, 258)
    centered_text(d2, "Technologinių problemų sprendimai", 278, 32, color=TEAL, bold=False)
    centered_text(d2, "Naglis Gudžiūnas ir Tadas Butelinis", 350, 30, color=GREY, bold=False)
    centered_text(d2, "Tema C", 560, 26, color=GREY, bold=False)
    return d2._image if hasattr(d2,'_image') else img2

def make_slide(title, bullets, icon=""):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient_bg(d)
    accent_line(d, 60)
    if icon:
        d.text((80, 80), icon, font=fnt(52), fill=WHITE)
        centered_text(d, title, 90, 48, color=BLUE)
    else:
        centered_text(d, title, 85, 48, color=BLUE)
    accent_line(d, 155)
    card_bg(d, 80, 175, W-80, H-80)
    bullet_lines(d, bullets, 205, size=32)
    return img

def slide_intro():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient_bg(d)
    accent_line(d, 60)
    centered_text(d, "Kas yra išorinės atminties įtaisas?", 85, 42, color=BLUE)
    accent_line(d, 148)
    card_bg(d, 100, 175, W-100, H-80)
    lines = [
        "Prietaisas duomenims saugoti",
        "už kompiuterio vidaus.",
        " ",
        "Leidžia perkelti, kurti atsargines",
        "kopijas ir saugoti didelius duomenis.",
    ]
    y = 200
    for line in lines:
        if line.strip():
            centered_text(d, line, y, 34, color=WHITE, bold=False)
        y += 52
    return img

def slide_usb():
    return make_slide(
        "USB atmintinė (Fleš atmintis)",
        [
            "Maža, lengva, atspari",
            "Jungiama per USB prievadą",
            "Talpa: 4 GB – 1 TB",
            "Failių perkėlimas, dokumentai,",
            "nuotraukos, video",
        ],
        icon=""
    )

def slide_hdd():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient_bg(d)
    accent_line(d, 60)
    centered_text(d, "Išorinis kietasis diskas", 85, 48, color=BLUE)
    accent_line(d, 148)
    # two cards
    card_bg(d, 60, 175, 610, H-80)
    card_bg(d, 660, 175, W-60, H-80)
    d.text((80,195), "HDD", font=fnt(36), fill=TEAL)
    d.text((680,195), "SSD", font=fnt(36), fill=GREEN)
    hdd = ["Judąčios dalys","Pigesnis","Lėtesnis","Iki 20 TB"]
    ssd = ["Be judąčių dalių","Greitesnis","Patvaresnis","Iki 8 TB"]
    bullet_lines(d, hdd, 248, size=29, color=WHITE)
    for i, item in enumerate(ssd):
        d.text((700, 248+i*47), f"▶ {item}", font=fnt(29,False), fill=WHITE)
    return img

def slide_sd():
    return make_slide(
        "SD kortelė",
        [
            "Fotoaparatai, telefonai, kameros",
            "Miniatiūrinė, tačiau didžiulė talpa",
            "Tipai: SD, miniSD, microSD",
            "Talpa: 2 GB – 1 TB",
        ],
        icon=""
    )

def slide_cd():
    return make_slide(
        "CD / DVD / Blu-ray diskai",
        [
            "Naudoja lazerio spindulį",
            "CD – iki 700 MB",
            "DVD – iki 8,5 GB",
            "Blu-ray – iki 25 GB",
            "⚠️  Šiuo metu retai naudojami",
        ],
        icon=""
    )

def slide_compare():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient_bg(d)
    accent_line(d, 60)
    centered_text(d, "Palyginimas", 85, 48, color=BLUE)
    accent_line(d, 148)
    rows = [
        ("Išorinės atminties įtaisas", "Talpa",  "Greitis",    "Patvarumas"),
        ("USB atmintinė",                     "iki 1 TB","Vidutinis",   "Geras"),
        ("Išorinis HDD",                      "iki 20 TB","Lėtokas","Vidutinis"),
        ("Išorinis SSD",                      "iki 8 TB", "Greitas",    "Puikus"),
        ("SD kortelė",                         "iki 1 TB", "Greitas",    "Geras"),
        ("CD/DVD",                                  "iki 8,5 GB","Lėtas","Trapus"),
    ]
    col_x = [80, 390, 620, 870]
    col_w = [300, 220, 240, 260]
    y = 175
    for ri, row in enumerate(rows):
        row_h = 72
        if ri == 0:
            d.rectangle([80, y, W-80, y+row_h], fill=(0,80,120))
            txt_color = BLUE
            f = fnt(26, bold=True)
        else:
            bg = (30,30,80) if ri%2==0 else (20,20,60)
            d.rectangle([80, y, W-80, y+row_h], fill=bg)
            txt_color = WHITE
            f = fnt(26, bold=False)
        for ci, cell in enumerate(row):
            bbox = d.textbbox((0,0), cell, font=f)
            tx = col_x[ci] + (col_w[ci]-(bbox[2]-bbox[0]))//2
            ty = y + (row_h-(bbox[3]-bbox[1]))//2
            d.text((tx, ty), cell, font=f, fill=txt_color)
        y += row_h + 2
    return img

def slide_conclusions():
    return make_slide(
        "Išvados",
        [
            "Išorinės atmintys būtinos kasdieniame gyvenime",
            "Kiekvienas įtaisas tinka skirtingoms reikmėms",
            "Pasirinkti pagal talpą, greitį ir kainą",
            "USB – patogiausia kasdieniam naudojimui",
        ],
        icon=""
    )

def slide_end():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient_bg(d)
    for cx,cy,r,op in [(640,360,300,20),(200,200,180,12),(1050,500,140,15)]:
        overlay = Image.new("RGBA",(W,H),(0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(*BLUE, op))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        d = ImageDraw.Draw(img)
    centered_text(d, "Ačiū už dėmesį!", 240, 60, color=BLUE)
    accent_line(d, 320)
    centered_text(d, "Naglis Gudžiūnas ir Tadas Butelinis", 345, 32, color=TEAL, bold=False)
    centered_text(d, "Tema C: Išorinės atminties įtaisai", 400, 26, color=GREY, bold=False)
    return img

# ── Build slides + durations ────────────────────────────────────────────────

slides_data = [
    (slide_title,        6),
    (slide_intro,        7),
    (slide_usb,          8),
    (slide_hdd,          8),
    (slide_sd,           7),
    (slide_cd,           7),
    (slide_compare,      9),
    (slide_conclusions,  7),
    (slide_end,          4),
]

print("Rendering slides...")
clips = []
for i, (builder, duration) in enumerate(slides_data):
    img = builder()
    arr = np.array(img)
    clip = ImageClip(arr, duration=duration)
    clips.append(clip)
    print(f"  Slide {i+1}/9 done")

print("Concatenating and writing MP4...")
video = concatenate_videoclips(clips, method="compose")
video.write_videofile(
    "/home/user/AI/isiorines_atminties_itaisai.mp4",
    fps=FPS,
    codec="libx264",
    audio=False,
    logger=None,
)
print("Done!")
