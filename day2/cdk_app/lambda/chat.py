import json
import os
import time
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


def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    user_message = body.get("message", "Hello!")
    start = time.time()
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": user_message}],
    }
    response = bedrock.invoke_model(modelId=MODEL, body=json.dumps(payload))
    latency = time.time() - start
    result = json.loads(response["body"].read())
    reply = result["content"][0]["text"]

    # Get token usage from the Bedrock response.
    # This is useful for monitoring token usage and estimating costs.
    usage = result.get("usage", {})

    # Log model, latency, and token usage to CloudWatch.
    # This helps us monitor the API in a production environment.
    logger.info(
        json.dumps(
            {
                "event": "bedrock_request",
                "model": MODEL,
                "latency_s": round(latency, 2),
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
            }
        )
    )
    # usage = response.get("usage", {})
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "reply": reply,
                "latency_s": round(latency, 2),
                "model": MODEL,
                "usage": usage,
            }
        ),
    }
