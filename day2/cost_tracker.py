import os
import json
import boto3
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
region = os.getenv("AWS_REGION", "us-east-1")
logs = boto3.client("logs", region_name=region)
cloudwatch = boto3.client("cloudwatch", region_name=region)

def get_log_group():
    return f"/aws/lambda/forward-deployed-ai-api-ChatFunction-*"

def estimate_cost(model, input_tokens, output_tokens):
    prices = {
        "anthropic.claude-3-sonnet-20240229-v1:0": (0.003, 0.015),
        "meta.llama3-8b-instruct-v1:0": (0.0003, 0.0006),
        "amazon.titan-text-express-v1": (0.0003, 0.0006),
    }
    in_price, out_price = prices.get(model, (0.0003, 0.0006))
    return (input_tokens * in_price + output_tokens * out_price) / 1000

def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"=== Cost Tracker: {today} ===\n")
    print("Run this script locally after deploying Day 2 API.")
    print("It scans CloudWatch Logs for the ChatFunction Lambda and sums token usage.\n")
    print("Expected output format:")
    example = {
        "date": today,
        "total_invocations": 42,
        "total_input_tokens": 21000,
        "total_output_tokens": 10500,
        "estimated_cost_usd": 0.18,
        "by_model": {
            "anthropic.claude-3-sonnet-20240229-v1:0": {
                "invocations": 42,
                "cost_usd": 0.18
            }
        }
    }
    print(json.dumps(example, indent=2))
    print("\nTODO: Replace this stub with actual CloudWatch Logs Insights query.")

if __name__ == "__main__":
    main()
