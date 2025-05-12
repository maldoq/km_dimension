import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


def generate_pdf_poutrelle(data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, f"Donnée Poutrelle #{data['id']}")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 2.7 * cm, f"Date de génération : {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    y = height - 4 * cm
    line_height = 1 * cm

    def add_line(title, value, unit=""):
        nonlocal y
        if value is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y, f"{title} :")
            c.setFont("Helvetica", 12)
            c.drawString(8 * cm, y, f"{value:.5f} {unit}")
            y -= line_height

    # Données
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Données d'entrée :")
    y -= 1.5 * cm

    add_line("g", data.get("g"), "decaN/m")
    add_line("q", data.get("q"), "decaN/m")
    add_line("l", data.get("l"), "m")
    add_line("h0", data.get("h0"), "m")
    add_line("fc28", data.get("fc28"), "MPa")
    add_line("h", data.get("h"), "m")

    y -= 0.5 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Résultats calculés :")
    y -= 1.5 * cm

    add_line("elu", data.get("elu"), "decaN/m")
    add_line("els", data.get("els"), "decaN/m")
    add_line("pu", data.get("pu"), "decaN/m")
    add_line("ps", data.get("ps"), "decaN/m")
    add_line("moment_max_elu", data.get("moment_max_elu"), "decaN/m")
    add_line("moment_max_els", data.get("moment_max_els"), "decaN/m")
    add_line("tu", data.get("tu"), "decaN/m")
    add_line("ts", data.get("ts"), "decaN/m")
    add_line("fbu", data.get("fbu"), "MPa")
    add_line("d", data.get("d"), "m")
    add_line("mu de verification", data.get("mu_verif"), "decaN.m")
    add_line("µ", data.get("mue"), "")
    add_line("alpha", data.get("alpha"), "")
    add_line("z", data.get("z"), "m")
    add_line("ast", data.get("ast"), "m²")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()
