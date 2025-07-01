# Market IQ - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Extract the Package
```bash
# For ZIP file
unzip market_iq_package.zip
cd market_iq_package

# For TAR.GZ file
tar -xzf market_iq_package.tar.gz
cd market_iq_package
```

### Step 2: Start with Docker (Recommended)
```bash
# Build and start the application
docker-compose up --build

# Wait 1-2 minutes for startup
```

### Step 3: Access the Application
Open your browser and go to: **http://localhost:5000**

## 🎯 What You'll See

- **Home Page**: Overview of companies and financial data
- **Search**: Ask questions like "What is TNET's revenue growth?"
- **Metrics**: Financial performance dashboards
- **Compare**: Side-by-side company comparisons
- **Insights**: AI-generated financial insights
- **Filings**: Browse SEC documents

## 🔧 Alternative Setup (Without Docker)

### Prerequisites
- Python 3.11+
- pip package manager

### Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements_full.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Run the application
cd src
python main.py
```

## 🏢 Companies Included

- **TNET** - TriNet Group, Inc.
- **ADP** - Automatic Data Processing, Inc.
- **PAYX** - Paychex, Inc.
- **NSP** - Insperity, Inc.
- **PYCR** - Paycor HCM, Inc.
- **PCTY** - Paylocity Holding Corporation

## 💡 Try These Sample Queries

- "Compare TNET and ADP revenue growth"
- "Show TNET's profit margins over time"
- "What are the key risks for TNET?"
- "Industry average metrics"
- "Latest earnings highlights"

## 🛑 Stop the Application

```bash
# If using Docker Compose
docker-compose down

# If running Python directly
Ctrl+C in the terminal
```

## 📚 Need More Help?

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md`
- **Features Overview**: See `FEATURES.md`

## ⚡ Performance Tips

- Allow 1-2 minutes for initial startup
- First search may take longer (NLTK data loading)
- Use Chrome/Firefox for best experience
- Ensure port 5000 is available

## 🔍 Troubleshooting

**Port 5000 in use?**
```bash
# Change port in docker-compose.yml
ports:
  - "8080:5000"  # Use port 8080 instead
```

**Application won't start?**
- Check Docker is running
- Verify Python 3.11+ installed
- Ensure sufficient disk space (500MB+)

**Need help?** Check the troubleshooting section in `DEPLOYMENT_GUIDE.md`

---

**Ready to explore financial data? Start with the search page and ask any question about TNET and its competitors!**

