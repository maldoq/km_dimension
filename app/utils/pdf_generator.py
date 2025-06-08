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
    add_line("moment_max_elu", data.get("moment_max_elu"), "decaN.m")
    add_line("moment_max_els", data.get("moment_max_els"), "decaN.m")
    add_line("tu", data.get("tu"), "decaN.m")
    add_line("ts", data.get("ts"), "decaN.m")
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

def generate_pdf_poutre(data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, f"Donnée Poutre #{data['id']}")
    
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

    add_line("fc28", data.get("fc28"), "MPa")
    add_line("fe", data.get("fe"), "MPa")
    add_line("g", data.get("g"), "T/m")
    add_line("q", data.get("q"), "T/m")
    add_line("lx", data.get("lx"), "m")
    add_line("b", data.get("b"), "m")
    add_line("h", data.get("h"), "cm")

    y -= 0.5 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Résultats calculés :")
    y -= 1.5 * cm

    add_line("fbu", data.get("fbu"), "MPa")
    add_line("fsu", data.get("fsu"), "MPa")
    add_line("pu", data.get("pu"), "T/m")
    add_line("mu", data.get("mu"), "T/m")
    add_line("d", data.get("d"), "m")
    add_line("µ", data.get("µ"), "")
    add_line("alpha", data.get("alpha"), "")
    add_line("z", data.get("z"), "m")
    add_line("As", data.get("As"), "m²")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()

def generate_pdf_poteau(data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, f"Donnée Poteau #{data['id']}")
    
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

    add_line("a", data.get("a"), "cm")
    add_line("b", data.get("b"), "cm")
    add_line("lf", data.get("lf"), "cm")
    add_line("nu", data.get("nu"), "T")
    add_line("fe", data.get("fe"), "MPa")
    add_line("fc28", data.get("fc28"), "MPa")

    y -= 0.5 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Résultats calculés :")
    y -= 1.5 * cm

    add_line("I_min", data.get("I_min"), "cm⁴")
    add_line("B", data.get("Bb"), "cm²")
    add_line("i", data.get("i"), "cm")
    add_line("gamma", data.get("gamma"), "")
    add_line("alpha", data.get("alpha"), "")
    add_line("Br", data.get("Br"), "cm²")
    add_line("Ath", data.get("Ath"), "cm²")
    add_line("u", data.get("u"), "m")
    add_line("A_4u", data.get("A_4u"), "cm²")
    add_line("A_2_percent", data.get("A_2_percent"), "cm²")
    add_line("A_min", data.get("A_min"), "cm²")
    add_line("A_5_percent", data.get("A_5_percent"), "cm²")
    add_line("A_max", data.get("A_max"), "cm²")
    add_line("As_calc", data.get("As_calc"), "cm²")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()

def generate_pdf_semelle(data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, f"Donnée Semelle #{data['id']}")
    
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

    add_line("a", data.get("a"), "m")
    add_line("b", data.get("b"), "m")
    add_line("g", data.get("g"), "T")
    add_line("q", data.get("q"), "T")
    add_line("cont_adm", data.get("cont_adm"), "MPa")
    add_line("fe", data.get("fe"), "MPa")

    y -= 0.5 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Résultats calculés :")
    y -= 1.5 * cm

    add_line("ns", data.get("ns"), "T")
    add_line("nu", data.get("nu"), "T")
    add_line("A", data.get("Aa"), "m")
    add_line("B", data.get("Bb"), "m")
    add_line("d1", data.get("d1"), "m")
    add_line("d2", data.get("d2"), "m")
    add_line("d", data.get("d"), "m")
    add_line("h", data.get("h_metre"), "m")
    add_line("As//A", data.get("As__A"), "cm²")
    add_line("As//B", data.get("As__B"), "cm²")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()

def generate_pdf_escalier(data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, f"Donnée Escalier #{data['id']}")
    
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

    add_line("fc28", data.get("fc28"), "MPa")
    add_line("fe", data.get("fe"), "MPa")
    add_line("g1", data.get("g1"), "kN/ml")
    add_line("g2", data.get("g2"), "kN/ml")
    add_line("l", data.get("l"), "m")
    add_line("alpha", data.get("alpha"), "°")
    add_line("d", data.get("d"), "cm")
    add_line("b", data.get("b"), "cm")
    add_line("q", data.get("q"), "kN/ml")
    add_line("As_reel", data.get("As_reel"), "cm²/ml")

    y -= 0.5 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Résultats calculés :")
    y -= 1.5 * cm

    add_line("pu", data.get("pu"), "kN/ml")
    add_line("ps", data.get("ps"), "kN/ml")
    add_line("mu", data.get("mu"), "kN/ml")
    add_line("ms", data.get("ms"), "kN/ml")
    add_line("fbu", data.get("fbu"), "MPa")
    add_line("fsu", data.get("fsu"), "MPa")
    add_line("µ", data.get("µ"), "")
    add_line("gamma", data.get("gamma"), "")
    add_line("µ_l1", data.get("µ_l1"), "")
    add_line("alpha", data.get("alpha"), "")
    add_line("z", data.get("z"), "cm")
    add_line("As", data.get("As"), "cm²/ml")
    add_line("As_y", data.get("As_y"), "cm²/ml")
    add_line("As_c", data.get("As_c"), "cm²/ml") 

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()
