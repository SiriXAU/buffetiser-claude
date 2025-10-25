/**
 * Dashboard Page
 *
 * Main portfolio overview with summary and charts.
 */

import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Button, Spinner, Alert } from 'react-bootstrap';
import { PortfolioSummaryCard } from '../components/Dashboard/PortfolioSummaryCard';
import { PortfolioChart } from '../components/Dashboard/PortfolioChart';
import { api } from '../api/client';
import './DashboardPage.css';

interface PortfolioSummary {
  total_cost: number;
  total_value: number;
  total_profit: number;
  total_profit_percent: number;
  total_investments: number;
}

interface PortfolioHistory {
  date: string;
  total_value: number;
}

export const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState<PortfolioSummary | null>(null);
  const [history, setHistory] = useState<PortfolioHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [summaryResponse, historyResponse] = await Promise.all([
        api.portfolio.getSummary(),
        api.portfolio.getHistory(),
      ]);

      setSummary(summaryResponse.data);
      setHistory(historyResponse.data);
    } catch (err: any) {
      console.error('Failed to load dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdatePrices = async () => {
    setUpdating(true);
    try {
      await fetch('http://localhost:8000/api/v1/updates/prices/all', {
        method: 'POST',
      });

      // Wait a bit for the update to process
      setTimeout(() => {
        loadDashboardData();
        setUpdating(false);
      }, 3000);
    } catch (err) {
      console.error('Failed to update prices:', err);
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <Container className="dashboard-page mt-5">
        <div className="text-center py-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-3">Loading dashboard...</p>
        </div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="dashboard-page mt-5">
        <Alert variant="danger">
          <h4>Error Loading Dashboard</h4>
          <p>{error}</p>
          <Button variant="primary" onClick={loadDashboardData}>
            Try Again
          </Button>
        </Alert>
      </Container>
    );
  }

  if (!summary) {
    return (
      <Container className="dashboard-page mt-5">
        <Alert variant="info">
          <h4>No Data Yet</h4>
          <p>Start by adding your first investment!</p>
        </Alert>
      </Container>
    );
  }

  return (
    <Container fluid className="dashboard-page">
      {/* Page Header */}
      <Row className="page-header mb-4">
        <Col>
          <h1 className="page-title">📊 Dashboard</h1>
          <p className="text-muted">Your portfolio at a glance</p>
        </Col>
        <Col className="text-end">
          <Button
            variant="outline-primary"
            onClick={handleUpdatePrices}
            disabled={updating}
          >
            {updating ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Updating...
              </>
            ) : (
              <>🔄 Update Prices</>
            )}
          </Button>
          <Button
            variant="outline-secondary"
            className="ms-2"
            onClick={loadDashboardData}
          >
            🔃 Refresh
          </Button>
        </Col>
      </Row>

      {/* Portfolio Summary */}
      <Row>
        <Col>
          <PortfolioSummaryCard summary={summary} />
        </Col>
      </Row>

      {/* Portfolio Chart */}
      <Row>
        <Col>
          <PortfolioChart data={history} />
        </Col>
      </Row>

      {/* Quick Actions */}
      <Row className="mt-4">
        <Col md={4}>
          <div className="quick-action-card">
            <h5>💰 Record Transaction</h5>
            <p className="text-muted">Add a purchase or sale</p>
            <Button variant="primary" href="/investments">
              Go to Investments
            </Button>
          </div>
        </Col>
        <Col md={4}>
          <div className="quick-action-card">
            <h5>📊 Tax Report</h5>
            <p className="text-muted">View your CGT events</p>
            <Button variant="success" href="/tax-report">
              View Tax Report
            </Button>
          </div>
        </Col>
        <Col md={4}>
          <div className="quick-action-card">
            <h5>📈 Add Investment</h5>
            <p className="text-muted">Track a new stock or crypto</p>
            <Button variant="info" href="/investments">
              Add Investment
            </Button>
          </div>
        </Col>
      </Row>

      {/* Footer Info */}
      <Row className="mt-5 mb-3">
        <Col>
          <div className="dashboard-footer text-muted text-center">
            <small>
              Last updated: {new Date().toLocaleString('en-AU')} |
              API: <a href="http://localhost:8000/api/v1/docs" target="_blank" rel="noreferrer">
                Documentation
              </a>
            </small>
          </div>
        </Col>
      </Row>
    </Container>
  );
};
