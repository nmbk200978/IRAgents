"""
Integration of NLP/NLX search capabilities into the Market IQ web application - Deployment Version.
This module connects the NLP search engine with the Flask web routes.
"""

import os
from flask import request, jsonify
from nlp_search import NLPSearchEngine

class NLPSearchIntegration:
    """
    Integrates the NLP search engine with the web application.
    Provides methods for handling natural language queries and generating responses.
    """
    
    def __init__(self, db_path):
        """
        Initialize the NLP search integration.
        
        Args:
            db_path (str): Path to the SQLite database
        """
        self.db_path = db_path
        self.search_engine = NLPSearchEngine(db_path)
    
    def process_search_query(self, query, filters=None):
        """
        Process a natural language search query.
        
        Args:
            query (str): Natural language query
            filters (dict, optional): Additional search filters
            
        Returns:
            dict: Search results with AI-generated answer
        """
        try:
            # Use the NLP search engine to process the query
            results = self.search_engine.search(query)
            
            # Apply additional filters if provided
            if filters:
                results = self._apply_filters(results, filters)
            
            return {
                'success': True,
                'query': query,
                'ai_answer': results['ai_answer'],
                'documents': results['documents'],
                'total_results': len(results['documents'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'ai_answer': 'Sorry, I encountered an error processing your query.',
                'documents': [],
                'total_results': 0
            }
    
    def _apply_filters(self, results, filters):
        """Apply additional filters to search results."""
        filtered_docs = results['documents']
        
        # Filter by company if specified
        if filters.get('company') and filters['company'] != 'All Companies':
            company_ticker = filters['company'].split(' - ')[0]
            filtered_docs = [
                doc for doc in filtered_docs 
                if company_ticker.lower() in doc.get('title', '').lower() or 
                   company_ticker.lower() in doc.get('content', '').lower()
            ]
        
        # Filter by document type if specified
        if filters.get('document_type') and filters['document_type'] != 'All Types':
            doc_type = filters['document_type'].split(' (')[0]  # Extract type before parentheses
            filtered_docs = [
                doc for doc in filtered_docs 
                if doc_type.lower() in doc.get('source', '').lower()
            ]
        
        results['documents'] = filtered_docs
        return results
    
    def get_suggested_prompts(self):
        """
        Get suggested search prompts for the user interface.
        
        Returns:
            list: List of suggested prompt strings
        """
        return self.search_engine.get_suggested_prompts()
    
    def get_search_analytics(self):
        """
        Get analytics about search usage (mock implementation).
        
        Returns:
            dict: Search analytics data
        """
        return {
            'total_searches': 1247,
            'popular_queries': [
                'TNET revenue growth',
                'Compare TNET ADP',
                'Industry metrics',
                'Profit margins'
            ],
            'avg_response_time': '0.3s'
        }

def get_nlp_integration(db_path):
    """
    Factory function to create and return an NLP integration instance.
    
    Args:
        db_path (str): Path to the SQLite database
        
    Returns:
        NLPSearchIntegration: Configured NLP integration instance
    """
    return NLPSearchIntegration(db_path)

