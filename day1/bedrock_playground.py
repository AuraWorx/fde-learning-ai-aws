import os
import json
import time
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# Create an AWS session using the Administrator profile and configured region
session = boto3.Session(
    profile_name="AWSAdministratorAccess-755785010596",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

# Create a Bedrock Runtime client to invoke foundation models
BEDROCK = session.client("bedrock-runtime")

# Original Bedrock client without explicitly selecting an AWS profile
# BEDROCK = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

MODELS = {
    "claude-sonnet-4-6": "us.anthropic.claude-sonnet-4-6",
    "llama-3-8b": "meta.llama3-8b-instruct-v1:0",
    "nova-lite": "amazon.nova-lite-v1:0",
}


def invoke_bedrock(model_id, prompt):
    payload = {
        "us.anthropic.claude-sonnet-4-6": {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        },
        "meta.llama3-8b-instruct-v1:0": {
            "prompt": prompt,
            "max_gen_len": 300,
            "temperature": 0.7,
        },
        "amazon.nova-lite-v1:0": {
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 300, "temperature": 0.7},
        },
        # "amazon.nova-lite-v1:0": {
        #     "inputText": prompt,
        #     "textGenerationConfig": {"maxTokenCount": 300, "temperature": 0.7}
        # }
    }

    body = payload[model_id]
    # body = payload.get(model_id, payload["amazon.nova-lite-v1:0"]) #default to nova-lite if model_id not found
    start = time.time()
    try:
        response = BEDROCK.invoke_model(modelId=model_id, body=json.dumps(body))

        latency = time.time() - start

        # Read the model response
        response_body = json.loads(response["body"].read())

        # Extract the generated text from each model's response
        if model_id.startswith("us.anthropic."):
            generated_text = response_body.get("content", [{}])[0].get("text", "")
        elif model_id.startswith("meta.llama"):
            generated_text = response_body.get("generation", "")
        elif model_id.startswith("amazon.nova"):
            generated_text = (
                response_body.get("output", {})
                .get("message", {})
                .get("content", [{}])[0]
                .get("text", "")
            )
        else:
            generated_text = ""

        # Extract token usage based on each model's response format
        if model_id.startswith("us.anthropic."):
            input_tokens = response_body.get("usage", {}).get("input_tokens", 0)
            output_tokens = response_body.get("usage", {}).get("output_tokens", 0)

        elif model_id.startswith("meta.llama"):
            input_tokens = response_body.get("prompt_token_count", 0)
            output_tokens = response_body.get("generation_token_count", 0)

        elif model_id.startswith("amazon.nova"):
            input_tokens = response_body.get("usage", {}).get("inputTokens", 0)
            output_tokens = response_body.get("usage", {}).get("outputTokens", 0)

        else:
            input_tokens = 0
            output_tokens = 0

        # Calculate estimated cost
        cost = estimate_cost(model_id, input_tokens, output_tokens)

        # Store the result
        result = {
            "model": model_id,
            "response": generated_text,
            "latency_s": round(latency, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": round(cost, 6),
        }

        # response = BEDROCK.invoke_model(modelId=model_id, body=json.dumps(body))
        # latency = time.time() - start
        # response_body = json.loads(response["body"].read())
        # usage = response.get("usage", {})
        # input_tokens = usage.get("inputTokens", 0)
        # output_tokens = usage.get("outputTokens", 0)
        # cost = estimate_cost(model_id, input_tokens, output_tokens)
        # result = {
        #     "model": model_id,
        #     "latency_s": round(latency, 2),
        #     "input_tokens": input_tokens,
        #     "output_tokens": output_tokens,
        #     "estimated_cost_usd": round(cost, 6),
        # }
        print(
            f"[{model_id}] {latency:.2f}s | in:{input_tokens} out:{output_tokens} | ${cost:.6f}"
        )
        return result
    except ClientError as e:
        print(f"Error invoking {model_id}: {e}")
        return None


def estimate_cost(model_id, input_tokens, output_tokens):
    prices = {
        "us.anthropic.claude-sonnet-4-6": (0.003, 0.015),
        "meta.llama3-8b-instruct-v1:0": (0.0003, 0.0006),
        "amazon.nova-lite-v1:0": (0.0003, 0.0006),
    }
    in_price, out_price = prices.get(model_id, (0.0003, 0.0006))
    return (input_tokens * in_price + output_tokens * out_price) / 1000


def main():
    prompt = "Explain, in two sentences, how attention mechanisms work in transformers."
    results = []
    for name, model_id in MODELS.items():
        print(f"\nInvoking {name}...")
        res = invoke_bedrock(model_id, prompt)
        if res:
            results.append(res)
    with open("bedrock_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to bedrock_results.json")


if __name__ == "__main__":
    main()
