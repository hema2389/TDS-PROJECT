# LLM Analysis Quiz — Automatic Python Solver

This project implements the student-side infrastructure for the **LLM Analysis Quiz**.

It includes:

- FastAPI server
- Secret validation
- A Playwright-based headless browser
- Dynamic quiz solver framework
- Automatic submission loop
- Fully MIT-licensed public repository structure

## 🚀 Quick Start

### Install Requirements
pip install -r requirements.txt
playwright install

### Run Server
uvicorn app.main:app --host 0.0.0.0 --port 8000

Send a test POST:
```json
{
  "email": "your-email",
  "secret": "your-secret",
  "url": "https://tds-llm-analysis.s-anand.net/demo"
}
🌐 Endpoint Behavior

Your server:
  Validates JSON
  Verifies secret
  Loads quiz page (with JavaScript)
  Detects task
  Solves data-related question
  Submits answer
  Repeats until quiz ends
