from pydantic import BaseModel
from browser_use import Agent, Controller
import asyncio
from dotenv import load_dotenv
from llm_adapter import OpenAIAdapter
import os
import json

load_dotenv()

# Set environment variables for browser-use
os.environ["BROWSER_USE_TIMEOUT"] = "120"  # Longer timeout for complex tasks
os.environ["BROWSER_USE_BROWSER"] = "chrome"
os.environ["BROWSER_USE_DEBUG"] = "true"

class Product(BaseModel):
    title: str
    price: str
    old_price: str
    link: str

class Job(BaseModel):
    title: str
    company: str
    location: str
    remote: bool
    posted: str
    link: str

class ScrapingResult(BaseModel):
    products: list[Product]
    jobs: list[Job]

async def main():
    """Main function to run both scraping tasks sequentially"""
    print("Starting browser automation tasks...")
    
    all_products = []
    all_jobs = []
    
    try:
        # Task 1: Amazon Products
        print("\n" + "="*50)
        print("PART 1: AMAZON DEALS")
        print("="*50)
        
        amazon_task = """
        1. Navigate to https://www.amazon.com
        2. Search for "wireless earbuds" in the search box
        3. Wait for the results page to fully load
        4. From the first page of results, find exactly 5 products that show clear discounts 
           (products with both a current price and a higher crossed-out original price)
        5. Skip sponsored listings, ads, or any products without visible discounts
        
        For each of the 5 discounted products, extract:
        - title: complete product name/title
        - price: current discounted price (e.g., "$29.99")
        - old_price: original higher price that's crossed out (e.g., "$49.99")
        - link: full URL to the product page
        
        Return exactly 5 products with genuine discount pricing.
        """
        
        amazon_controller = Controller(output_model=ScrapingResult)
        amazon_model = OpenAIAdapter(model="gpt-4")
        amazon_agent = Agent(task=amazon_task, llm=amazon_model, controller=amazon_controller)
        
        print("Executing Amazon scraping...")
        amazon_history = await amazon_agent.run()
        amazon_result = amazon_history.final_result()
        
        if amazon_result:
            amazon_parsed = ScrapingResult.model_validate_json(amazon_result)
            all_products = amazon_parsed.products[:5]  # Ensure only 5 products
            print(f"✓ Found {len(all_products)} Amazon products with discounts")
        else:
            print("✗ No Amazon results found")
            
    except Exception as e:
        print(f"✗ Error scraping Amazon: {e}")
    
    try:
        # Task 2: LinkedIn Jobs
        print("\n" + "="*50)
        print("PART 2: LINKEDIN JOBS")
        print("="*50)
        
        linkedin_task = """
        1. Navigate to https://www.linkedin.com/jobs
        2. Search for jobs with titles containing "Remote Software Engineer" OR "AI Engineer"
        3. Wait for job listings to load completely
        4. From the search results, extract the first 5 real job listings 
           (skip promoted/sponsored posts, ads, or expired listings)
        
        For each of the 5 job listings, extract:
        - title: exact job title
        - company: company name
        - location: job location (e.g., "Remote", "New York, NY", etc.)
        - remote: true if job allows remote work, false otherwise
        - posted: posting time (e.g., "2 days ago", "1 week ago")
        - link: direct URL to the job posting
        
        Return exactly 5 current, real job postings.
        """
        
        linkedin_controller = Controller(output_model=ScrapingResult)
        linkedin_model = OpenAIAdapter(model="gpt-4")
        linkedin_agent = Agent(task=linkedin_task, llm=linkedin_model, controller=linkedin_controller)
        
        print("Executing LinkedIn scraping...")
        linkedin_history = await linkedin_agent.run()
        linkedin_result = linkedin_history.final_result()
        
        if linkedin_result:
            linkedin_parsed = ScrapingResult.model_validate_json(linkedin_result)
            all_jobs = linkedin_parsed.jobs[:5]  # Ensure only 5 jobs
            print(f"✓ Found {len(all_jobs)} LinkedIn job listings")
        else:
            print("✗ No LinkedIn results found")
            
    except Exception as e:
        print(f"✗ Error scraping LinkedIn: {e}")
    
    # Create final combined result
    final_result = {
        "products": [product.model_dump() for product in all_products],
        "jobs": [job.model_dump() for job in all_jobs]
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
