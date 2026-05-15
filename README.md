# StockMaster AI Agent

## Overview

StockMaster AI Agent is a real-time AI-powered stock analysis assistant built using:

* Dify AI Agent
* Groq LLM
* FastAPI
* Yahoo Finance API
* Technical Analysis Indicators (RSI)
* ngrok
* OpenAPI Tool Calling

This project demonstrates how modern AI agents work using:

```text
LLM + Tool Calling + APIs + Backend + Real-Time Data
```

The AI agent can:

* Understand natural language stock questions
* Convert company names into valid Yahoo Finance symbols
* Call a backend API automatically
* Fetch live stock market data
* Perform RSI-based technical analysis
* Return beginner-friendly explanations

---

# Final Architecture

```text
User
  ↓
Dify AI Agent
  ↓
Groq LLM
  ↓
Tool Calling
  ↓
FastAPI Backend
  ↓
Yahoo Finance API
  ↓
Technical Analysis (RSI)
  ↓
JSON Response
  ↓
AI Explanation
```

---

# Technologies Used

| Technology | Purpose                    |
| ---------- | -------------------------- |
| Python     | Backend language           |
| FastAPI    | API framework              |
| yfinance   | Stock data retrieval       |
| ta         | Technical analysis library |
| Groq       | LLM provider               |
| Dify       | AI agent orchestration     |
| ngrok      | Public API tunneling       |
| OpenAPI    | Tool schema integration    |
| VS Code    | Development environment    |

---

# Step-by-Step Complete Setup

# Step 1 — Install Python

Download Python:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

IMPORTANT:
During installation enable:

```text
Add Python to PATH
```

Verify installation:

```bash
python --version
```

---

# Step 2 — Install VS Code

Download:

