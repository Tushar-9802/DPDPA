"""
PDF Download Script
Verifies and downloads official DPDP documents
"""

import requests
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DPDP_RULES_2025_URL, DPDP_ACT_2023_URL

# PDF storage location
RAW_DATA_PATH = project_root / "data" / "raw"

def download_pdf(url: str, filename: str) -> bool:
    #Download PDF from URL to data/raw/

    file_path = RAW_DATA_PATH / filename
    
    # Check if file already exists
    if file_path.exists():
        file_size = file_path.stat().st_size
        print(f"✓ {filename} already exists ({file_size:,} bytes)")
        return True
    
    try:
        print(f"Downloading {filename}...")
        print(f"URL: {url}")
        
        # Download with streaming for large files
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Save to file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = file_path.stat().st_size
        print(f"✓ Downloaded {filename} ({file_size:,} bytes)")
        return True
        
    except requests.RequestException as e:
        print(f"✗ Download failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_pdfs() -> bool:
    #Verify both PDFs exist and are valid
    pdfs = [
        "DPDP_Rules_2025_English_only.pdf",
        "DPDPA_2023_official.pdf"
    ]
    
    all_present = True
    
    for pdf in pdfs:
        file_path = RAW_DATA_PATH / pdf
        if file_path.exists():
            size = file_path.stat().st_size
            if size > 1000:  # At least 1KB
                print(f"✓ {pdf} verified ({size:,} bytes)")
            else:
                print(f"⚠ {pdf} exists but seems too small ({size} bytes)")
                all_present = False
        else:
            print(f"✗ {pdf} missing")
            all_present = False
    
    return all_present

def main():
    """Main execution"""
    print("=" * 70)
    print("DPDPA PDF Download and Verification")
    print("=" * 70)
    print()
    
    # Ensure directory exists
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    print(f"Storage directory: {RAW_DATA_PATH}")
    print()
    
    # Define PDFs
    pdfs = [
        {
            "url": DPDP_RULES_2025_URL,
            "filename": "DPDP_Rules_2025_English_only.pdf",
            "description": "DPDP Rules 2025 (Official Notification)"
        },
        {
            "url": DPDP_ACT_2023_URL,
            "filename": "DPDPA_2023_official.pdf",
            "description": "DPDP Act 2023 (Official Gazette)"
        }
    ]
    
    # Download/verify PDFs
    results = []
    for pdf in pdfs:
        print(f"Processing: {pdf['description']}")
        success = download_pdf(pdf['url'], pdf['filename'])
        results.append(success)
        print()
    
    # Final verification
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    print()
    
    if verify_pdfs():
        print("✓ All PDFs present and verified")
        print()
        print("Ready for text extraction!")
        print("Next step: python src/extraction/parse_rules.py")
        return 0
    else:
        print("✗ Some PDFs missing or invalid")
        print()
        print("Please:")
        print("1. Check internet connection")
        print("2. Verify URLs in config/config.py")
        print("3. Or manually download PDFs to data/raw/")
        return 1

if __name__ == "__main__":
    sys.exit(main())