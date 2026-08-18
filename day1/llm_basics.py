import os
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def tokenization_demo():
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    text = "Artificial intelligence is transforming how we build software."
    tokens = tokenizer.encode(text)
    decoded = tokenizer.decode(tokens)
    print(f"Original: {text}")
    print(f"Token IDs: {tokens}")
    print(f"Token count: {len(tokens)}")
    print(f"Decoded: {decoded}")
    return len(tokens)

def generate_with_temperature(prompt, temperature):
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    inputs = tokenizer(prompt, return_tensors="pt")
    start = time.time()
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        temperature=temperature,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    latency = time.time() - start
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\n--- Temperature {temperature} ---")
    print(f"Output: {generated}")
    print(f"Latency: {latency:.2f}s")
    return generated, latency

def main():
    print("=== LLM Basics: Tokenization + Generation ===\n")
    tokenization_demo()
    print("\n" + "="*60)
    low_temp, t1 = generate_with_temperature("The future of AI is", temperature=0.1)
    high_temp, t2 = generate_with_temperature("The future of AI is", temperature=1.0)
    print(f"\nLatency diff: {abs(t1-t2):.2f}s")

if __name__ == "__main__":
    main()
