/**
 * Tax Report Page
 *
 * Main page for viewing and exporting CGT reports.
 */

import React, { useState, useEffect } from 'react';
import { TaxReportTable } from '../components/TaxReport/TaxReportTable';
import { TaxSummaryCard } from '../components/TaxReport/TaxSummaryCard';
import { api } from '../api/client';
import { TaxReport } from '../types';
import { saveAs } from 'file-saver';
import './TaxReportPage.css';

export const TaxReportPage: React.FC = () => {
  const currentYear = new Date().getMonth() >= 6
    ? new Date().getFullYear()
    : new Date().getFullYear() - 1;

  const [year, setYear] = useState<number>(currentYear);
  const [report, setReport] = useState<TaxReport | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [exporting, setExporting] = useState<{
    csv: boolean;
    pdf: boolean;
  }>({ csv: false, pdf: false });

  useEffect(() => {
    loadReport();
  }, [year]);

  const loadReport = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.tax.getReport(year);
      setReport(response.data);
    } catch (err: any) {
      console.error('Failed to load tax report:', err);
      setError(
        err.response?.data?.detail || 'Failed to load tax report. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = async () => {
    if (!report) return;

    setExporting((prev) => ({ ...prev, csv: true }));
    try {
      const blob = await api.export.taxCSV(
        report.date_range.start,
        report.date_range.end
      );
      saveAs(blob, `cgt_report_${report.financial_year}.csv`);
    } catch (err) {
      console.error('Failed to export CSV:', err);
      alert('Failed to export CSV. Please try again.');
    } finally {
      setExporting((prev) => ({ ...prev, csv: false }));
    }
  };

  const handleExportPDF = async () => {
    if (!report) return;

    setExporting((prev) => ({ ...prev, pdf: true }));
    try {
      const blob = await api.export.taxPDF(year);
      saveAs(blob, `cgt_report_FY${report.financial_year}.pdf`);
    } catch (err) {
      console.error('Failed to export PDF:', err);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setExporting((prev) => ({ ...prev, pdf: false }));
    }
  };

  const handleYearChange = (increment: number) => {
    setYear((prev) => prev + increment);
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading tax report...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          <h4>Error Loading Report</h4>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={loadReport}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="container mt-5">
        <div className="alert alert-info">
          No tax report data available.
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid tax-report-page">
      {/* Header */}
      <div className="page-header">
        <h1 className="page-title">
          Australian Capital Gains Tax Report
        </h1>
        <div className="year-selector">
          <button
            className="btn btn-outline-secondary"
            onClick={() => handleYearChange(-1)}
          >
            ← Previous FY
          </button>
          <span className="current-year">
            FY {report.financial_year}
          </span>
          <button
            className="btn btn-outline-secondary"
            onClick={() => handleYearChange(1)}
            disabled={year >= currentYear}
          >
            Next FY →
          </button>
        </div>
      </div>

      {/* Export Buttons */}
      <div className="export-section mb-4">
        <div className="d-flex gap-2">
          <button
            className="btn btn-success"
            onClick={handleExportCSV}
            disabled={exporting.csv || report.events.length === 0}
          >
            {exporting.csv ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" />
                Exporting...
              </>
            ) : (
              <>
                📊 Export to CSV
              </>
            )}
          </button>
          <button
            className="btn btn-danger"
            onClick={handleExportPDF}
            disabled={exporting.pdf || report.events.length === 0}
          >
            {exporting.pdf ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" />
                Generating...
              </>
            ) : (
              <>
                📄 Export to PDF
              </>
            )}
          </button>
          <button
            className="btn btn-outline-primary ms-auto"
            onClick={loadReport}
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Summary Card */}
      <TaxSummaryCard summary={report.summary} />

      {/* Events Table */}
      <div className="card">
        <div className="card-header bg-dark text-white">
          <h4 className="mb-0">
            Detailed CGT Events ({report.events.length})
          </h4>
        </div>
        <div className="card-body p-0">
          <TaxReportTable events={report.events} />
        </div>
      </div>

      {/* Report Metadata */}
      <div className="report-footer mt-4 text-muted">
        <small>
          Report Period: {new Date(report.date_range.start).toLocaleDateString('en-AU')} -{' '}
          {new Date(report.date_range.end).toLocaleDateString('en-AU')} |{' '}
          Generated: {new Date(report.report_generated).toLocaleString('en-AU')} |{' '}
          Total Investments: {report.total_investments}
        </small>
      </div>
    </div>
  );
};
