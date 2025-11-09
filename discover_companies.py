"""
Company Discovery Tool - Finds new companies to add to your scraper!

This script scrapes job boards and startup directories to discover companies
posting EE/hardware/semiconductor internships. Run this periodically to find
new companies to add to your scraper.

Usage:
    python discover_companies.py
"""

import os
from scrapers.company_discovery_scraper import CompanyDiscoveryScraper


def main():
    print("="*70)
    print("🔍 COMPANY DISCOVERY TOOL")
    print("="*70)
    print("\nSearching job boards and startup directories for companies")
    print("posting EE/Hardware/Semiconductor internships...\n")

    # Create data directory
    os.makedirs('data', exist_ok=True)

    # Initialize discovery scraper
    scraper = CompanyDiscoveryScraper()

    # Run discovery
    keywords = [
        "hardware engineer",
        "electrical engineer",
        "semiconductor",
        "circuit design",
        "VLSI"
    ]

    scraper.scrape(keywords)

    print("\n✅ Discovery complete!")
    print("\nNext steps:")
    print("1. Check 'data/discovered_companies.json' for the full list")
    print("2. Research interesting companies")
    print("3. Add promising companies to 'scrapers/company_scraper.py'")
    print("4. Run the main scraper to start tracking their jobs!")

    print("\n💡 Tip: Run this script monthly to discover new startups and companies!")


if __name__ == "__main__":
    main()
