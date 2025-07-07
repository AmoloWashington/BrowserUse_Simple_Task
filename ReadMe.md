# Automated Job and Learning Resource Agent

This project uses `browser-use` and `OpenAI GPT-4o` to perform two automated web tasks:

1. **Job Search on LinkedIn**  
   Finds jobs that match a user profile (based on name, skills, experience, and location), posted within the last 24 hours.

2. **Learning Resource Aggregation**  
   Searches for **MLOps learning resources and best practices** from high-quality, freely available sources. It returns the top 10 with summaries and metadata (difficulty, type, etc.).

---

## 🔧 Tech Stack

- **Python 3.10+**
- **[browser-use](https://pypi.org/project/browser-use/)** for browser automation
- **OpenAI GPT-4o** for intelligent task execution
- **Pydantic** for structured data models
- **dotenv** for environment configuration

---



## ✅ Requirements

Install the following Python dependencies (preferably in a virtual environment):

```bash
pip install browser-use openai python-dotenv pydantic
```

You also need:
- A Chromium-based browser installed (e.g., Chrome)
- An OpenAI API key

---

## 🔑 Environment Variables

Create a `.env` file in the root directory with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 How to Run

Make sure Python and Chrome are installed.

Then run:

```bash
python structured.py
```

> ⚠️ Note: If you face issues with browser launch paths on Windows, ensure the `executable_path` in the script points to your actual Chrome installation:
>
> ```python
> executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe'
> ```

---

## 🧠 What the Script Does

The agent:
1. Navigates to LinkedIn and searches for jobs based on the defined `JobSearchProfile` parameters.
2. Searches Google for top **MLOps** resources.
3. Parses and summarizes the top 10 freely accessible results.
4. Returns results in a structured format (defined by `pydantic.BaseModel`).
5. Gracefully closes the browser session after execution.

---

## 📝 Example Output

```json
{
  "jobsearch": [
    {
      "name": "John Doe",
      "skills": ["MLOps", "Python", "Kubernetes"],
      "experience_years": 3,
      "location": "Nairobi"
    }
  ],
  "mlops_resources": [
    {
      "title": "Introduction to MLOps",
      "url": "https://example.com/mlops-course",
      "summary": "Covers MLOps fundamentals including CI/CD for ML, model deployment, and monitoring.",
      "type": "Course",
      "difficulty": "Intermediate"
    }
  ]
}
```

---

## 🛠️ Troubleshooting

- **Chrome fails to launch?**  
  Ensure your `executable_path` is valid and points to a Chromium browser.

- **Agent gets stuck or slow?**  
  Sometimes external websites like LinkedIn can throttle or block automation. Use a VPN or tweak the agent’s delay settings.

---

## 📜 License

MIT License. Use it, hack it, improve it.

---

## 🙏 Acknowledgements

- [browser-use](https://github.com/gzuidhof/browser-use)
- [OpenAI](https://platform.openai.com/)
