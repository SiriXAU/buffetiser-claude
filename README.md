# 📈 Buffetiser

> **Your Personal Investment Portfolio Tracker & Visualizer with Australian CGT Tax Tracking**

Buffetiser is a powerful, full-stack web application designed to help you organize, track, and visualize your investment portfolio with ease. Named as a nod to Warren Buffett, this tool brings professional-grade portfolio management to your fingertips! 💼

## 🆕 **Version 2.0 - Now with Australian CGT Tax Tracking!**

**New in v2.0:**
- 🇦🇺 **Australian Capital Gains Tax (CGT) Calculator** with 50% discount for long-term holdings
- 📊 **Tax Parcel Tracking** - Track individual parcels for each purchase
- 🎯 **Parcel Selection** - Choose which parcels to sell for tax optimization
- 📅 **Financial Year Reports** - Automatic FY reports (July 1 - June 30)
- 📄 **Export to PDF & CSV** - Professional tax reports ready for your accountant
- ⚡ **FastAPI Backend** - Modern, async Python backend with SQLAlchemy 2.0
- 📘 **TypeScript Frontend** - Type-safe React application with full type coverage

![Portfolio Dashboard](https://github.com/user-attachments/assets/c747eb11-02e9-44ca-91fa-0dcdfa8b2320)

---

## 🌟 Features

### 🇦🇺 **Australian CGT Tax Tracking** (NEW in v2.0)
- **Tax Parcel System**: Each purchase creates an individual tax parcel with acquisition date and cost base
- **Parcel Selection**: Choose which specific parcels to sell for maximum tax efficiency
- **FIFO Support**: Automatic first-in-first-out allocation if you prefer simplicity
- **50% CGT Discount**: Automatic calculation for assets held 12+ months
- **Financial Year Reports**: Complete FY reports from July 1 to June 30
- **Sortable Tax Events Table**: View all CGT events with sorting by date, gain, holding period, etc.
- **Tax Summary Dashboard**: See total gains, discounts applied, and net assessable gain
- **Export to PDF**: Professional formatted tax report ready for your accountant
- **Export to CSV**: Import into Excel or your tax software
- **Holding Period Tracking**: Visual indicators for short-term vs long-term holdings
- **Optimization Recommendations**: Auto-select features to minimize tax liability

### 📊 **Investment Tracking**
- **Multi-Asset Support**: Track both shares/stocks and cryptocurrencies in one unified platform
- **Real-Time Price Updates**: Automatic price updates with configurable scheduling
- **Historical Data**: Complete price history with daily high, low, close, and volume data
- **Transaction Management**: Record purchases, sales, dividend reinvestments, and dividend payments

### 💰 **Portfolio Analytics**
- **Interactive Charts**: Beautiful visualizations powered by Recharts
- **Individual Investment Cards**: Each investment displayed in its own tab with live price variations
- **Portfolio Totals**: Comprehensive overview of your entire portfolio performance
- **Profit/Loss Tracking**: Real-time calculation of gains and losses
- **Fee Tracking**: Keep track of all transaction fees to understand true costs
- **Average Cost Basis**: Automatic calculation of your average purchase price

### 🌍 **Multi-Exchange & Multi-Platform Support**
- **Global Exchanges**: Support for 20+ major stock exchanges worldwide including:
  - 🇦🇺 ASX (Australian Securities Exchange)
  - 🇺🇸 NASDAQ & NYSE (US Markets)
  - 🇬🇧 LSE (London Stock Exchange)
  - 🇯🇵 JPX (Japan Exchange)
  - 🇭🇰 HKEX (Hong Kong Exchange)
  - And many more!

- **Multiple Trading Platforms**: CMC, LINK, Boardroom, Direct trading, IPO purchases

### 📈 **Advanced Features**
- **Dividend Management**: Track both reinvested and paid-out dividends
- **Daily Change Indicators**: Real-time daily price changes and percentages
- **Custom Reports**: Generate detailed transaction reports
- **Database Backup/Restore**: Built-in backup and restore functionality
- **Configurable Updates**: Set your preferred update time and timezone
- **Redis Caching**: Fast performance with intelligent caching

---

## 🛠️ Technology Stack

### **Version 2.0 (Current - With Tax Features)**

#### **Backend (FastAPI)**
- ⚡ **FastAPI** - Modern, async Python web framework
- 🗄️ **SQLAlchemy 2.0** - Async ORM with type hints
- 🔄 **Alembic** - Database migrations
- 📋 **Pydantic V2** - Data validation and serialization
- 🐘 **PostgreSQL 17** - Database
- 🔴 **Redis 7** - Caching with FastAPI-Cache2
- 🇦🇺 **Australian CGT Calculator** - Custom tax calculation service
- 📄 **ReportLab** - PDF generation
- 📊 **Pandas** - CSV export and data processing
- 🌐 **HTTPX** - Async HTTP client
- 📅 **APScheduler** - Task scheduling
- 🐳 **Docker** - Containerization

#### **Frontend (TypeScript)**
- ⚛️ **React 18** - Modern React with hooks
- 📘 **TypeScript 5** - Full type safety
- 🎯 **TanStack Table** - Sortable tables for tax reports
- 🎨 **Bootstrap 5** & **React Bootstrap** - UI components
- 📊 **Recharts** - Data visualization
- 🔄 **React Router 6** - Navigation
- 🌐 **Axios** - Typed API communication
- 💾 **file-saver** - File downloads (CSV/PDF)
- 📅 **date-fns** - Date handling
- 🐳 **Docker** - Containerization

### **Version 1.0 (Legacy - Django)**

#### **Backend (Django)**
- 🐍 **Python** with **Django** framework
- 🔥 **Django REST Framework** (DRF)
- 🔐 **Django REST Framework Simple JWT**
- 🐘 **PostgreSQL 17**
- 🔴 **Redis 7**
- 🌐 **NGINX** as reverse proxy
- 🐳 **Docker & Docker Compose**

#### **Frontend (JavaScript)**
- ⚛️ **React 18**
- 🎨 **Bootstrap 5**
- 📊 **Recharts**
- 🔄 **React Router DOM**
- 🌐 **Axios**

**Note**: The Django/JS version is in `buffetiser/backend` and `buffetiser/frontend`. The new FastAPI/TS version is in `buffetiser/backend_fastapi` and `buffetiser/frontend_ts`.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- 🐳 **Docker** (version 20.10 or higher)
- 🐳 **Docker Compose** (version 2.0 or higher)
- 💻 At least 2GB of free RAM
- 🌐 Internet connection for initial image pulls

---

## 🚀 Quick Start

### **Version 2.0 (FastAPI + TypeScript with Tax Features)** ⭐ RECOMMENDED

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SiriXAU/buffetiser-claude.git
cd buffetiser-claude/buffetiser
```

#### 2️⃣ Start the Application
```bash
docker-compose -f docker-compose-new.yaml up --build
```

#### 3️⃣ Access the Application
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/v1/docs (Interactive!)
- **Tax Report**: http://localhost:3000/tax-report
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

#### 4️⃣ Create Initial Migration
```bash
docker exec -it buffetiser_backend_fastapi alembic upgrade head
```

#### 5️⃣ Try the Tax Features!
1. Visit http://localhost:8000/api/v1/docs
2. Create an investment
3. Record purchases (creates tax parcels automatically)
4. Record a sale (with parcel selection!)
5. View your tax report at http://localhost:3000/tax-report
6. Export to PDF or CSV

---

### **Version 1.0 (Django + JavaScript - Legacy)**

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SiriXAU/buffetiser-claude.git
cd buffetiser-claude/buffetiser
```

#### 2️⃣ Build and Start
```bash
docker-compose up --build
```

This will:
- 🐘 Start PostgreSQL database
- 🔴 Start Redis cache
- 🐍 Build and start Django backend
- ⚛️ Build React frontend
- 🌐 Start NGINX web server

### 4️⃣ Access the Application
Once all services are running, access Buffetiser at:
- **Frontend**: http://localhost:81
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

---

## 📖 Detailed Setup Guide

### **First Time Setup**

#### Create a Superuser
To access the Django admin panel:
```bash
docker exec -it buffetiser_backend python manage.py createsuperuser
```

Follow the prompts to create your admin account.

#### Load Sample Data (Optional)
The application comes with fixture data for testing:
```bash
docker exec -it buffetiser_backend python manage.py loaddata --exclude=auth.permission --exclude=contenttypes fixtures/buffetiser_25-06-06_data.json
```

---

## 🎯 Usage Guide

### **Adding Your First Investment**

1. 📝 **Create New Investment**:
   - Click the "New Investment" button
   - Enter the stock symbol (e.g., "AAPL" for Apple)
   - Select the exchange (e.g., NASDAQ)
   - Choose investment type (Shares or Crypto)

2. 💵 **Record a Purchase**:
   - Click on the investment card
   - Select "Add Purchase"
   - Enter:
     - Number of units/shares
     - Price per unit
     - Transaction fee
     - Purchase date
     - Platform used

3. 📈 **View Performance**:
   - Click on the investment header to expand
   - View detailed charts showing:
     - Historical price movements
     - Your cost basis
     - Current profit/loss
     - Total returns

### **Managing Dividends**

#### Dividend Reinvestment
For dividends that were used to purchase more shares:
```
Menu → Add Reinvestment → Fill in details
```

#### Dividend Payments
For cash dividend payments:
```
Menu → Add Dividend Payment → Enter payment details
```

### **Recording Sales**
When you sell shares:
1. Navigate to the investment
2. Click "Record Sale"
3. Enter sale details (units, price, fee, date)
4. The app automatically updates your holdings and profit/loss

### **Generating Reports**
Access comprehensive transaction reports:
```
Menu → Reports → View all transactions by type
```

Reports include:
- 📊 All purchases with dates and prices
- 💰 All sales and realized gains
- 🎁 Dividend history
- 📈 Reinvestment records

---

## 🏗️ Architecture

### **Service Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    NGINX (Port 81)                      │
│              Reverse Proxy & Static Files               │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌────────▼────────┐
│  React Frontend│      │ Django Backend   │
│   (Port 8080)  │◄────►│   (Port 8000)   │
└────────────────┘      └────────┬────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
          ┌─────────▼────────┐    ┌──────────▼─────────┐
          │  PostgreSQL 17   │    │    Redis 7         │
          │   (Port 5433)    │    │  (Port 6379)       │
          └──────────────────┘    └────────────────────┘
```

### **Data Models**

#### Investment
Core model representing a stock or cryptocurrency:
- Unique key (exchange-symbol)
- Name and symbol
- Type (Shares/Crypto)
- Live price
- Calculated properties:
  - Total units held
  - Total cost (including fees)
  - Average cost per unit
  - Current value
  - Total profit/loss

#### Purchase
Records individual buy transactions:
- Investment reference
- Units purchased
- Price per unit
- Transaction fee
- Date and trade count
- Exchange and platform

#### Sale
Records sell transactions:
- Investment reference
- Units sold
- Sale price per unit
- Transaction fee
- Date and trade count

#### DividendReinvestment
Tracks dividends used to buy more shares:
- Investment reference
- Units acquired
- Price per unit
- Reinvestment date

#### DividendPayment
Tracks cash dividend payments:
- Investment reference
- Payment amount
- Payment date

#### History
Daily price records:
- Date
- High, Low, Close prices
- Trading volume

---

## 🔧 Configuration

### **Update Schedule Configuration**
Configure when the app updates prices:

1. Access the config modal in the UI
2. Set your preferred update time
3. Select your timezone
4. Save configuration

Default: 3:00 PM Australia/Perth time

### **Manual Updates**
Trigger manual price updates:
```bash
# Update daily changes
curl http://localhost:8000/api/update_daily/

# Update all investment data
curl http://localhost:8000/api/update_all/
```

---

## 🗄️ Database Operations

### **Backup Database**
Create a backup of your portfolio data:
```bash
# From inside the Django container
python manage.py dumpdata buffetiser --indent 2 > buffetiser_backup.json
```

Or use the built-in backup API:
```bash
curl http://localhost:8000/api/backup_db/
```

### **Restore Database**
Restore from a backup:
```bash
# From inside the Django container
python manage.py loaddata buffetiser_backup.json
```

Or via API:
```bash
curl http://localhost:8000/api/restore_db/path/to/backup.json
```

### **Direct PostgreSQL Backup**
```bash
# Backup
docker exec buffetiser_db pg_dump -U buffetiser BUFFETISER_DB > backup.sql

# Restore
docker cp backup.sql buffetiser_db:/backup.sql
docker exec -it buffetiser_db psql -U buffetiser -d BUFFETISER_DB -f /backup.sql
```

---

## 🔌 API Endpoints

### **Investment Endpoints**
```
GET    /api/investments/              # List all investments
GET    /api/investments/{id}/         # Get specific investment
POST   /api/investments/              # Create new investment
PUT    /api/investments/{id}/         # Update investment
DELETE /api/investments/{id}/         # Delete investment
GET    /api/all/                      # Get all investment data with details
GET    /api/portfolio/                # Get portfolio totals
```

### **Transaction Endpoints**
```
POST   /api/new_investment/           # Create new investment with initial data
POST   /api/purchase/                 # Record a purchase
POST   /api/sale/                     # Record a sale
POST   /api/add_reinvestment/         # Add dividend reinvestment
POST   /api/add_dividend_payment/     # Add dividend payment
DELETE /api/remove/                   # Remove an investment
```

### **Data & Reports**
```
GET    /api/reports/                  # Get transaction reports
GET    /api/constants/                # Get all constant values (exchanges, platforms, etc.)
GET    /api/config/                   # Get/Set configuration
POST   /api/config/                   # Update configuration
```

### **Updates**
```
POST   /api/update_daily/             # Update daily changes
POST   /api/update_all/               # Update all investments
```

### **Maintenance**
```
GET    /api/backup_db/                # Backup database
GET    /api/restore_db/{path}/        # Restore database
GET    /api/cron_time/                # Get scheduled update time
```

---

## 🧪 Development

### **Running in Development Mode**

#### Backend Development
```bash
cd buffetiser/backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Frontend Development
```bash
cd buffetiser/frontend

# Install dependencies
npm install

# Start development server
npm start
```

The development server will run at http://localhost:3000

### **Running Tests**

#### Backend Tests
```bash
docker exec -it buffetiser_backend python manage.py test
```

#### Frontend Tests
```bash
docker exec -it buffetiser_frontend npm test
```

---

## 📁 Project Structure

```
buffetiser-claude/
├── buffetiser/
│   ├── backend/
│   │   ├── buffetiser_api/         # Django project settings
│   │   ├── core/                   # Main application
│   │   │   ├── models.py           # Data models
│   │   │   ├── views.py            # API views
│   │   │   ├── serializers.py      # DRF serializers
│   │   │   ├── urls.py             # URL routing
│   │   │   ├── config.py           # Constants & enums
│   │   │   ├── services/           # Business logic
│   │   │   └── management/         # Custom Django commands
│   │   ├── fixtures/               # Sample data
│   │   ├── staticfiles/            # Static files
│   │   ├── Dockerfile              # Backend container config
│   │   ├── manage.py               # Django management script
│   │   ├── requirements.txt        # Python dependencies
│   │   └── wait-for-it.sh          # Service startup script
│   │
│   ├── frontend/
│   │   ├── public/                 # Public assets
│   │   ├── src/
│   │   │   ├── components/         # React components
│   │   │   │   ├── dashboard.js    # Main dashboard
│   │   │   │   ├── investment_cards/ # Investment displays
│   │   │   │   ├── menu/           # Menu & modals
│   │   │   │   ├── totals_card.js  # Portfolio totals
│   │   │   │   └── totals_chart.js # Portfolio chart
│   │   │   ├── context/            # React context (Auth)
│   │   │   ├── assets/             # Images & logos
│   │   │   ├── App.js              # Main app component
│   │   │   └── index.js            # Entry point
│   │   ├── Dockerfile              # Frontend container config
│   │   └── package.json            # NPM dependencies
│   │
│   ├── nginx/                      # NGINX configuration
│   ├── docs/                       # Documentation
│   └── docker-compose.yaml         # Multi-container orchestration
│
├── stuff/                          # Additional resources
└── README.md                       # This file! 📖
```

---

## 🐛 Troubleshooting

### **Common Issues**

#### Port Already in Use
If you get port conflicts:
```bash
# Change ports in docker-compose.yaml
# For example, change "81:80" to "8081:80"
```

#### Database Connection Issues
```bash
# Restart the database service
docker-compose restart db

# Check database logs
docker logs buffetiser_db
```

#### Frontend Build Failures
```bash
# Clear npm cache
docker exec -it buffetiser_frontend npm cache clean --force

# Rebuild
docker-compose up --build frontend
```

#### Migration Issues
```bash
# Reset migrations (⚠️ This will delete data!)
docker exec -it buffetiser_backend python manage.py migrate --fake core zero
docker exec -it buffetiser_backend python manage.py migrate core
```

### **Viewing Logs**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 backend
```

---

## 🔒 Security Considerations

### **Production Deployment**

Before deploying to production:

1. 🔐 **Change Default Passwords**:
   - Update PostgreSQL password
   - Generate strong Django SECRET_KEY

2. 🛡️ **HTTPS Setup**:
   - Configure SSL certificates
   - Update NGINX configuration for HTTPS

3. 🚫 **Disable Debug Mode**:
   ```
   DJANGO_DEBUG=False
   ```

4. 🌐 **CORS Configuration**:
   - Restrict allowed origins in Django settings
   - Update CORS headers in NGINX

5. 🔒 **Authentication**:
   - Enable JWT authentication (currently commented out)
   - Implement proper user management

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 Open a Pull Request

### **Development Guidelines**
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write tests for new features
- Update documentation as needed

---

## 📜 License

This project is open source and available for personal use.

---

## 🙏 Acknowledgments

- 💡 Inspired by Warren Buffett's investment philosophy
- 📊 Built with amazing open-source technologies
- 🌟 Special thanks to all contributors

---

## 📞 Support

Having issues or questions?

- 📝 Open an issue on GitHub
- 📧 Contact: dodgydesigns@gmail.com
- 📖 Check the `/docs` folder for additional documentation

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] 📱 Mobile app (React Native)
- [ ] 🔔 Price alerts and notifications
- [ ] 📊 More chart types and analytics
- [ ] 🌍 Support for more exchanges
- [ ] 🤖 Automated portfolio rebalancing suggestions
- [ ] 📈 Technical indicators (RSI, MACD, etc.)
- [ ] 💱 Multi-currency support with conversion
- [ ] 📁 Export to Excel/CSV
- [ ] 🔄 Import from broker statements
- [ ] 👥 Multi-user support with separate portfolios

---

## 💖 Support the Project

If you find Buffetiser useful, consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code

---

<div align="center">

**Made with ❤️ for investors, by investors**

*Track Smart. Invest Smarter.* 📈

</div>
