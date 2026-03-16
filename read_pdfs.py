import pdfplumber
import sys

def read_pdf(filename):
    print(f"\n{'='*80}")
    print(f"Reading: {filename}")
    print('='*80)
    
    try:
        with pdfplumber.open(filename) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\n--- Page {page_num} ---")
                
                # Extract text
                text = page.extract_text()
                if text:
                    print("\nText Content:")
                    print(text)
                
                # Extract tables
                tables = page.extract_tables()
                if tables:
                    print(f"\nFound {len(tables)} table(s)")
                    for i, table in enumerate(tables, 1):
                        print(f"\nTable {i}:")
                        for row in table:
                            print(row)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    files = [
        'batting_leaderboard_1828126.pdf',
        'bowling_leaderboard_1828126.pdf',
        'mvp_leaderboard_1828126.pdf'
    ]
    
    for file in files:
        read_pdf(file)
