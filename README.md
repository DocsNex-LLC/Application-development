# Legal Citation Identification and Verification System

An application for identifying legal citations in documents and websites using FreeLawProject's [eyecite](https://github.com/freelawproject/eyecite) library and verifying them through [CourtListener's Legal Citation API](https://www.courtlistener.com/help/api/rest/citations/).

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run quick test
python3 quick_test.py

# Try examples
python3 example_usage.py

# See full demo
python3 demo.py
```

## Features

- **Citation Extraction**: Automatically identify legal citations in text, documents, or websites
- **Citation Verification**: Verify citations are real using CourtListener's comprehensive legal database
- **Multiple Input Sources**: Process plain text, files, or web pages
- **Detailed Metadata**: Extract citation details including volume, reporter, page numbers, and years
- **API Integration**: Leverage CourtListener's REST API for validation and additional case information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DocsNex-LLC/Application-development.git
cd Application-development
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API access (optional, but required for verification):
```bash
cp .env.example .env
# Edit .env and add your CourtListener API token
```

To get a free API token:
- Visit https://www.courtlistener.com/api/rest-info/
- Create a free account
- Generate an API token

## Usage

### Basic Usage - Extract Citations

```python
from citation_processor import LegalCitationProcessor

# Initialize processor
processor = LegalCitationProcessor()

# Extract citations from text
text = "The Supreme Court ruled in Roe v. Wade, 410 U.S. 113 (1973)."
results = processor.process_text(text, verify=False)

print(f"Found {results['citations_found']} citations")
for citation in results['citations']:
    print(f"- {citation['text']}")
```

### Verify Citations with CourtListener API

```python
# Verify citations (requires API token in .env)
results = processor.process_text(text, verify=True)

for citation in results['citations']:
    if 'verification' in citation:
        print(f"Citation: {citation['text']}")
        print(f"Valid: {citation['verification']['is_valid']}")
        
        if 'details' in citation:
            details = citation['details']
            print(f"Case: {details['case_name']}")
            print(f"Court: {details['court']}")
            print(f"URL: {details['url']}")
```

### Process Files

```python
# Extract citations from a file
results = processor.process_file('legal_document.txt', verify=True)
```

### Process Websites

```python
# Extract citations from a webpage
results = processor.process_url('https://example.com/legal-opinion', verify=True)
```

### Run Examples

```bash
python example_usage.py
```

## API Reference

### `LegalCitationProcessor`

Main class for processing and verifying legal citations.

**Methods:**
- `process_text(text: str, verify: bool = True)` - Extract citations from text
- `process_file(file_path: str, verify: bool = True)` - Extract citations from a file
- `process_url(url: str, verify: bool = True)` - Extract citations from a webpage

### `CitationExtractor`

Handles citation extraction using eyecite.

**Methods:**
- `extract_citations(text: str)` - Extract citation objects from text
- `format_citation(citation)` - Format citation object as dictionary

### `CitationVerifier`

Handles citation verification using CourtListener API.

**Methods:**
- `verify_citation(citation_text: str)` - Verify if citation exists
- `get_citation_details(citation_text: str)` - Get detailed citation information

## Citation Types Supported

The system can identify various types of legal citations:

- **Full Case Citations**: Complete citations (e.g., "410 U.S. 113 (1973)")
- **Short Case Citations**: Abbreviated references (e.g., "410 U.S., at 113")
- **Supra Citations**: References to previously cited cases (e.g., "Smith, supra")
- **Id. Citations**: References to immediately preceding citation

## Dependencies

- **eyecite**: Legal citation extraction library
- **requests**: HTTP library for API calls
- **beautifulsoup4**: HTML parsing for website processing
- **lxml**: XML/HTML parser
- **python-dotenv**: Environment variable management

## Project Structure

```
Application-development/
├── citation_processor.py       # Main citation processing module
├── example_usage.py           # Example usage demonstrations
├── demo.py                    # Comprehensive feature demonstration
├── quick_test.py              # Quick verification test
├── test_citation_processor.py # Unit tests (14 test cases)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
├── CONFIGURATION.md          # Detailed configuration guide
└── README.md                 # This file
```

## Additional Resources

- **[CONFIGURATION.md](CONFIGURATION.md)** - Detailed setup and configuration guide
- **[example_usage.py](example_usage.py)** - Practical code examples
- **[demo.py](demo.py)** - Comprehensive feature demonstrations
- **[test_citation_processor.py](test_citation_processor.py)** - Test suite with examples
```

## How It Works

1. **Text Input**: The system accepts text from various sources (strings, files, URLs)
2. **Citation Extraction**: Uses eyecite's pattern matching to identify legal citations
3. **Parsing**: Extracts citation components (volume, reporter, page, year)
4. **Verification**: Queries CourtListener API to verify citation validity
5. **Enrichment**: Retrieves additional case metadata (case name, court, filing date)
6. **Results**: Returns structured data with all extracted and verified information

## CourtListener API

This application uses the [CourtListener REST API v3](https://www.courtlistener.com/help/api/rest/) for citation verification. CourtListener is a free, open-source legal research website containing millions of legal opinions from federal and state courts.

### API Features Used:
- Citation search and validation
- Case metadata retrieval
- Court information
- Filing dates and case status

## License

This project is open source and available for use in legal research, document analysis, and citation verification applications.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Acknowledgments

- [Free Law Project](https://free.law/) for the eyecite library and CourtListener API
- [eyecite](https://github.com/freelawproject/eyecite) - Citation extraction library
- [CourtListener](https://www.courtlistener.com/) - Legal opinion database and API
