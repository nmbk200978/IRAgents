"""
Prebuilt prompts and dashboard configurations for the Financial Knowledge Base.
This module provides structured prompt templates and dashboard configurations.
"""

import json
from datetime import datetime

class PromptLibrary:
    """
    Library of prebuilt prompts for the Financial Knowledge Base.
    Provides categorized, contextual prompts to help users explore financial data.
    """
    
    def __init__(self):
        """Initialize the prompt library with categorized prompt templates."""
        # General prompts applicable to any company
        self.general_prompts = {
            "company_overview": [
                "What does {company} do?",
                "Give me an overview of {company}'s business model",
                "What industry is {company} in?",
                "Who are {company}'s main competitors?",
                "What is {company}'s market position?"
            ],
            "financial_performance": [
                "How has {company}'s revenue grown over the past 3 years?",
                "What is {company}'s profit margin trend?",
                "Show me {company}'s key financial metrics",
                "How profitable is {company} compared to industry average?",
                "What is {company}'s earnings per share (EPS) growth?"
            ],
            "risk_analysis": [
                "What are the biggest risks facing {company}?",
                "How is {company} addressing cybersecurity risks?",
                "What regulatory challenges does {company} face?",
                "How exposed is {company} to economic downturns?",
                "What litigation risks does {company} have?"
            ],
            "growth_strategy": [
                "What is {company}'s growth strategy?",
                "How is {company} expanding its market share?",
                "What new products or services is {company} developing?",
                "What acquisitions has {company} made recently?",
                "How is {company} investing in innovation?"
            ],
            "management_team": [
                "Who is the CEO of {company}?",
                "Tell me about {company}'s executive leadership team",
                "How long has the current CEO been leading {company}?",
                "What is the background of {company}'s management team?",
                "Have there been any recent changes to {company}'s leadership?"
            ],
            "competitive_analysis": [
                "How does {company} compare to {competitor}?",
                "What are {company}'s competitive advantages?",
                "How is {company} differentiated from competitors?",
                "Compare {company}'s market share with competitors",
                "What threats do competitors pose to {company}?"
            ]
        }
        
        # PEO industry-specific prompts
        self.peo_industry_prompts = {
            "industry_trends": [
                "What are the current trends in the PEO industry?",
                "How is technology changing the PEO industry?",
                "What regulatory changes are affecting PEO companies?",
                "How is the gig economy impacting PEO services?",
                "What is the growth forecast for the PEO industry?"
            ],
            "service_offerings": [
                "What HR services does {company} offer?",
                "How comprehensive is {company}'s benefits administration?",
                "What payroll solutions does {company} provide?",
                "How does {company} handle compliance management?",
                "What risk management services does {company} offer?"
            ],
            "client_metrics": [
                "What is {company}'s client retention rate?",
                "How many worksite employees does {company} serve?",
                "What is {company}'s average revenue per client?",
                "How has {company}'s client base grown?",
                "What industries do {company}'s clients primarily come from?"
            ],
            "technology_platform": [
                "How is {company} investing in its technology platform?",
                "What digital capabilities does {company} offer clients?",
                "How does {company}'s technology compare to competitors?",
                "What mobile features does {company}'s platform offer?",
                "How is {company} using AI or automation in its services?"
            ]
        }
        
        # TNET-specific prompts
        self.tnet_specific_prompts = {
            "strategic_initiatives": [
                "What are TNET's current strategic initiatives?",
                "How is TNET expanding its vertical market strategy?",
                "What technology investments is TNET making?",
                "How is TNET addressing the mid-market segment?",
                "What is TNET's acquisition strategy?"
            ],
            "financial_highlights": [
                "What were the highlights from TNET's latest earnings call?",
                "How has TNET's revenue mix changed over time?",
                "What is TNET's guidance for the next fiscal year?",
                "How has TNET's stock performed compared to the S&P 500?",
                "What is TNET's dividend policy?"
            ],
            "competitive_position": [
                "How does TNET differentiate from ADP and Paychex?",
                "What market segments is TNET strongest in?",
                "How is TNET responding to competition from Rippling and Gusto?",
                "What is TNET's value proposition compared to competitors?",
                "How has TNET's market share evolved over the past 5 years?"
            ]
        }
        
        # Document-specific prompts
        self.document_prompts = {
            "10K": [
                "What are the key risks mentioned in this 10-K?",
                "Summarize the financial results in this annual report",
                "What strategic initiatives are outlined in this 10-K?",
                "How does the company describe its competitive position?",
                "What legal proceedings are disclosed in this 10-K?"
            ],
            "10Q": [
                "What are the highlights from this quarterly report?",
                "How did financial results change from the previous quarter?",
                "What factors affected performance in this quarter?",
                "Were there any significant events in this quarter?",
                "What guidance did management provide for future quarters?"
            ],
            "earnings_call": [
                "What were the key points from management in this earnings call?",
                "What questions did analysts ask during the Q&A?",
                "How did management explain the financial results?",
                "What forward-looking statements were made?",
                "Were there any notable concerns raised during the call?"
            ],
            "analyst_report": [
                "What is the analyst's rating for the company?",
                "What price target did the analyst set?",
                "What are the key investment thesis points?",
                "What risks did the analyst identify?",
                "How does the analyst view the company compared to peers?"
            ]
        }
        
        # Comparison prompts
        self.comparison_prompts = [
            "Compare revenue growth between {company1} and {company2}",
            "How do profit margins compare between {company1} and {company2}?",
            "Compare the client retention rates of {company1} and {company2}",
            "How do the technology platforms of {company1} and {company2} differ?",
            "Compare the market focus of {company1} and {company2}",
            "How do {company1} and {company2} differ in service offerings?",
            "Compare the financial metrics of {company1}, {company2}, and {company3}",
            "How do stock valuations compare between {company1} and {company2}?"
        ]
    
    def get_company_prompts(self, company_ticker):
        """
        Get prompts tailored for a specific company.
        
        Args:
            company_ticker (str): Company ticker symbol
            
        Returns:
            dict: Categorized prompts for the company
        """
        company_name = self._get_company_name(company_ticker)
        
        # Format general prompts with company name
        formatted_prompts = {}
        for category, prompts in self.general_prompts.items():
            formatted_prompts[category] = [
                prompt.format(company=company_name) for prompt in prompts
            ]
        
        # Add industry-specific prompts
        if self._is_peo_company(company_ticker):
            for category, prompts in self.peo_industry_prompts.items():
                formatted_prompts[category] = [
                    prompt.format(company=company_name) for prompt in prompts
                ]
        
        # Add TNET-specific prompts if applicable
        if company_ticker == 'TNET':
            for category, prompts in self.tnet_specific_prompts.items():
                formatted_prompts[category] = prompts
        
        return formatted_prompts
    
    def get_document_prompts(self, doc_type):
        """
        Get prompts specific to a document type.
        
        Args:
            doc_type (str): Document type (10K, 10Q, earnings_call, analyst_report)
            
        Returns:
            list: Prompts for the document type
        """
        doc_type = doc_type.replace('-', '').upper()
        if doc_type in self.document_prompts:
            return self.document_prompts[doc_type]
        elif 'EARNINGS' in doc_type or 'CALL' in doc_type or 'TRANSCRIPT' in doc_type:
            return self.document_prompts['earnings_call']
        elif 'ANALYST' in doc_type or 'RESEARCH' in doc_type:
            return self.document_prompts['analyst_report']
        else:
            return self.document_prompts['10K'][:2]  # Default to first two general document prompts
    
    def get_comparison_prompts(self, companies):
        """
        Get prompts for comparing multiple companies.
        
        Args:
            companies (list): List of company ticker symbols
            
        Returns:
            list: Comparison prompts
        """
        if len(companies) < 2:
            return []
        
        company_names = [self._get_company_name(ticker) for ticker in companies]
        
        formatted_prompts = []
        for prompt in self.comparison_prompts:
            if len(companies) >= 3 and '{company3}' in prompt:
                formatted_prompts.append(
                    prompt.format(
                        company1=company_names[0],
                        company2=company_names[1],
                        company3=company_names[2]
                    )
                )
            else:
                formatted_prompts.append(
                    prompt.format(
                        company1=company_names[0],
                        company2=company_names[1]
                    )
                )
        
        return formatted_prompts
    
    def get_trending_prompts(self):
        """
        Get trending or timely prompts based on current date or events.
        
        Returns:
            list: Trending prompts
        """
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        trending_prompts = [
            f"What are the latest industry trends in the PEO sector in {current_year}?",
            "How are PEO companies adapting to remote work trends?",
            "What impact is AI having on HR outsourcing services?",
            "How are PEO companies addressing healthcare cost challenges?"
        ]
        
        # Add quarterly prompts if we're near quarter end
        if current_month in [3, 6, 9, 12]:
            quarter = current_month // 3
            trending_prompts.extend([
                f"What are analysts expecting for TNET's Q{quarter} {current_year} results?",
                f"How did PEO companies perform in Q{quarter} {current_year}?",
                f"Compare Q{quarter} results across the PEO industry"
            ])
        
        return trending_prompts
    
    def _get_company_name(self, ticker):
        """Get company name from ticker symbol."""
        company_names = {
            'TNET': 'TriNet',
            'ADP': 'ADP',
            'PAYX': 'Paychex',
            'NSP': 'Insperity',
            'PYCR': 'Paycor',
            'PCTY': 'Paylocity'
        }
        return company_names.get(ticker, ticker)
    
    def _is_peo_company(self, ticker):
        """Check if company is in the PEO industry."""
        peo_companies = ['TNET', 'ADP', 'PAYX', 'NSP', 'PYCR', 'PCTY']
        return ticker in peo_companies


