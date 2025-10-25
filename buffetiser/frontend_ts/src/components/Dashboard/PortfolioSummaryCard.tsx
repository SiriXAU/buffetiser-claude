/**
 * Portfolio Summary Card
 *
 * Displays overall portfolio statistics.
 */

import React from 'react';
import { Card } from 'react-bootstrap';
import './PortfolioSummaryCard.css';

interface PortfolioSummary {
  total_cost: number;
  total_value: number;
  total_profit: number;
  total_profit_percent: number;
  total_investments: number;
}

interface PortfolioSummaryCardProps {
  summary: PortfolioSummary;
}

export const PortfolioSummaryCard: React.FC<PortfolioSummaryCardProps> = ({ summary }) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  return (
    <Card className="portfolio-summary-card shadow-sm">
      <Card.Header className="bg-gradient-primary text-white">
        <h4 className="mb-0">📊 Portfolio Summary</h4>
      </Card.Header>
      <Card.Body>
        <div className="row g-4">
          <div className="col-md-3">
            <div className="metric-box">
              <label>Total Invested</label>
              <div className="value">{formatCurrency(summary.total_cost)}</div>
              <small className="text-muted">Cost basis</small>
            </div>
          </div>

          <div className="col-md-3">
            <div className="metric-box">
              <label>Current Value</label>
              <div className="value text-primary">{formatCurrency(summary.total_value)}</div>
              <small className="text-muted">Market value</small>
            </div>
          </div>

          <div className="col-md-3">
            <div className="metric-box">
              <label>Total Profit/Loss</label>
              <div className={`value ${summary.total_profit >= 0 ? 'text-success' : 'text-danger'}`}>
                {formatCurrency(summary.total_profit)}
              </div>
              <small className={summary.total_profit >= 0 ? 'text-success' : 'text-danger'}>
                {formatPercent(summary.total_profit_percent)}
              </small>
            </div>
          </div>

          <div className="col-md-3">
            <div className="metric-box">
              <label>Investments</label>
              <div className="value text-secondary">{summary.total_investments}</div>
              <small className="text-muted">Active holdings</small>
            </div>
          </div>
        </div>
      </Card.Body>
    </Card>
  );
};
