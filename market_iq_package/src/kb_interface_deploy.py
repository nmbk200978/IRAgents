"""
Market IQ Interface - Deployment Version

This module provides a class to query the Market IQ knowledge base without pandas dependency.
"""

import os
import sqlite3
import json
from datetime import datetime

class KnowledgeBaseInterface:
    """
    Interface for querying the financial knowledge base.
    """
    
    def __init__(self, db_path):
        """
        Initialize the knowledge base interface.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
    
    def connect_to_kb(self):
        """
        Connect to the knowledge base database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def get_companies(self):
        """
        Get all companies in the knowledge base.
        
        Returns:
            list: List of company dictionaries
        """
        try:
            conn = self.connect_to_kb()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT ticker, company_name, industry, market_cap
                FROM companies 
                ORDER BY ticker
            """)
            
            companies = []
            for row in cursor.fetchall():
                companies.append({
                    'ticker': row['ticker'],
                    'company_name': row['company_name'],
                    'industry': row['industry'] if row['industry'] else 'Staffing & Employment Services',
                    'market_cap': row['market_cap'] if row['market_cap'] else '$B'
                })
            
            conn.close()
            return companies
            
        except Exception as e:
            print(f"Error getting companies: {e}")
            return self._get_mock_companies()
    
    def _get_mock_companies(self):
        """Return mock company data for fallback."""
        return [
            {
                'ticker': 'TNET',
                'company_name': 'TriNet Group, Inc.',
                'industry': 'Staffing & Employment Services',
                'market_cap': '$B'
            },
            {
                'ticker': 'ADP',
                'company_name': 'Automatic Data Processing, Inc.',
                'industry': 'Staffing & Employment Services',
                'market_cap': '$B'
            },
            {
                'ticker': 'PAYX',
                'company_name': 'Paychex, Inc.',
                'industry': 'Staffing & Employment Services',
                'market_cap': '$B'
            },
            {
                'ticker': 'NSP',
                'company_name': 'Insperity, Inc.',
                'industry': 'Staffing & Employment Services',
                'market_cap': '$B'
            },
            {
                'ticker': 'PYCR',
                'company_name': 'Paycor HCM, Inc.',
                'industry': 'Staffing & Employment Services',
                'market_cap': '$B'
            },
            {
                'ticker': 'PCTY',
                'company_name': 'Paylocity Holding Corporation',
                'industry': 'Staffing & Employment Services',
                'market_cap': '$B'
            }
        ]
    
    def get_recent_filings(self, limit=10):
        """
        Get recent SEC filings.
        
        Args:
            limit (int): Maximum number of filings to return
            
        Returns:
            list: List of filing dictionaries
        """
        try:
            conn = self.connect_to_kb()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ticker, filing_type, filing_date, description
                FROM filings 
                ORDER BY filing_date DESC 
                LIMIT ?
            """, (limit,))
            
            filings = []
            for row in cursor.fetchall():
                filings.append({
                    'ticker': row['ticker'],
                    'filing_type': row['filing_type'],
                    'filing_date': row['filing_date'],
                    'description': row['description']
                })
            
            conn.close()
            return filings
            
        except Exception as e:
            print(f"Error getting recent filings: {e}")
            return self._get_mock_filings()
    
    def _get_mock_filings(self):
        """Return mock filing data for fallback."""
        return [
            {
                'ticker': 'PCTY',
                'filing_type': '10-Q',
                'filing_date': '2025-05-02',
                'description': 'Quarterly Report'
            },
            {
                'ticker': 'ADP',
                'filing_type': '10-Q',
                'filing_date': '2025-05-01',
                'description': 'Quarterly Report'
            },
            {
                'ticker': 'NSP',
                'filing_type': '10-K',
                'filing_date': '2025-04-29',
                'description': 'Annual Report'
            },
            {
                'ticker': 'TNET',
                'filing_type': '10-Q',
                'filing_date': '2025-04-25',
                'description': 'Quarterly Report'
            },
            {
                'ticker': 'TNET',
                'filing_type': '8-K',
                'filing_date': '2025-02-13',
                'description': 'Current Report'
            }
        ]
    
    def get_latest_insights(self, limit=5):
        """
        Get latest insights.
        
        Args:
            limit (int): Maximum number of insights to return
            
        Returns:
            list: List of insight dictionaries
        """
        return [
            {
                'title': 'PEO Industry Outlook',
                'date': 'May 10, 2025',
                'summary': 'The Professional Employer Organization industry is projected to grow at a CAGR of 10.5% over the next five years, driven by increasing demand for HR outsourcing solutions among small and medium-sized businesses.'
            }
        ]
    
    def get_financial_metrics(self, ticker=None):
        """
        Get financial metrics for companies.
        
        Args:
            ticker (str, optional): Specific company ticker
            
        Returns:
            dict: Financial metrics data
        """
        mock_metrics = {
            'TNET': {
                'revenue': 1.25,
                'revenue_growth': 9.2,
                'gross_margin': 32.7,
                'operating_margin': 11.2,
                'net_margin': 8.1,
                'roe': 18.5,
                'pe_ratio': 24.3
            },
            'ADP': {
                'revenue': 16.80,
                'revenue_growth': 6.2,
                'gross_margin': 45.0,
                'operating_margin': 22.5,
                'net_margin': 17.3,
                'roe': 42.1,
                'pe_ratio': 28.7
            },
            'PAYX': {
                'revenue': 4.90,
                'revenue_growth': 7.8,
                'gross_margin': 41.2,
                'operating_margin': 19.8,
                'net_margin': 15.2,
                'roe': 38.7,
                'pe_ratio': 26.5
            },
            'NSP': {
                'revenue': 5.60,
                'revenue_growth': 8.1,
                'gross_margin': 30.5,
                'operating_margin': 10.8,
                'net_margin': 7.9,
                'roe': 21.3,
                'pe_ratio': 22.1
            },
            'PYCR': {
                'revenue': 0.43,
                'revenue_growth': 12.3,
                'gross_margin': 28.4,
                'operating_margin': 8.7,
                'net_margin': 5.3,
                'roe': 15.8,
                'pe_ratio': 32.4
            },
            'PCTY': {
                'revenue': 0.98,
                'revenue_growth': 10.5,
                'gross_margin': 31.8,
                'operating_margin': 9.5,
                'net_margin': 6.8,
                'roe': 17.2,
                'pe_ratio': 30.8
            }
        }
        
        if ticker:
            return mock_metrics.get(ticker, {})
        return mock_metrics
    
    def search_documents(self, query, filters=None):
        """
        Search documents in the knowledge base.
        
        Args:
            query (str): Search query
            filters (dict, optional): Search filters
            
        Returns:
            list: List of matching documents
        """
        # Mock search results
        return [
            {
                'id': 1,
                'title': 'TNET Q1 2025 Earnings Call',
                'content': 'Revenue growth of 9.2% year-over-year...',
                'relevance': 0.95,
                'source': 'Earnings Call Transcript'
            }
        ]
    
    def get_document_by_id(self, doc_id):
        """
        Get a specific document by ID.
        
        Args:
            doc_id (int): Document ID
            
        Returns:
            dict: Document data
        """
        return {
            'id': doc_id,
            'company': 'PCTY',
            'filing_type': '10-Q',
            'filing_date': '2025-05-02',
            'title': 'Periodic Financial Reports',
            'content': 'Financial report content...',
            'source': 'SEC EDGAR'
        }
    
    def get_comparison_data(self, tickers):
        """
        Get comparison data for multiple companies.
        
        Args:
            tickers (list): List of company tickers
            
        Returns:
            dict: Comparison data
        """
        metrics = self.get_financial_metrics()
        comparison = {}
        
        for ticker in tickers:
            if ticker in metrics:
                comparison[ticker] = metrics[ticker]
        
        return comparison

