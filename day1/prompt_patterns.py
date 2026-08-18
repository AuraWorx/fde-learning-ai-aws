import json
import os
import sys
import boto3
from dotenv import load_dotenv

load_dotenv()
# Create an AWS session using the Administrator profile
session = boto3.Session(
    profile_name="AWSAdministratorAccess-755785010596"
)

# Create a Bedrock Runtime client
BEDROCK = session.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Original Bedrock client without explicitly selecting an AWS profile
# BEDROCK = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

QUESTION = "What is the capital of France? Provide only the city name."

PROMPTS = {
    "zero-shot": QUESTION,
    "few-shot": "Examples:\nQ: Capital of Spain?\nA: Madrid\nQ: Capital of Italy?\nA: Rome\nQ: Capital of France?\nA:",
    "chain-of-thought": f"Question: {QUESTION}\nLet's think step by step before answering."
}

# The original exercise used Claude 3 Sonnet.
# Claude 3 Sonnet has reached the end of its life in our Bedrock environment,
# so Llama 3 8B is used temporarily for testing the same prompt patterns.
def invoke_llama(prompt):
    body = {
        "prompt": prompt,
        "max_gen_len": 100,
        "temperature": 0
    }
    response = BEDROCK.invoke_model(
        modelId="meta.llama3-8b-instruct-v1:0",
        body=json.dumps(body)
    )
    result = json.loads(response["body"].read())
    return result["generation"].strip()

def main():
    print("=== Prompt Patterns Playground ===\n")
    outputs = {}
    for style, prompt in PROMPTS.items():
        print(f"--- {style.replace('-', ' ').title()} ---")
        print(f"Prompt: {prompt[:120]}...")
        answer = invoke_llama(prompt)
        print(f"Answer: {answer}\n")
        outputs[style] = {"prompt": prompt, "answer": answer}
    with open("prompt_results.json", "w") as f:
        json.dump(outputs, f, indent=2)
    print("Saved to prompt_results.json. Manually score: which style was most accurate?")

if __name__ == "__main__":
    main()
