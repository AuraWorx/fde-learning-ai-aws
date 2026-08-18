# FDE Learning: AI + AWS (2-Day Intensive)

Welcome, forward-deployed engineers. This repo is your guided onboarding to building AI-powered systems on AWS. You will code everything yourself — no copy-pasting solutions.

## Prerequisites

- AWS account with Bedrock access enabled (request model access in us-east-1 for Claude, Llama, Titan)
- Python 3.9+
- `pip`, `git`
- AWS CLI configured locally (`aws configure`)
- Node.js 18+ (for CDK)
- Hugging Face account (free) for Day 1 local models

## Setup

```bash
git clone <repo-url> && cd fde-learning
cp .env.example .env   # fill in your AWS creds region
python -m venv .venv && source .venv/bin/activate
pip install -r day1/requirements.txt -r day2/requirements.txt
```

## Day 1 — LLM Fundamentals + Bedrock (4–5 hours)

**Goal:** Understand how models generate text, then learn to call them from AWS.

### Morning: How LLMs Work

**Read (30 min):**
- Tokenization: text → token IDs → embedding vectors
- Attention mechanism: how context is weighted
- Temperature / top_p: controlling randomness
- Context window limits

**Code (1.5 hrs):** `day1/llm_basics.py`
- Tokenize a sentence with `transformers`, show token IDs and decode back
- Load `distilgpt2` locally, generate text, measure latency
- Run the same prompt at temperature 0.1 and 1.0 — observe the difference

### Afternoon: Bedrock + Prompt Engineering

**Learn (30 min):**
- Bedrock `InvokeModel` vs `Converse` API
- Claude 3 Sonnet, Llama 3, Titan differences
- Streaming vs non-streaming
- Token pricing

**Code (2 hrs):**
1. `day1/bedrock_playground.py` — invoke 3 models, log latency, token usage, and estimated cost
2. `day1/prompt_patterns.py` — CLI that runs zero-shot, few-shot, and chain-of-thought on 3 questions; save outputs to JSON; manually score which is best

**End of Day 1:** Push code. Write 2 sentences in `exercises/day1/your-learnings.md` answering:
1. What surprised you about how models generate text?
2. When would you use Claude vs Llama vs Titan?

---

## Day 2 — AWS AI Engineering (4–5 hours)

**Goal:** Build a real serverless AI API and a simple agent on AWS.

### Morning: Serverless AI API + RAG

**Learn (30 min):**
- Lambda + API Gateway + Bedrock integration
- Cold starts with AI workloads
- RAG basics: chunking, embeddings, retrieval

**Code (2.5 hrs):**
1. Deploy `day2/cdk_app/` with AWS CDK:
   - `POST /chat` → Lambda → Bedrock Claude → streaming response
   - `POST /summarize` → Lambda → fetches URL → summarizes with Bedrock
   - Measure cold start latency
2. `day2/rag_lite.py` — ingest a text file, chunk it, embed with Titan Embeddings, store vectors in local FAISS, retrieve top-3 chunks, pass as context to Claude

### Afternoon: Agent Pattern + Cost Tracking

**Learn (30 min):**
- ReAct agent pattern
- Step Functions + Lambda orchestration
- CloudWatch structured logging for AI costs

**Code (2 hrs):**
1. `day2/simple_agent/` — deploy a 3-step Step Functions agent:
   - Step 1: Receive user question
   - Step 2: Lambda decides whether to call a tool (mock weather API or DB)
   - Step 3: Lambda synthesizes final answer with Bedrock
2. Add structured JSON logging to the Day 2 API
3. `day2/cost_tracker.py` — pull CloudWatch logs, count tokens per model, output daily spend estimate

**End of Day 2:** API works via curl. Agent runs end-to-step in AWS console. Write learnings in `exercises/day2/your-learnings.md`.

---

## Submission & Grading

1. Create your branch from `main`:
   ```bash
   git checkout -b fde/your-name
   ```
2. Implement all exercises
3. Write learnings in `exercises/day1/your-learnings.md` and `exercises/day2/your-learnings.md`
4. Push your branch:
   ```bash
   git push -u origin fde/your-name
   ```

Your branch will be evaluated against the rubric in `grading/rubric.md`.

## Repo Structure

```
fde-learning/
├── README.md
├── day1/
│   ├── llm_basics.py
│   ├── bedrock_playground.py
│   ├── prompt_patterns.py
│   └── requirements.txt
├── day2/
│   ├── cdk_app/
│   │   ├── app.py
│   │   ├── cdk_stack.py
│   │   ├── requirements.txt
│   │   └── lambda/
│   │       ├── chat.py
│   │       └── summarize.py
│   ├── rag_lite.py
│   ├── simple_agent/
│   │   ├── state_machine.json
│   │   ├── decide_tool.py
│   │   ├── fetch_data.py
│   │   └── synthesize.py
│   └── cost_tracker.py
├── exercises/
│   ├── day1/
│   │   └── your-learnings.md
│   └── day2/
│       └── your-learnings.md
└── grading/
    └── rubric.md
```
