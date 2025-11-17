#!/usr/bin/env python3
"""
Example script demonstrating the legal citation extraction and verification system.
"""

import json
from citation_processor import LegalCitationProcessor


def print_results(results: dict, title: str):
    """Pretty print results."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print('=' * 60)
    print(json.dumps(results, indent=2, default=str))


def main():
    """Run examples of citation extraction and verification."""
    
    # Initialize the processor
    processor = LegalCitationProcessor()
    
    print("Legal Citation Identification and Verification System")
    print("Using FreeLawProject's eyecite and CourtListener API")
    
    # Example 1: Process text with citations
    print("\n\n" + "=" * 60)
    print("EXAMPLE 1: Processing text with legal citations")
    print("=" * 60)
    
    sample_text = """
    The Supreme Court's decision in Roe v. Wade, 410 U.S. 113 (1973), 
    was a landmark case. Later, in Planned Parenthood v. Casey, 505 U.S. 833 (1992),
    the Court reaffirmed the central holding of Roe. The case Miranda v. Arizona, 
    384 U.S. 436 (1966), established important rights for criminal defendants.
    """
    
    print(f"\nSample text:\n{sample_text}")
    
    # Extract citations without verification (faster)
    results_no_verify = processor.process_text(sample_text, verify=False)
    print(f"\nFound {results_no_verify['citations_found']} citations:")
    for i, citation in enumerate(results_no_verify['citations'], 1):
        print(f"  {i}. {citation['text']} (Type: {citation['type']})")
    
    # Example 2: Process with verification
    print("\n\n" + "=" * 60)
    print("EXAMPLE 2: Processing with CourtListener verification")
    print("=" * 60)
    print("\nNote: Verification requires a CourtListener API token")
    print("Set COURTLISTENER_API_TOKEN in .env file")
    
    results_with_verify = processor.process_text(sample_text, verify=True)
    
    for i, citation in enumerate(results_with_verify['citations'], 1):
        print(f"\n{i}. Citation: {citation['text']}")
        print(f"   Type: {citation['type']}")
        
        if 'verification' in citation:
            ver = citation['verification']
            print(f"   Valid: {ver['is_valid']}")
            print(f"   Matches found: {ver['count']}")
            
            if 'details' in citation:
                details = citation['details']
                print(f"   Case name: {details['case_name']}")
                print(f"   Court: {details['court']}")
                print(f"   Date filed: {details['date_filed']}")
                print(f"   URL: {details['url']}")
    
    # Example 3: Process a file
    print("\n\n" + "=" * 60)
    print("EXAMPLE 3: Processing a file")
    print("=" * 60)
    
    # Create a sample file
    sample_file = "/tmp/sample_legal_doc.txt"
    with open(sample_file, 'w') as f:
        f.write("""
        Legal Document Sample
        
        This document references several important cases:
        
        1. Brown v. Board of Education, 347 U.S. 483 (1954) - landmark civil rights case
        2. Marbury v. Madison, 5 U.S. 137 (1803) - established judicial review
        3. Citizens United v. FEC, 558 U.S. 310 (2010) - campaign finance case
        """)
    
    print(f"\nProcessing file: {sample_file}")
    file_results = processor.process_file(sample_file, verify=False)
    
    print(f"\nStatus: {file_results['status']}")
    print(f"Citations found: {file_results['citations_found']}")
    for i, citation in enumerate(file_results['citations'], 1):
        print(f"  {i}. {citation['text']}")
    
    # Example 4: Process a URL (demonstration - requires actual URL)
    print("\n\n" + "=" * 60)
    print("EXAMPLE 4: Processing a website URL")
    print("=" * 60)
    print("\nTo process a website:")
    print("  url_results = processor.process_url('https://example.com/legal-doc')")
    print("\nThis will extract citations from the webpage content.")
    
    print("\n\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nFor API verification, make sure to:")
    print("1. Copy .env.example to .env")
    print("2. Add your CourtListener API token")
    print("3. Get a free token at: https://www.courtlistener.com/api/rest-info/")


if __name__ == "__main__":
    main()
