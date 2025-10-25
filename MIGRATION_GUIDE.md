# 🚀 Buffetiser Refactoring Migration Guide

## FastAPI + React/TypeScript + Australian CGT Tax Tracking

---

## 📋 What's Been Completed

### ✅ Backend (FastAPI + SQLAlchemy + PostgreSQL)

#### **1. Project Structure**
Complete backend structure in `buffetiser/backend_fastapi/`:
```
backend_fastapi/
├── app/
│   ├── main.py                    # FastAPI app initialization ✅
│   ├── config.py                  # Settings with Pydantic ✅
│   ├── database.py                # Async SQLAlchemy setup ✅
│   ├── models/                    # SQLAlchemy models ✅
│   │   ├── investment.py          # Investment model
│   │   ├── transaction.py         # Purchase, Sale, TaxParcel models
│   │   ├── dividend.py            # Dividend models
│   │   └── history.py             # Price history models
│   ├── schemas/                   # Pydantic schemas ✅
│   │   ├── investment.py
│   │   ├── transaction.py
│   │   ├── dividend.py
│   │   └── tax.py                 # Tax reporting schemas
│   ├── api/endpoints/             # API routes ✅
│   │   ├── investments.py         # Investment CRUD
│   │   ├── transactions.py        # Purchase/Sale with tax parcels
│   │   ├── dividends.py           # Dividend tracking
│   │   ├── tax.py                 # CGT reporting (KEY FEATURE!)
│   │   ├── exports.py             # CSV/PDF exports
│   │   └── portfolio.py           # Portfolio stats (TODO: complete logic)
│   ├── services/                  # Business logic ✅
│   │   ├── tax_calculator.py      # Australian CGT calculator
│   │   └── export_service.py      # CSV/PDF generation
│   └── utils/
│       └── constants.py           # Enums and constants ✅
├── alembic/                       # Database migrations ✅
│   ├── env.py
│   └── versions/
├── alembic.ini                    # Alembic config ✅
├── Dockerfile                     # Docker setup ✅
└── requirements.txt               # Dependencies ✅
```

#### **2. Key Features Implemented**

##### **Australian Capital Gains Tax (CGT) Calculator** 🇦🇺
Location: `app/services/tax_calculator.py`

Features:
- ✅ **Financial Year Support**: July 1 - June 30
- ✅ **50% CGT Discount**: For assets held >= 12 months
- ✅ **Tax Parcel Tracking**: Individual parcels for each purchase
- ✅ **Parcel Selection**: Users can choose which parcels to sell
- ✅ **FIFO Support**: Automatic first-in-first-out allocation
- ✅ **Holding Period Calculation**: Days between acquisition and disposal
- ✅ **CGT Event Generation**: Complete tax events with all details

##### **Tax Reporting Endpoints**
Location: `app/api/endpoints/tax.py`

Endpoints:
- `GET /api/v1/tax/events` - Get CGT events for date range
- `GET /api/v1/tax/report/{year}` - Complete FY report with summary
- `GET /api/v1/tax/parcels/{investment_id}` - Available parcels for sale
- `GET /api/v1/tax/summary/{year}` - Quick summary without details

##### **Export Services**
Location: `app/services/export_service.py`

Features:
- ✅ **CSV Export**: All CGT events with full details
- ✅ **PDF Export**: Professional tax report with:
  - Summary page with totals
  - Breakdown by investment
  - Detailed event table
  - Short-term vs long-term analysis

Endpoints:
- `GET /api/v1/export/tax/csv` - Download CSV
- `GET /api/v1/export/tax/pdf/{year}` - Download PDF for FY

##### **Transaction Management**
Location: `app/api/endpoints/transactions.py`

Features:
- ✅ **Purchase Recording**: Automatically creates tax parcels
- ✅ **Sale with Auto FIFO**: Default FIFO allocation
- ✅ **Sale with Parcel Selection**: Choose specific parcels to sell
- ✅ **CGT Calculation**: Automatic capital gains calculation on sale

##### **Models & Relationships**

**Investment Model**:
- One-to-many: purchases, sales, dividends, reinvestments, history

**Purchase Model**:
- Creates `TaxParcel` automatically
- Tracks: units, price, fee, date, platform, exchange

**Sale Model**:
- Links to multiple `TaxParcelAllocation`
- Calculates CGT on sale

**TaxParcel Model** (NEW!):
- Tracks individual investment parcels
- `units_acquired` vs `units_remaining`
- Cost base per unit
- Acquisition date for holding period

