/**
 * Tax Summary Card Component
 *
 * Displays CGT summary with key metrics.
 */

import React from 'react';
import { CGTSummary } from '../../types';
import './TaxSummaryCard.css';

interface TaxSummaryCardProps {
  summary: CGTSummary;
}

export const TaxSummaryCard: React.FC<TaxSummaryCardProps> = ({ summary }) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  return (
    <div className="card tax-summary-card mb-4">
      <div className="card-header bg-primary text-white">
        <h4 className="mb-0">
          Tax Summary - Financial Year {summary.financial_year}
        </h4>
      </div>
      <div className="card-body">
        {/* Main Summary */}
        <div className="row mb-4">
          <div className="col-md-3">
            <div className="summary-item">
              <label>Total Capital Gains</label>
              <div className="summary-value text-success">
                {formatCurrency(summary.total_capital_gains)}
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="summary-item">
              <label>CGT Discount Applied</label>
              <div className="summary-value text-primary">
                -{formatCurrency(summary.total_discount_amount)}
              </div>
              <small className="text-muted">50% discount on long-term holdings</small>
            </div>
          </div>
          <div className="col-md-3">
            <div className="summary-item">
              <label>Net Capital Gain</label>
              <div className="summary-value text-dark fw-bold fs-4">
                {formatCurrency(summary.net_capital_gain)}
              </div>
              <small className="text-muted">Assessable amount</small>
            </div>
          </div>
          <div className="col-md-3">
            <div className="summary-item">
              <label>Total Events</label>
              <div className="summary-value text-secondary">
                {summary.total_events}
              </div>
            </div>
          </div>
        </div>

        {/* Capital Losses */}
        {summary.total_capital_losses > 0 && (
          <div className="row mb-4">
            <div className="col-12">
              <div className="alert alert-warning">
                <strong>Capital Losses:</strong>{' '}
                {formatCurrency(summary.total_capital_losses)} (can be offset against gains)
              </div>
            </div>
          </div>
        )}

        {/* Breakdown */}
        <div className="row">
          <div className="col-md-6">
            <h5>Holding Period Breakdown</h5>
            <table className="table table-sm">
              <tbody>
                <tr>
                  <td>Short-term Gains (&lt; 12 months)</td>
                  <td className="text-end">
                    {formatCurrency(summary.short_term_gains)}
                  </td>
                  <td className="text-end text-muted">
                    {summary.short_term_events} event
                    {summary.short_term_events !== 1 ? 's' : ''}
                  </td>
                </tr>
                <tr>
                  <td>Long-term Gains (≥ 12 months)</td>
                  <td className="text-end">
                    {formatCurrency(summary.long_term_gains)}
                  </td>
                  <td className="text-end text-muted">
                    {summary.long_term_events} event
                    {summary.long_term_events !== 1 ? 's' : ''}
                  </td>
                </tr>
                <tr className="table-active">
                  <td>
                    <strong>After 50% Discount</strong>
                  </td>
                  <td className="text-end">
                    <strong>{formatCurrency(summary.long_term_discounted)}</strong>
                  </td>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="col-md-6">
            <h5>Gains by Investment</h5>
            <table className="table table-sm">
              <tbody>
                {Object.entries(summary.gains_by_investment)
                  .sort(([, a], [, b]) => b - a)
                  .map(([symbol, gain]) => (
                    <tr key={symbol}>
                      <td>
                        <strong>{symbol}</strong>
                      </td>
                      <td className="text-end">
                        <span
                          className={
                            gain >= 0 ? 'text-success' : 'text-danger'
                          }
                        >
                          {formatCurrency(gain)}
                        </span>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Important Note */}
        <div className="row mt-3">
          <div className="col-12">
            <div className="alert alert-info mb-0">
              <strong>Note:</strong> This report is for informational purposes only.
              Please consult with a qualified tax professional or accountant for
              official tax advice and lodgement.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