class DashboardConfigurations:
    """
    Configurations for interactive dashboards in the Financial Knowledge Base.
    Provides structured dashboard definitions for various data visualizations.
    """
    
    def __init__(self):
        """Initialize dashboard configurations."""
        # Company overview dashboard
        self.company_overview = {
            "title": "Company Overview",
            "description": "Key information and metrics for the selected company",
            "layout": "grid",
            "widgets": [
                {
                    "id": "company_profile",
                    "type": "profile",
                    "title": "Company Profile",
                    "width": 12,
                    "height": 2,
                    "data_source": "company_info"
                },
                {
                    "id": "key_metrics",
                    "type": "metrics",
                    "title": "Key Financial Metrics",
                    "width": 6,
                    "height": 3,
                    "data_source": "company_metrics",
                    "metrics": ["revenue", "net_income", "eps", "operating_margin"]
                },
                {
                    "id": "stock_performance",
                    "type": "chart",
                    "chart_type": "line",
                    "title": "Stock Performance",
                    "width": 6,
                    "height": 3,
                    "data_source": "stock_data",
                    "time_range": "1y"
                },
                {
                    "id": "recent_filings",
                    "type": "table",
                    "title": "Recent SEC Filings",
                    "width": 6,
                    "height": 3,
                    "data_source": "company_filings",
                    "limit": 5
                },
                {
                    "id": "latest_insights",
                    "type": "insights",
                    "title": "Latest Insights",
                    "width": 6,
                    "height": 3,
                    "data_source": "company_insights",
                    "limit": 5
                }
            ]
        }
        
        # Financial performance dashboard
        self.financial_performance = {
            "title": "Financial Performance",
            "description": "Detailed financial metrics and trends",
            "layout": "grid",
            "widgets": [
                {
                    "id": "revenue_trend",
                    "type": "chart",
                    "chart_type": "bar",
                    "title": "Revenue Trend",
                    "width": 6,
                    "height": 3,
                    "data_source": "financial_metrics",
                    "metric": "revenue",
                    "time_range": "5y",
                    "comparison": True
                },
                {
                    "id": "profit_margin_trend",
                    "type": "chart",
                    "chart_type": "line",
                    "title": "Profit Margin Trend",
                    "width": 6,
                    "height": 3,
                    "data_source": "financial_metrics",
                    "metric": "profit_margin",
                    "time_range": "5y",
                    "comparison": True
                },
                {
                    "id": "eps_trend",
                    "type": "chart",
                    "chart_type": "line",
                    "title": "EPS Trend",
                    "width": 6,
                    "height": 3,
                    "data_source": "financial_metrics",
                    "metric": "eps",
                    "time_range": "5y",
                    "comparison": True
                },
                {
                    "id": "revenue_breakdown",
                    "type": "chart",
                    "chart_type": "pie",
                    "title": "Revenue Breakdown",
                    "width": 6,
                    "height": 3,
                    "data_source": "revenue_segments"
                },
                {
                    "id": "financial_ratios",
                    "type": "table",
                    "title": "Financial Ratios",
                    "width": 12,
                    "height": 3,
                    "data_source": "financial_ratios"
                }
            ]
        }
        
        # Industry comparison dashboard
        self.industry_comparison = {
            "title": "Industry Comparison",
            "description": "Compare key metrics across companies in the industry",
            "layout": "grid",
            "widgets": [
                {
                    "id": "revenue_comparison",
                    "type": "chart",
                    "chart_type": "bar",
                    "title": "Revenue Comparison",
                    "width": 6,
                    "height": 3,
                    "data_source": "industry_metrics",
                    "metric": "revenue",
                    "companies": ["TNET", "ADP", "PAYX", "NSP", "PYCR", "PCTY"]
                },
                {
                    "id": "profit_margin_comparison",
                    "type": "chart",
                    "chart_type": "bar",
                    "title": "Profit Margin Comparison",
                    "width": 6,
                    "height": 3,
                    "data_source": "industry_metrics",
                    "metric": "profit_margin",
                    "companies": ["TNET", "ADP", "PAYX", "NSP", "PYCR", "PCTY"]
                },
                {
                    "id": "market_share",
                    "type": "chart",
                    "chart_type": "pie",
                    "title": "Market Share",
                    "width": 6,
                    "height": 3,
                    "data_source": "market_share"
                },
                {
                    "id": "valuation_comparison",
                    "type": "chart",
                    "chart_type": "bar",
                    "title": "Valuation Metrics",
                    "width": 6,
                    "height": 3,
                    "data_source": "valuation_metrics",
                    "metrics": ["pe_ratio", "ev_ebitda", "price_sales"],
                    "companies": ["TNET", "ADP", "PAYX", "NSP", "PYCR", "PCTY"]
                },
                {
                    "id": "growth_comparison",
                    "type": "table",
                    "title": "Growth Metrics Comparison",
                    "width": 12,
                    "height": 3,
                    "data_source": "growth_metrics",
                    "companies": ["TNET", "ADP", "PAYX", "NSP", "PYCR", "PCTY"]
                }
            ]
        }
        
        # Risk analysis dashboard
        self.risk_analysis = {
            "title": "Risk Analysis",
            "description": "Analysis of key risks and risk factors",
            "layout": "grid",
            "widgets": [
                {
                    "id": "risk_summary",
                    "type": "summary",
                    "title": "Risk Summary",
                    "width": 12,
                    "height": 2,
                    "data_source": "risk_factors"
                },
                {
                    "id": "risk_categories",
                    "type": "chart",
                    "chart_type": "radar",
                    "title": "Risk Categories",
                    "width": 6,
                    "height": 4,
                    "data_source": "risk_categories"
                },
                {
                    "id": "risk_trends",
                    "type": "chart",
                    "chart_type": "line",
                    "title": "Risk Trends",
                    "width": 6,
                    "height": 4,
                    "data_source": "risk_trends",
                    "time_range": "3y"
                },
                {
                    "id": "risk_factors",
                    "type": "table",
                    "title": "Key Risk Factors",
                    "width": 12,
                    "height": 4,
                    "data_source": "risk_factors_detail"
                }
            ]
        }
        
        # Document analysis dashboard
        self.document_analysis = {
            "title": "Document Analysis",
            "description": "Analysis and insights from financial documents",
            "layout": "grid",
            "widgets": [
                {
                    "id": "document_summary",
                    "type": "summary",
                    "title": "Document Summary",
                    "width": 12,
                    "height": 2,
                    "data_source": "document_info"
                },
                {
                    "id": "key_topics",
                    "type": "chart",
                    "chart_type": "wordcloud",
                    "title": "Key Topics",
                    "width": 6,
                    "height": 3,
                    "data_source": "document_topics"
                },
                {
                    "id": "sentiment_analysis",
                    "type": "chart",
                    "chart_type": "gauge",
                    "title": "Sentiment Analysis",
                    "width": 6,
                    "height": 3,
                    "data_source": "document_sentiment"
                },
                {
                    "id": "key_metrics_mentioned",
                    "type": "table",
                    "title": "Key Metrics Mentioned",
                    "width": 6,
                    "height": 3,
                    "data_source": "document_metrics"
                },
                {
                    "id": "key_insights",
                    "type": "insights",
                    "title": "Key Insights",
                    "width": 6,
                    "height": 3,
                    "data_source": "document_insights"
                }
            ]
        }
    
    def get_dashboard_config(self, dashboard_type):
        """
        Get configuration for a specific dashboard type.
        
        Args:
            dashboard_type (str): Type of dashboard
            
        Returns:
            dict: Dashboard configuration
        """
        if dashboard_type == 'company_overview':
            return self.company_overview
        elif dashboard_type == 'financial_performance':
            return self.financial_performance
        elif dashboard_type == 'industry_comparison':
            return self.industry_comparison
        elif dashboard_type == 'risk_analysis':
            return self.risk_analysis
        elif dashboard_type == 'document_analysis':
            return self.document_analysis
        else:
            return self.company_overview  # Default to company overview
    
    def get_all_dashboards(self):
        """
        Get all available dashboard configurations.
        
        Returns:
            dict: All dashboard configurations
        """
        return {
            'company_overview': self.company_overview,
            'financial_performance': self.financial_performance,
            'industry_comparison': self.industry_comparison,
            'risk_analysis': self.risk_analysis,
            'document_analysis': self.document_analysis
        }
    
    def get_dashboard_for_company(self, ticker):
        """
        Get customized dashboard configuration for a specific company.
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            dict: Customized dashboard configuration
        """
        # Start with the company overview dashboard
        dashboard = self.company_overview.copy()
        
        # Customize title and description
        company_name = self._get_company_name(ticker)
        dashboard['title'] = f"{company_name} Overview"
        dashboard['description'] = f"Key information and metrics for {company_name}"
        
        # Customize data sources to include ticker
        for widget in dashboard['widgets']:
            if 'data_source' in widget:
                widget['data_source'] = f"{widget['data_source']}_{ticker}"
        
        return dashboard
    
    def _get_company_name(self, ticker):
        """Get company name from ticker symbol."""
        company_names = {
            'TNET': 'TriNet',
            'ADP': 'ADP',
            'PAYX': 'Paychex',
            'NSP': 'Insperity',
            'PYCR': 'Paycor',
            'PCTY': 'Paylocity'
        }
        return company_names.get(ticker, ticker)


