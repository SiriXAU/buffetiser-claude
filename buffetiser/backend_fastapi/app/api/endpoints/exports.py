"""
Export endpoints for CSV and PDF generation.
"""
from datetime import date

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.export_service import ExportService
from app.services.tax_calculator import AustralianCGTCalculator

router = APIRouter()


@router.get("/tax/csv")
async def export_tax_csv(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Export CGT events as CSV."""
    # Get events
    tax_calculator = AustralianCGTCalculator(db)
    events = await tax_calculator.get_cgt_events_for_period(start_date, end_date)

    # Generate CSV
    export_service = ExportService()
    csv_content = export_service.generate_csv(events)

    # Return as downloadable file
    filename = f"cgt_report_{start_date}_{end_date}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/tax/pdf/{year}")
async def export_tax_pdf(
    year: int,
    db: AsyncSession = Depends(get_db)
):
    """Export CGT report as PDF for a financial year."""
    # Get complete report
    tax_calculator = AustralianCGTCalculator(db)

    start_date, end_date = tax_calculator.get_financial_year_dates(year)
    events = await tax_calculator.get_cgt_events_for_period(start_date, end_date)
    summary = await tax_calculator.get_financial_year_summary(year)

    unique_investments = len(set(e.investment_symbol for e in events))

    from app.schemas.tax import TaxReportResponse
    from datetime import datetime

    report = TaxReportResponse(
        financial_year=summary.financial_year,
        report_generated=datetime.utcnow(),
        events=events,
        summary=summary,
        total_investments=unique_investments,
        date_range={"start": start_date, "end": end_date}
    )

    # Generate PDF
    export_service = ExportService()
    pdf_content = export_service.generate_pdf(report)

    # Return as downloadable file
    filename = f"cgt_report_fy{summary.financial_year}.pdf"
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
