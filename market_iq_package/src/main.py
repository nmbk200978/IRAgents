"""
Updated main.py with NLP/NLX search integration for the Market IQ web application - Deployment Version.
"""

import sys
import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for

from src.kb_interface import KnowledgeBaseInterface
from src.nlp_integration import get_nlp_integration

# Configure application
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize knowledge base interface
db_path = os.path.join(os.path.dirname(__file__), 'financial_kb.db')
kb_interface = KnowledgeBaseInterface(db_path)

# Initialize NLP search integration
nlp_integration = get_nlp_integration(db_path)

@app.route('/')
def index():
    """Render the modern home page."""
    companies = kb_interface.get_companies()
    recent_filings = kb_interface.get_recent_filings(limit=5)
    insights = kb_interface.get_latest_insights(limit=5)
    suggested_prompts = nlp_integration.get_suggested_prompts()
    
    return render_template('modern_index.html', 
                         companies=companies,
                         recent_filings=recent_filings,
                         insights=insights,
                         suggested_prompts=suggested_prompts,
                         title="Market IQ | TNET & Competitors")

@app.route('/search')
def search():
    """Render the search page with results."""
    query = request.args.get('query', '')
    
    if query:
        # Process the search query using NLP integration
        search_results = nlp_integration.process_search_query(query)
        
        return render_template('modern_search.html',
                             query=query,
                             search_results=search_results,
                             title="Search | Financial Knowledge Base")
    else:
        return render_template('modern_search.html',
                             query='',
                             search_results=None,
                             title="Search | Financial Knowledge Base")

@app.route('/metrics')
def metrics():
    """Render the metrics page."""
    companies = kb_interface.get_companies()
    financial_metrics = kb_interface.get_financial_metrics()
    
    return render_template('modern_metrics.html',
                         companies=companies,
                         financial_metrics=financial_metrics,
                         title="Metrics | Market IQ")

@app.route('/compare')
def compare():
    """Render the company comparison page."""
    companies = kb_interface.get_companies()
    
    return render_template('modern_compare.html',
                         companies=companies,
                         title="Compare | Financial Knowledge Base")

@app.route('/insights')
def insights():
    """Render the insights page."""
    companies = kb_interface.get_companies()
    
    return render_template('modern_insights.html',
                         companies=companies,
                         title="Insights | Financial Knowledge Base")

@app.route('/filings')
def filings():
    """Render the SEC filings page."""
    companies = kb_interface.get_companies()
    recent_filings = kb_interface.get_recent_filings(limit=10)
    
    return render_template('modern_filings.html',
                         companies=companies,
                         filings=recent_filings,
                         title="SEC Filings | Financial Knowledge Base")

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page."""
    companies = kb_interface.get_companies()
    financial_metrics = kb_interface.get_financial_metrics()
    
    # Get TNET specific metrics for dashboard
    tnet_metrics = financial_metrics.get('TNET', {})
    
    return render_template('modern_dashboard.html',
                         companies=companies,
                         financial_metrics=financial_metrics,
                         tnet_metrics=tnet_metrics,
                         title="Dashboard | Market IQ")

@app.route('/document/<int:doc_id>')
def document_detail(doc_id):
    """Render document detail page."""
    document = kb_interface.get_document_by_id(doc_id)
    recent_filings = kb_interface.get_recent_filings(limit=5)
    
    return render_template('modern_document_detail.html',
                         document=document,
                         recent_filings=recent_filings,
                         title="Document Detail | Financial Knowledge Base")

# API Routes
@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for search queries."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        filters = data.get('filters', {})
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = nlp_integration.process_search_query(query, filters)
        return jsonify(results)
        
    except Exception as e:
        app.logger.error(f"Error in api_search: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def api_metrics():
    """API endpoint for financial metrics."""
    try:
        ticker = request.args.get('ticker')
        metrics = kb_interface.get_financial_metrics(ticker)
        return jsonify({'metrics': metrics})
        
    except Exception as e:
        app.logger.error(f"Error in api_metrics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def api_comparison():
    """API endpoint for company comparison."""
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        
        if not tickers:
            return jsonify({'error': 'At least one ticker is required'}), 400
        
        comparison_data = kb_interface.get_comparison_data(tickers)
        return jsonify({'comparison': comparison_data})
        
    except Exception as e:
        app.logger.error(f"Error in api_comparison: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors with a custom error page."""
    return render_template('error.html', 
                         error="The page you requested could not be found.", 
                         title="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors with a custom error page."""
    return render_template('error.html', 
                         error="An internal server error occurred. Please try again later.", 
                         title="Server Error"), 500

if __name__ == '__main__':
    # Ensure the application is accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)

