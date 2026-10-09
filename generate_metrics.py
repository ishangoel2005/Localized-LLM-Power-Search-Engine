import os
import sys
import glob
import subprocess
from pathlib import Path

def ensure_dependencies():
    """Ensure matplotlib, pandas, and seaborn are installed since they are standard for graphing but missing from requirements."""
    missing = []
    for pkg in ['matplotlib', 'pandas', 'seaborn', 'pdfplumber']:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Installing missing graphing dependencies: {', '.join(missing)}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)

ensure_dependencies()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pdfplumber

def setup_output_dir(output_dir="metrics_output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def analyze_ragas_experiments(base_dir, output_dir):
    print("Analyzing RAG evaluation experiments...")
    csv_files = glob.glob(os.path.join(base_dir, "**", "*.csv"), recursive=True)
    # Filter out common non-experiment csvs if needed, or just keep them all
    csv_files = [f for f in csv_files if "venv" not in f and ".git" not in f]
    
    if not csv_files:
        print("No CSV files found in project.")
        return

    all_data = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df['source_experiment'] = os.path.basename(file)
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        if 'score' in combined_df.columns:
            plt.figure(figsize=(8, 5))
            sns.countplot(x='score', data=combined_df, palette="viridis")
            plt.title("RAG Evaluation Score Distribution (Pass vs Fail)")
            plt.xlabel("Score")
            plt.ylabel("Count")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "rag_evaluation_scores.png"))
            plt.close()
            print(f"Saved: {output_dir}/rag_evaluation_scores.png")

def analyze_pdfs(base_dir, output_dir):
    print("Analyzing PDF documents...")
    pdf_files = glob.glob(os.path.join(base_dir, "data", "**", "*.pdf"), recursive=True)
    if not pdf_files:
        print("No PDFs found.")
        return

    pdf_stats = []
    for pdf_path in pdf_files:
        file_size_kb = os.path.getsize(pdf_path) / 1024
        try:
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
        except:
            num_pages = 0
            
        pdf_stats.append({
            "filename": os.path.basename(pdf_path),
            "size_kb": file_size_kb,
            "pages": num_pages
        })

    if pdf_stats:
        df = pd.DataFrame(pdf_stats)
        
        # 1. Plot file sizes
        plt.figure(figsize=(10, 6))
        sns.barplot(x="size_kb", y="filename", data=df.sort_values("size_kb", ascending=False), palette="Blues_d")
        plt.title("PDF File Sizes (KB)")
        plt.xlabel("Size in KB")
        plt.ylabel("Document")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "pdf_file_sizes.png"))
        plt.close()
        print(f"Saved: {output_dir}/pdf_file_sizes.png")

        # 2. Plot number of pages
        plt.figure(figsize=(10, 6))
        sns.barplot(x="pages", y="filename", data=df.sort_values("pages", ascending=False), palette="Greens_d")
        plt.title("Number of Pages per PDF")
        plt.xlabel("Pages")
        plt.ylabel("Document")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "pdf_page_counts.png"))
        plt.close()
        print(f"Saved: {output_dir}/pdf_page_counts.png")

def count_vector_db_elements(base_dir, output_dir):
    print("Analyzing Vector Database size...")
    vector_dir = os.path.join(base_dir, "data", "vectors")
    
    if not os.path.exists(vector_dir):
        print("No Vector Database found.")
        return

    # Approximate size of vector db directory
    total_size = 0
    for dirpath, _, filenames in os.walk(vector_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                
    total_size_mb = total_size / (1024 * 1024)
    
    # Save a text summary
    with open(os.path.join(output_dir, "system_metrics.txt"), "w") as f:
        f.write(f"Vector Database Path: {vector_dir}\n")
        f.write(f"Approximate Vector DB Size (MB): {total_size_mb:.2f}\n")
    print(f"Saved: {output_dir}/system_metrics.txt")

def generate_dashboard(base_dir):
    output_dir = setup_output_dir(os.path.join(base_dir, "metrics_output"))
    print(f"Generating metrics in: {output_dir}\n...")
    
    analyze_ragas_experiments(base_dir, output_dir)
    analyze_pdfs(base_dir, output_dir)
    count_vector_db_elements(base_dir, output_dir)

    print("\nGeneration Complete! Check the 'metrics_output' directory for your graphs.")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    generate_dashboard(project_root)
