import json
import os
import sys
import boto3
from dotenv import load_dotenv

load_dotenv()
# Create an AWS session using the Administrator profile
session = boto3.Session(profile_name="AWSAdministratorAccess-755785010596")

# Create a Bedrock Runtime client
BEDROCK = session.client(
    "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Original Bedrock client without explicitly selecting an AWS profile
# BEDROCK = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

QUESTION = "What is the capital of France? Provide only the city name."

PROMPTS = {
    "zero-shot": QUESTION,
    "few-shot": "Examples:\nQ: Capital of Spain?\nA: Madrid\nQ: Capital of Italy?\nA: Rome\nQ: Capital of France?\nA:",
    "chain-of-thought": f"Question: {QUESTION}\nLet's think step by step before answering.",
}


def invoke_claude(prompt):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = BEDROCK.invoke_model(
        modelId="us.anthropic.claude-sonnet-4-6", body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"].strip()


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
    print(
        "Saved to prompt_results.json. Manually score: which style was most accurate?"
    )


if __name__ == "__main__":
    main()
