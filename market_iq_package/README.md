# Market IQ - Financial Knowledge Base Application

A comprehensive financial knowledge base web application for analyzing TNET (TriNet Group, Inc.) and its competitors in the Professional Employer Organization (PEO) industry.

## Features

- **Natural Language Search**: AI-powered search with natural language queries
- **Financial Metrics Dashboard**: Comprehensive financial metrics and KPIs
- **Company Comparison**: Side-by-side comparison of financial performance
- **SEC Filings Browser**: Access to SEC filings and documents
- **Interactive Charts**: Revenue comparisons, market share, and trend analysis
- **Insights Engine**: AI-generated insights from financial documents

## Companies Covered

- **TNET** - TriNet Group, Inc.
- **ADP** - Automatic Data Processing, Inc.
- **PAYX** - Paychex, Inc.
- **NSP** - Insperity, Inc.
- **PYCR** - Paycor HCM, Inc.
- **PCTY** - Paylocity Holding Corporation

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed on your system
- At least 2GB of available RAM
- Port 5000 available on your host machine

### Option 1: Using Docker Compose (Recommended)

1. **Extract the package and navigate to the directory:**
   ```bash
   cd market_iq_package
   ```

2. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   Open your browser and go to: `http://localhost:5000`

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker directly

1. **Build the Docker image:**
   ```bash
   docker build -t market-iq .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 market-iq
   ```

3. **Access the application:**
   Open your browser and go to: `http://localhost:5000`

## Manual Installation (Without Docker)

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation Steps

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements_full.txt
   ```

3. **Download NLTK data:**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

4. **Run the application:**
   ```bash
   cd src
   python main.py
   ```

5. **Access the application:**
   Open your browser and go to: `http://localhost:5000`

## Application Structure

```
market_iq_package/
├── src/                          # Application source code
│   ├── main.py                   # Flask application entry point
│   ├── kb_interface.py           # Knowledge base interface
│   ├── nlp_integration.py        # NLP search integration
│   ├── nlp_search.py            # Natural language processing engine
│   ├── financial_kb.db          # SQLite database with financial data
│   ├── static/                  # CSS, JavaScript, and assets
│   │   ├── css/modern/          # Modern UI stylesheets
│   │   └── js/modern/           # JavaScript functionality
│   └── templates/               # HTML templates
│       ├── modern_index.html    # Home page
│       ├── modern_search.html   # Search interface
│       ├── modern_metrics.html  # Metrics dashboard
│       ├── modern_compare.html  # Company comparison
│       ├── modern_insights.html # Insights explorer
│       ├── modern_filings.html  # SEC filings browser
│       └── modern_dashboard.html # Performance dashboard
├── requirements_full.txt        # Complete Python dependencies
├── requirements.txt             # Minimal dependencies (serverless compatible)
├── Dockerfile                   # Docker container configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                    # This file
```

## Usage Guide

### Home Page
- Overview of companies in the knowledge base
- Quick access to search functionality
- Recent filings and industry insights

### Search
- Natural language queries (e.g., "What is TNET's revenue growth?")
- Advanced filtering by company, document type, and date range
- AI-generated answers based on financial documents

### Metrics
- Financial performance metrics for all companies
- Interactive charts and visualizations
- Company-specific metric details

### Compare
- Side-by-side comparison of multiple companies
- Customizable metric selection
- Visual comparison charts

### Insights
- AI-generated insights from financial documents
- Company-specific analysis
- Industry trends and benchmarks

### Filings
- Browse SEC filings (10-K, 10-Q, 8-K, etc.)
- Document details and content
- Direct links to EDGAR database

### Dashboard
- Executive summary of key metrics
- TNET-focused performance indicators
- Industry comparison charts

## API Endpoints

The application provides REST API endpoints for programmatic access:

- `POST /api/search` - Natural language search
- `GET /api/metrics` - Financial metrics data
- `POST /api/compare` - Company comparison data

## Configuration

### Environment Variables

- `FLASK_APP`: Application module (default: `src.main`)
- `FLASK_ENV`: Environment mode (`development` or `production`)
- `PYTHONPATH`: Python path for module imports

### Database

The application uses a SQLite database (`financial_kb.db`) containing:
- Company information and profiles
- Financial metrics and KPIs
- SEC filing metadata
- Document content for search

## Troubleshooting

### Common Issues

1. **Port 5000 already in use:**
   ```bash
   # Change port in docker-compose.yml or use different port
   docker-compose up --build -p 8080:5000
   ```

2. **NLTK data not found:**
   ```bash
   # Download NLTK data manually
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

3. **Permission denied errors:**
   ```bash
   # Ensure proper file permissions
   chmod +x src/main.py
   ```

### Performance Optimization

- For production deployment, consider using a WSGI server like Gunicorn
- Enable caching for better performance with large datasets
- Use a production database (PostgreSQL/MySQL) for better scalability

## Development

### File Versions

The package includes two versions of key files:

- **Standard version** (`main.py`, `kb_interface.py`, etc.): Full functionality with pandas/numpy
- **Deploy version** (`*_deploy.py`): Serverless-compatible without native dependencies

### Adding New Features

1. Modify the appropriate Python files in the `src/` directory
2. Update templates in `src/templates/` for UI changes
3. Add new CSS/JS in `src/static/` for styling and functionality
4. Test locally before deployment

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure Docker/Python versions meet requirements
4. Check application logs for error details

## License

This application is provided as-is for demonstration and educational purposes.

