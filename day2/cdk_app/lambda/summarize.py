import json
import os
import time
import urllib.request
import logging
import boto3
# from dotenv import load_dotenv

# load_dotenv()
bedrock = boto3.client(
    "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Configure Lambda logging so request information can be viewed in CloudWatch Logs.
logger = logging.getLogger()
logger.setLevel(logging.INFO)
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

    # Record the start time to measure how long the Bedrock request takes.
    start = time.time()

    response = bedrock.invoke_model(modelId=MODEL, body=json.dumps(payload))

    # Calculate the time taken by the Bedrock model request.
    latency = time.time() - start

    # Read and parse the response returned by Bedrock.
    result = json.loads(response["body"].read())

    # Extract the generated summary from Claude's response.
    summary = result["content"][0]["text"]

    # Get token usage from the Bedrock response.
    # This is useful for monitoring token usage and estimating costs.
    usage = result.get("usage", {})

    # Log model, latency, and token usage to CloudWatch.
    logger.info(
        json.dumps(
            {
                "event": "bedrock_summarize_request",
                "model": MODEL,
                "latency_s": round(latency, 2),
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
            }
        )
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "url": url,
                "summary": summary,
                "latency_s": round(latency, 2),
                "model": MODEL,
                "usage": usage,
            }
        ),
    }
