"""
Export service for generating CSV and PDF reports.
"""
import io
from datetime import datetime
from typing import BinaryIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.schemas.tax import CGTEvent, CGTSummary, TaxReportResponse


class ExportService:
    """Service for exporting tax reports to CSV and PDF."""

    @staticmethod
    def generate_csv(events: list[CGTEvent]) -> bytes:
        """
        Generate CSV file from CGT events.

        Args:
            events: List of CGT events

        Returns:
            CSV file content as bytes
        """
        # Convert events to DataFrame
        data = []
        for event in events:
            data.append({
                "Financial Year": event.financial_year,
                "Event Date": event.event_date.strftime("%d/%m/%Y"),
                "Investment": event.investment_symbol,
                "Name": event.investment_name or "",
                "Units Sold": f"{event.units_sold:.4f}",
                "Acquisition Date": event.acquisition_date.strftime("%d/%m/%Y"),
                "Disposal Date": event.disposal_date.strftime("%d/%m/%Y"),
                "Holding Period (Days)": event.holding_period_days,
                "Cost Base": f"{event.cost_base:.2f}",
                "Proceeds": f"{event.proceeds:.2f}",
                "Capital Gain": f"{event.capital_gain:.2f}",
                "CGT Treatment": event.cgt_treatment.value,
                "CGT Discount Applied": "Yes" if event.cgt_discount_applied else "No",
                "Discount Amount": f"{event.discount_amount:.2f}",
                "Net Capital Gain": f"{event.net_capital_gain:.2f}",
            })

        df = pd.DataFrame(data)

        # Convert to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue().encode("utf-8")

    @staticmethod
    def generate_pdf(report: TaxReportResponse) -> bytes:
        """
        Generate PDF report from tax report data.

        Args:
            report: Complete tax report

        Returns:
            PDF file content as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=18,
        )

        # Container for PDF elements
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#2C3E50"),
            spaceAfter=30,
            alignment=1,  # Center
        )
        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#34495E"),
            spaceAfter=12,
        )
        normal_style = styles["Normal"]

        # Title Page
        elements.append(Spacer(1, 1 * inch))
        elements.append(Paragraph("Capital Gains Tax Report", title_style))
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(
            Paragraph(
                f"Financial Year: {report.financial_year}",
                heading_style
            )
        )
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(
            Paragraph(
                f"Report Generated: {report.report_generated.strftime('%d/%m/%Y %H:%M')}",
                normal_style
            )
        )
        elements.append(Spacer(1, 0.5 * inch))

        # Summary Section
        summary = report.summary
        elements.append(Paragraph("Summary", heading_style))
        elements.append(Spacer(1, 0.2 * inch))

        summary_data = [
            ["Metric", "Value"],
            ["Total Capital Gains", f"${summary.total_capital_gains:,.2f}"],
            ["Total Capital Losses", f"${summary.total_capital_losses:,.2f}"],
            ["Total CGT Discount", f"${summary.total_discount_amount:,.2f}"],
            ["Net Capital Gain", f"${summary.net_capital_gain:,.2f}"],
            ["", ""],
            ["Short-term Gains (< 12 months)", f"${summary.short_term_gains:,.2f}"],
            ["Long-term Gains (≥ 12 months)", f"${summary.long_term_gains:,.2f}"],
            ["Long-term (after 50% discount)", f"${summary.long_term_discounted:,.2f}"],
            ["", ""],
            ["Total CGT Events", str(summary.total_events)],
            ["Short-term Events", str(summary.short_term_events)],
            ["Long-term Events", str(summary.long_term_events)],
        ]

        summary_table = Table(summary_data, colWidths=[3.5 * inch, 2 * inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498DB")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Gains by Investment
        if summary.gains_by_investment:
            elements.append(Paragraph("Gains by Investment", heading_style))
            elements.append(Spacer(1, 0.2 * inch))

            inv_data = [["Investment", "Net Capital Gain"]]
            for symbol, gain in sorted(
                summary.gains_by_investment.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                inv_data.append([symbol, f"${gain:,.2f}"])

            inv_table = Table(inv_data, colWidths=[3 * inch, 2 * inch])
            inv_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2ECC71")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))

            elements.append(inv_table)
            elements.append(Spacer(1, 0.3 * inch))

        # Page break before detailed events
        elements.append(PageBreak())

        # Detailed CGT Events
        elements.append(Paragraph("Detailed CGT Events", heading_style))
        elements.append(Spacer(1, 0.2 * inch))

        if report.events:
            # Create table data
            event_data = [[
                "Date",
                "Investment",
                "Units",
                "Held (days)",
                "Cost Base",
                "Proceeds",
                "Capital Gain",
                "Discount",
                "Net Gain",
            ]]

            for event in report.events:
                event_data.append([
                    event.disposal_date.strftime("%d/%m/%Y"),
                    event.investment_symbol,
                    f"{event.units_sold:.2f}",
                    str(event.holding_period_days),
                    f"${event.cost_base:.2f}",
                    f"${event.proceeds:.2f}",
                    f"${event.capital_gain:.2f}",
                    "50%" if event.cgt_discount_applied else "0%",
                    f"${event.net_capital_gain:.2f}",
                ])

            # Column widths for landscape-oriented table
            col_widths = [0.8 * inch, 0.9 * inch, 0.6 * inch, 0.7 * inch,
                         0.9 * inch, 0.9 * inch, 1 * inch, 0.7 * inch, 1 * inch]

            event_table = Table(event_data, colWidths=col_widths, repeatRows=1)
            event_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E74C3C")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))

            elements.append(event_table)
        else:
            elements.append(Paragraph("No CGT events for this period.", normal_style))

        # Footer
        elements.append(Spacer(1, 0.5 * inch))
        footer_style = ParagraphStyle(
            "Footer",
            parent=normal_style,
            fontSize=8,
            textColor=colors.grey,
        )
        elements.append(
            Paragraph(
                "This report is for informational purposes only. "
                "Please consult with a qualified tax professional for tax advice.",
                footer_style
            )
        )

        # Build PDF
        doc.build(elements)

        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()

        return pdf_content
