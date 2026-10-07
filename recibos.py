from fpdf import FPDF
from datetime import datetime

def generar_recibo(viaje, tipo):
    pdf = FPDF(format='A5')
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "TAXI HOTEL", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    titulo = "RECIBO HUÉSPED" if tipo == "huesped" else "COPIA RECEPCIÓN"
    pdf.cell(0, 6, titulo, ln=True, align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Recibo #: {viaje['id']}", ln=True)
    pdf.cell(0, 6, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(0, 6, f"Habitacion: {viaje.get('habitacion') or 'N/A'}", ln=True)
    pdf.cell(0, 6, f"Huesped: {viaje.get('huesped') or 'N/A'}", ln=True)
    pdf.cell(0, 6, f"Destino: {viaje.get('destino')}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"TOTAL: Q{viaje.get('monto')}", ln=True, align="R")

    pdf.set_font("Helvetica", "I", 9)
    pdf.ln(4)
    pdf.cell(0, 5, "Gracias por su preferencia", ln=True, align="C")

    return bytes(pdf.output())