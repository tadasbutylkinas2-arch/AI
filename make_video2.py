from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageSequenceClip, AudioArrayClip

W, H = 1280, 720
FPS = 24
SAMPLE_RATE = 44100

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG1   = (10,  10,  46)
BG2   = (13,  32,  96)
BLUE  = (0,   198, 255)
GREEN = (0,   230, 118)
WHITE = (255, 255, 255)
GREY  = (180, 180, 200)
TEAL  = (128, 203, 196)
CARD  = (22,  22,  72)


def gradient_bg(draw):
    for y in range(H):
        r = int(BG1[0] + (BG2[0]-BG1[0]) * y/H)
        g = int(BG1[1] + (BG2[1]-BG1[1]) * y/H)
        b = int(BG1[2] + (BG2[2]-BG1[2]) * y/H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))


def fnt(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def centered_text(draw, text, y, size, color=WHITE, bold=True):
    font = fnt(size, bold)
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (W - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=color)


def accent_line(draw, y):
    draw.rectangle([80, y, W-80, y+4], fill=BLUE)


def card_rect(draw, x1=80, y1=175, x2=None, y2=None):
    draw.rounded_rectangle(
        [x1, y1, x2 or W-80, y2 or H-80],
        radius=16, fill=CARD, outline=BLUE, width=2
    )


def new_frame():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient_bg(d)
    return img, d


# ─────────────────────────────────────────────────────────────────────────────
# Typing animation builder
# ─────────────────────────────────────────────────────────────────────────────

def typing_slide(title, subtitle=None, bullets=None, duration=8, lh=52):
    bullets = bullets or []
    total_frames = int(duration * FPS)
    CHARS_PER_SEC = 28
    cpf = CHARS_PER_SEC / FPS

    def draw_base(typed_done, active_text="", cursor_on=False):
        img, d = new_frame()
        accent_line(d, 60)
        if subtitle:
            centered_text(d, title,    78, 36, color=BLUE)
            centered_text(d, subtitle, 124, 36, color=BLUE)
            accent_line(d, 170)
            card_rect(d, 80, 190)
        else:
            centered_text(d, title, 85, 44, color=BLUE)
            accent_line(d, 148)
            card_rect(d, 80, 175)
        f_r = fnt(31, False)
        f_b = fnt(31, True)
        y = 205 if subtitle else 195
        for i, b in enumerate(bullets):
            if i < len(typed_done):
                d.text((122, y), "▶", font=f_b, fill=GREEN)
                d.text((162, y), b,  font=f_r, fill=WHITE)
            elif i == len(typed_done) and active_text is not None:
                d.text((122, y), "▶", font=f_b, fill=GREEN)
                d.text((162, y), active_text, font=f_r, fill=WHITE)
                if cursor_on:
                    bx = d.textbbox((0, 0), active_text, font=f_r)
                    cx = 162 + bx[2] - bx[0] + 2
                    d.text((cx, y), "|", font=f_r, fill=BLUE)
            y += lh
        return np.array(img)

    frames = [draw_base([])] * 10
    done = []
    for bullet in bullets:
        n = len(bullet)
        for fi in range(int(n / cpf) + 1):
            shown = bullet[:min(n, int(fi * cpf) + 1)]
            frames.append(draw_base(done, shown, (fi % 14) < 10))
        done.append(bullet)
        frames.extend([draw_base(done)] * 7)

    final = draw_base(done)
    while len(frames) < total_frames:
        frames.append(final)
    return frames[:total_frames]


# ─────────────────────────────────────────────────────────────────────────────
# Slides
# ─────────────────────────────────────────────────────────────────────────────

def slide_title(duration=7):
    img, d = new_frame()
    centered_text(d, "Papildoma programinė įranga",          195, 46, color=BLUE)
    centered_text(d, "kompiuterio įtaisams ir išoriniams",   250, 46, color=BLUE)
    centered_text(d, "įrenginiams valdyti",                  305, 46, color=BLUE)
    accent_line(d, 366)
    centered_text(d, "Tadas Butylkinas ir Naglis Gudžiūnas", 392, 28, color=GREY, bold=False)
    arr = np.array(img)
    return [arr] * int(duration * FPS)


def slide_intro(duration=8):
    total = int(duration * FPS)
    CHARS_PER_SEC = 30
    cpf = CHARS_PER_SEC / FPS
    lines = [
        "Kad OS galėtų bendrauti su",
        "aparatine įranga – reikalinga",
        "papildoma programinė įranga.",
        "",
        "Be jos įrenginiai neveiks tinkamai",
        "arba visai nebus atpažinti.",
    ]

    def draw(typed_lines, active="", cursor_on=False):
        img, d = new_frame()
        accent_line(d, 60)
        centered_text(d, "Kas yra papildoma programinė įranga?", 85, 37, color=BLUE)
        accent_line(d, 140)
        card_rect(d)
        f = fnt(33, False)
        y = 178
        for ln in typed_lines:
            if ln:
                centered_text(d, ln, y, 33, color=WHITE, bold=False)
            y += 52
        if active is not None:
            centered_text(d, active, y, 33, color=WHITE, bold=False)
            if cursor_on and active:
                bx = d.textbbox((0, 0), active, font=f)
                cx = (W + bx[2] - bx[0]) // 2 + 3
                d.text((cx, y), "|", font=f, fill=BLUE)
        return np.array(img)

    frames = [draw([])] * 8
    done = []
    for line in lines:
        if not line:
            done.append(line)
            frames.extend([draw(done)] * 4)
            continue
        n = len(line)
        for fi in range(int(n / cpf) + 1):
            shown = line[:min(n, int(fi * cpf) + 1)]
            frames.append(draw(done, shown, (fi % 14) < 10))
        done.append(line)
        frames.extend([draw(done)] * 5)
    final = draw(done)
    while len(frames) < total:
        frames.append(final)
    return frames[:total]


def slide_drivers(duration=8):
    return typing_slide(
        "Tvarkyklės (Drivers)",
        bullets=[
            "Sujungia operacinę sistemą su įrenginiu",
            "Reikalingos spausdintuvams, vaizdo,",
            "garso plokštėms, pelėms ir kt.",
            "Atnaujinamos per Windows Update",
            "Be tvarkyklės – įrenginys neatpažįstamas",
        ],
        duration=duration,
        lh=52,
    )


def slide_firmware(duration=8):
    return typing_slide(
        "Firmware (Mikroprograminė įranga)",
        bullets=[
            "Įrašyta tiesiai į įrenginį gamykloje",
            "Valdo žemiausiąjį įrenginio veikimo lygį",
            "Pvz.: SSD firmware, klaviatūros firmware",
            "Atnaujinama gamintojo specialia programa",
            "Klaidos gali sugadinti įrenginį",
        ],
        duration=duration,
        lh=52,
    )


def slide_management(duration=8):
    return typing_slide(
        "Valdymo programinė įranga",
        bullets=[
            "Specialios programos įrenginių konfigūracijai",
            "Spausdintuvo programa – kasečių lygis, kokybė",
            "Pelės programa – DPI, mygtukų programavimas",
            "Klaviatūros programa – apšvietimas, makros",
            "Monitoriaus programa – spalvų kalibracija",
        ],
        duration=duration,
        lh=52,
    )


def slide_diagnostics(duration=8):
    return typing_slide(
        "Diagnostikos įrankiai",
        bullets=[
            "Tikrina įrenginio veikimo būklę",
            "CrystalDiskInfo – kietojo disko sveikata",
            "GPU-Z – vaizdo plokštės temperatūra",
            "HWiNFO – visų komponentų stebėjimas",
            "Rodo klaidas prieš sugedus įrenginiui",
        ],
        duration=duration,
        lh=52,
    )


def slide_compare(duration=10):
    rows = [
        ("Programinė įranga",   "Paskirtis",              "Pavyzdys"),
        ("Tvarkyklė",           "OS ↔ įrenginys ryšys",   "Spausdintuvo driver"),
        ("Firmware",            "Žemo lygio valdymas",     "SSD firmware"),
        ("Valdymo programa",    "Nustatymų keitimas",      "Logitech G Hub"),
        ("Diagnostikos įrankis","Būklės stebėjimas",       "CrystalDiskInfo"),
    ]
    col_x = [85, 400, 680]
    col_w = [305, 270, 480]
    ROW_H = 74
    total = int(duration * FPS)

    def draw(n_rows):
        img, d = new_frame()
        accent_line(d, 60)
        centered_text(d, "Palyginimas", 85, 46, color=BLUE)
        accent_line(d, 148)
        y = 168
        for ri in range(min(n_rows, len(rows))):
            row = rows[ri]
            if ri == 0:
                d.rectangle([80, y, W-80, y+ROW_H], fill=(0, 60, 110))
                tc, bold = BLUE, True
            else:
                bg = (30, 30, 80) if ri % 2 == 0 else (20, 20, 60)
                d.rectangle([80, y, W-80, y+ROW_H], fill=bg)
                tc, bold = WHITE, False
            f = fnt(27, bold)
            for ci, cell in enumerate(row):
                bx = d.textbbox((0, 0), cell, font=f)
                tx = col_x[ci] + (col_w[ci] - (bx[2]-bx[0])) // 2
                ty = y + (ROW_H - (bx[3]-bx[1])) // 2
                d.text((tx, ty), cell, font=f, fill=tc)
            y += ROW_H + 2
        return np.array(img)

    frames = [draw(1)] * 14
    for r in range(2, len(rows) + 1):
        frames.extend([draw(r)] * 22)
    final = draw(len(rows))
    while len(frames) < total:
        frames.append(final)
    return frames[:total]


def slide_conclusions(duration=7):
    return typing_slide(
        "Išvados",
        bullets=[
            "Papildoma programinė įranga – būtina šiuolaikiniame kompiuteryje",
            "Tvarkyklės leidžia OS kalbėtis su įrenginiais",
            "Firmware valdo įrenginio veikimą žemiausiame lygyje",
            "Valdymo ir diagnostikos programos – patogiau ir saugiau",
        ],
        duration=duration,
        lh=54,
    )


def slide_end(duration=4):
    img, d = new_frame()
    centered_text(d, "Ačiū už dėmesį!", 265, 58, color=BLUE)
    accent_line(d, 342)
    centered_text(d, "Tadas Butylkinas ir Naglis Gudžiūnas", 365, 30, color=TEAL, bold=False)
    arr = np.array(img)
    return [arr] * int(duration * FPS)


# ─────────────────────────────────────────────────────────────────────────────
# Assemble frames
# ─────────────────────────────────────────────────────────────────────────────

builders = [
    slide_title,
    slide_intro,
    slide_drivers,
    slide_firmware,
    slide_management,
    slide_diagnostics,
    slide_compare,
    slide_conclusions,
    slide_end,
]

print("Rendering slides...")
all_frames = []
for i, builder in enumerate(builders):
    frames = builder()
    all_frames.extend(frames)
    print(f"  Slide {i+1}/{len(builders)}  ({len(frames)} frames)")

total_duration = len(all_frames) / FPS
print(f"Total frames: {len(all_frames)}  (~{total_duration:.1f}s)")

# ─────────────────────────────────────────────────────────────────────────────
# Generate ambient piano music
# ─────────────────────────────────────────────────────────────────────────────

print("Generating music...")


def piano_note(freq, dur, sr=SAMPLE_RATE, vol=0.18):
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    wave = (np.sin(2*np.pi*freq*t)
            + 0.50 * np.sin(2*np.pi*2*freq*t)
            + 0.25 * np.sin(2*np.pi*3*freq*t)
            + 0.12 * np.sin(2*np.pi*4*freq*t))
    attack  = int(0.01 * sr)
    decay   = int(0.05 * sr)
    release = int(0.25 * dur * sr)
    sustain = 0.6
    env = np.ones(len(t))
    env[:attack] = np.linspace(0, 1, attack)
    env[attack:attack+decay] = np.linspace(1, sustain, decay)
    env[-release:] = np.linspace(sustain, 0, release)
    return wave * env * vol


def note_freq(name):
    notes = {
        "C3":130.81,"D3":146.83,"E3":164.81,"F3":174.61,"G3":196.00,
        "A3":220.00,"B3":246.94,"C4":261.63,"D4":293.66,"E4":329.63,
        "F4":349.23,"G4":392.00,"A4":440.00,"B4":493.88,"C5":523.25,
        "D5":587.33,"E5":659.25,"F5":698.46,"G5":783.99,"A5":880.00,
    }
    return notes[name]


chord_prog = [
    ["A3","C4","E4"],
    ["F3","A3","C4"],
    ["C3","E3","G3"],
    ["G3","B3","D4"],
]
melody_notes = [
    ("E5",0.5),("D5",0.5),("C5",0.5),("E5",0.5),
    ("A5",0.5),("G5",0.5),("F5",0.5),("E5",0.5),
    ("D5",0.5),("C5",0.5),("D5",0.5),("E5",0.5),
    ("C5",0.5),("C5",0.5),("B4",0.5),("C5",0.5),
]

total_samples = int(SAMPLE_RATE * total_duration)
audio = np.zeros(total_samples)

t, ci = 0.0, 0
while t < total_duration:
    chord = chord_prog[ci % len(chord_prog)]
    for note in chord:
        dur = min(2.0, total_duration - t)
        if dur > 0.1:
            seg = piano_note(note_freq(note), dur, vol=0.10)
            start = int(t * SAMPLE_RATE)
            audio[start:start+len(seg)] += seg
    ci += 1
    t += 2.0

t, mi = 0.0, 0
while t < total_duration:
    name, dur = melody_notes[mi % len(melody_notes)]
    actual = min(dur, total_duration - t)
    if actual > 0.05:
        seg = piano_note(note_freq(name), actual, vol=0.13)
        start = int(t * SAMPLE_RATE)
        audio[start:start+len(seg)] += seg
    mi += 1
    t += dur

fade = int(1.5 * SAMPLE_RATE)
audio[:fade]  *= np.linspace(0, 1, fade)
audio[-fade:] *= np.linspace(1, 0, fade)
audio = audio / (np.max(np.abs(audio)) + 1e-9) * 0.85

stereo = np.stack([audio, audio], axis=1).astype(np.float32)
audio_clip = AudioArrayClip(stereo, fps=SAMPLE_RATE)

# ─────────────────────────────────────────────────────────────────────────────
# Render
# ─────────────────────────────────────────────────────────────────────────────

print("Writing MP4...")
clip = ImageSequenceClip(all_frames, fps=FPS)
clip = clip.with_audio(audio_clip)
clip.write_videofile(
    "/home/user/AI/papildoma_programine_iranga.mp4",
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    logger=None,
)
print("Done!")