# Example usage
if __name__ == "__main__":
    # Initialize prompt library
    prompt_library = PromptLibrary()
    
    # Get prompts for TNET
    tnet_prompts = prompt_library.get_company_prompts('TNET')
    print("TNET Prompts:")
    for category, prompts in tnet_prompts.items():
        print(f"  {category}:")
        for prompt in prompts[:2]:  # Print first two prompts in each category
            print(f"    - {prompt}")
    
    # Get comparison prompts
    comparison_prompts = prompt_library.get_comparison_prompts(['TNET', 'ADP', 'PAYX'])
    print("\nComparison Prompts:")
    for prompt in comparison_prompts[:3]:  # Print first three comparison prompts
        print(f"  - {prompt}")
    
    # Initialize dashboard configurations
    dashboard_configs = DashboardConfigurations()
    
    # Get company overview dashboard
    overview_dashboard = dashboard_configs.get_dashboard_config('company_overview')
    print("\nCompany Overview Dashboard:")
    print(f"  Title: {overview_dashboard['title']}")
    print(f"  Widgets: {len(overview_dashboard['widgets'])}")
    
    # Get customized dashboard for TNET
    tnet_dashboard = dashboard_configs.get_dashboard_for_company('TNET')
    print("\nTNET Dashboard:")
    print(f"  Title: {tnet_dashboard['title']}")
    print(f"  Description: {tnet_dashboard['description']}")
