import json
import os
import boto3
# from dotenv import load_dotenv

# load_dotenv()
bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

def handler(event, context):
    question = event.get("question", "")
    tool_output = event.get("tool_output", {})
    prompt = f"""You are a helpful assistant. Answer the user's question using the tool output if relevant.
Question: {question}
Tool output: {json.dumps(tool_output)}
Answer:"""
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = bedrock.invoke_model(modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0", body=json.dumps(payload))
    result = json.loads(response["body"].read())
    answer = result["content"][0]["text"]
    return {"question": question, "answer": answer, "tool_used": event.get("tool")}
