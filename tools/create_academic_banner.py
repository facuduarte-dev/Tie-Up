from pathlib import Path
import sys

sys.path.append("/usr/lib/python3/dist-packages")

import qrcode
from PIL import Image, ImageOps
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "banner-academico-tie-up-60x90.pdf"
TMP = ROOT / "tmp" / "pdfs"
LOGO = ROOT / "docs" / "tie-up" / "logo-tie-up-transparente.png"
SCREEN = ROOT / "docs" / "tie-up" / "evidencias" / "inicio-escritorio.png"
ITSP_LOGO = ROOT / "docs" / "tie-up" / "logo-itsp-mejorado.png"
URL = "https://itspvm.duckdns.org/proyectos/facu_fx/tieup/Tie-Up/html/"

# 60 x 90 cm in PDF points.
CM = 72 / 2.54
W, H = 60 * CM, 90 * CM

GREEN_DARK = HexColor("#174E49")
GREEN = HexColor("#306E68")
GREEN_MID = HexColor("#3F928A")
GREEN_LIGHT = HexColor("#50B4AA")
MINT = HexColor("#DDEDE7")
CREAM = HexColor("#F7F2E7")
INK = HexColor("#111B1A")
MUTED = HexColor("#53615F")

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", REG))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", BOLD))


def round_rect(c, x, y, w, h, r=20, fill=white, stroke=None, sw=1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
    else:
        c.setStrokeColor(fill)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)


def fit_image(c, path, x, y, w, h, contain=True):
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = min(w / iw, h / ih) if contain else max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(img, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh,
                preserveAspectRatio=True, mask="auto")


def wrap_lines(text, font, size, max_width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paragraph(c, text, x, top, w, size=24, leading=None, color=INK, font="DejaVu"):
    leading = leading or size * 1.3
    c.setFont(font, size)
    c.setFillColor(color)
    y = top
    for line in wrap_lines(text, font, size, w):
        c.drawString(x, y, line)
        y -= leading
    return y


def heading(c, text, x, y, size=32, color=GREEN_DARK):
    c.setFont("DejaVu-Bold", size)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())


