"""
Vector embeddings and LLM integration for the Financial Knowledge Base.
This module implements document vectorization and LLM-powered retrieval for enhanced NLP/NLX capabilities.
"""

import os
import numpy as np
import sqlite3
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class VectorKnowledgeBase:
    """
    Vector-based knowledge base for financial documents using embeddings and LLM integration.
    """
    
    def __init__(self, db_path):
        """
        Initialize the vector knowledge base with the SQLite database.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        
        # Initialize the sentence transformer model for embeddings
        # Using a smaller model for demonstration, would use a more powerful one in production
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create vector database tables if they don't exist
        self._initialize_vector_db()
    
    def _initialize_vector_db(self):
        """Initialize the vector database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for document section embeddings
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id TEXT NOT NULL,
            section_id TEXT NOT NULL,
            section_title TEXT,
            section_content TEXT NOT NULL,
            embedding BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create table for company information embeddings
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            info_type TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create table for financial metrics embeddings
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS metric_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            period TEXT NOT NULL,
            value TEXT NOT NULL,
            embedding BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create index for faster retrieval
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_doc_embeddings ON document_embeddings(doc_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_company_embeddings ON company_embeddings(ticker)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metric_embeddings ON metric_embeddings(ticker, metric_name)')
        
        conn.commit()
        conn.close()
    
    def vectorize_documents(self, limit=None):
        """
        Vectorize all documents in the knowledge base.
        
        Args:
            limit (int, optional): Limit the number of documents to process
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get documents to vectorize
        if limit:
            cursor.execute('SELECT id, ticker, doc_type, title, content FROM documents LIMIT ?', (limit,))
        else:
            cursor.execute('SELECT id, ticker, doc_type, title, content FROM documents')
        
        documents = cursor.fetchall()
        
        # Process each document
        for doc_id, ticker, doc_type, title, content in documents:
            # Split document into sections
            sections = self._split_document_into_sections(content, title)
            
            # Vectorize each section
            for section_id, section_data in enumerate(sections):
                section_title = section_data.get('title', f'Section {section_id}')
                section_content = section_data.get('content', '')
                
                # Skip empty sections
                if not section_content.strip():
                    continue
                
                # Generate embedding for the section
                embedding = self.model.encode(section_content)
                
                # Store embedding in the database
                cursor.execute(
                    'INSERT INTO document_embeddings (doc_id, section_id, section_title, section_content, embedding) VALUES (?, ?, ?, ?, ?)',
                    (doc_id, str(section_id), section_title, section_content, embedding.tobytes())
                )
        
        conn.commit()
        conn.close()
        
        print(f"Vectorized {len(documents)} documents")
    
    def vectorize_company_info(self):
        """Vectorize company information for all companies in the knowledge base."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all companies
        cursor.execute('SELECT ticker, name, description, industry, sector FROM companies')
        companies = cursor.fetchall()
        
        # Process each company
        for ticker, name, description, industry, sector in companies:
            # Vectorize company overview
            overview = f"{name} ({ticker}) is a company in the {industry} industry within the {sector} sector. {description}"
            overview_embedding = self.model.encode(overview)
            
            cursor.execute(
                'INSERT INTO company_embeddings (ticker, info_type, content, embedding) VALUES (?, ?, ?, ?)',
                (ticker, 'overview', overview, overview_embedding.tobytes())
            )
            
            # Get and vectorize company metrics
            cursor.execute('SELECT metric_name, period, value FROM metrics WHERE ticker = ?', (ticker,))
            metrics = cursor.fetchall()
            
            for metric_name, period, value in metrics:
                metric_content = f"{ticker} {metric_name} for {period}: {value}"
                metric_embedding = self.model.encode(metric_content)
                
                cursor.execute(
                    'INSERT INTO metric_embeddings (ticker, metric_name, period, value, embedding) VALUES (?, ?, ?, ?, ?)',
                    (ticker, metric_name, period, value, metric_embedding.tobytes())
                )
        
        conn.commit()
        conn.close()
        
        print(f"Vectorized information for {len(companies)} companies")
    
    def _split_document_into_sections(self, content, title):
        """
        Split a document into logical sections for vectorization.
        
        Args:
            content (str): Document content
            title (str): Document title
            
        Returns:
            list: List of section dictionaries with title and content
        """
        # Simple splitting by paragraphs for demonstration
        # In a production system, would use more sophisticated methods
        paragraphs = content.split('\n\n')
        
        # Group paragraphs into sections (max ~512 tokens per section)
        sections = []
        current_section = {'title': title, 'content': ''}
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            # If paragraph starts with a potential heading, start a new section
            if paragraph.isupper() or (len(paragraph) < 100 and paragraph.endswith(':')):
                if current_section['content']:
                    sections.append(current_section)
                current_section = {'title': paragraph, 'content': ''}
            else:
                if len(current_section['content']) + len(paragraph) > 2000:  # Approximate token limit
                    sections.append(current_section)
                    current_section = {'title': current_section['title'] + ' (continued)', 'content': paragraph}
                else:
                    if current_section['content']:
                        current_section['content'] += '\n\n'
                    current_section['content'] += paragraph
        
        # Add the last section if it has content
        if current_section['content']:
            sections.append(current_section)
        
        return sections
    
    def semantic_search(self, query, top_k=5):
        """
        Perform semantic search using vector embeddings.
        
        Args:
            query (str): Search query
            top_k (int): Number of top results to return
            
        Returns:
            list: Top matching document sections
        """
        # Generate embedding for the query
        query_embedding = self.model.encode(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all document embeddings
        cursor.execute('SELECT id, doc_id, section_title, section_content, embedding FROM document_embeddings')
        results = cursor.fetchall()
        
        # Calculate similarity scores
        similarities = []
        for id, doc_id, section_title, section_content, embedding_bytes in results:
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            similarity = cosine_similarity([query_embedding], [embedding])[0][0]
            similarities.append((id, doc_id, section_title, section_content, similarity))
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x[4], reverse=True)
        
        # Get document details for top results
        top_results = []
        for id, doc_id, section_title, section_content, similarity in similarities[:top_k]:
            cursor.execute('SELECT ticker, doc_type, title, filing_date FROM documents WHERE id = ?', (doc_id,))
            doc_info = cursor.fetchone()
            
            if doc_info:
                ticker, doc_type, title, filing_date = doc_info
                top_results.append({
                    'id': id,
                    'doc_id': doc_id,
                    'ticker': ticker,
                    'doc_type': doc_type,
                    'doc_title': title,
                    'filing_date': filing_date,
                    'section_title': section_title,
                    'section_content': section_content,
                    'similarity': float(similarity)
                })
        
        conn.close()
        return top_results
    
    def company_semantic_search(self, query, ticker=None, top_k=5):
        """
        Perform semantic search on company information.
        
        Args:
            query (str): Search query
            ticker (str, optional): Limit search to specific company
            top_k (int): Number of top results to return
            
        Returns:
            list: Top matching company information
        """
        # Generate embedding for the query
        query_embedding = self.model.encode(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get company embeddings
        if ticker:
            cursor.execute('SELECT id, ticker, info_type, content, embedding FROM company_embeddings WHERE ticker = ?', (ticker,))
        else:
            cursor.execute('SELECT id, ticker, info_type, content, embedding FROM company_embeddings')
        
        results = cursor.fetchall()
        
        # Calculate similarity scores
        similarities = []
        for id, ticker, info_type, content, embedding_bytes in results:
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            similarity = cosine_similarity([query_embedding], [embedding])[0][0]
            similarities.append((id, ticker, info_type, content, similarity))
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x[4], reverse=True)
        
        # Format top results
        top_results = []
        for id, ticker, info_type, content, similarity in similarities[:top_k]:
            top_results.append({
                'id': id,
                'ticker': ticker,
                'info_type': info_type,
                'content': content,
                'similarity': float(similarity)
            })
        
        conn.close()
        return top_results
    
    def metric_semantic_search(self, query, ticker=None, top_k=5):
        """
        Perform semantic search on financial metrics.
        
        Args:
            query (str): Search query
            ticker (str, optional): Limit search to specific company
            top_k (int): Number of top results to return
            
        Returns:
            list: Top matching financial metrics
        """
        # Generate embedding for the query
        query_embedding = self.model.encode(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get metric embeddings
        if ticker:
            cursor.execute('SELECT id, ticker, metric_name, period, value, embedding FROM metric_embeddings WHERE ticker = ?', (ticker,))
        else:
            cursor.execute('SELECT id, ticker, metric_name, period, value, embedding FROM metric_embeddings')
        
        results = cursor.fetchall()
        
        # Calculate similarity scores
        similarities = []
        for id, ticker, metric_name, period, value, embedding_bytes in results:
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            similarity = cosine_similarity([query_embedding], [embedding])[0][0]
            similarities.append((id, ticker, metric_name, period, value, similarity))
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x[5], reverse=True)
        
        # Format top results
        top_results = []
        for id, ticker, metric_name, period, value, similarity in similarities[:top_k]:
            top_results.append({
                'id': id,
                'ticker': ticker,
                'metric_name': metric_name,
                'period': period,
                'value': value,
                'similarity': float(similarity)
            })
        
        conn.close()
        return top_results
    
    def hybrid_search(self, query, ticker=None, doc_types=None, top_k=10):
        """
        Perform hybrid search combining semantic and keyword search.
        
        Args:
            query (str): Search query
            ticker (str, optional): Limit search to specific company
            doc_types (list, optional): Limit search to specific document types
            top_k (int): Number of top results to return
            
        Returns:
            list: Top matching results
        """
        # Get semantic search results
        semantic_results = self.semantic_search(query, top_k=top_k*2)
        
        # Filter by ticker and doc_type if specified
        if ticker or doc_types:
            filtered_results = []
            for result in semantic_results:
                if ticker and result['ticker'] != ticker:
                    continue
                if doc_types and result['doc_type'] not in doc_types:
                    continue
                filtered_results.append(result)
            semantic_results = filtered_results
        
        # Perform keyword search
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build the SQL query
        sql = "SELECT id, ticker, doc_type, title, filing_date, content FROM documents WHERE content LIKE ?"
        params = [f"%{query}%"]
        
        if ticker:
            sql += " AND ticker = ?"
            params.append(ticker)
        
        if doc_types:
            placeholders = ', '.join(['?'] * len(doc_types))
            sql += f" AND doc_type IN ({placeholders})"
            params.extend(doc_types)
        
        sql += " ORDER BY filing_date DESC LIMIT ?"
        params.append(top_k*2)
        
        # Execute the query
        cursor.execute(sql, params)
        keyword_results = [dict(row) for row in cursor.fetchall()]
        
        # Add snippets to keyword results
        for result in keyword_results:
            result['snippet'] = self._generate_snippet(result['content'], query)
            result['similarity'] = 0.5  # Default similarity score for keyword results
        
        # Combine and deduplicate results
        combined_results = semantic_results.copy()
        doc_ids = {result['doc_id'] for result in combined_results}
        
        for result in keyword_results:
            if result['id'] not in doc_ids:
                doc_ids.add(result['id'])
                # Format to match semantic results structure
                combined_results.append({
                    'id': None,
                    'doc_id': result['id'],
                    'ticker': result['ticker'],
                    'doc_type': result['doc_type'],
                    'doc_title': result['title'],
                    'filing_date': result['filing_date'],
                    'section_title': 'Keyword Match',
                    'section_content': result['snippet'],
                    'similarity': result['similarity']
                })
        
        # Sort by similarity score
        combined_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        conn.close()
        return combined_results[:top_k]
    
    def _generate_snippet(self, content, query, max_length=200):
        """
        Generate a relevant snippet from document content based on search query.
        
        Args:
            content (str): Document content
            query (str): Search query
            max_length (int): Maximum snippet length
            
        Returns:
            str: Generated snippet
        """
        # Find the position of the query in the content
        query_lower = query.lower()
        content_lower = content.lower()
        
        pos = content_lower.find(query_lower)
        if pos == -1:
            # If exact query not found, look for individual words
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 3:  # Only consider significant words
                    pos = content_lower.find(word)
                    if pos != -1:
                        break
        
        # If still not found, return the beginning of the content
        if pos == -1:
            return content[:max_length] + "..."
        
        # Calculate snippet start and end positions
        start = max(0, pos - max_length // 2)
        end = min(len(content), pos + max_length // 2)
        
        # Adjust to avoid cutting words
        while start > 0 and content[start] != ' ':
            start -= 1
        
        while end < len(content) and content[end] != ' ':
            end += 1
        
        # Create the snippet
        snippet = content[start:end].strip()
        
        # Add ellipsis if needed
        if start > 0:
            snippet = "..." + snippet
        
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet

# Example usage
if __name__ == "__main__":
    db_path = "../financial_kb.db"
    vector_kb = VectorKnowledgeBase(db_path)
    
    # Vectorize documents (limit to 10 for testing)
    vector_kb.vectorize_documents(limit=10)
    
    # Vectorize company information
    vector_kb.vectorize_company_info()
    
    # Test semantic search
    results = vector_kb.semantic_search("What are the key risks for TNET?")
    print(f"Found {len(results)} results")
    for i, result in enumerate(results[:3]):
        print(f"{i+1}. {result['ticker']} - {result['doc_type']} - {result['section_title']} (Score: {result['similarity']:.4f})")
        print(f"   {result['section_content'][:100]}...")