**TaxParcelAllocation Model** (NEW!):
- Links sales to specific parcels
- Stores: capital gain, holding period, discount applied
- Enables tax optimization

#### **3. Database & Migrations**

- ✅ Async PostgreSQL with SQLAlchemy 2.0
- ✅ Alembic configured for migrations
- ✅ Proper relationships and cascading deletes
- ✅ Unique constraints on dates and trade counts

#### **4. API Features**

- ✅ FastAPI with automatic OpenAPI docs
- ✅ Pydantic validation
- ✅ Async/await throughout
- ✅ Redis caching setup
- ✅ CORS configured
- ✅ Proper error handling

---

## 🚧 What Still Needs to be Done

### **1. Frontend - React + TypeScript Conversion**

**Priority: HIGH**

Create: `buffetiser/frontend_ts/`

#### **A. Project Setup**
```bash
cd buffetiser
npx create-react-app frontend_ts --template typescript
cd frontend_ts
```

#### **B. Install Dependencies**
```bash
npm install axios react-router-dom@7 recharts
npm install react-bootstrap bootstrap
npm install @types/react @types/react-dom
npm install @tanstack/react-table  # For sortable tax table
npm install date-fns  # Date handling
npm install file-saver @types/file-saver  # CSV download
npm install jspdf jspdf-autotable @types/jspdf  # PDF generation (client-side option)
```

#### **C. Create Type Definitions**

Create `src/types/`:

**`investment.ts`**:
```typescript
export interface Investment {
  id: number;
  key: string;
  symbol: string;
  name: string | null;
  type: "Shares" | "Crypto";
  live_price: number;
  visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface InvestmentDetail extends Investment {
  units_held: number;
  average_cost: number;
  total_cost: number;
  current_value: number;
  total_profit: number;
  total_profit_percent: number;
  daily_change: number;
  daily_change_percent: number;
  price_history: PriceHistory[];
}

export interface PriceHistory {
  date: string;
  high: number;
  low: number;
  close: number;
  volume: number;
}
```

**`tax.ts`**:
```typescript
export interface CGTEvent {
  id: number;
  event_date: string;
  financial_year: string;
  investment_symbol: string;
  investment_name: string | null;
  units_sold: number;
  acquisition_date: string;
  disposal_date: string;
  cost_base: number;
  proceeds: number;
  capital_gain: number;
  holding_period_days: number;
  cgt_treatment: "short_term" | "long_term";
  cgt_discount_applied: boolean;
  discount_amount: number;
  net_capital_gain: number;
  sale_id: number;
  parcel_id: number | null;
}

export interface CGTSummary {
  financial_year: string;
  total_capital_gains: number;
  total_capital_losses: number;
  total_discount_amount: number;
  net_capital_gain: number;
  short_term_gains: number;
  long_term_gains: number;
  long_term_discounted: number;
  total_events: number;
  short_term_events: number;
  long_term_events: number;
  gains_by_investment: Record<string, number>;
}

export interface TaxReport {
  financial_year: string;
  report_generated: string;
  events: CGTEvent[];
  summary: CGTSummary;
  total_investments: number;
  date_range: {
    start: string;
    end: string;
  };
}

export interface TaxParcel {
  id: number;
  investment_id: number;
  acquisition_date: string;
  units_acquired: number;
  units_remaining: number;
  cost_base_per_unit: number;
  total_cost_base: number;
  description: string | null;
  is_fully_sold: boolean;
  percentage_remaining: number;
}
```

#### **D. Create API Client**

**`src/api/client.ts`**:
```typescript
import axios from 'axios';
import type { Investment, InvestmentDetail } from '../types/investment';
import type { CGTEvent, TaxReport, TaxParcel } from '../types/tax';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const investmentAPI = {
  getAll: () => api.get<Investment[]>('/investments'),
  getById: (id: number) => api.get<InvestmentDetail>(`/investments/${id}`),
  create: (data: any) => api.post<Investment>('/investments', data),
  update: (id: number, data: any) => api.patch<Investment>(`/investments/${id}`, data),
  delete: (id: number) => api.delete(`/investments/${id}`),
};

export const taxAPI = {
  getEvents: (startDate: string, endDate: string) =>
    api.get<CGTEvent[]>('/tax/events', { params: { start_date: startDate, end_date: endDate } }),
  getReport: (year: number) => api.get<TaxReport>(`/tax/report/${year}`),
  getParcels: (investmentId: number) => api.get<{ parcels: TaxParcel[] }>(`/tax/parcels/${investmentId}`),
  exportCSV: (startDate: string, endDate: string) =>
    api.get('/export/tax/csv', {
      params: { start_date: startDate, end_date: endDate },
      responseType: 'blob',
    }),
  exportPDF: (year: number) =>
    api.get(`/export/tax/pdf/${year}`, { responseType: 'blob' }),
};

export const transactionAPI = {
  createPurchase: (data: any) => api.post('/transactions/purchase', data),
  createSale: (data: any) => api.post('/transactions/sale', data),
  createSaleWithParcels: (data: any) => api.post('/transactions/sale-with-parcels', data),
};

export default api;
```

