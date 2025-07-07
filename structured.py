from browser_use.llm import ChatOpenAI
from browser_use import Agent
from browser_use import Agent, BrowserSession, Controller
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
load_dotenv()

import asyncio

class JobSearchProfile(BaseModel):
    name: str
    skills: list[str]
    experience_years: int
    location: str

class JobSearch(BaseModel):
    jobsearch: List[JobSearchProfile]

controller = Controller(output_model=JobSearch)


browser_session = BrowserSession(
    # Path to a specific Chromium-based executable (optional)
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    
    user_data_dir='~/.config/browseruse/profiles/default', 
)

llm = ChatOpenAI(model="gpt-4o")



async def main():
    agent = Agent(
        task=""" first Go to linkedin and find for me jobs that matches my profile the jobs should have been posted in the last 24 hours.Then next Search for 'MLOps learning resources' and 'MLOps best practices' on Google.
        Find the top 10 learning resources that are freely accessible (no login required).
        For each resource, provide:
        1. Title of the resource
        2. URL
        3. Brief summary of what it covers (2-3 sentences)
        4. Type (course, tutorial, documentation, blog post, etc.)
        5. Difficulty level (beginner, intermediate, advanced)
        
        Focus on high-quality, reputable sources like:
        - Official documentation
        - University courses
        - Well-known tech blogs
        - Open source projects
        - Industry publications
        
        Ignore sources that require paid subscriptions or mandatory registration.""",
        llm=llm,
        browser=browser_session,
        controller=controller,
    )
    result = await agent.run()
    print(result.final_result())
    await browser_session.close()

asyncio.run(main())