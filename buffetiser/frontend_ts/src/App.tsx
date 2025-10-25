/**
 * Main App Component
 */

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { TaxReportPage } from './pages/TaxReportPage';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
          <Container>
            <Navbar.Brand as={Link} to="/">
              <strong>📈 Buffetiser</strong>
              <span className="ms-2 badge bg-primary">v2.0</span>
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="ms-auto">
                <Nav.Link as={Link} to="/">
                  Dashboard
                </Nav.Link>
                <Nav.Link as={Link} to="/tax-report">
                  Tax Report
                </Nav.Link>
                <Nav.Link as={Link} to="/investments">
                  Investments
                </Nav.Link>
                <Nav.Link href="http://localhost:8000/api/v1/docs" target="_blank">
                  API Docs
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>

        {/* Main Content */}
        <Routes>
          <Route path="/" element={<DashboardPlaceholder />} />
          <Route path="/tax-report" element={<TaxReportPage />} />
          <Route path="/investments" element={<InvestmentsPlaceholder />} />
        </Routes>

        {/* Footer */}
        <footer className="app-footer">
          <Container>
            <div className="text-center text-muted py-3">
              <small>
                Buffetiser v2.0 - Australian CGT Tax Tracking | FastAPI + React + TypeScript
              </small>
            </div>
          </Container>
        </footer>
      </div>
    </Router>
  );
}

// Placeholder components (to be implemented)
const DashboardPlaceholder: React.FC = () => (
  <Container className="mt-5">
    <div className="alert alert-info">
      <h2>Welcome to Buffetiser v2.0!</h2>
      <p>
        This is the new FastAPI + TypeScript version with Australian CGT tax tracking.
      </p>
      <h4>New Features:</h4>
      <ul>
        <li>✅ Tax parcel tracking for each purchase</li>
        <li>✅ Parcel selection for tax-optimized sales</li>
        <li>✅ Australian CGT with 50% discount calculation</li>
        <li>✅ Financial year tax reports (July 1 - June 30)</li>
        <li>✅ Export to CSV and PDF</li>
        <li>✅ Sortable tax event tables</li>
      </ul>
      <hr />
      <p>
        <strong>Get Started:</strong> Visit the{' '}
        <Link to="/tax-report">Tax Report</Link> page to see your CGT events!
      </p>
      <p>
        <strong>API Documentation:</strong>{' '}
        <a href="http://localhost:8000/api/v1/docs" target="_blank" rel="noreferrer">
          http://localhost:8000/api/v1/docs
        </a>
      </p>
    </div>
  </Container>
);

const InvestmentsPlaceholder: React.FC = () => (
  <Container className="mt-5">
    <div className="alert alert-warning">
      <h3>Investments Dashboard</h3>
      <p>
        This page is coming soon! It will include:
      </p>
      <ul>
        <li>Investment cards with live prices</li>
        <li>Purchase/Sale recording with parcel selection</li>
        <li>Dividend tracking</li>
        <li>Performance charts</li>
      </ul>
      <p className="mb-0">
        For now, use the API docs to create investments:{' '}
        <a href="http://localhost:8000/api/v1/docs" target="_blank" rel="noreferrer">
          API Docs
        </a>
      </p>
    </div>
  </Container>
);

export default App;
