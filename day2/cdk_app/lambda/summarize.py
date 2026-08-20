import json
import os
import time
import urllib.request
import boto3
# from dotenv import load_dotenv

# load_dotenv()
bedrock = boto3.client(
    "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
)
MODEL = os.getenv("BEDROCK_MODEL", "us.anthropic.claude-sonnet-4-6")


def fetch_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="ignore")[:4000]


def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    url = body.get("url")
    if not url:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing url"})}
    try:
        text = fetch_url(url)
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    prompt = f"Summarize the following content in 2-3 sentences:\n\n{text}"
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = bedrock.invoke_model(modelId=MODEL, body=json.dumps(payload))
    result = json.loads(response["body"].read())
    summary = result["content"][0]["text"]
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"url": url, "summary": summary}),
    }
