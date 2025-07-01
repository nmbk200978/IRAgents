"""
NLP/NLX Search Implementation for Market IQ - Deployment Version

This module implements natural language processing capabilities for the Market IQ platform,
allowing users to query financial documents and data using natural language.
"""

import os
import re
import json
import sqlite3
import nltk
from collections import Counter

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class NLPSearchEngine:
    """
    Natural Language Processing search engine for financial documents.
    """
    
    def __init__(self, db_path):
        """
        Initialize the NLP search engine.
        
        Args:
            db_path (str): Path to the SQLite database
        """
        self.db_path = db_path
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Financial keywords and patterns
        self.financial_keywords = {
            'revenue': ['revenue', 'sales', 'income', 'earnings'],
            'growth': ['growth', 'increase', 'expansion', 'rise'],
            'profit': ['profit', 'margin', 'profitability', 'earnings'],
            'comparison': ['compare', 'versus', 'vs', 'against'],
            'performance': ['performance', 'metrics', 'kpi', 'indicators']
        }
    
    def preprocess_query(self, query):
        """
        Preprocess the natural language query.
        
        Args:
            query (str): Raw query string
            
        Returns:
            dict: Processed query components
        """
        # Convert to lowercase and tokenize
        tokens = word_tokenize(query.lower())
        
        # Remove stop words and punctuation
        filtered_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token.isalnum() and token not in self.stop_words
        ]
        
        # Extract company tickers
        tickers = self._extract_tickers(query)
        
        # Identify query intent
        intent = self._identify_intent(filtered_tokens)
        
        # Extract financial concepts
        concepts = self._extract_financial_concepts(filtered_tokens)
        
        return {
            'original_query': query,
            'tokens': filtered_tokens,
            'tickers': tickers,
            'intent': intent,
            'concepts': concepts
        }
    
    def _extract_tickers(self, query):
        """Extract company tickers from the query."""
        known_tickers = ['TNET', 'ADP', 'PAYX', 'NSP', 'PYCR', 'PCTY']
        found_tickers = []
        
        query_upper = query.upper()
        for ticker in known_tickers:
            if ticker in query_upper:
                found_tickers.append(ticker)
        
        return found_tickers
    
    def _identify_intent(self, tokens):
        """Identify the intent of the query."""
        intent_patterns = {
            'comparison': ['compare', 'versus', 'vs', 'against', 'difference'],
            'growth': ['growth', 'increase', 'trend', 'change'],
            'financial_metric': ['revenue', 'profit', 'margin', 'earnings'],
            'general_info': ['what', 'how', 'when', 'where', 'why']
        }
        
        for intent, keywords in intent_patterns.items():
            if any(keyword in tokens for keyword in keywords):
                return intent
        
        return 'general_info'
    
    def _extract_financial_concepts(self, tokens):
        """Extract financial concepts from tokens."""
        concepts = []
        
        for category, keywords in self.financial_keywords.items():
            if any(keyword in tokens for keyword in keywords):
                concepts.append(category)
        
        return concepts
    
    def search(self, query, limit=10):
        """
        Perform natural language search.
        
        Args:
            query (str): Natural language query
            limit (int): Maximum number of results
            
        Returns:
            dict: Search results with AI-generated answer
        """
        processed_query = self.preprocess_query(query)
        
        # Generate AI response based on query analysis
        ai_answer = self._generate_ai_answer(processed_query)
        
        # Get relevant documents (mock for deployment)
        documents = self._get_relevant_documents(processed_query, limit)
        
        return {
            'query': query,
            'ai_answer': ai_answer,
            'documents': documents,
            'processed_query': processed_query
        }
    
    def _generate_ai_answer(self, processed_query):
        """Generate AI answer based on processed query."""
        tickers = processed_query['tickers']
        intent = processed_query['intent']
        concepts = processed_query['concepts']
        
        # Mock financial data
        financial_data = {
            'TNET': {
                'revenue_growth': '9.2%',
                'gross_margin': '32.7%',
                'operating_margin': '11.2%',
                'net_margin': '8.1%'
            },
            'ADP': {
                'revenue_growth': '6.2%',
                'gross_margin': '45.0%',
                'operating_margin': '22.5%',
                'net_margin': '17.3%'
            }
        }
        
        if 'TNET' in tickers and 'revenue' in concepts and 'growth' in concepts:
            return "Based on the latest data, TNET's revenue growth is approximately 9.2% year-over-year."
        
        elif intent == 'comparison' and len(tickers) >= 2:
            if 'TNET' in tickers and 'ADP' in tickers:
                return "Comparing TNET and ADP: TNET has higher revenue growth (9.2% vs 6.2%), while ADP has better profit margins (gross margin: 45.0% vs 32.7%)."
        
        elif 'profit' in concepts or 'margin' in concepts:
            if 'TNET' in tickers:
                return "TNET's profitability metrics show a gross margin of 32.7%, operating margin of 11.2%, and net margin of 8.1%."
        
        # Default response
        return "Based on the available data in the knowledge base, I can provide insights about the companies and metrics you're asking about."
    
    def _get_relevant_documents(self, processed_query, limit):
        """Get relevant documents (mock implementation for deployment)."""
        return [
            {
                'id': 1,
                'title': 'TNET Q1 2025 Earnings Report',
                'content': 'Revenue growth analysis and financial performance...',
                'relevance': 0.95,
                'source': '10-Q Filing'
            },
            {
                'id': 2,
                'title': 'Industry Analysis: PEO Sector',
                'content': 'Comprehensive analysis of the Professional Employer Organization industry...',
                'relevance': 0.87,
                'source': 'Analyst Report'
            }
        ]
    
    def get_suggested_prompts(self):
        """Get suggested search prompts."""
        return [
            "Compare TNET and ADP revenue growth",
            "Show TNET's profit margins over time",
            "Latest earnings call highlights for TNET",
            "Key risks mentioned in TNET's 10-K",
            "Compare employee productivity across competitors",
            "Show industry average metrics",
            "TNET's market position analysis",
            "Competitive advantages of TNET"
        ]

