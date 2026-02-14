"""
Legal Citation Identification and Verification System

This module uses FreeLawProject's eyecite library to identify legal citations
in documents and websites, and verifies them through CourtListener's API.
"""

import os
from typing import List, Dict, Any, Optional
import requests
from eyecite import get_citations
from eyecite.models import FullCaseCitation, ShortCaseCitation, SupraCitation, IdCitation
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CitationVerifier:
    """Handles verification of legal citations using CourtListener API."""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the Citation Verifier.
        
        Args:
            api_token: CourtListener API token. If None, reads from environment.
        """
        self.api_token = api_token or os.getenv('COURTLISTENER_API_TOKEN')
        self.base_url = "https://www.courtlistener.com/api/rest/v3"
        self.session = requests.Session()
        if self.api_token:
            self.session.headers.update({
                'Authorization': f'Token {self.api_token}'
            })
    
    def verify_citation(self, citation_text: str) -> Dict[str, Any]:
        """
        Verify a citation using CourtListener API.
        
        Args:
            citation_text: The citation text to verify (e.g., "410 U.S. 113")
        
        Returns:
            Dictionary containing verification results and metadata
        """
        try:
            # Search for the citation in CourtListener
            endpoint = f"{self.base_url}/search/"
            params = {
                'q': citation_text,
                'type': 'o',  # Opinion search
                'format': 'json'
            }
            
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'citation': citation_text,
                'is_valid': data.get('count', 0) > 0,
                'count': data.get('count', 0),
                'results': data.get('results', [])[:5],  # Limit to top 5 results
                'error': None
            }
        except requests.exceptions.RequestException as e:
            return {
                'citation': citation_text,
                'is_valid': False,
                'count': 0,
                'results': [],
                'error': str(e)
            }
    
    def get_citation_details(self, citation_text: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a citation.
        
        Args:
            citation_text: The citation text
        
        Returns:
            Dictionary with detailed citation information or None
        """
        verification = self.verify_citation(citation_text)
        
        if verification['is_valid'] and verification['results']:
            # Get the most relevant (first) result
            top_result = verification['results'][0]
            
            return {
                'citation': citation_text,
                'case_name': top_result.get('caseName', 'N/A'),
                'court': top_result.get('court', 'N/A'),
                'date_filed': top_result.get('dateFiled', 'N/A'),
                'status': top_result.get('status', 'N/A'),
                'url': f"https://www.courtlistener.com{top_result.get('absolute_url', '')}",
                'is_most_recent': True  # TODO: Implement jurisdiction-specific logic
            }
        
        return None


class CitationExtractor:
    """Extracts legal citations from text using eyecite."""
    
    @staticmethod
    def extract_citations(text: str) -> List[Any]:
        """
        Extract legal citations from text.
        
        Args:
            text: The text to extract citations from
        
        Returns:
            List of citation objects found in the text
        """
        # Handle empty text
        if not text or not text.strip():
            return []
        
        return get_citations(text)
    
    @staticmethod
    def format_citation(citation) -> Dict[str, Any]:
        """
        Format a citation object into a dictionary.
        
        Args:
            citation: An eyecite citation object
        
        Returns:
            Dictionary with citation details
        """
        citation_dict = {
            'text': str(citation),
            'type': type(citation).__name__,
            'groups': {}
        }
        
        # Add specific fields based on citation type
        if isinstance(citation, FullCaseCitation):
            citation_dict['groups'] = citation.groups
            
            # Extract metadata from the citation
            metadata = {}
            if hasattr(citation, 'groups') and citation.groups:
                metadata['volume'] = citation.groups.get('volume')
                metadata['reporter'] = citation.groups.get('reporter')
                metadata['page'] = citation.groups.get('page')
            
            if hasattr(citation, 'metadata') and citation.metadata:
                metadata['year'] = citation.metadata.year
                metadata['court'] = citation.metadata.court
                metadata['plaintiff'] = citation.metadata.plaintiff
                metadata['defendant'] = citation.metadata.defendant
            
            citation_dict['metadata'] = metadata
            
        elif isinstance(citation, (ShortCaseCitation, SupraCitation, IdCitation)):
            citation_dict['metadata'] = {}
            if hasattr(citation, 'metadata') and citation.metadata:
                citation_dict['metadata']['antecedent_guess'] = citation.metadata.antecedent_guess
        
        return citation_dict


class LegalCitationProcessor:
    """Main class for processing and verifying legal citations."""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the Legal Citation Processor.
        
        Args:
            api_token: CourtListener API token
        """
        self.extractor = CitationExtractor()
        self.verifier = CitationVerifier(api_token)
    
    def process_text(self, text: str, verify: bool = True) -> Dict[str, Any]:
        """
        Process text to extract and optionally verify citations.
        
        Args:
            text: The text to process
            verify: Whether to verify citations with CourtListener API
        
        Returns:
            Dictionary containing extracted citations and verification results
        """
        # Extract citations
        citations = self.extractor.extract_citations(text)
        
        results = {
            'text_length': len(text),
            'citations_found': len(citations),
            'citations': []
        }
        
        for citation in citations:
            citation_data = self.extractor.format_citation(citation)
            
            # Verify if requested and it's a full citation
            if verify and isinstance(citation, FullCaseCitation):
                citation_text = str(citation)
                verification = self.verifier.verify_citation(citation_text)
                citation_data['verification'] = verification
                
                # Get detailed info if valid
                if verification['is_valid']:
                    details = self.verifier.get_citation_details(citation_text)
                    if details:
                        citation_data['details'] = details
            
            results['citations'].append(citation_data)
        
        return results
    
    def process_url(self, url: str, verify: bool = True) -> Dict[str, Any]:
        """
        Process a URL to extract and verify citations from its content.
        
        Args:
            url: The URL to process
            verify: Whether to verify citations
        
        Returns:
            Dictionary containing extraction and verification results
        """
        try:
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            
            results = self.process_text(text, verify=verify)
            results['url'] = url
            results['status'] = 'success'
            
            return results
        
        except Exception as e:
            return {
                'url': url,
                'status': 'error',
                'error': str(e),
                'citations_found': 0,
                'citations': []
            }
    
    def process_file(self, file_path: str, verify: bool = True) -> Dict[str, Any]:
        """
        Process a file to extract and verify citations.
        
        Args:
            file_path: Path to the file
            verify: Whether to verify citations
        
        Returns:
            Dictionary containing extraction and verification results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            results = self.process_text(text, verify=verify)
            results['file_path'] = file_path
            results['status'] = 'success'
            
            return results
        
        except Exception as e:
            return {
                'file_path': file_path,
                'status': 'error',
                'error': str(e),
                'citations_found': 0,
                'citations': []
            }
