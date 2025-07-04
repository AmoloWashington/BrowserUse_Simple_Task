#!/usr/bin/env python3
"""
Simple runner script for the browser automation tasks.
This script will control a Chrome browser to:
1. Scrape Amazon for wireless earbuds deals
2. Scrape LinkedIn for remote software engineer and AI engineer jobs
"""

import asyncio
import sys
from browser_scraper_simple import main

if __name__ == "__main__":
    print("🚀 Starting Browser Automation Tasks")
    print("This will open Chrome and scrape Amazon + LinkedIn")
    print("-" * 50)

    try:
        result = asyncio.run(main())
        print("\n✅ All tasks completed successfully!")

        # Summary
        products_count = len(result.get("products", []))
        jobs_count = len(result.get("jobs", []))

        print(f"📊 Summary:")
        print(f"   • Amazon products with discounts: {products_count}")
        print(f"   • LinkedIn job listings: {jobs_count}")
        print(f"   • Results saved to: scraping_results.json")

    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
