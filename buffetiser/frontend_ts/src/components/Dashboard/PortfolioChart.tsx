/**
 * Portfolio Value Chart
 *
 * Displays portfolio value over time using Recharts.
 */

import React from 'react';
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Card } from 'react-bootstrap';
import './PortfolioChart.css';

interface PortfolioHistoryData {
  date: string;
  total_value: number;
}

interface PortfolioChartProps {
  data: PortfolioHistoryData[];
  title?: string;
}

export const PortfolioChart: React.FC<PortfolioChartProps> = ({
  data,
  title = 'Portfolio Value History',
}) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-AU', {
      month: 'short',
      day: 'numeric',
    });
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="label">{new Date(payload[0].payload.date).toLocaleDateString('en-AU')}</p>
          <p className="value">{formatCurrency(payload[0].value)}</p>
        </div>
      );
    }
    return null;
  };

  if (!data || data.length === 0) {
    return (
      <Card className="portfolio-chart-card">
        <Card.Header>
          <h5 className="mb-0">{title}</h5>
        </Card.Header>
        <Card.Body>
          <div className="text-center py-5 text-muted">
            No history data available yet.
          </div>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card className="portfolio-chart-card shadow-sm">
      <Card.Header className="bg-light">
        <h5 className="mb-0">📈 {title}</h5>
      </Card.Header>
      <Card.Body>
        <ResponsiveContainer width="100%" height={350}>
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#667eea" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#667eea" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              stroke="#6c757d"
              style={{ fontSize: '0.875rem' }}
            />
            <YAxis
              tickFormatter={formatCurrency}
              stroke="#6c757d"
              style={{ fontSize: '0.875rem' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="total_value"
              stroke="#667eea"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorValue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </Card.Body>
    </Card>
  );
};
