from browser_use.llm import ChatOpenAI
from browser_use import Agent, BrowserSession, Controller
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
load_dotenv()

import asyncio

class FormData(BaseModel):
    name: str
    reg_no: str
    missing_unit: str
    lecturer_name: str

class FormSubmission(BaseModel):
    form: FormData

controller = Controller(output_model=FormSubmission)

browser_session = BrowserSession(
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    user_data_dir='~/.config/browseruse/profiles/Washington',
)

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task="""Fill out the Google Form at https://docs.google.com/forms/d/e/1FAIpQLSfc2DFYlbWy2ByF4xgwPjijElBO8TDwxlKvceK-7ypMZrlaGQ/viewform with the following details:
        - Name: Amolo Washington
        - Registration Number: SIT/B/01-02315/2021
        - Missing Mark: Web Technologies 2
        - Lecturer Name: Dr. Ujunju
        
        Make sure to:
        1. Navigate to the form URL
        2. Fill in all the required fields accurately
        3. Submit the form by clicking the submit button
        4. Verify that the submission was successful""",
        llm=llm,
        browser=browser_session,
        controller=controller,
    )
    result = await agent.run()
    print(result.final_result())
    await browser_session.close()

asyncio.run(main())