def chip(c, label, x, y, w, color=GREEN):
    round_rect(c, x, y, w, 60, 30, fill=Color(1, 1, 1, alpha=0.92), stroke=MINT, sw=2)
    c.setFillColor(color)
    c.circle(x + 29, y + 30, 11, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("DejaVu-Bold", 23)
    c.drawString(x + 51, y + 20, label)


def architecture_icon(c, cx, cy, kind):
    c.setStrokeColor(GREEN_DARK)
    c.setFillColor(MINT)
    c.setLineWidth(5)
    if kind == "browser":
        c.roundRect(cx - 75, cy - 49, 150, 100, 10, fill=1, stroke=1)
        c.line(cx - 75, cy + 24, cx + 75, cy + 24)
        for dx in (-55, -36, -17):
            c.circle(cx + dx, cy + 38, 5, fill=1, stroke=0)
    elif kind == "server":
        for oy in (-46, -6, 34):
            c.roundRect(cx - 66, cy + oy - 16, 132, 33, 6, fill=1, stroke=1)
            c.circle(cx + 46, cy + oy, 5, fill=1, stroke=0)
    else:
        c.ellipse(cx - 68, cy + 24, cx + 68, cy + 61, fill=1, stroke=1)
        c.rect(cx - 68, cy - 41, 136, 84, fill=1, stroke=0)
        c.line(cx - 68, cy - 41, cx - 68, cy + 43)
        c.line(cx + 68, cy - 41, cx + 68, cy + 43)
        c.arc(cx - 68, cy - 60, cx + 68, cy - 22, 180, 180)
        c.arc(cx - 68, cy - 14, cx + 68, cy + 24, 180, 180)


def arrow(c, x1, x2, y):
    c.setStrokeColor(GREEN_MID)
    c.setFillColor(GREEN_MID)
    c.setLineWidth(7)
    c.line(x1, y, x2, y)
    p = c.beginPath()
    p.moveTo(x2, y)
    p.lineTo(x2 - 20, y + 14)
    p.lineTo(x2 - 20, y - 14)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    qr_path = TMP / "qr-tie-up.png"
    screen_crop = TMP / "inicio-escritorio-banner.jpg"
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=14, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    qr.make_image(fill_color="#111B1A", back_color="#FFFFFF").save(qr_path)
    with Image.open(SCREEN) as source:
        # Crop the real homepage to the wide viewport used by the browser mockup.
        ImageOps.fit(source.convert("RGB"), (1952, 976), method=Image.Resampling.LANCZOS,
                     centering=(0.5, 0.0)).save(screen_crop, quality=94)

    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("Banner académico Tie-Up - Muestra 2026")
    c.setAuthor("Facundo Duarte, Joaquín Castro, Bryan Chialvo y Benjamin Molineli")

    # Background and visual rhythm.
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN_DARK)
    c.rect(0, H - 520, W, 520, fill=1, stroke=0)
    c.setFillColor(GREEN_MID)
    c.circle(W + 50, H - 600, 360, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.circle(-110, 100, 340, fill=1, stroke=0)

    margin, gap = 56, 28
    content_w = W - 2 * margin

    # Hero.
    fit_image(c, LOGO, margin + 10, H - 340, 780, 260)
    c.setFillColor(white)
    c.setFont("DejaVu-Bold", 35)
    c.drawString(margin + 12, H - 385, "PLATAFORMA WEB PARA CONECTAR TALENTO DIGITAL")
    c.setFont("DejaVu", 22)
    c.drawString(margin + 12, H - 427, "WEB DESIGN 2026 · INSTITUTO TECNOLÓGICO SUPERIOR · MUESTRA ACADÉMICA")

    # Main content area: two columns.
    left_w = 1000
    right_x = margin + left_w + gap
    right_w = content_w - left_w - gap

    # Website preview card.
    card_top = H - 550
    preview_h = 630
    round_rect(c, margin, card_top - preview_h, left_w, preview_h, 26, fill=white)
    # Clean browser chrome with a wide, readable crop of the real homepage.
    c.setFillColor(MINT)
    c.roundRect(margin, card_top - 60, left_w, 60, 26, fill=1, stroke=0)
    c.rect(margin, card_top - 60, left_w, 30, fill=1, stroke=0)
    for i, col in enumerate((HexColor("#EF5B68"), HexColor("#E7C351"), HexColor("#5DC97A"))):
        c.setFillColor(col); c.circle(margin + 30 + i * 31, card_top - 30, 8, fill=1, stroke=0)
    round_rect(c, margin + 125, card_top - 48, left_w - 165, 34, 13, fill=white)
    c.setFont("DejaVu", 12); c.setFillColor(MUTED)
    c.drawString(margin + 145, card_top - 39, "itspvm.duckdns.org  /  Tie-Up")
    c.drawImage(str(screen_crop), margin + 12, card_top - preview_h + 12,
                left_w - 24, preview_h - 82, preserveAspectRatio=False, mask="auto")

    # Problem / solution cards.
    problem_h = 300
    round_rect(c, right_x, card_top - problem_h, right_w, problem_h, 26, fill=white, stroke=GREEN_MID, sw=6)
    heading(c, "Problemática", right_x + 28, card_top - 55, 32)
    paragraph(c, "Personas y pequeñas empresas buscan servicios digitales en redes sociales o por recomendaciones dispersas. Así resulta difícil comparar especialidades, experiencia y valoraciones en un mismo lugar.",
              right_x + 28, card_top - 105, right_w - 56, 21, 27, MUTED)

    sol_y = card_top - preview_h
    sol_h = 302
    round_rect(c, right_x, sol_y, right_w, sol_h, 26, fill=GREEN_DARK)
    heading(c, "Solución", right_x + 28, sol_y + sol_h - 55, 32, white)
    paragraph(c, "Tie-Up centraliza perfiles de profesionales digitales y facilita el contacto con potenciales clientes. Permite explorar categorías, conocer perfiles y acceder a una experiencia adaptable desde cualquier dispositivo.",
              right_x + 28, sol_y + sol_h - 105, right_w - 56, 21, 27, white)

    # Stack.
    stack_top = card_top - preview_h - 32
    stack_h = 430
    round_rect(c, margin, stack_top - stack_h, content_w, stack_h, 26, fill=white)
    heading(c, "Stack tecnológico", margin + 32, stack_top - 57, 34)
    c.setFont("DejaVu", 19); c.setFillColor(MUTED)
    c.drawRightString(W - margin - 32, stack_top - 53, "Tecnologías utilizadas en la versión presentada")
    labels = ["HTML5", "CSS3", "JavaScript", "PHP 8", "MySQL", "XAMPP / Apache", "Git + GitHub", "Diseño responsive"]
    chip_w = (content_w - 3 * 32 - 3 * 18) / 4
    for i, label in enumerate(labels):
        row, col = divmod(i, 4)
        chip(c, label, margin + 32 + col * (chip_w + 18), stack_top - 150 - row * 82, chip_w,
             (GREEN_LIGHT, GREEN_MID, HexColor("#E6AF2E"), GREEN_DARK)[col])
    c.setFont("DejaVu", 19); c.setFillColor(MUTED)
    c.drawString(margin + 34, stack_top - 337, "Frontend: estructura, estilos, interacción e idioma · Backend: registro, autenticación y sesiones · Datos: usuarios en MySQL")

    # Architecture and QR row.
    lower_top = stack_top - stack_h - 32
    arch_w = 1100
    qr_x = margin + arch_w + gap
    qr_w = content_w - arch_w - gap
    lower_h = 670
    round_rect(c, margin, lower_top - lower_h, arch_w, lower_h, 26, fill=white)
    heading(c, "Arquitectura", margin + 32, lower_top - 57, 34)
    base_y = lower_top - 250
    centers = [margin + 205, margin + 550, margin + 895]
    for cx, kind in zip(centers, ("browser", "server", "database")):
        architecture_icon(c, cx, base_y, kind)
    arrow(c, centers[0] + 102, centers[1] - 102, base_y)
    arrow(c, centers[1] + 102, centers[2] - 102, base_y)
    for cx, title, desc in zip(centers,
                               ("NAVEGADOR", "APACHE + PHP", "MYSQL"),
                               ("HTML · CSS · JavaScript", "Lógica · validación · sesión", "Usuarios y credenciales")):
        c.setFillColor(INK); c.setFont("DejaVu-Bold", 25); c.drawCentredString(cx, base_y - 116, title)
        c.setFillColor(MUTED); c.setFont("DejaVu", 18); c.drawCentredString(cx, base_y - 152, desc)
    c.setFillColor(MINT)
    c.roundRect(margin + 32, lower_top - lower_h + 28, arch_w - 64, 80, 16, fill=1, stroke=0)
    c.setFillColor(GREEN_DARK); c.setFont("DejaVu-Bold", 20)
    c.drawString(margin + 55, lower_top - lower_h + 73, "FLUJO PRINCIPAL:")
    c.setFont("DejaVu", 18); c.setFillColor(MUTED)
    c.drawString(margin + 285, lower_top - lower_h + 73, "Formulario → PHP valida → consulta preparada → MySQL → respuesta y sesión")

    # QR card.
    round_rect(c, qr_x, lower_top - lower_h, qr_w, lower_h, 26, fill=GREEN_DARK)
    c.setFillColor(white); c.setFont("DejaVu-Bold", 34)
    c.drawCentredString(qr_x + qr_w / 2, lower_top - 58, "PROBÁ TIE-UP")
    c.setFont("DejaVu", 19)
    c.drawCentredString(qr_x + qr_w / 2, lower_top - 91, "Escaneá el código para visitar el sitio")
    qr_size = 320
    round_rect(c, qr_x + (qr_w - qr_size - 28) / 2, lower_top - 505, qr_size + 28, qr_size + 28, 18, fill=white)
    c.drawImage(str(qr_path), qr_x + (qr_w - qr_size) / 2, lower_top - 491, qr_size, qr_size, mask="auto")
    c.setFont("DejaVu-Bold", 17); c.setFillColor(MINT)
    c.drawCentredString(qr_x + qr_w / 2, lower_top - 558, "itspvm.duckdns.org · Tie-Up")

    # Footer.
    footer_y = 0
    footer_h = lower_top - lower_h - 25
    c.setFillColor(GREEN_DARK)
    c.rect(0, footer_y, W, footer_h, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("DejaVu-Bold", 29)
    c.drawCentredString(W / 2, footer_h - 42, "TIE-UP · CONECTANDO TALENTO CON OPORTUNIDADES")
    c.setFont("DejaVu", 21)
    c.drawCentredString(W / 2, footer_h - 79, "Facundo Duarte · Joaquín Castro · Bryan Chialvo · Benjamin Molineli")
    c.setFont("DejaVu", 17); c.setFillColor(MINT)
    c.drawCentredString(W / 2, footer_h - 110, "2°MC · Tecnologías de la Información · Opción Bilingüe · 2026")
    # Institutional mark with generous breathing room from both page edges.
    logo_size = 155
    fit_image(c, ITSP_LOGO, W - margin - logo_size, 14, logo_size, logo_size)

    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
