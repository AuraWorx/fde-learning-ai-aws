# Day 1 Exercises — LLM Fundamentals

## Instructions
Complete all exercises below. Write your answers and observations directly in this file.

---

## Exercise 1: Tokenization (llm_basics.py)

Run `python day1/llm_basics.py` and answer:

1. How many tokens did the sample sentence produce?
2. What is one token that surprised you (subword, word, or character)?
3. Why does token count matter for AWS Bedrock pricing?

**Your answer:**

1. 10 Tokens are produced by sample senetnce 
2. I am suprised by having a token even for a character
3. Because tokens are the basic units of work for any AI model. Specicifically, AWS Bedrock is purely billed based on total number of used tokens(Input/Output).

---

## Exercise 2: Temperature Effects (llm_basics.py)

Compare outputs at temperature 0.1 vs 1.0:

1. Which temperature produced more consistent output?
2. Which temperature would you use for a customer support chatbot vs creative writing? Why?

**Your answer:**

1. I feel neither of the outputs are consistent, while comparing both outputs, 0.1 temperature is better in consistency. 
2. I use temperatue 0.1 for customer support chatbot because the answers are more likely and short. On the otherhand, I will use temperature 1.0 for creative writing because of the broader perspectives and detailed answers.

---

## Exercise 3: Bedrock Model Comparison (bedrock_playground.py)

Run `python day1/bedrock_playground.py`:

1. Which model was fastest? Which was slowest?
2. Which model gave the best explanation of attention? Why do you think so?
3. What was the cost difference between the cheapest and most expensive model for the same prompt?

**Your answer:**

1. Fastest: Nova-lite, Slowest: Llama3-8b-instruct
2. Haiku 4.5 model gives the best explanation because it's answer is exactly two sentences with reasonable length, uses right wordings and doesn't go into too much technical details.
3. 1.499s

---

## Exercise 4: Prompt Engineering (prompt_patterns.py)

Run `python day1/prompt_patterns.py` and inspect `prompt_results.json`:

1. Which prompt style (zero-shot, few-shot, chain-of-thought) gave the most accurate answer?
2. When would you use chain-of-thought in a production FDE deployment?
3. Rewrite the zero-shot prompt to get a better answer. Paste your improved prompt here:

**Your answer:**

1. All three gave accurate answer 
2. I apply chain-of-thoughts when there is a need to think step-by-step and analyze before making a decicion(accuracy).
3. what is the capital of France?

---

## Daily Reflection

Answer these 2 sentences before you close your laptop:

1. What surprised you about how models generate text?
2. When would you use Claude vs Llama vs Titan in an AWS deployment?

**Your reflection:**

1. The attention step is the one that suprised me, because it is the process of understanding a prompt by weighing each vector aganist every other vector in the prompt.
2. Real-time voice assistance embedded in a mobile app requires low latency with moderate reasoning, so I will use Nova Lite. Code generation assistant integrated into a developer's IDE require very high reasoning irrespective of cost, so I will use Hailu 4.5. Simple FAQ/knowledge-base retrieval bot will be fine with low speed, moderate reason and with less cost, so I prefer Llama 3-8b
