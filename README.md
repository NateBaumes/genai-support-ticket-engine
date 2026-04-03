# 🤖 GenAI Support Ticket Engine

Production-ready support ticket system with LLM classification, sentiment analysis, vector search, circuit breakers, and vendor abstraction layers.

## 🎯 What This Demonstrates

| Capability | Implementation |
|------------|----------------|
| **GenAI Applications** | GPT-4o mini for classification, sentiment, resolution generation |
| **Support Domain** | Complete ticket lifecycle: ingest → classify → retrieve → resolve → escalate |
| **Platform Mindset** | Abstracted LLM, vector store, and vendor interfaces (swap in 15 mins) |
| **Production Patterns** | Circuit breakers, rate limiting, idempotency |
| **Hybrid Ecosystems** | Multiple vendor support with fallback strategies |

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/genai-support-ticket-engine.git
cd genai-support-ticket-engine

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your OPENAI_API_KEY
python -m app.main

# Frontend (new terminal)
cd frontend
npm install
npm run dev
