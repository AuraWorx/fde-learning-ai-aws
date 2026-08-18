# Day 2 Exercises — AWS AI Engineering

## Instructions
Complete all exercises below. Write your answers and observations directly in this file.

---

## Exercise 1: Serverless AI API (cdk_app/)

Deploy the CDK app and test with curl:

1. What was your cold start latency on the first invocation?
2. What was the latency on the second invocation?
3. How would you reduce cold starts in production? List 3 techniques.

```bash
curl -X POST https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is AWS Bedrock?"}'
```

**Your answer:**

1. 
2. 
3. 

---

## Exercise 2: RAG Lite (rag_lite.py)

Run `python day2/rag_lite.py`:

1. What chunk size and overlap did you use? Why?
2. Were the top-3 retrieved chunks relevant to the query? Explain.
3. If you were building this for production, what would you change? (Hint: think about vector DBs, embedding models, chunking strategies)

**Your answer:**

1. 
2. 
3. 

---

## Exercise 3: Simple Agent (simple_agent/)

Deploy the Step Functions state machine and run a test:

1. Draw (or describe) the flow when the user asks "What is the weather in Paris?"
2. What happens if the LLM routing step returns an unknown tool name?
3. How would you add retry logic or human-in-the-loop approval to this agent?

**Your answer:**

1. 
2. 
3. 

---

## Exercise 4: Cost Tracking (cost_tracker.py)

1. Complete the `cost_tracker.py` script so it queries CloudWatch Logs Insights.
2. Run it and paste your output here:
3. If your API served 10,000 requests/day, what would your estimated monthly Bedrock cost be?

**Your answer:**

1. 
2. 
3. 

---

## Daily Reflection

Answer these 2 sentences before you close your laptop:

1. What is the biggest operational concern when running AI on serverless Lambda?
2. What is one pattern from today you would recommend to a customer?

**Your reflection:**

1. 
2. 
