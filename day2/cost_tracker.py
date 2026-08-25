import os
import json
import time
import boto3
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
region = os.getenv("AWS_REGION", "us-east-1")
logs = boto3.client("logs", region_name=region)
cloudwatch = boto3.client("cloudwatch", region_name=region)

def get_log_group():
    return "/aws/lambda/AIServerlessStack-ChatFunction3D7C447E-2EQ3vIKOUfy4"

def estimate_cost(model, input_tokens, output_tokens):
    prices = {
        "us.anthropic.claude-haiku-4-5-20251001-v1:0": (0.003, 0.015),
        "meta.llama3-8b-instruct-v1:0": (0.0003, 0.0006),
        "amazon.nova-lite-v1:0": (0.0003, 0.0006),
    }
    in_price, out_price = prices.get(model, (0.0003, 0.0006))
    return (input_tokens * in_price + output_tokens * out_price) / 1000

def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"=== Cost Tracker: {today} ===\n")

    end_time = int(datetime.now(timezone.utc).timestamp())
    start_time = end_time - 24 * 60 * 60  # last 24 hours

    query = """
    fields model, input_tokens, output_tokens
    | filter ispresent(model)
    """

    response = logs.start_query(
        logGroupName=get_log_group(),
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )
    query_id = response["queryId"]

    while True:
        result = logs.get_query_results(queryId=query_id)
        if result["status"] in ("Complete", "Failed", "Cancelled"):
            break
        time.sleep(1)

    if result["status"] != "Complete":
        print(f"Query did not complete: {result['status']}")
        return

    total_invocations = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    by_model = {}

    for row in result["results"]:
        fields = {f["field"]: f["value"] for f in row}
        model = fields.get("model", "unknown")
        input_tokens = int(fields.get("input_tokens", 0) or 0)
        output_tokens = int(fields.get("output_tokens", 0) or 0)

        cost = estimate_cost(model, input_tokens, output_tokens)

        total_invocations += 1
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cost += cost

        if model not in by_model:
            by_model[model] = {"invocations": 0, "cost_usd": 0.0}
            by_model[model]["invocations"] += 1
            by_model[model]["cost_usd"] = round(by_model[model]["cost_usd"] + cost, 4)

    output = {
        "date": today,
        "total_invocations": total_invocations,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "estimated_cost_usd": round(total_cost, 4),
        "by_model": by_model,
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
