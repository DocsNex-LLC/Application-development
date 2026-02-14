#!/usr/bin/env python3
"""
Comprehensive demonstration of the legal citation system capabilities.
This script showcases all features of the citation processor.
"""

import json
from citation_processor import LegalCitationProcessor, CitationExtractor, CitationVerifier


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"{title:^70}")
    print('=' * 70)


def demo_basic_extraction():
    """Demonstrate basic citation extraction."""
    print_section("BASIC CITATION EXTRACTION")
    
    extractor = CitationExtractor()
    
    text = """
    Important Supreme Court cases include:
    - Roe v. Wade, 410 U.S. 113 (1973)
    - Brown v. Board of Education, 347 U.S. 483 (1954)
    - Marbury v. Madison, 5 U.S. 137 (1803)
    - Miranda v. Arizona, 384 U.S. 436 (1966)
    """
    
    print(f"\nInput Text:\n{text}")
    
    citations = extractor.extract_citations(text)
    
    print(f"\n✓ Found {len(citations)} citations:\n")
    for i, citation in enumerate(citations, 1):
        formatted = extractor.format_citation(citation)
        meta = formatted.get('metadata', {})
        
        print(f"{i}. Citation: {formatted['text']}")
        print(f"   Type: {formatted['type']}")
        if meta:
            print(f"   Volume: {meta.get('volume')}, "
                  f"Reporter: {meta.get('reporter')}, "
                  f"Page: {meta.get('page')}")
            print(f"   Year: {meta.get('year')}, Court: {meta.get('court')}")
            if meta.get('plaintiff') and meta.get('defendant'):
                print(f"   Parties: {meta.get('plaintiff')} v. {meta.get('defendant')}")
        print()


def demo_various_citation_formats():
    """Demonstrate extraction of various citation formats."""
    print_section("VARIOUS CITATION FORMATS")
    
    extractor = CitationExtractor()
    
    examples = [
        ("Supreme Court", "410 U.S. 113 (1973)"),
        ("Federal Reporter", "123 F.3d 456 (9th Cir. 2000)"),
        ("Federal Supplement", "789 F. Supp. 2d 123 (S.D.N.Y. 2011)"),
        ("State Reporter", "123 Cal. App. 4th 789 (2005)"),
        ("Atlantic Reporter", "456 A.2d 789 (N.J. 1983)"),
    ]
    
    for label, citation_text in examples:
        citations = extractor.extract_citations(citation_text)
        status = "✓" if citations else "✗"
        print(f"{status} {label:20} - {citation_text}")
        if citations:
            formatted = extractor.format_citation(citations[0])
            print(f"   Groups: {formatted.get('groups', {})}")
        print()


def demo_file_processing():
    """Demonstrate file processing."""
    print_section("FILE PROCESSING")
    
    processor = LegalCitationProcessor()
    
    # Create a sample legal document
    sample_file = "/tmp/legal_opinion_sample.txt"
    
    content = """
    SUPREME COURT OF THE UNITED STATES
    
    Opinion Summary
    
    In this case, we consider whether the precedent established in 
    Brown v. Board of Education, 347 U.S. 483 (1954), applies to the 
    present circumstances. The appellant cites Miranda v. Arizona, 
    384 U.S. 436 (1966), in support of their argument.
    
    The Court also notes the holding in Marbury v. Madison, 5 U.S. 137 (1803),
    which established the principle of judicial review. More recently,
    Citizens United v. FEC, 558 U.S. 310 (2010), addressed campaign finance.
    """
    
    with open(sample_file, 'w') as f:
        f.write(content)
    
    print(f"Processing file: {sample_file}\n")
    
    results = processor.process_file(sample_file, verify=False)
    
    print(f"Status: {results['status']}")
    print(f"Found {results['citations_found']} citations:\n")
    
    for i, citation in enumerate(results['citations'], 1):
        meta = citation.get('metadata', {})
        print(f"{i}. {citation['text']}")
        if meta.get('year'):
            print(f"   Year: {meta['year']}, Court: {meta.get('court', 'N/A')}")
        if meta.get('plaintiff'):
            print(f"   Case: {meta['plaintiff']} v. {meta.get('defendant', 'N/A')}")
        print()


