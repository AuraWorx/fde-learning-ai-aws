import os
import json
import boto3
import time
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

region = os.getenv("AWS_REGION", "us-east-1")
logs = boto3.client("logs", region_name=region)


# Claude Sonnet 4.6 pricing:
# $3 per 1M input tokens
# $15 per 1M output tokens
PRICES = {
    "us.anthropic.claude-sonnet-4-6": (3.00, 15.00),
}


def get_log_groups():
    """Find the Lambda log groups created by the CDK stack."""
    groups = []

    paginator = logs.get_paginator("describe_log_groups")

    for page in paginator.paginate(logGroupNamePrefix="/aws/lambda/AIServerlessStack-"):
        for group in page.get("logGroups", []):
            groups.append(group["logGroupName"])

    return groups


def query_logs_insights(log_group, start_time, end_time):
    """Query Bedrock request logs using CloudWatch Logs Insights."""

    query = """
        fields @message
        | filter @message like /"event": "bedrock_request"/
        | parse @message '"model": "*"' as parsed_model
        | parse @message '"input_tokens": *,' as parsed_input_tokens
        | parse @message '"output_tokens": *}' as parsed_output_tokens
        | stats count() as invocations,
            sum(parsed_input_tokens) as total_input_tokens,
            sum(parsed_output_tokens) as total_output_tokens
            by parsed_model
        """

    response = logs.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )

    query_id = response["queryId"]

    # Logs Insights queries run asynchronously, so wait for the result.
    while True:
        result = logs.get_query_results(queryId=query_id)

        if result["status"] in ["Complete", "Failed", "Cancelled"]:
            break

        time.sleep(1)

    if result["status"] != "Complete":
        return []

    return result.get("results", [])


def estimate_cost(model, input_tokens, output_tokens):
    """Calculate estimated Bedrock cost from token usage."""
    input_price, output_price = PRICES.get(model, (3.00, 15.00))

    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price

    return input_cost + output_cost


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Start of today in UTC, converted to milliseconds for CloudWatch.
    start_time = int(
        datetime.now(timezone.utc)
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .timestamp()
        * 1000
    )

    total_invocations = 0
    total_input_tokens = 0
    total_output_tokens = 0
    by_model = {}

    log_groups = get_log_groups()

    print(f"=== Cost Tracker: {today} ===\n")
    end_time = int(datetime.now(timezone.utc).timestamp())

    for log_group in log_groups:
        print(f"Reading: {log_group}")

        results = query_logs_insights(
            log_group,
            start_time // 1000,
            end_time,
        )

        for row in results:
            data = {item["field"]: item["value"] for item in row}

            model = data.get("parsed_model", "unknown")
            input_tokens = int(float(data.get("total_input_tokens", 0)))
            output_tokens = int(float(data.get("total_output_tokens", 0)))
            invocations = int(float(data.get("invocations", 0)))

            total_invocations += invocations
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens

            if model not in by_model:
                by_model[model] = {
                    "invocations": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0,
                }

            by_model[model]["invocations"] += invocations
            by_model[model]["input_tokens"] += input_tokens
            by_model[model]["output_tokens"] += output_tokens

            by_model[model]["cost_usd"] = round(
                estimate_cost(
                    model,
                    by_model[model]["input_tokens"],
                    by_model[model]["output_tokens"],
                ),
                6,
            )

    total_cost = estimate_cost(
        "us.anthropic.claude-sonnet-4-6",
        total_input_tokens,
        total_output_tokens,
    )

    result = {
        "date": today,
        "total_invocations": total_invocations,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "estimated_cost_usd": round(total_cost, 6),
        "by_model": by_model,
    }

    print("\n=== Daily Cost Estimate ===")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
