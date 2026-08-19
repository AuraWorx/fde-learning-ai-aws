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

1. the sample tokens produce 10 tokens.['Art', 'ificial', 'Ġintelligence', 'Ġis', 'Ġtransforming', 'Ġhow', 'Ġwe', 'Ġbuild', 'Ġsoftware', '.']
2. i was suprised by the punctuation("."), because i knew that words can be split into multiple tokens during tokenisation but i didnt know that punctuation also counted as a token.
3. Here token count is matters because bedrock pricing is based on the numbers of tokens used instead words thats why, more tokens more cost.

---

## Exercise 2: Temperature Effects (llm_basics.py)

Compare outputs at temperature 0.1 vs 1.0:

1. Which temperature produced more consistent output?
2. Which temperature would you use for a customer support chatbot vs creative writing? Why?

**Your answer:**

1. Temperature 0.1 is produced more consistent output because the lower temparature makes the model to choose the higher pobability tokens and maintain consistency.
2. For customer support chatbot i would use lower temperature such as 0.1, because it gives more consistent responses and make the model more likely choose to higher probability tokens. For creative writing i would choose higher temperature such as 1.0, because it completely opposite it lower temperature like it makes the model choose to more different and creative tokens includes lower probability tokens.

---

## Exercise 3: Bedrock Model Comparison (bedrock_playground.py)

Run `python day1/bedrock_playground.py`:

1. Which model was fastest? Which was slowest?
2. Which model gave the best explanation of attention? Why do you think so?
3. What was the cost difference between the cheapest and most expensive model for the same prompt?

**Your answer:**

1. Nova Lite was the fastest at 1.02 seconds, and Claude Sonnet 4.6 was the slowest at 4.94 seconds.
2. Claude Sonnet 4.6 gave the best explanation of attention because its response was clear and detailed while still staying within the two-sentence requirement.
3. Nova Lite was the cheapest at $0.000036, while Claude Sonnet 4.6 was the most expensive at $0.001326. The cost difference was $0.00129 for the same prompt.

---

## Exercise 4: Prompt Engineering (prompt_patterns.py)

Run `python day1/prompt_patterns.py` and inspect `prompt_results.json`:

1. Which prompt style (zero-shot, few-shot, chain-of-thought) gave the most accurate answer?
2. When would you use chain-of-thought in a production FDE deployment?
3. Rewrite the zero-shot prompt to get a better answer. Paste your improved prompt here:

**Your answer:**

1. zero-shot and few-shot gave the most accurate answers, bacause both correctly answered "paris".
2. I would use chain-of-thought for tasks that require multiple steps of reasoning, where the model needs to work through the problem before giving the final answer.
3. What is the capital city of France?
   Answer with only the city name and no additional text.

---

## Daily Reflection

Answer these 2 sentences before you close your laptop:

1. What surprised you about how models generate text?
2. When would you use Claude vs Llama vs Nova Lite in an AWS deployment?

**Your reflection:**

1. I was surprised that model changes how it chooses the tokens based on the temperature value.
2. I would use Claude for complex tasks and coding purposes, Llama for flexible and cost-effective solutions, and Nova Lite for fast and cost-effective AWS-native AI tasks.