#### **E. Create Tax Report Component** ⭐ KEY COMPONENT

**`src/components/TaxReport/TaxReportTable.tsx`**:
```typescript
import React, { useMemo, useState } from 'react';
import { useTable, useSortBy, Column } from 'react-table';
import type { CGTEvent } from '../../types/tax';

interface Props {
  events: CGTEvent[];
}

export const TaxReportTable: React.FC<Props> = ({ events }) => {
  const columns: Column<CGTEvent>[] = useMemo(
    () => [
      {
        Header: 'Date',
        accessor: 'disposal_date',
        Cell: ({ value }) => new Date(value).toLocaleDateString('en-AU'),
      },
      {
        Header: 'Investment',
        accessor: 'investment_symbol',
      },
      {
        Header: 'Units',
        accessor: 'units_sold',
        Cell: ({ value }) => value.toFixed(4),
      },
      {
        Header: 'Holding Period',
        accessor: 'holding_period_days',
        Cell: ({ value }) => `${value} days`,
      },
      {
        Header: 'Cost Base',
        accessor: 'cost_base',
        Cell: ({ value }) => `$${value.toFixed(2)}`,
      },
      {
        Header: 'Proceeds',
        accessor: 'proceeds',
        Cell: ({ value }) => `$${value.toFixed(2)}`,
      },
      {
        Header: 'Capital Gain',
        accessor: 'capital_gain',
        Cell: ({ value }) => (
          <span style={{ color: value >= 0 ? 'green' : 'red' }}>
            ${value.toFixed(2)}
          </span>
        ),
      },
      {
        Header: 'CGT Discount',
        accessor: 'cgt_discount_applied',
        Cell: ({ value }) => (value ? '50%' : '0%'),
      },
      {
        Header: 'Net Gain',
        accessor: 'net_capital_gain',
        Cell: ({ value }) => (
          <span style={{ color: value >= 0 ? 'green' : 'red' }}>
            ${value.toFixed(2)}
          </span>
        ),
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data: events }, useSortBy);

  return (
    <div className="table-responsive">
      <table {...getTableProps()} className="table table-striped">
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps((column as any).getSortByToggleProps())}>
                  {column.render('Header')}
                  <span>
                    {(column as any).isSorted
                      ? (column as any).isSortedDesc
                        ? ' 🔽'
                        : ' 🔼'
                      : ''}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
```

#### **F. Create Tax Report Page**

**`src/pages/TaxReport.tsx`**:
```typescript
import React, { useState, useEffect } from 'react';
import { TaxReportTable } from '../components/TaxReport/TaxReportTable';
import { taxAPI } from '../api/client';
import type { TaxReport } from '../types/tax';

export const TaxReportPage: React.FC = () => {
  const [year, setYear] = useState(2023);
  const [report, setReport] = useState<TaxReport | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadReport();
  }, [year]);

  const loadReport = async () => {
    setLoading(true);
    try {
      const response = await taxAPI.getReport(year);
      setReport(response.data);
    } catch (error) {
      console.error('Failed to load tax report:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = async () => {
    try {
      const response = await taxAPI.exportCSV(
        report!.date_range.start,
        report!.date_range.end
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cgt_report_${year}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to export CSV:', error);
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await taxAPI.exportPDF(year);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cgt_report_FY${report!.financial_year}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to export PDF:', error);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!report) return <div>No data</div>;

  return (
    <div className="container mt-4">
      <h1>Capital Gains Tax Report</h1>
      <h2>Financial Year {report.financial_year}</h2>

      {/* Summary Card */}
      <div className="card mb-4">
        <div className="card-body">
          <h3>Summary</h3>
          <div className="row">
            <div className="col-md-3">
              <strong>Total Capital Gains:</strong>
              <br />${report.summary.total_capital_gains.toFixed(2)}
            </div>
            <div className="col-md-3">
              <strong>Total CGT Discount:</strong>
              <br />${report.summary.total_discount_amount.toFixed(2)}
            </div>
            <div className="col-md-3">
              <strong>Net Capital Gain:</strong>
              <br />${report.summary.net_capital_gain.toFixed(2)}
            </div>
            <div className="col-md-3">
              <strong>Total Events:</strong>
              <br />{report.summary.total_events}
            </div>
          </div>
        </div>
      </div>

      {/* Export Buttons */}
      <div className="mb-3">
        <button className="btn btn-success me-2" onClick={handleExportCSV}>
          Export CSV
        </button>
        <button className="btn btn-danger" onClick={handleExportPDF}>
          Export PDF
        </button>
      </div>

      {/* Events Table */}
      <TaxReportTable events={report.events} />
    </div>
  );
};
```

