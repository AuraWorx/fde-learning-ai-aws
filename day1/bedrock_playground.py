import os
import json
import time
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

BEDROCK = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

MODELS = {
    "claude-haiku-4-5": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    "llama-3-8b": "meta.llama3-8b-instruct-v1:0",
    "nova-lite": "amazon.nova-lite-v1:0",
}

def extract_usage(model_id, response_body):
    """Token usage lives in a different-shaped field per provider under raw InvokeModel."""
    if "anthropic" in model_id:
        usage = response_body.get("usage", {})
        return usage.get("input_tokens", 0), usage.get("output_tokens", 0)
    if "llama" in model_id:
        return response_body.get("prompt_token_count", 0), response_body.get("generation_token_count", 0)
    if "nova" in model_id:
        usage = response_body.get("usage", {})
        return usage.get("inputTokens", 0), usage.get("outputTokens", 0)
    return 0, 0

def extract_text(model_id, response_body):
    """Generated text lives in a different-shaped field per provider under raw InvokeModel."""
    if "anthropic" in model_id:
        content = response_body.get("content", [])
        return content[0].get("text", "") if content else ""
    if "llama" in model_id:
        return response_body.get("generation", "")
    if "nova" in model_id:
        content = response_body.get("output", {}).get("message", {}).get("content", [])
        return content[0].get("text", "") if content else ""
    return ""

def invoke_bedrock(model_id, prompt):
    payload = {
        "us.anthropic.claude-haiku-4-5-20251001-v1:0": {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}]
        },
        "meta.llama3-8b-instruct-v1:0": {
            "prompt": prompt,
            "max_gen_len": 300,
            "temperature": 0.7
        },
        "amazon.nova-lite-v1:0": {
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 300, "temperature": 0.7}
        }
    }

    body = payload.get(model_id, payload["amazon.nova-lite-v1:0"])
    start = time.time()
    try:
        response = BEDROCK.invoke_model(modelId=model_id, body=json.dumps(body))
        latency = time.time() - start
        response_body = json.loads(response["body"].read())
        input_tokens, output_tokens = extract_usage(model_id, response_body)
        text = extract_text(model_id, response_body)
        cost = estimate_cost(model_id, input_tokens, output_tokens)
        result = {
            "model": model_id,
            "latency_s": round(latency, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": round(cost, 6),
            "response_text": text,
        }
        print(f"[{model_id}] {latency:.2f}s | in:{input_tokens} out:{output_tokens} | ${cost:.6f}")
        return result
    except ClientError as e:
        print(f"Error invoking {model_id}: {e}")
        return None

def estimate_cost(model_id, input_tokens, output_tokens):
    prices = {
        "us.anthropic.claude-haiku-4-5-20251001-v1:0": (0.001, 0.005),
        "meta.llama3-8b-instruct-v1:0": (0.0003, 0.0006),
        "amazon.nova-lite-v1:0": (0.00006, 0.00024),
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
