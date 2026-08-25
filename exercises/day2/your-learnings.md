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

1. 3.29 
2. 3.14
3. By using the complied languages like GO/Rust,reducing the deployment package size and by avoiding heavy logics in the handler

---

## Exercise 2: RAG Lite (rag_lite.py)

Run `python day2/rag_lite.py`:

1. What chunk size and overlap did you use? Why?
2. Were the top-3 retrieved chunks relevant to the query? Explain.
3. If you were building this for production, what would you change? (Hint: think about vector DBs, embedding models, chunking strategies)

**Your answer:**

1. I used chunk size 30 and overlap 0.2 because the sample doc I gave is only of 51 words long, so this calculation generates a decent amount of chunks with meaningful context.
2. Only first one is completely relevant and the other two are totaly irrelevant, because the logic picks the nearest vectors to the question's vector. However, second chunck was considered closest as it has the main word "RAG" and third chunck was chosen becasue of the closest context 
3. I would change vectore db to Amazon OpenSearch because it is serverless, with native hybrid search, moderate latency and reasonable pricing. I would change Titan text embeddings V2 to either Titan Multimodal Embeddings for text and image only or Cohere Embed for text, images and business documents. Finally, I will increase the chuck size to 600 and decrease the overlap to 0.1. 

---

## Exercise 3: Simple Agent (simple_agent/)

Deploy the Step Functions state machine and run a test:

1. Draw (or describe) the flow when the user asks "What is the weather in Paris?"
2. What happens if the LLM routing step returns an unknown tool name?
3. How would you add retry logic or human-in-the-loop approval to this agent?

**Your answer:**

1. apigateway --> stepfunction --> "decide_tool" lambda --> stepfunction --> "fetch_data" lambda, specifically weather --> "synthesize" lambda --> Step Function --> APi Gateway
2. It will be directed to Synthesize lambda as it is default. The output will be question and whatever the answer from bedrock model.
3. I will add retry logic and human-in-the-loop approval in Step Function

---

## Exercise 4: Cost Tracking (cost_tracker.py)

1. Complete the `cost_tracker.py` script so it queries CloudWatch Logs Insights.
2. Run it and paste your output here:
3. If your API served 10,000 requests/day, what would your estimated monthly Bedrock cost be?

**Your answer:**

1. Done
2. {
  "date": "2026-08-23",
  "total_invocations": 4,
  "total_input_tokens": 28,
  "total_output_tokens": 659,
  "estimated_cost_usd": 0.01,
  "by_model": {
    "us.anthropic.claude-haiku-4-5-20251001-v1:0": {
      "invocations": 2,
      "cost_usd": 0.0099
    },
    "claude-haiku-4-5-20251001": {
      "invocations": 2,
      "cost_usd": 0.0
    }
  }
}
3. 2,970

---

## Daily Reflection

Answer these 2 sentences before you close your laptop:

1. What is the biggest operational concern when running AI on serverless Lambda?
2. What is one pattern from today you would recommend to a customer?

**Your reflection:**

1. Cold start is the biggest operational concern when running AI on serverless Lambda. 
2. Cost tracking pattern for bedrock
