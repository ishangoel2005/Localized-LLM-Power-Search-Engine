import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from langchain_community.llms import Ollama

def setup_output_dir(output_dir="metrics_output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def measure_llm_performance():
    print("Initializing LLM Performance Test with local Ollama (Phi-3)...")
    try:
        # User doesn't have llama3.2, using phi3 instead
        llm = Ollama(model="phi3", base_url="http://localhost:11434")
    except Exception as e:
        print(f"Failed to initialize Ollama: {e}")
        return

    test_prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity briefly in one paragraph.",
        "Write a python script to reverse a string.",
        "Summarize the plot of the movie The Matrix.",
        "What are the main differences between Python and JavaScript?",
        "Write a short essay on the impact of artificial intelligence."
    ]

    results = []

    print("Running queries to measure latency and generation speed...")
    for i, prompt in enumerate(test_prompts):
        print(f"Running prompt {i+1}/{len(test_prompts)}...")
        
        start_time = time.time()
        try:
            response = llm.invoke(prompt)
            end_time = time.time()
            
            latency = end_time - start_time
            # Rough approximation of tokens: 1 word ~ 1.3 tokens
            word_count = len(response.split())
            approx_tokens = int(word_count * 1.3)
            tokens_per_second = approx_tokens / latency if latency > 0 else 0
            
            results.append({
                "prompt_id": f"P{i+1}",
                "prompt_length": len(prompt.split()),
                "latency_sec": latency,
                "response_words": word_count,
                "approx_tokens": approx_tokens,
                "tokens_per_second": tokens_per_second
            })
        except Exception as e:
            print(f"Error querying LLM: {e}. Is Ollama running?")
            return

    if results:
        df = pd.DataFrame(results)
        output_dir = setup_output_dir()
        
        # 1. Bar Chart: Latency per Prompt
        plt.figure(figsize=(10, 5))
        sns.barplot(x="prompt_id", y="latency_sec", data=df, palette="Reds_d")
        plt.title("LLM Inference Latency per Prompt (Seconds)")
        plt.xlabel("Prompt ID")
        plt.ylabel("Latency (sec)")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "llm_latency.png"))
        plt.close()
        
        # 2. Line Chart: Latency vs Response Size
        plt.figure(figsize=(10, 5))
        sns.scatterplot(x="approx_tokens", y="latency_sec", data=df, s=100, color="blue")
        sns.regplot(x="approx_tokens", y="latency_sec", data=df, scatter=False, color="red") # add trendline
        plt.title("LLM Latency vs Generated Tokens")
        plt.xlabel("Approx Output Tokens")
        plt.ylabel("Latency (sec)")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "llm_latency_vs_tokens.png"))
        plt.close()
        
        # 3. Bar Chart: Tokens per Second
        plt.figure(figsize=(10, 5))
        sns.barplot(x="prompt_id", y="tokens_per_second", data=df, palette="Greens_d")
        plt.title("LLM Generation Speed (Tokens / Second)")
        plt.xlabel("Prompt ID")
        plt.ylabel("Tokens per Second")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "llm_tokens_per_sec.png"))
        plt.close()

        # Save raw data
        df.to_csv(os.path.join(output_dir, "llm_performance_data.csv"), index=False)
        
        print("\nLLM Performance testing complete!")
        print(f"Average Latency: {df['latency_sec'].mean():.2f} sec")
        print(f"Average Generation Speed: {df['tokens_per_second'].mean():.2f} tokens/sec")
        print("Graphs saved to 'metrics_output': llm_latency.png, llm_latency_vs_tokens.png, llm_tokens_per_sec.png")

if __name__ == "__main__":
    measure_llm_performance()
