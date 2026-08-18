import json
import random

def handler(event, context):
    tool = event.get("tool", "none")
    if tool == "weather":
        output = {"temperature_c": random.randint(10, 35), "condition": random.choice(["sunny", "cloudy", "rainy"])}
    elif tool == "database":
        output = {"records_found": random.randint(1, 100), "status": "success"}
    else:
        output = {"message": "No tool called"}
    return {"tool": tool, "tool_output": output}
