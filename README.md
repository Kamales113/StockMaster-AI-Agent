# StockMaster AI Agent

An AI-powered stock analysis assistant built using:

* Python
* FastAPI
* Dify AI Agent
* Groq LLM
* yFinance
* Technical Indicators (RSI, MACD, Moving Averages)
* ngrok

---

# Project Overview

StockMaster is an AI-based stock analysis system that:

* Retrieves live stock market data
* Calculates technical indicators
* Generates BUY / HOLD / SELL recommendations
* Provides confidence scores
* Compares multiple stocks
* Uses an AI agent for natural conversation

The system combines:

* AI reasoning
* Backend APIs
* Technical analysis logic
* Tool calling
* Financial data processing

---

# Features

## Current Features

### Single Stock Analysis

Analyze stocks using:

* RSI
* MACD
* Moving Average Trend
* Confidence Score
* Recommendation Engine

Example:

```text
Analyze TCS
```

---

### Multi-Stock Comparison

Compare two stocks and identify which looks technically stronger.

Example:

```text
Compare TCS and Infosys
```

---

### Confidence Scoring Engine

Weighted scoring system:

| Indicator | Weight |
| --------- | ------ |
| RSI       | 30     |
| Trend     | 35     |
| MACD      | 35     |

Final confidence:

* 70+ → BUY
* 40–69 → HOLD
* Below 40 → SELL

---

### Natural Language Interaction

Users can ask:

```text
Analyze TCS
```

instead of:

```text
TCS.NS
```

---

# Architecture

```text
Dify AI Agent
      ↓
Tool Calling
      ↓
FastAPI Backend
      ↓
Technical Analysis Engine
      ↓
Yahoo Finance Data
```

---

# Technologies Used

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Backend logic        |
| FastAPI    | API server           |
| Dify       | AI orchestration     |
| Groq       | LLM provider         |
| yFinance   | Stock data           |
| ta         | Technical indicators |
| ngrok      | Public API exposure  |
| GitHub     | Version control      |

---

# Installation Guide

## Step 1 — Clone Repository

```bash
git clone YOUR_GITHUB_REPO_URL
cd StockMaster
```

---

## Step 2 — Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

---

## Step 3 — Install Dependencies

```bash
pip install fastapi uvicorn yfinance pandas ta
```

---

# Running The Backend

## Start FastAPI Server

```bash
python -m uvicorn app:app --reload
```

Expected Output:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# Testing API

## Test Single Stock

```text
http://127.0.0.1:8000/analyze?symbol=TCS.NS
```

---

## Test Compare API

```text
http://127.0.0.1:8000/compare?symbol1=TCS.NS&symbol2=INFY.NS
```

---

# ngrok Setup

## Why ngrok?

Dify cannot access localhost directly.
ngrok creates a public URL for the FastAPI server.

---

## Step 1 — Download ngrok

Download from:

[https://ngrok.com](https://ngrok.com)

---

## Step 2 — Add Auth Token

```bash
ngrok config add-authtoken YOUR_TOKEN
```

---

## Step 3 — Start ngrok

```bash
ngrok http 8000
```

Example Output:

```text
https://your-ngrok-url.ngrok-free.app
```

---

# OpenAPI Schema

FastAPI automatically generates:

```text
/openapi.json
```

Example:

```text
https://your-ngrok-url.ngrok-free.app/openapi.json
```

This schema is used inside Dify Custom Tool.

---

# Dify Setup

## Create Agent

1. Open Dify
2. Create Agent
3. Add instructions
4. Select Groq model

Recommended Model:

```text
Llama-3.1-8b-instant
```

---

# Custom Tool Setup

## Steps

1. Open Tools
2. Create Custom Tool
3. Import OpenAPI schema using:

```text
https://your-ngrok-url.ngrok-free.app/openapi.json
```

4. Enable the tool
5. Add tool to the agent

---

# Common Errors & Fixes

## Error 1 — uvicorn not recognized

### Problem

```text
uvicorn is not recognized
```

### Fix

Use:

```bash
python -m uvicorn app:app --reload
```

---

## Error 2 — Internal Server Error

### Problem

```text
Internal Server Error
```

### Cause

Incorrect API route or missing query parameter.

### Fix

Correct usage:

```text
/analyze?symbol=TCS.NS
```

---

## Error 3 — 404 Not Found

### Cause

Opening:

```text
/
```

instead of:

```text
/analyze
```

### Fix

Use valid routes.

---

## Error 4 — invalid schema: servers

### Cause

Dify schema import issue.

### Fix

Manually edit schema or re-import OpenAPI after backend restart.

---

## Error 5 — ngrok not recognized

### Cause

ngrok executable path issue.

### Fix

Run command from ngrok folder:

```bash
.\ngrok.exe http 8000
```

---

# Important Development Notes

## ngrok URLs Change Every Restart

Every time ngrok restarts:

* new public URL generated
* Dify schema must be updated

This is normal during local development.

Permanent deployment later solves this issue.

---

# Current API Endpoints

## Home Route

```text
/
```

---

## Analyze Single Stock

```text
/analyze?symbol=TCS.NS
```

---

## Compare Two Stocks

```text
/compare?symbol1=TCS.NS&symbol2=INFY.NS
```

---

# Project Workflow

```text
User Query
    ↓
Dify Agent
    ↓
Tool Calling
    ↓
FastAPI Backend
    ↓
Technical Analysis
    ↓
AI Explanation
```

---

# Future Improvements

## Phase 1 — Intelligence Upgrades

* Company name → stock symbol mapping
* Better confidence engine
* More indicators
* Support/resistance detection
* Candlestick pattern analysis
* Volatility analysis

---

## Phase 2 — User Experience

* Dashboard UI
* Charts
* Portfolio tracking
* Watchlists
* Login system
* Mobile-friendly interface

---

## Phase 3 — AI Enhancements

* News sentiment analysis
* RAG financial knowledge base
* Personalized recommendations
* AI memory
* Risk profiling

---

## Phase 4 — Production Deployment

* Deploy backend to Render
* Permanent public API
* Remove ngrok dependency
* Database integration
* Authentication
* Monitoring
* Rate limiting
* Caching

---

# Next Recommended Tasks

## Immediate Next Step

### Natural Language Stock Mapping

Allow users to type:

```text
Analyze TCS
```

instead of:

```text
TCS.NS
```

This improves usability significantly.

---

## After That

### Add News Sentiment Analysis

Combine:

* technical analysis
* market news
* AI reasoning

This creates much more intelligent recommendations.

---

## Later

### Deploy To Render

This removes:

* ngrok restarts
* manual schema updates
* local dependency

and makes the AI publicly accessible.

---

# What This Project Teaches

This project teaches:

* API development
* AI orchestration
* Tool calling
* LLM integration
* Financial data processing
* Technical analysis
* Backend engineering
* Debugging
* OpenAPI integration
* Public API exposure
* Real-world AI architecture

---

# Final Note

This is not just a beginner chatbot project.

This project combines:

* AI
* APIs
* backend systems
* live data
* technical analysis
* orchestration

which is much closer to real-world AI engineering systems.
