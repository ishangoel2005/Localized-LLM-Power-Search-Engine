import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
csv_path = r"f:\Localized-LLM-Minor-Project\metrics_output\llm_performance_data.csv"
output_path = r"f:\Localized-LLM-Minor-Project\metrics_output\latency_vs_speed_comparison.png"

# Load data
df = pd.read_csv(csv_path)

# Calculate correlation
correlation = df['latency_sec'].corr(df['tokens_per_second'])
print(f"Correlation between latency and tokens_per_second: {correlation:.4f}")

# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot latency on primary y-axis
color = 'tab:red'
ax1.set_xlabel('Prompt ID', fontweight='bold')
ax1.set_ylabel('Latency (seconds)', color=color, fontweight='bold')
line1 = ax1.plot(df['prompt_id'], df['latency_sec'], marker='o', color=color, label='Latency (sec)')
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot tokens per second on secondary y-axis
color = 'tab:blue'
ax2.set_ylabel('Generation Speed (tokens/second)', color=color, fontweight='bold')
line2 = ax2.plot(df['prompt_id'], df['tokens_per_second'], marker='s', color=color, label='Tokens/sec')
ax2.tick_params(axis='y', labelcolor=color)

# Add title
plt.title('Latency vs Generation Speed of LLM Across Prompts', fontsize=14, fontweight='bold')

# Combine legends from both axes
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

# Adjust layout and save
plt.grid(True, linestyle='--', alpha=0.5)
fig.tight_layout()
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Graph successfully saved to: {output_path}")