### **2. Complete Portfolio Service**

**Priority: MEDIUM**

Location: `backend_fastapi/app/services/portfolio_service.py`

Create a service similar to the Django `investment_details.py` that calculates:
- Total units held
- Total cost
- Current value
- Profit/loss
- Portfolio history for charting

### **3. Price Update Service**

**Priority: MEDIUM**

Port the web scraping logic from Django to FastAPI:
- Location: `backend_fastapi/app/services/scraper_service.py`
- Use `httpx` for async requests
- Update investment prices
- Update history data

### **4. Scheduled Tasks**

**Priority: LOW**

Location: `backend_fastapi/app/tasks/price_updater.py`

Use APScheduler to schedule daily price updates.

### **5. Create Initial Alembic Migration**

```bash
cd buffetiser/backend_fastapi
alembic revision --autogenerate -m "Initial migration"
```

---

## 🚀 Getting Started

### **1. Start the New Stack**

```bash
cd buffetiser
docker-compose -f docker-compose-new.yaml up --build
```

Services:
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs
- **Frontend**: http://localhost:3000 (once created)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### **2. Create Initial Migration**

```bash
docker exec -it buffetiser_backend_fastapi alembic revision --autogenerate -m "Initial migration"
docker exec -it buffetiser_backend_fastapi alembic upgrade head
```

### **3. Test the API**

Visit: http://localhost:8000/api/v1/docs

Try:
1. Create an investment
2. Record a purchase (creates tax parcel automatically)
3. Record a sale (calculates CGT)
4. Get tax report for current FY
5. Export to PDF/CSV

---

## 📝 Key Differences from Django Version

### **Improvements**

1. **Tax Parcel Tracking**: Individual parcels with specific identification
2. **Parcel Selection**: Choose which parcels to sell for tax optimization
3. **Australian CGT**: Proper 50% discount calculation
4. **Financial Year**: Correct FY handling (July-June)
5. **Type Safety**: Pydantic schemas throughout
6. **Async**: True async/await for better performance
7. **Modern Stack**: Latest FastAPI, SQLAlchemy 2.0, React 18, TypeScript

### **What's the Same**

1. Investment tracking (shares & crypto)
2. Purchase/sale recording
3. Dividend tracking
4. Price history
5. Portfolio totals

---

## 🎯 Next Steps

1. ✅ Complete frontend TypeScript conversion
2. ✅ Build tax report UI
3. ✅ Port portfolio calculation service
4. ✅ Port price scraping service
5. ✅ Test thoroughly with real data
6. ✅ Update README with new features
7. ✅ Deploy!

---

## 💡 Tips

### **Testing Tax Calculations**

Create test data:
```python
# Via API or Python shell
# 1. Create investment
# 2. Purchase 100 units on Jan 1, 2023 @ $10
# 3. Purchase 50 units on July 1, 2023 @ $12
# 4. Sell 75 units on Feb 1, 2024 @ $15
# Expected: FIFO = 75 units from first purchase
# Held: 13 months = Long-term = 50% discount applies
```

### **Parcel Selection UI**

When selling, show available parcels with:
- Acquisition date
- Units available
- Cost base
- Potential CGT impact
- Recommendation (e.g., "Sell newer parcels to maximize discount")

---

## 📚 Documentation

- **FastAPI Docs**: http://localhost:8000/api/v1/docs
- **Australian CGT**: https://www.ato.gov.au/individuals/capital-gains-tax
- **Financial Year**: July 1 - June 30
- **CGT Discount**: 50% for assets held >= 12 months

---

**Questions?** Check the code comments or FastAPI auto-generated docs!
