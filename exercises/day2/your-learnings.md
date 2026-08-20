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

1.The cold start latency on the first invocation was 2.49 seconds.
2.The latency on the second invocation was 1.57 seconds. It was faster because second time using the existing lambda execution environment.
3.Three techniques to reduce cold starts in production are:
Provisioned Concurrency — keep Lambda instances ready.
Smaller packages — reduce dependencies so Lambda starts faster.
Less startup work — keep initialization code minimal.

---

## Exercise 2: RAG Lite (rag_lite.py)

Run `python day2/rag_lite.py`:

1. What chunk size and overlap did you use? Why?
2. Were the top-3 retrieved chunks relevant to the query? Explain.
3. If you were building this for production, what would you change? (Hint: think about vector DBs, embedding models, chunking strategies)

**Your answer:**

1. I used a small chunk size with some overlap. This helps break the document into smaller pieces while keeping some information connected between the chunks.
2. Yes, they were relevant because they contained information about AI, language models, and RAG. However, my document was only split into 1 chunk, so the top 3 results were very similar.
3. I would use a proper vector database instead of local FAISS. I would also try a better embedding model and improve the way the document is split into chunks.

---

## Exercise 3: Simple Agent (simple_agent/)

Deploy the Step Functions state machine and run a test:

1. Draw (or describe) the flow when the user asks "What is the weather in Paris?"
2. What happens if the LLM routing step returns an unknown tool name?
3. How would you add retry logic or human-in-the-loop approval to this agent?

**Your answer:**

1.When the user asks “What is the weather in Paris?”, the question first goes to the decide_tool Lambda. Claude identifies that the weather tool is needed. Step Functions then calls fetch_data with the weather tool, and finally sends the question and weather result to the synthesize Lambda to generate the final answer.
2.If the LLM returns an unknown tool name, Step Functions will not match it with weather or database, so it goes to the default path. The workflow will then call synthesize with that unknown tool name, instead of calling fetch_data for it.
the JSON looks like:
{
"question": "What is the weather in Paris?",
"tool": "none",
"reason": "Could not parse LLM output"
} 3. I would add retry logic in Step Functions so failed Lambda calls can be retried automatically. For human approval, I would add an approval step where a person can review the tool decision and approve or reject it before the agent continues.

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
