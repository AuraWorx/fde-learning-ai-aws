import json
import os
import boto3
import re
# from dotenv import load_dotenv

# load_dotenv()
bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

def handler(event, context):
    # print(repr(event))
    question = event.get("question", "")
    # print(repr(question))
    prompt = f"""You are a routing agent. Decide which tool to use for this question.
Available tools: weather, database.
Question: {question}
Respond with JSON only: {{"tool": "weather" or "database", "reason": "..."}}"""
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": prompt}]
    }
    # print(repr(payload))
    response = bedrock.invoke_model(modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0", body=json.dumps(payload))
    # print(repr(response))
    result = json.loads(response["body"].read())
    # print(result)
    md_text = result["content"][0]["text"]
    match = re.search(r"\{.*\}", md_text, re.DOTALL)
    if match:
        text = match.group(0)
    # print(repr(text))
    try:
        decision = json.loads(text)
    except json.JSONDecodeError:
        decision = {"tool": "none", "reason": "Could not parse LLM output"}
    return {"question": question, "tool": decision.get("tool", "none"), "reason": decision.get("reason", "")}
