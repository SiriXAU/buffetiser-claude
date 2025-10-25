# Buffetiser Frontend (TypeScript)

React + TypeScript frontend for Buffetiser with Australian CGT tax tracking.

## Features

- ✅ **Tax Report Page**: Sortable CGT events table
- ✅ **Tax Summary**: Financial year summary with breakdown
- ✅ **Export Functionality**: CSV and PDF exports
- ✅ **Parcel Selection**: Choose specific parcels for tax-optimized sales
- ✅ **Type Safety**: Full TypeScript coverage
- ✅ **Modern UI**: Bootstrap 5 with custom styling

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at http://localhost:3000

### Environment Variables

Create a `.env` file:

```
REACT_APP_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── components/
│   ├── TaxReport/
│   │   ├── TaxReportTable.tsx       # Sortable tax events table
│   │   └── TaxSummaryCard.tsx       # Summary with metrics
│   └── Modals/
│       └── ParcelSelectionModal.tsx # Parcel selection for sales
├── pages/
│   └── TaxReportPage.tsx            # Main tax report page
├── types/
│   ├── investment.ts                # Investment types
│   ├── transaction.ts               # Transaction types
│   ├── tax.ts                       # Tax types
│   └── index.ts                     # Type exports
├── api/
│   └── client.ts                    # Typed API client
├── App.tsx                          # Main app with routing
└── index.tsx                        # Entry point
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/api/v1`.

All API calls are fully typed using TypeScript interfaces.

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Key Components

### TaxReportPage

Main page for viewing CGT reports with:
- Financial year selection
- Export to CSV/PDF
- Summary metrics
- Detailed events table

### TaxReportTable

Sortable table showing:
- Disposal date
- Investment symbol
- Units sold
- Holding period
- Cost base & proceeds
- Capital gains (gross & net)
- CGT discount status

### ParcelSelectionModal

Modal for selecting which parcels to sell:
- View all available parcels
- See tax treatment (short/long-term)
- Auto-select FIFO or optimized
- Manual selection for tax optimization

## Docker

Run with Docker:

```bash
docker build -t buffetiser-frontend .
docker run -p 3000:3000 buffetiser-frontend
```

## Next Steps

TODO:
- [ ] Complete Dashboard page
- [ ] Add Investments page with CRUD
- [ ] Convert remaining components from old frontend
- [ ] Add charts for portfolio performance
- [ ] Add authentication

## License

MIT
