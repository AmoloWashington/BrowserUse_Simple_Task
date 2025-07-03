from pydantic import BaseModel
from browser_use import Agent, Controller
import asyncio
from dotenv import load_dotenv
from llm_adapter import OpenAIAdapter
import os

load_dotenv()

# Set environment variables for browser-use
os.environ["BROWSER_USE_TIMEOUT"] = "60"
os.environ["BROWSER_USE_BROWSER"] = "chrome"

class Post(BaseModel):
    post_title: str
    post_url: str
    num_comments: int
    hours_since_post: int

class Posts(BaseModel):
    posts: list[Post]

controller = Controller(output_model=Posts)

async def main():
    task = 'Go to hackernews show hn and give me the first 5 posts'
    model = OpenAIAdapter(model="gpt-3.5-turbo")
    agent = Agent(task=task, llm=model, controller=controller)

    history = await agent.run()
    # Add to your main() functions
    os.environ["BROWSER_USE_DEBUG"] = "true"  # Enable debug logging

    result = history.final_result()

    if result:
        parsed: Posts = Posts.model_validate_json(result)
        for post in parsed.posts:
            print('\n--------------------------------')
            print(f'Title:            {post.post_title}')
            print(f'URL:              {post.post_url}')
            print(f'Comments:         {post.num_comments}')
            print(f'Hours since post: {post.hours_since_post}')
    else:
        print("No result")


asyncio.run(main())