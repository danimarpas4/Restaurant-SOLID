from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from producto import Session
from pedido import Pedido

def generar_reporte(nombre_archivo):
    """
    Generates an immutable PDF audit trail of all recorded transactions.
    Orchestrates data fetching and document composition using ReportLab.
    """
    # Establish connection to fetch the global state
    session = Session()
    pedidos = session.query(Pedido).all()

    # Initialize Document Template with standard layout
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    elementos = []
    estilos = getSampleStyleSheet()

    # Define strict styling for document integrity and readability
    estilo_titulo = ParagraphStyle(
        'TituloFactura',
        parent=estilos['Heading1'],
        fontSize=18,
        spaceAfter=20,
        textColor=colors.HexColor("#2E4053")
    )
    
    estilo_negrita = ParagraphStyle(
        'Negrita',
        parent=estilos['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10
    )

    # Iterate through the ledger to populate the report
    for pedido in pedidos:
        # Header Metadata
        elementos.append(Paragraph(f"INVOICE - Transaction ID #{pedido.id}", estilo_titulo))
        elementos.append(Paragraph(f"<b>Client:</b> {pedido.cliente}", estilo_negrita))
        elementos.append(Paragraph(f"<b>Timestamp:</b> {pedido.fecha.strftime('%Y-%m-%d %H:%M:%S UTC')}", estilos['Normal']))
        elementos.append(Spacer(1, 12))

        # Table Data Structure
        datos_tabla = [["Asset", "Qty", "Unit Price", "Subtotal"]]
        
        for pp in pedido.productos:
            subtotal = pp.producto.precio * pp.cantidad
            datos_tabla.append([
                pp.producto.nombre,
                pp.cantidad,
                f"${pp.producto.precio:.2f}",
                f"${subtotal:.2f}"
            ])

        # Apply visual constraints to the data table
        tabla = Table(datos_tabla, colWidths=[200, 80, 80, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#D5D8DC")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 10))

        # Final Settlement Value
        total_texto = f"<b>TOTAL SETTLEMENT: ${pedido.total:.2f}</b>"
        elementos.append(Paragraph(total_texto, ParagraphStyle('Total', parent=estilos['Normal'], alignment=2, fontSize=12)))
        
        # Delimiter for batch processing visual separation
        elementos.append(Spacer(1, 30))
        elementos.append(Paragraph("-" * 100, estilos['Normal']))
        elementos.append(Spacer(1, 20))

    # Compile and save the artifact
    doc.build(elementos)
    
    # Close session to release resources
    session.close()