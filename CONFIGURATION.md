# Configuration Guide

## Getting Started

### 1. Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. CourtListener API Setup (Optional but Recommended)

The citation verification feature requires a CourtListener API token.

#### Obtaining an API Token:

1. Visit [CourtListener](https://www.courtlistener.com/)
2. Create a free account
3. Navigate to [API Settings](https://www.courtlistener.com/api/rest-info/)
4. Generate an API token

#### Configuring the Token:

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your token:

```
COURTLISTENER_API_TOKEN=3149ff4a1dfd96b754c75d1afc4366e2177c1f2f<img width="318" height="18" alt="image" src="https://github.com/user-attachments/assets/91c2657f-aa9c-4621-90f3-e935e1440e76" />

```

### 3. Verification

Run the quick test to verify everything is working:

```bash
python3 quick_test.py
```

## Usage Modes

### Without API Token

The system can extract and parse citations without an API token:

```python
from citation_processor import LegalCitationProcessor

processor = LegalCitationProcessor()
results = processor.process_text(text, verify=False)
```

**Capabilities:**
- ✓ Extract citations from text
- ✓ Parse citation components (volume, reporter, page, year)
- ✓ Identify case parties
- ✗ Verify citation validity
- ✗ Get case details from database

### With API Token

With a CourtListener API token, you get full verification:

```python
processor = LegalCitationProcessor()
results = processor.process_text(text, verify=True)
```

**Additional Capabilities:**
- ✓ Verify citation exists in database
- ✓ Get official case name
- ✓ Retrieve court and jurisdiction
- ✓ Access filing date
- ✓ Get link to full opinion

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `COURTLISTENER_API_TOKEN` | No | API token for citation verification |

## API Rate Limits

CourtListener has the following rate limits:

- **Free accounts**: 5,000 API calls per day
- **Authenticated**: Higher limits available

To avoid rate limit issues:
- Use `verify=False` when verification isn't needed
- Cache results when processing large documents
- Consider batch processing

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### API Connection Issues

If verification fails:
1. Check your internet connection
2. Verify your API token is correct
3. Check CourtListener service status
4. The system will gracefully handle API failures

### Citation Not Found

If a valid citation isn't extracted:
- Ensure proper formatting (e.g., "410 U.S. 113")
- Check the citation uses a supported reporter
- Some citation formats may not be recognized

## Supported Citation Formats

The system recognizes citations in these reporters:

- **Federal:**
  - U.S. Reports: `410 U.S. 113`
  - Federal Reporter: `123 F.3d 456`
  - Federal Supplement: `789 F. Supp. 2d 123`

- **State:**
  - California: `123 Cal. App. 4th 789`
  - New York: `123 N.Y.2d 456`
  - Plus many others

- **Regional:**
  - Atlantic: `456 A.2d 789`
  - Pacific: `123 P.3d 456`
  - And more

For a complete list, see the [eyecite documentation](https://github.com/freelawproject/eyecite).

## Performance Tips

### Processing Large Documents

For large documents:

```python
# Process in chunks if memory is a concern
def process_large_file(file_path, chunk_size=1000000):
    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            results = processor.process_text(chunk, verify=False)
            # Handle results...
```

### Batch Processing

For multiple files:

```python
import os

for filename in os.listdir('legal_docs/'):
    if filename.endswith('.txt'):
        results = processor.process_file(
            os.path.join('legal_docs/', filename),
            verify=True
        )
        # Process results...
```

## Examples

See these files for more examples:
- `example_usage.py` - Basic usage examples
- `demo.py` - Comprehensive feature demonstration
- `test_citation_processor.py` - Test cases showing various scenarios

## Support

For issues or questions:
- Check the README.md for general documentation
- Review test cases in test_citation_processor.py
- Consult eyecite documentation: https://github.com/freelawproject/eyecite
- CourtListener API docs: https://www.courtlistener.com/help/api/
