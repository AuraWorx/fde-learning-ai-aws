import json
import os
import time
import boto3

bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
MODEL = os.getenv("BEDROCK_MODEL", "us.anthropic.claude-3-haiku-20240307-v1:0")

def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    user_message = body.get("message", "Hello!")
    start = time.time()
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": user_message}]
    }
    response = bedrock.invoke_model(modelId=MODEL, body=json.dumps(payload))
    latency = time.time() - start
    result = json.loads(response["body"].read())
    # print("result=",repr(result))
    reply = result["content"][0]["text"]
    # print("reply=", repr(reply))
    usage = result.get("usage", {})
    # print("usage=", repr(usage))
    print(json.dumps({
        "model": MODEL,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "latency_s": round(latency, 2)
    }))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "reply": reply,
            "latency_s": round(latency, 2),
            "model": MODEL,
            "usage": usage,
            "input_token": usage.get("input_tokens"),
            "outpur_tokens": usage.get("output_tokens")
        })
    }
