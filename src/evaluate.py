import argparse
import json
import pandas as pd
from akgc_optimized import OptimizedAKGC
from utils.metrics import compute_accuracy, compute_rouge_l, compute_bertscore, compute_hvi
import yaml

def load_dataset(dataset_path):
    """Load dataset from JSON file."""
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate(dataset_path, metrics, output_dir):
    """Evaluate AKGC on dataset and save results."""
    import torch
    from akgc_algorithm import load_config, load_model, load_llm
    
    dataset = load_dataset(dataset_path)
    results = {"prompt": [], "response": [], "is_factual": [], "hvi": []}
    
    # Load models
    config = load_config()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, tokenizer = load_model(config["model"], device)
    llm, llm_tokenizer = load_llm(device)
    
    for item in dataset:
        prompt = item["prompt"]
        ground_truth = item.get("ground_truth", "")
        akgc = OptimizedAKGC()
        try:
            response, is_factual, hvi = akgc.adaptive_correction_optimized(
                prompt,
                sim_threshold=akgc.config.get("sim_threshold", 0.8),
                hvi_threshold=akgc.config.get("hvi_threshold", 0.7)
            )
        except Exception as e:
            print(f"[ERROR] KG fetch or correction failed for prompt: '{prompt}' | Error: {e}")
            response, is_factual, hvi = "[KG fetch failed]", False, 0.0
        
        results["prompt"].append(prompt)
        results["response"].append(response)
        results["is_factual"].append(is_factual)
        results["hvi"].append(hvi)
        
        if ground_truth:
            if "accuracy" in metrics:
                results.setdefault("accuracy", []).append(compute_accuracy(response, ground_truth))
            if "rouge_l" in metrics:
                results.setdefault("rouge_l", []).append(compute_rouge_l(response, ground_truth))
            if "bertscore" in metrics:
                results.setdefault("bertscore", []).append(compute_bertscore(response, ground_truth))
    
    # Save results
    df = pd.DataFrame(results)
    for metric in metrics + ["hvi"]:
        df[[metric]].to_csv(f"{output_dir}/{metric}.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate AKGC on dataset")
    parser.add_argument("--dataset", type=str, required=True, help="Path to dataset (e.g., data/halu_eval/qa.json)")
    parser.add_argument("--metrics", nargs="+", default=["accuracy", "rouge_l", "bertscore", "hvi"], help="Metrics to compute")
    parser.add_argument("--output_dir", type=str, default="results/halu_eval_results", help="Output directory")
    args = parser.parse_args()
    
    evaluate(args.dataset, args.metrics, args.output_dir)