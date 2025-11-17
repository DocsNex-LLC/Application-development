#!/usr/bin/env python3
"""
Quick test script to verify the legal citation system is working.
Run this to ensure the installation is successful.
"""

import sys
from citation_processor import LegalCitationProcessor


def main():
    """Quick verification test."""
    print("Legal Citation System - Quick Test")
    print("=" * 50)
    
    try:
        # Initialize processor
        processor = LegalCitationProcessor()
        print("✓ System initialized successfully")
        
        # Test citation extraction
        test_text = "The Supreme Court ruled in Roe v. Wade, 410 U.S. 113 (1973)."
        results = processor.process_text(test_text, verify=False)
        
        if results['citations_found'] == 1:
            print("✓ Citation extraction working")
            citation = results['citations'][0]
            print(f"  Extracted: {citation['text']}")
            
            # Check metadata
            if citation.get('metadata', {}).get('year') == '1973':
                print("✓ Metadata parsing working")
            else:
                print("✗ Metadata parsing issue")
                return False
        else:
            print(f"✗ Expected 1 citation, found {results['citations_found']}")
            return False
        
        # Test file processing
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test case: 347 U.S. 483 (1954)")
            temp_file = f.name
        
        file_results = processor.process_file(temp_file, verify=False)
        
        if file_results['status'] == 'success' and file_results['citations_found'] == 1:
            print("✓ File processing working")
        else:
            print("✗ File processing issue")
            return False
        
        # Clean up
        import os
        os.unlink(temp_file)
        
        print("\n" + "=" * 50)
        print("All tests passed! System is ready to use.")
        print("=" * 50)
        print("\nTry running:")
        print("  python3 example_usage.py    - For usage examples")
        print("  python3 demo.py            - For full demonstration")
        print("  python3 -m unittest test_citation_processor - For unit tests")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
