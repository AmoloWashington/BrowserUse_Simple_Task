from pydantic import BaseModel
from browser_use import Agent, Controller
import asyncio
from dotenv import load_dotenv
from llm_adapter import OpenAIAdapter
import os
import json

load_dotenv()

# Set environment variables for browser-use
os.environ["BROWSER_USE_TIMEOUT"] = "60"
os.environ["BROWSER_USE_BROWSER"] = "chromium"
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

class AmazonProducts(BaseModel):
    products: list[Product]

class LinkedInJobs(BaseModel):
    jobs: list[Job]

class FinalResult(BaseModel):
    products: list[Product]
    jobs: list[Job]

async def scrape_amazon_deals():
    """Scrape Amazon wireless earbuds deals"""
    print("Starting Amazon deals scraping...")
    
    task = """
    Navigate to https://www.amazon.com and search for "wireless earbuds".
    Wait for the results to fully load.
    From the first page of results, find 5 products that have visible discounts 
    (showing both a current price and a higher old/original price crossed out).
    
    For each discounted product, extract:
    - title: the complete product name
    - price: the current discounted price (just the number with currency symbol)
    - old_price: the original price before discount (crossed out price)
    - link: the direct URL link to the product page
    
    Skip sponsored products, ads, or any listings without clear discount pricing.
    Only include genuine product listings with visible price reductions.
    """
    
    controller = Controller(output_model=AmazonProducts)
    model = OpenAIAdapter(model="gpt-4")
    agent = Agent(task=task, llm=model, controller=controller)
    
    history = await agent.run()
    result = history.final_result()
    
    if result:
        parsed = AmazonProducts.model_validate_json(result)
        return parsed.products
    return []

async def scrape_linkedin_jobs():
    """Scrape LinkedIn job listings"""
    print("Starting LinkedIn jobs scraping...")
    
    task = """
    Navigate to https://www.linkedin.com/jobs and search for jobs with titles 
    "Remote Software Engineer" OR "AI Engineer".
    Wait for the job listings to fully load.
    
    From the search results, extract the first 5 real job listings 
    (skip ads, promoted posts, or expired listings).
    
    For each job listing, extract:
    - title: the exact job title
    - company: the name of the hiring company
    - location: the job location (e.g., "Remote", "San Francisco, CA", etc.)
    - remote: true if the job is remote/work-from-home, false otherwise
    - posted: when the job was posted (e.g., "3 days ago", "1 week ago")
    - link: the direct URL to the job posting
    
    Make sure to get real, current job postings only.
    """
    
    controller = Controller(output_model=LinkedInJobs)
    model = OpenAIAdapter(model="gpt-4")
    agent = Agent(task=task, llm=model, controller=controller)
    
    history = await agent.run()
    result = history.final_result()
    
    if result:
        parsed = LinkedInJobs.model_validate_json(result)
        return parsed.jobs
    return []

async def main():
    """Main function to run both scraping tasks"""
    print("Starting browser automation tasks...")
    
    try:
        # Run both tasks concurrently for efficiency
        amazon_task = scrape_amazon_deals()
        linkedin_task = scrape_linkedin_jobs()
        
        products, jobs = await asyncio.gather(amazon_task, linkedin_task)
        
        # Create final result
        final_result = {
            "products": [product.model_dump() for product in products],
            "jobs": [job.model_dump() for job in jobs]
        }
        
        # Print results
        print("\n" + "="*50)
        print("FINAL RESULTS")
        print("="*50)
        print(json.dumps(final_result, indent=2))
        
        # Optionally save to file
        with open("scraping_results.json", "w") as f:
            json.dump(final_result, f, indent=2)
        
        print(f"\nResults saved to scraping_results.json")
        print(f"Found {len(products)} Amazon products and {len(jobs)} LinkedIn jobs")
        
        return final_result
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return {"products": [], "jobs": [], "error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())
