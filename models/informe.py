from datetime import date, datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    LongTable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)


class Informe:
    def __init__(
        self,
        id_informe: int,
        fecha_generacion: date | datetime | str,
        id_empleado: int,
        nombre_empleado: str = "",
        registros_horas: list[tuple] | None = None,
        proyectos: list[tuple] | None = None,
    ):
        self.id_informe = id_informe
        self.fecha_generacion = fecha_generacion
        self.id_empleado = id_empleado
        self.nombre_empleado = nombre_empleado
        self.registros_horas = registros_horas or []
        self.proyectos = proyectos or []

    def __str__(self):
        return (
            f"Informe(id_informe={self.id_informe}, "
            f"fecha_generacion={self.fecha_generacion}, "
            f"id_empleado={self.id_empleado})"
        )

    def exportarPDF(self, ruta: str | None = None) -> str:
        if ruta is None:
            ruta = f"informe_{self.id_informe}.pdf"

        estilos = getSampleStyleSheet()
        documento = SimpleDocTemplate(
            ruta,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
            title=f"Informe {self.id_informe}",
        )
        contenido = [
            Paragraph(f"Informe de horas #{self.id_informe}", estilos["Title"]),
            Spacer(1, 8 * mm),
            Paragraph(
                f"Fecha de generación: {escape(str(self.fecha_generacion))}",
                estilos["BodyText"],
            ),
            Paragraph(
                f"Empleado: {escape(self.nombre_empleado)} "
                f"(ID: {self.id_empleado})",
                estilos["BodyText"],
            ),
            Spacer(1, 8 * mm),
            Paragraph("Proyectos del empleado", estilos["Heading2"]),
        ]

        if self.proyectos:
            for id_proyecto, nombre_proyecto in self.proyectos:
                contenido.append(
                    Paragraph(
                        f"{id_proyecto}: {escape(str(nombre_proyecto))}",
                        estilos["BodyText"],
                    )
                )
        else:
            contenido.append(
                Paragraph(
                    "El empleado no tiene proyectos asociados.",
                    estilos["BodyText"],
                )
            )

        contenido.extend([
            Spacer(1, 8 * mm),
            Paragraph("Detalle de horas registradas", estilos["Heading2"]),
        ])
        datos_tabla = [[
            "Fecha", "Horas", "Descripción de tarea", "Proyecto"
        ]]
        for fecha, horas, descripcion, nombre_proyecto in self.registros_horas:
            datos_tabla.append([
                escape(str(fecha)),
                escape(str(horas)),
                Paragraph(escape(str(descripcion or "")), estilos["BodyText"]),
                Paragraph(escape(str(nombre_proyecto)), estilos["BodyText"]),
            ])

        tabla = LongTable(
            datos_tabla,
            colWidths=[27 * mm, 17 * mm, 87 * mm, 43 * mm],
            repeatRows=1,
        )
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#264653")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.white, colors.HexColor("#eef3f5")
            ]),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        contenido.append(tabla)
        documento.build(contenido)

        return ruta