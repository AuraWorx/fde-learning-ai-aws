import json
import os
import sys
import boto3
from dotenv import load_dotenv

load_dotenv()
BEDROCK = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

QUESTION = "What is the capital of France? Provide only the city name."

PROMPTS = {
    "zero-shot": QUESTION,
    "few-shot": "Examples:\nQ: Capital of Spain?\nA: Madrid\nQ: Capital of Italy?\nA: Rome\nQ: Capital of France?\nA:",
    "chain-of-thought": f"Question: {QUESTION}\nLet's think step by step before answering."
}

def invoke_claude(prompt):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = BEDROCK.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body)
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

def main():
    print("=== Prompt Patterns Playground ===\n")
    outputs = {}
    for style, prompt in PROMPTS.items():
        print(f"--- {style.replace('-', ' ').title()} ---")
        print(f"Prompt: {prompt[:120]}...")
        answer = invoke_claude(prompt)
        print(f"Answer: {answer}\n")
        outputs[style] = {"prompt": prompt, "answer": answer}
    with open("prompt_results.json", "w") as f:
        json.dump(outputs, f, indent=2)
    print("Saved to prompt_results.json. Manually score: which style was most accurate?")

if __name__ == "__main__":
    main()
