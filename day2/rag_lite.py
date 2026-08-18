import os
import json
import time
import numpy as np
import faiss
import boto3
from dotenv import load_dotenv

load_dotenv()
bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

def get_embedding(text):
    payload = {"inputText": text}
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps(payload)
    )
    result = json.loads(response["body"].read())
    return result["embedding"]

def chunk_text(text, chunk_size=512, overlap=0.1):
    words = text.split()
    chunk_words = int(chunk_size / 4)
    step = int(chunk_words * (1 - overlap))
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_words])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def build_index(chunks):
    embeddings = [get_embedding(c) for c in chunks]
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings

def retrieve(query, chunks, index, embeddings, k=3):
    query_vec = np.array([get_embedding(query)]).astype("float32")
    distances, indices = index.search(query_vec, k)
    return [chunks[i] for i in indices[0]]

def main():
    sample_doc = """
    Artificial intelligence is transforming industries by automating complex tasks.
    Machine learning models can now generate human-like text, translate languages,
    and write code. Large language models like Claude and GPT-4 are built on
    transformer architectures that use attention mechanisms to process context.
    RAG combines retrieval with generation to produce grounded, factual answers.
    """
    chunks = chunk_text(sample_doc)
    print(f"Chunked document into {len(chunks)} chunks")
    index, embeddings = build_index(chunks)
    query = "How do RAG systems work?"
    top_chunks = retrieve(query, chunks, index, embeddings)
    print(f"\nTop chunks for query: '{query}'\n")
    for i, c in enumerate(top_chunks, 1):
        print(f"{i}. {c[:200]}...")
    context = "\n".join(top_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    print(f"\n--- Final prompt sent to Claude ---\n{prompt[:400]}...")

if __name__ == "__main__":
    main()
