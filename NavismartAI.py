from browser_use.llm import ChatOpenAI
from browser_use import Agent, BrowserSession
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

async def analyze_navismart():
    browser_session = BrowserSession(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        user_data_dir='~/.config/browseruse/profiles/washington',
    )

    llm = ChatOpenAI(model="gpt-4o")
    
    agent = Agent(
        task="""Comprehensively analyze https://www.navismartai.com/ by:
        1. Exploring all sections: Home, Features, How it Works, Pricing, Testimonials, Get Started, and Contact Us.
        2. Interacting with all available features
        3. For each feature:
           - Describe its functionality
           - Identify potential problems
           - Suggest specific improvements
        4. Analyze the complete user flow
        5. Identify UI/UX issues and technical challenges
        
        Return ONLY a JSON object with this structure:
        {
            "features": [{
                "name": "Feature name",
                "description": "What it does",
                "problems": ["issue 1", "issue 2"],
                "improvements": ["solution 1", "solution 2"]
            }],
            "user_flow_analysis": {
                "friction_points": ["point 1", "point 2"],
                "suggestions": ["improvement 1", "improvement 2"]
            },
            "technical_challenges": [{
                "area": "Area name",
                "problem": "Specific issue",
                "solution": "Recommended fix"
            }]
        }""",
        llm=llm,
        browser=browser_session,
    )
    
    try:
        result = await agent.run()
        
        if hasattr(result, 'final_result'):
            raw_output = result.final_result()
            
            try:
                parsed_output = json.loads(raw_output)
                return parsed_output
            except json.JSONDecodeError:
                # Handle case where output might be wrapped in markdown
                if raw_output.startswith('```json') and raw_output.endswith('```'):
                    cleaned_output = raw_output[7:-3].strip()
                    try:
                        return json.loads(cleaned_output)
                    except json.JSONDecodeError:
                        pass
                return {"error": "Output is not valid JSON"}
        else:
            return {"error": "No final result available"}
            
    except Exception as e:
        return {"error": str(e)}
    finally:
        await browser_session.close()

def print_analysis(analysis):
    """Print the analysis in a structured format"""
    if "error" in analysis:
        print(f"Error: {analysis['error']}")
        return
        
    print("\n=== NAVISMART AI ANALYSIS SUMMARY ===\n")
    
    print("FEATURE ANALYSIS:")
    for feature in analysis.get("features", []):
        print(f"\n{feature['name']}:")
        print(f"Description: {feature['description']}")
        print("Problems:")
        for problem in feature.get("problems", []):
            print(f" - {problem}")
        print("Improvements:")
        for improvement in feature.get("improvements", []):
            print(f" - {improvement}")
   
    print("\nUSER FLOW ANALYSIS:")
    flow = analysis.get("user_flow_analysis", {})
    print("Friction Points:")
    for point in flow.get("friction_points", []):
        print(f" - {point}")
    print("Suggestions:")
    for suggestion in flow.get("suggestions", []):
        print(f" - {suggestion}")
    
    print("\nTECHNICAL CHALLENGES:")
    for challenge in analysis.get("technical_challenges", []):
        print(f"\n{challenge['area']}:")
        print(f"Problem: {challenge['problem']}")
        print(f"Solution: {challenge['solution']}")

if __name__ == "__main__":
    analysis = asyncio.run(analyze_navismart())
    print_analysis(analysis)