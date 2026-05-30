"""
Генератор OG-картинок (1200x630) для страниц-гайдов под отдельные игры.

Запуск из корня сайта:
    python tools/generate_og.py

Создаёт PNG в assets/og/.
Чтобы добавить новую игру — расширь GAMES снизу.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "og"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Фирменная палитра — берётся из styles.css проекта
BG_TOP    = (10, 22, 40)       # --bg
BG_BOTTOM = (5, 12, 24)        # темнее, для градиента
ACCENT    = (255, 107, 26)     # --accent (оранжевый)
TEXT      = (240, 246, 252)    # --text
MUTED     = (140, 156, 172)    # --text-muted

FONT_DISPLAY = "C:/Windows/Fonts/impact.ttf"  # для крупных заголовков
FONT_BOLD    = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG     = "C:/Windows/Fonts/arial.ttf"


def _make_gradient_bg() -> Image.Image:
    img = Image.new("RGB", (W, H), BG_TOP)
    pixels = img.load()
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        for x in range(W):
            pixels[x, y] = (r, g, b)
    return img


def _draw_crosshair(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    """Декоративный прицел — как в hero на главной."""
    line = (255, 107, 26, 60)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ACCENT, width=2)
    draw.ellipse((cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6), outline=ACCENT, width=1)
    draw.line((cx, cy - r - 20, cx, cy - r + 10), fill=ACCENT, width=2)
    draw.line((cx, cy + r - 10, cx, cy + r + 20), fill=ACCENT, width=2)
    draw.line((cx - r - 20, cy, cx - r + 10, cy), fill=ACCENT, width=2)
    draw.line((cx + r - 10, cy, cx + r + 20, cy), fill=ACCENT, width=2)


def make_og(game_slug: str, tag: str, title: str, accent: str, out_name: str) -> None:
    img = _make_gradient_bg()
    draw = ImageDraw.Draw(img, "RGBA")

    # Прицел в правой части — декор
    _draw_crosshair(draw, cx=950, cy=315, r=180)

    # ---- Шапка: AIMWOLF + полоска ----
    f_brand = ImageFont.truetype(FONT_BOLD, 32)
    draw.rectangle((60, 70, 110, 76), fill=ACCENT)
    draw.text((130, 56), "AIMWOLF", font=f_brand, fill=TEXT)

    # ---- Тег секции (как // BRAWL STARS на сайте) ----
    f_tag = ImageFont.truetype(FONT_BOLD, 26)
    draw.text((60, 175), tag.upper(), font=f_tag, fill=ACCENT)

    # ---- Главный заголовок ----
    f_title = ImageFont.truetype(FONT_DISPLAY, 120)
    draw.text((60, 215), title, font=f_title, fill=TEXT)

    # ---- Акцентный подзаголовок ----
    f_accent = ImageFont.truetype(FONT_DISPLAY, 76)
    draw.text((60, 355), accent, font=f_accent, fill=ACCENT)

    # ---- Низ: aimwolf.fun + слоган ----
    f_foot_main = ImageFont.truetype(FONT_BOLD, 28)
    f_foot_sub = ImageFont.truetype(FONT_REG, 22)
    draw.text((60, 540), "aimwolf.fun", font=f_foot_main, fill=TEXT)
    draw.text((60, 580), "VPN для геймеров · 2 дня бесплатно", font=f_foot_sub, fill=MUTED)

    # Полоска оранжевая снизу — фирменный акцент
    draw.rectangle((0, H - 6, W, H), fill=ACCENT)

    out_path = OUT_DIR / out_name
    img.save(out_path, "JPEG", quality=88, optimize=True)
    print(f"  [ok] {out_path.relative_to(ROOT)}")


GAMES = [
    {
        "slug": "brawl-stars",
        "tag": "// BRAWL STARS",
        "title": "не открывается?",
        "accent": "ЧИНИМ ЗА 2 МИНУТЫ",
        "out": "brawl-stars.jpg",
    },
    {
        "slug": "discord",
        "tag": "// DISCORD",
        "title": "глючит голос?",
        "accent": "ЧИНИМ ЗА 2 МИНУТЫ",
        "out": "discord.jpg",
    },
]


if __name__ == "__main__":
    print(f"Generating OG images -> {OUT_DIR.relative_to(ROOT)}/")
    for g in GAMES:
        make_og(g["slug"], g["tag"], g["title"], g["accent"], g["out"])
    print("Done.")