[https://code.visualstudio.com/](https://code.visualstudio.com/)

Install VS Code and open the project folder.

---

# Step 3 — Create Project Folder

Create folder:

```text
StockMaster
```

Open it in VS Code.

---

# Step 4 — Install Required Libraries

Open terminal inside VS Code.

Run:

```bash
pip install fastapi uvicorn yfinance pandas ta
```

Installed libraries:

| Library  | Purpose                       |
| -------- | ----------------------------- |
| fastapi  | API creation                  |
| uvicorn  | FastAPI server                |
| yfinance | Stock market data             |
| pandas   | Data handling                 |
| ta       | Technical analysis indicators |

---

# Step 5 — Create Backend API

Create file:

```text
app.py
```

Paste:

```python
from fastapi import FastAPI
import yfinance as yf
from ta.momentum import RSIIndicator

app = FastAPI()

@app.get("/analyze")
def analyze_stock(symbol: str):

    stock = yf.download(symbol, period="3mo")

    if stock.empty:
        return {"error": "Invalid stock symbol"}

    close_prices = stock['Close'].squeeze()

    rsi = RSIIndicator(close_prices).rsi().iloc[-1]

    current_price = close_prices.iloc[-1]

    if rsi > 70:
        signal = "Overbought"
    elif rsi < 30:
        signal = "Oversold"
    else:
        signal = "Neutral"

    return {
        "stock": symbol,
        "price": round(float(current_price), 2),
        "RSI": round(float(rsi), 2),
        "signal": signal
    }
```

---

# Step 6 — Run Backend Server

Run:

```bash
python -m uvicorn app:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# Step 7 — Test API

Open browser:

```text
http://127.0.0.1:8000/analyze?symbol=TCS.NS
```

Expected JSON response:

```json
{
  "stock": "TCS.NS",
  "price": 4200,
  "RSI": 55.3,
  "signal": "Neutral"
}
```

---

# Step 8 — Setup Dify AI Agent

Open:

[https://dify.ai/](https://dify.ai/)

Create account.

Go to:

```text
Studio → Create From Blank → Agent
```

Agent name:

```text
StockMaster
```

---

# Step 9 — Setup Groq Model Provider

Open:

[https://console.groq.com/](https://console.groq.com/)

Create free account.

Generate API key.

Inside Dify:

```text
Settings → Model Provider → Groq
```

Paste API key.

Use model:

```text
Llama-3.1-8b-instant
```

Reason:

* Stable
* Fast
* Beginner friendly
* Reliable with Dify

---

# Step 10 — Configure Agent Prompt

Inside Dify Agent Instructions:

```text
You are an AI stock analyst.

IMPORTANT:
You MUST use the analyze_stock tool whenever a user asks about any stock.

Indian stock symbols MUST use the Yahoo Finance format:
- TCS → TCS.NS
- RELIANCE → RELIANCE.NS
- INFY → INFY.NS
- HDFCBANK → HDFCBANK.NS

Steps:
1. Extract the company name or stock symbol.
2. Convert it into Yahoo Finance symbol format ending with .NS
3. Use the analyze_stock tool with that symbol.
4. Read the returned JSON.
5. Explain the RSI, signal, and price simply.
6. Mention whether the stock looks overbought, oversold, or neutral.
7. Always warn this is not financial advice.
```

---

# Step 11 — Install ngrok

Download:

[https://ngrok.com/download](https://ngrok.com/download)

Create free account:

[https://dashboard.ngrok.com/](https://dashboard.ngrok.com/)

---

# Step 12 — Configure ngrok

Open terminal inside ngrok folder.

Run:

```bash
.\ngrok.exe config add-authtoken YOUR_TOKEN
```

---

# Step 13 — Expose Backend Publicly

Keep FastAPI server running.

Open NEW terminal.

Run:

```bash
.\ngrok.exe http 8000
```

You will get:

```text
https://your-ngrok-url.ngrok-free.app
```

Test:

```text
https://your-ngrok-url.ngrok-free.app/analyze?symbol=TCS.NS
```

---

# Step 14 — Import OpenAPI Schema into Dify

Open:

```text
https://your-ngrok-url.ngrok-free.app/openapi.json
```

Verify schema loads.

Inside Dify:

```text
Tools → Create Custom Tool → Import from URL
```

Paste:

```text
https://your-ngrok-url.ngrok-free.app/openapi.json
```

---

# Step 15 — Manual OpenAPI Schema (Fallback)

If automatic import fails:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Stock Analyzer API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://your-ngrok-url.ngrok-free.app"
    }
  ],
  "paths": {
    "/analyze": {
      "get": {
        "summary": "Analyze Stock",
        "operationId": "analyze_stock",
        "parameters": [
          {
            "name": "symbol",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response"
          }
        }
      }
    }
  }
}
```

---

# Step 16 — Enable Tool in Agent

Inside Dify:

```text
Tools → Add Tool → Enable analyze_stock
```

You should see:

```text
1/1 Enabled
```

---

# Final Test

Ask:

```text
Analyze TCS stock
```

Expected workflow:

```text
User asks question
↓
LLM extracts stock symbol
↓
LLM calls tool
↓
FastAPI backend fetches stock data
↓
RSI calculated
↓
JSON returned
↓
LLM explains naturally
```

---

# Debugging Journey and Fixes

# 1. Model Compatibility Issues

Problem:

```text
Deprecated or incompatible models
```

Fix:

Used:

```text
Llama-3.1-8b-instant
```

Reason:
Stable and officially supported.

---

# 2. Uvicorn Not Recognized

Problem:

```text
uvicorn is not recognized
```

Fix:

Used:

```bash
python -m uvicorn app:app --reload
```

Reason:
Windows PATH issue.

---

# 3. Internal Server Error

Problem:

```text
500 Internal Server Error
```

Cause:

Missing query parameter.

Fix:

Correct endpoint:

```text
/analyze?symbol=TCS.NS
```

---

# 4. Pandas Dimensionality Error

Problem:

```text
Data must be 1-dimensional
```

Cause:

Yahoo Finance returned dataframe shape:

```text
(60,1)
```

instead of series.

Fix:

```python
close_prices = stock['Close'].squeeze()
```

---

# 5. localhost Access Problem

Problem:

Dify cloud could not access:

```text
127.0.0.1
```

Reason:

localhost only works inside your computer.

Fix:

Used ngrok public tunnel.

---

# 6. OpenAPI Import Failure

Problem:

```text
schema is required
```

Fix:

Added:

```json
"servers"
```

inside schema.

---

# 7. Tool Not Being Used

Problem:

```text
0/0 Enabled
```

Cause:

Tool package enabled but endpoint not selected.

Fix:

Enabled actual:

```text
analyze_stock
```

endpoint.

---

# 8. AI Failed to Detect Symbols

Problem:

AI passed invalid stock symbols.

Fix:

Added Yahoo Finance symbol rules into system prompt.

Example:

```text
TCS → TCS.NS
```

---

# Concepts Learned

This project teaches:

* AI agents
* LLM orchestration
* FastAPI
* APIs
* JSON
* OpenAPI
* Tool calling
* Prompt engineering
* Backend debugging
* ngrok tunneling
* Real-time data systems
* Technical analysis
* AI architecture

---

# Future Improvements

Potential upgrades:

* MACD analysis
* Moving averages
* Bollinger bands
* Candlestick charts
* News sentiment analysis
* Portfolio management
* Buy/sell confidence score
* Multi-stock comparison
* Automatic company-to-symbol mapping
* Deployment to cloud platforms

---

# Recommended Deployment Platforms

For permanent hosting:

* Render
* Railway
* AWS
* Azure
* Google Cloud

---

# GitHub Setup

Initialize repository:

```bash
git init
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Initial commit"
```

Connect remote:

```bash
git remote add origin YOUR_REPO_URL
```

Push:

```bash
git branch -M main
git push -u origin main
```

---

# Important Security Notes

Never upload:

* API keys
* ngrok tokens
* .env files
* secrets

Use:

```text
.gitignore
```

for sensitive files.

---

# Final Learning Outcome

This project demonstrates the core architecture behind modern AI systems:

```text
LLM + Tools + APIs + Backend + Live Data
```

This is the same foundational pattern used in:

* AI copilots
* autonomous agents
* ChatGPT plugins
* enterprise AI assistants
* production AI systems

---

# Disclaimer

This project is for educational purposes only.

It is NOT financial advice.

Stock market trading involves risk.
Always perform your own research before investing.
