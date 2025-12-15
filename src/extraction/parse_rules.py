"""
Extracts text from DPDP PDFs using PyMuPDF (fitz)
"""

import fitz  # PyMuPDF
from pathlib import Path
import sys
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Paths
RAW_DATA_PATH = project_root / "data" / "raw"
PROCESSED_DATA_PATH = project_root / "data" / "processed"

def extract_text_from_pdf(pdf_path: Path) -> dict:
    """
    Extract text from PDF page by page
    Returns a dictionary with the total number of pages and the text of each page
    """
    try:
        doc = fitz.open(pdf_path)
        
        result = {
            'filename': pdf_path.name,
            'total_pages': len(doc),
            'pages': []
        }
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            result['pages'].append({
                'page_num': page_num + 1,
                'text': text
            })
            
            # Progress indicator
            if (page_num + 1) % 5 == 0:
                print(f"  Processed {page_num + 1}/{len(doc)} pages...")
        
        doc.close()
        return result
        
    except Exception as e:
        print(f"✗ Error extracting text: {e}")
        return None

def save_extracted_text(data: dict, output_filename: str):
    """
    Save extracted text to JSON and TXT files
    
    Args:
        data: Extraction result dictionary
        output_filename: Base filename (without extension)
    """
    # Save as JSON (structured)
    json_path = PROCESSED_DATA_PATH / f"{output_filename}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved JSON: {json_path.name}")
    
    # Save as TXT (all text combined)
    txt_path = PROCESSED_DATA_PATH / f"{output_filename}.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        for page in data['pages']:
            f.write(f"\n{'='*70}\n")
            f.write(f"PAGE {page['page_num']}\n")
            f.write(f"{'='*70}\n\n")
            f.write(page['text'])
            f.write("\n")
    print(f"  ✓ Saved TXT: {txt_path.name}")
    
    # Save summary
    total_chars = sum(len(page['text']) for page in data['pages'])
    print(f"  Total pages: {data['total_pages']}")
    print(f"  Total characters: {total_chars:,}")

def main():
    """Main execution"""
    print("=" * 70)
    print("DPDPA PDF Text Extraction")
    print("=" * 70)
    print()
    
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    
    # PDFs to process
    pdfs = [
        {
            "filename": "DPDP_Rules_2025_English_only.pdf",
            "output": "rules_2025_extracted",
            "description": "DPDP Rules 2025"
        },
        {
            "filename": "DPDPA_2023_official.pdf",
            "output": "act_2023_extracted",
            "description": "DPDP Act 2023"
        }
    ]
    
    # Processing PDFs
    for pdf_info in pdfs:
        pdf_path = RAW_DATA_PATH / pdf_info['filename']
        
        print(f"Processing: {pdf_info['description']}")
        print(f"File: {pdf_path.name}")
        
        if not pdf_path.exists():
            print(f"✗ File not found: {pdf_path}")
            print(f"  Run: python src/extraction/download_pdfs.py")
            print()
            continue
        
        # Text extraction
        data = extract_text_from_pdf(pdf_path)
        
        if data:
            # Save results
            save_extracted_text(data, pdf_info['output'])
            print()
        else:
            print(f"✗ Failed to extract text from {pdf_info['filename']}")
            print()
    
    # Final summary
    print("=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print()
    print("Output files in: data/processed/")
    print("  - rules_2025_extracted.json")
    print("  - rules_2025_extracted.txt")
    print("  - act_2023_extracted.json")
    print("  - act_2023_extracted.txt")
    print()
    print("Next step: python src/extraction/extract_requirements.py")

if __name__ == "__main__":
    main()