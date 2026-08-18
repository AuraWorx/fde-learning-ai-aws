# Grading Rubric — FDE AI + AWS Learning

Each engineer is graded on their `fde/your-name` branch. Score: 0 (missing), 1 (partial), 2 (complete).

## Day 1 — LLM Fundamentals (Max: 16 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| llm_basics.py runs | 2 | Tokenization demo works; temperature comparison runs without error |
| bedrock_playground.py runs | 3 | Invokes at least 2 Bedrock models; outputs JSON with latency + token count |
| prompt_patterns.py runs | 3 | CLI runs all 3 styles; outputs JSON file |
| Exercises completed | 4 | All 4 exercises in `exercises/day1/your-learnings.md` answered with substance |
| Code quality | 2 | Readable, uses functions, has comments explaining what each block does |
| Daily reflection | 2 | 2 sentences written answering the reflection questions |

## Day 2 — AWS AI Engineering (Max: 16 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| CDK app deploys | 3 | `cdk deploy` succeeds; API Gateway endpoint returns valid responses |
| /chat endpoint works | 2 | Streaming or non-streaming response from Bedrock via curl/Postman |
| rag_lite.py runs | 2 | Chunks text, embeds with Titan or sentence-transformers, retrieves top-3 |
| simple_agent deployed | 3 | Step Functions state machine executes all 3 steps end-to-end |
| cost_tracker.py | 2 | Script structure complete; queries CloudWatch or provides clear stub with output format |
| Exercises completed | 2 | All 4 exercises in `exercises/day2/your-learnings.md` answered |
| Daily reflection | 2 | 2 sentences written answering the reflection questions |

## Total: 32 points

### Grade Boundaries
- **A (29–32):** Ready for customer-facing AI work. Code is production-aware.
- **B (22–28):** Solid understanding. Minor gaps in operational awareness.
- **C (15–21):** Basic competency. Needs review on cost tracking and agent patterns.
- **D / F (<15):** Does not meet baseline. Retake Day 1.

## Evaluation Notes
- Code is evaluated for **correctness** (does it run?), **completeness** (did they do all exercises?), and **clarity** (can I understand their learnings?).
- If Bedrock is not enabled in their account, they may mock the invoke with local transformers for grading. Points are adjusted accordingly.
