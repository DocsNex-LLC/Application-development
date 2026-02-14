"""
Unit tests for the legal citation identification and verification system.
"""

import unittest
from citation_processor import (
    CitationExtractor,
    CitationVerifier,
    LegalCitationProcessor
)


class TestCitationExtractor(unittest.TestCase):
    """Test citation extraction functionality."""
    
    def setUp(self):
        self.extractor = CitationExtractor()
    
    def test_extract_single_citation(self):
        """Test extraction of a single citation."""
        text = "The Supreme Court ruled in Roe v. Wade, 410 U.S. 113 (1973)."
        citations = self.extractor.extract_citations(text)
        
        self.assertEqual(len(citations), 1)
        self.assertIn('410 U.S. 113', str(citations[0]))
    
    def test_extract_multiple_citations(self):
        """Test extraction of multiple citations."""
        text = """
        Roe v. Wade, 410 U.S. 113 (1973) and 
        Miranda v. Arizona, 384 U.S. 436 (1966).
        """
        citations = self.extractor.extract_citations(text)
        
        self.assertEqual(len(citations), 2)
    
    def test_no_citations(self):
        """Test text with no citations."""
        text = "This is a document without any legal citations."
        citations = self.extractor.extract_citations(text)
        
        self.assertEqual(len(citations), 0)
    
    def test_format_citation(self):
        """Test citation formatting."""
        text = "Brown v. Board of Education, 347 U.S. 483 (1954)."
        citations = self.extractor.extract_citations(text)
        
        self.assertTrue(len(citations) > 0)
        
        formatted = self.extractor.format_citation(citations[0])
        
        self.assertIn('text', formatted)
        self.assertIn('type', formatted)
        self.assertEqual(formatted['type'], 'FullCaseCitation')
        
        # Check metadata
        self.assertIn('metadata', formatted)
        metadata = formatted['metadata']
        self.assertEqual(metadata['volume'], '347')
        self.assertEqual(metadata['reporter'], 'U.S.')
        self.assertEqual(metadata['page'], '483')
        self.assertEqual(metadata['year'], '1954')
    
    def test_various_citation_types(self):
        """Test extraction of various legal citation formats."""
        # Supreme Court citation
        text1 = "410 U.S. 113"
        citations1 = self.extractor.extract_citations(text1)
        self.assertTrue(len(citations1) > 0)
        
        # Federal Reporter citation
        text2 = "123 F.3d 456"
        citations2 = self.extractor.extract_citations(text2)
        self.assertTrue(len(citations2) > 0)
        
        # State reporter citation
        text3 = "123 Cal. App. 4th 789"
        citations3 = self.extractor.extract_citations(text3)
        self.assertTrue(len(citations3) > 0)


class TestCitationVerifier(unittest.TestCase):
    """Test citation verification functionality."""
    
    def setUp(self):
        # Initialize without token for testing
        self.verifier = CitationVerifier(api_token=None)
    
    def test_verifier_initialization(self):
        """Test verifier initialization."""
        self.assertIsNotNone(self.verifier.session)
        self.assertEqual(self.verifier.base_url, 
                        "https://www.courtlistener.com/api/rest/v3")
    
    def test_verify_citation_structure(self):
        """Test the structure of verification results."""
        citation = "410 U.S. 113"
        result = self.verifier.verify_citation(citation)
        
        # Check result structure
        self.assertIn('citation', result)
        self.assertIn('is_valid', result)
        self.assertIn('count', result)
        self.assertIn('results', result)
        self.assertIn('error', result)
        
        self.assertEqual(result['citation'], citation)
        self.assertIsInstance(result['is_valid'], bool)
        self.assertIsInstance(result['count'], int)
        self.assertIsInstance(result['results'], list)


class TestLegalCitationProcessor(unittest.TestCase):
    """Test the main legal citation processor."""
    
    def setUp(self):
        self.processor = LegalCitationProcessor()
    
    def test_process_text_without_verification(self):
        """Test text processing without verification."""
        text = "The case Brown v. Board of Education, 347 U.S. 483 (1954)."
        results = self.processor.process_text(text, verify=False)
        
        # Check result structure
        self.assertIn('text_length', results)
        self.assertIn('citations_found', results)
        self.assertIn('citations', results)
        
        # Check values
        self.assertEqual(results['text_length'], len(text))
        self.assertEqual(results['citations_found'], 1)
        self.assertTrue(len(results['citations']) > 0)
        
        # Check citation details
        citation = results['citations'][0]
        self.assertIn('text', citation)
        self.assertIn('type', citation)
        self.assertNotIn('verification', citation)  # No verification
    
    def test_process_text_with_verification(self):
        """Test text processing with verification."""
        text = "The case Miranda v. Arizona, 384 U.S. 436 (1966)."
        results = self.processor.process_text(text, verify=True)
        
        self.assertEqual(results['citations_found'], 1)
        
        # Check verification was attempted (even if it fails due to no network)
        citation = results['citations'][0]
        self.assertIn('verification', citation)
    
    def test_process_file(self):
        """Test file processing."""
        # Create a temporary test file
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Legal case: Marbury v. Madison, 5 U.S. 137 (1803).")
            temp_file = f.name
        
        try:
            results = self.processor.process_file(temp_file, verify=False)
            
            self.assertEqual(results['status'], 'success')
            self.assertEqual(results['file_path'], temp_file)
            self.assertEqual(results['citations_found'], 1)
        finally:
            os.unlink(temp_file)
    
    def test_process_nonexistent_file(self):
        """Test processing a nonexistent file."""
        results = self.processor.process_file('/nonexistent/file.txt', verify=False)
        
        self.assertEqual(results['status'], 'error')
        self.assertIn('error', results)
        self.assertEqual(results['citations_found'], 0)
    
    def test_empty_text(self):
        """Test processing empty text."""
        results = self.processor.process_text('', verify=False)
        
        self.assertEqual(results['text_length'], 0)
        self.assertEqual(results['citations_found'], 0)
        self.assertEqual(len(results['citations']), 0)
    
    def test_multiple_citations_in_text(self):
        """Test processing text with multiple citations."""
        text = """
        The cases Roe v. Wade, 410 U.S. 113 (1973) and 
        Brown v. Board of Education, 347 U.S. 483 (1954)
        are landmark Supreme Court decisions.
        """
        results = self.processor.process_text(text, verify=False)
        
        self.assertEqual(results['citations_found'], 2)
        
        # Verify both citations were extracted
        citation_texts = [c['text'] for c in results['citations']]
        self.assertTrue(any('410 U.S. 113' in str(c) for c in citation_texts))
        self.assertTrue(any('347 U.S. 483' in str(c) for c in citation_texts))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_end_to_end_extraction(self):
        """Test complete extraction pipeline."""
        processor = LegalCitationProcessor()
        
        text = """
        In the landmark case of Brown v. Board of Education, 347 U.S. 483 (1954),
        the Supreme Court ruled that racial segregation in public schools was 
        unconstitutional. This overturned the precedent set in Plessy v. Ferguson,
        163 U.S. 537 (1896), which had established the "separate but equal" doctrine.
        """
        
        results = processor.process_text(text, verify=False)
        
        # Should find both citations
        self.assertEqual(results['citations_found'], 2)
        
        # Check that both citations have proper metadata
        for citation in results['citations']:
            self.assertIn('metadata', citation)
            metadata = citation['metadata']
            self.assertIsNotNone(metadata.get('volume'))
            self.assertIsNotNone(metadata.get('reporter'))
            self.assertIsNotNone(metadata.get('page'))
            self.assertIsNotNone(metadata.get('year'))


if __name__ == '__main__':
    unittest.main()