def demo_processor_features():
    """Demonstrate full processor features."""
    print_section("FULL PROCESSOR FEATURES")
    
    processor = LegalCitationProcessor()
    
    text = """
    This legal memorandum discusses the principles established in 
    Roe v. Wade, 410 U.S. 113 (1973), and how they relate to 
    subsequent cases including Planned Parenthood v. Casey, 505 U.S. 833 (1992).
    """
    
    print(f"Input Text:\n{text}\n")
    
    # Process without verification
    print("Processing without API verification...")
    results = processor.process_text(text, verify=False)
    
    print(f"\nResults:")
    print(f"  Text length: {results['text_length']} characters")
    print(f"  Citations found: {results['citations_found']}")
    
    print(f"\nCitations extracted:")
    for citation in results['citations']:
        meta = citation.get('metadata', {})
        print(f"\n  • {citation['text']}")
        print(f"    Type: {citation['type']}")
        if meta:
            print(f"    Metadata: Volume {meta.get('volume')}, "
                  f"Reporter {meta.get('reporter')}, "
                  f"Page {meta.get('page')}")


def demo_api_features():
    """Demonstrate API verification features (structure only)."""
    print_section("API VERIFICATION FEATURES")
    
    print("The system supports CourtListener API verification:")
    print("\n1. Citation Verification")
    print("   - Checks if citation exists in the database")
    print("   - Returns match count and confidence")
    
    print("\n2. Detailed Case Information")
    print("   - Case name and parties")
    print("   - Court and jurisdiction")
    print("   - Filing date and status")
    print("   - Direct URL to full opinion")
    
    print("\n3. API Configuration")
    print("   - Set COURTLISTENER_API_TOKEN in .env file")
    print("   - Free API tokens available at:")
    print("     https://www.courtlistener.com/api/rest-info/")
    
    print("\nExample usage with API:")
    print("  processor = LegalCitationProcessor()")
    print("  results = processor.process_text(text, verify=True)")
    print("  # Results include verification status and case details")


def demo_error_handling():
    """Demonstrate error handling."""
    print_section("ERROR HANDLING")
    
    processor = LegalCitationProcessor()
    
    test_cases = [
        ("Empty text", ""),
        ("No citations", "This is a document without any legal citations."),
        ("Invalid file", "/nonexistent/file.txt"),
    ]
    
    print("Testing error handling:\n")
    
    # Test empty text
    print("1. Empty text:")
    results = processor.process_text("", verify=False)
    print(f"   ✓ Handled gracefully - found {results['citations_found']} citations\n")
    
    # Test text without citations
    print("2. Text without citations:")
    results = processor.process_text("This is plain text.", verify=False)
    print(f"   ✓ Handled gracefully - found {results['citations_found']} citations\n")
    
    # Test invalid file
    print("3. Invalid file path:")
    results = processor.process_file("/invalid/path.txt", verify=False)
    print(f"   ✓ Handled gracefully - status: {results['status']}")
    if 'error' in results:
        print(f"   Error captured: {results['error'][:50]}...\n")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("LEGAL CITATION IDENTIFICATION AND VERIFICATION SYSTEM".center(70))
    print("Comprehensive Feature Demonstration".center(70))
    print("=" * 70)
    
    print("\nThis demonstration showcases the capabilities of the system")
    print("built with FreeLawProject's eyecite and CourtListener API.\n")
    
    try:
        demo_basic_extraction()
        demo_various_citation_formats()
        demo_file_processing()
        demo_processor_features()
        demo_api_features()
        demo_error_handling()
        
        print_section("DEMONSTRATION COMPLETE")
        print("\n✓ All features demonstrated successfully!")
        print("\nFor more information, see:")
        print("  - README.md for full documentation")
        print("  - example_usage.py for code examples")
        print("  - test_citation_processor.py for test cases")
        
    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
