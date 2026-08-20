import json
import os
import boto3

bedrock = boto3.client(
    "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
)


def handler(event, context):
    question = event.get("question", "")
    prompt = f"""You are a routing agent. Decide which tool to use for this question.
Available tools: weather, database.
Question: {question}
Respond with JSON only: {{"tool": "weather" or "database", "reason": "..."}}"""
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = bedrock.invoke_model(
        modelId="us.anthropic.claude-sonnet-4-6", body=json.dumps(payload)
    )
    result = json.loads(response["body"].read())
    text = result["content"][0]["text"]
    print("BEDROCK RAW TEXT:", repr(text))
    print("BEDROCK RAW RESPONSE:", json.dumps(result))
    try:
        cleaned_text = text.strip()

        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.replace("```json", "", 1)
            cleaned_text = cleaned_text.replace("```", "", 1).strip()

        decision = json.loads(cleaned_text)

    except json.JSONDecodeError:
        decision = {"tool": "none", "reason": "Could not parse LLM output"}
    # try:
    #     decision = json.loads(text)
    # except json.JSONDecodeError:
    #     decision = {"tool": "none", "reason": "Could not parse LLM output"}
    return {
        "question": question,
        "tool": decision.get("tool", "none"),
        "reason": decision.get("reason", ""),
    }
