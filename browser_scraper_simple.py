from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from llm_adapter import OpenAIAdapter
import os
import json
import re

load_dotenv()

# Set environment variables for browser-use
os.environ["BROWSER_USE_TIMEOUT"] = "120"
os.environ["BROWSER_USE_BROWSER"] = "chrome"
os.environ["BROWSER_USE_DEBUG"] = "true"

async def scrape_amazon_deals():
    """Scrape Amazon wireless earbuds deals"""
    print("Starting Amazon deals scraping...")
    
    task = """
    Navigate to https://www.amazon.com and search for "wireless earbuds".
    Wait for the results to fully load.
    From the first page of results, find exactly 5 products that have visible discounts 
    (showing both a current price and a higher crossed-out original price).
    Skip sponsored listings, ads, or any products without visible discounts.
    
    For each of the 5 discounted products, extract and return in this exact format:
    
    PRODUCT 1:
    Title: [complete product name]
    Price: [current discounted price like $29.99]
    Old Price: [original crossed-out price like $49.99]
    Link: [full URL to product page]
    
    PRODUCT 2:
    Title: [complete product name]
    Price: [current discounted price]
    Old Price: [original crossed-out price]
    Link: [full URL to product page]
    
    Continue for all 5 products...
    
    Make sure to only include genuine product listings with clear discount pricing visible on the page.
    """
    
    model = OpenAIAdapter(model="gpt-4")
    agent = Agent(task=task, llm=model)
    
    history = await agent.run()
    result = history.final_result()
    
    # Parse the text result into structured data
    products = []
    if result:
        lines = result.split('\n')
        current_product = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Title:'):
                current_product['title'] = line.replace('Title:', '').strip()
            elif line.startswith('Price:'):
                current_product['price'] = line.replace('Price:', '').strip()
            elif line.startswith('Old Price:'):
                current_product['old_price'] = line.replace('Old Price:', '').strip()
            elif line.startswith('Link:'):
                current_product['link'] = line.replace('Link:', '').strip()
                if all(key in current_product for key in ['title', 'price', 'old_price', 'link']):
                    products.append(current_product.copy())
                    current_product = {}
    
    return products[:5]  # Ensure only 5 products

async def scrape_linkedin_jobs():
    """Scrape LinkedIn job listings"""
    print("Starting LinkedIn jobs scraping...")
    
    task = """
    Navigate to https://www.linkedin.com/jobs and search for jobs with titles 
    "Remote Software Engineer" OR "AI Engineer".
    Wait for job listings to load completely.
    From the search results, extract the first 5 real job listings 
    (skip promoted/sponsored posts, ads, or expired listings).
    
    For each of the 5 job listings, extract and return in this exact format:
    
    JOB 1:
    Title: [exact job title]
    Company: [company name]
    Location: [job location like "Remote" or "New York, NY"]
    Remote: [true if remote work allowed, false otherwise]
    Posted: [posting time like "2 days ago"]
    Link: [direct URL to job posting]
    
    JOB 2:
    Title: [exact job title]
    Company: [company name]
    Location: [job location]
    Remote: [true/false]
    Posted: [posting time]
    Link: [direct URL to job posting]
    
    Continue for all 5 jobs...
    
    Make sure to get real, current job postings only.
    """
    
    model = OpenAIAdapter(model="gpt-4")
    agent = Agent(task=task, llm=model)
    
    history = await agent.run()
    result = history.final_result()
    
    # Parse the text result into structured data
    jobs = []
    if result:
        lines = result.split('\n')
        current_job = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Title:'):
                current_job['title'] = line.replace('Title:', '').strip()
            elif line.startswith('Company:'):
                current_job['company'] = line.replace('Company:', '').strip()
            elif line.startswith('Location:'):
                current_job['location'] = line.replace('Location:', '').strip()
            elif line.startswith('Remote:'):
                remote_text = line.replace('Remote:', '').strip().lower()
                current_job['remote'] = remote_text in ['true', 'yes', '1']
            elif line.startswith('Posted:'):
                current_job['posted'] = line.replace('Posted:', '').strip()
            elif line.startswith('Link:'):
                current_job['link'] = line.replace('Link:', '').strip()
                if all(key in current_job for key in ['title', 'company', 'location', 'remote', 'posted', 'link']):
                    jobs.append(current_job.copy())
                    current_job = {}
    
    return jobs[:5]  # Ensure only 5 jobs

async def main():
    """Main function to run both scraping tasks"""
    print("Starting browser automation tasks...")
    
    all_products = []
    all_jobs = []
    
    try:
        # Task 1: Amazon Products
        print("\n" + "="*50)
        print("PART 1: AMAZON DEALS")
        print("="*50)
        
        all_products = await scrape_amazon_deals()
        print(f"✓ Found {len(all_products)} Amazon products with discounts")
        
    except Exception as e:
        print(f"✗ Error scraping Amazon: {e}")
    
    try:
        # Task 2: LinkedIn Jobs  
        print("\n" + "="*50)
        print("PART 2: LINKEDIN JOBS")
        print("="*50)
        
        all_jobs = await scrape_linkedin_jobs()
        print(f"✓ Found {len(all_jobs)} LinkedIn job listings")
        
    except Exception as e:
        print(f"✗ Error scraping LinkedIn: {e}")
    
    # Create final combined result
    final_result = {
        "products": all_products,
        "jobs": all_jobs
    }
    
    # Display results
    print("\n" + "="*60)
    print("FINAL COMBINED RESULTS")
    print("="*60)
    print(json.dumps(final_result, indent=2))
    
    # Save results to file
    with open("scraping_results.json", "w") as f:
        json.dump(final_result, f, indent=2)
    
    print(f"\n✓ Results saved to scraping_results.json")
    print(f"✓ Total: {len(all_products)} products, {len(all_jobs)} jobs")
    
    return final_result

if __name__ == "__main__":
    asyncio.run(main())
