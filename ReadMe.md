# Browser-Use Demo - Web Scraping Automation

This project demonstrates web scraping automation using the browser-use library with OpenAI GPT models. It can scrape Hacker News posts, search Google for MLOps resources, and extract structured data from web pages.

## 🚀 Quick Start

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/AmoloWashington/BrowserUse_Simple_Task.git
cd browser-use-demo
\`\`\`

### 2. Set Up Python Environment
\`\`\`bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install browser-use python-dotenv openai playwright pydantic
\`\`\`

### 4. Install Playwright Browsers
\`\`\`bash
playwright install chromium
\`\`\`

### 5. Set Up Environment Variables
Create a `.env` file in the project root:
\`\`\`env
OPENAI_API_KEY=your_openai_api_key_here
\`\`\`

### 1. Basic Functionality Test
Tests if browser automation is working:
\`\`\`bash
python structured.py
\`\`\`

### 2. Simple Scraper
Basic web scraping without structured output:
\`\`\`bash
python basic_scraper.py
\`\`\`

### 3. Structured Data Scraper
Advanced scraper with JSON output:
\`\`\`bash
python structured.py
\`\`\`

## 📊 What Each Script Does

### `test_adapter.py`
- **Purpose**: Verify basic browser automation works
- **Target**: httpbin.org/json (simple test site)
- **Output**: Console output describing what it sees

### `basic_scraper.py`
- **Purpose**: Basic web scraping examples
- **Targets**: 
  - Hacker News Show HN posts
  - Google search for MLOps resources
- **Output**: Console output with scraped data

### `structured.py`
- **Purpose**: Extract structured data as JSON
- **Targets**:
  - Hacker News Show HN posts (title, URL, comments, hours ago)
  - Google MLOps resources (title, URL, description)
- 
## 🛠️ Troubleshooting

### Common Issues

1. **"Agent.__init__() missing 1 required positional argument: 'llm'"**
   - Make sure your LLM class has all required attributes
   - Ensure `model_name` attribute is set

2. **"'WorkingLLM' object has no attribute 'model_name'"**
   - Add `self.model_name = "gpt-4o-mini"` to your LLM class `__init__` method

3. **OpenAI API Key Issues**
   - Verify your `.env` file exists and contains the correct API key
   - Check that your OpenAI API key is valid and has credits

4. **Browser Issues**
   - Run `playwright install chromium` to install browser
   - Check if Chrome/Chromium is properly installed

### Debug Mode
To see what the browser is doing, you can enable headful mode by modifying the scripts:
```python
os.environ["BROWSER_USE_HEADFUL"] = "true"
