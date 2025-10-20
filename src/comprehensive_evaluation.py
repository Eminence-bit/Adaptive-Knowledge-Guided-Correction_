#!/usr/bin/env python3
"""
Comprehensive Evaluation Pipeline for AKGC Algorithm
Evaluates on HaluEval, HotpotQA, and Custom datasets
"""

import argparse
import json
import os
import time
import pandas as pd
from datetime import datetime
from akgc_optimized import OptimizedAKGC
from utils.metrics import compute_accuracy, compute_rouge_l, compute_bertscore, compute_hvi
import torch

def load_dataset(dataset_path):
    """Load dataset from JSON file."""
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_dataset(model, tokenizer, llm, llm_tokenizer, dataset, device, 
                   dataset_name, max_samples=None):
    """Evaluate AKGC on a specific dataset."""
    print(f"\n{'='*60}")
    print(f"EVALUATING: {dataset_name.upper()}")
    print(f"{'='*60}")
    
    if max_samples:
        dataset = dataset[:max_samples]
        print(f"Using {len(dataset)} samples (limited from original)")
    
    results = {
        "prompt": [],
        "response": [],
        "ground_truth": [],
        "is_factual": [],
        "hvi": [],
        "accuracy": [],
        "rouge_l": [],
        "bertscore": [],
        "processing_time": []
    }
    
    start_time = time.time()
    
    for i, item in enumerate(dataset):
        if i % 10 == 0:
            print(f"Processing sample {i+1}/{len(dataset)}...")
        
        prompt = item["prompt"]
        ground_truth = item.get("ground_truth", item.get("answer", ""))
        
        # Measure processing time
        sample_start = time.time()
        
        try:
            response, is_factual, hvi = adaptive_correction(
                model, tokenizer, llm, llm_tokenizer, prompt, device, 
                sim_threshold=0.8, hvi_threshold=0.7
            )
            
            # Compute metrics
            acc = compute_accuracy(response, ground_truth)
            rouge_l = compute_rouge_l(response, ground_truth)
            bertscore = compute_bertscore(response, ground_truth)
            
            sample_time = time.time() - sample_start
            
        except Exception as e:
            print(f"Error processing sample {i+1}: {e}")
            response = "Error in processing"
            is_factual = False
            hvi = 0.0
            acc = 0.0
            rouge_l = 0.0
            bertscore = 0.0
            sample_time = 0.0
        
        # Store results
        results["prompt"].append(prompt)
        results["response"].append(response)
        results["ground_truth"].append(ground_truth)
        results["is_factual"].append(is_factual)
        results["hvi"].append(hvi)
        results["accuracy"].append(acc)
        results["rouge_l"].append(rouge_l)
        results["bertscore"].append(bertscore)
        results["processing_time"].append(sample_time)
    
    total_time = time.time() - start_time
    
    # Calculate summary statistics
    summary = {
        "dataset": dataset_name,
        "total_samples": len(dataset),
        "total_time": total_time,
        "avg_time_per_sample": total_time / len(dataset),
        "accuracy": sum(results["accuracy"]) / len(results["accuracy"]),
        "rouge_l": sum(results["rouge_l"]) / len(results["rouge_l"]),
        "bertscore": sum(results["bertscore"]) / len(results["bertscore"]),
        "hvi": sum(results["hvi"]) / len(results["hvi"]),
        "factual_rate": sum(results["is_factual"]) / len(results["is_factual"])
    }
    
    print(f"\nRESULTS SUMMARY:")
    print(f"Total samples: {summary['total_samples']}")
    print(f"Total time: {summary['total_time']:.2f}s")
    print(f"Avg time per sample: {summary['avg_time_per_sample']:.3f}s")
    print(f"Accuracy: {summary['accuracy']:.3f}")
    print(f"ROUGE-L: {summary['rouge_l']:.3f}")
    print(f"BERTScore: {summary['bertscore']:.3f}")
    print(f"HVI: {summary['hvi']:.3f}")
    print(f"Factual Rate: {summary['factual_rate']:.3f}")
    
    return results, summary

def save_results(results, summary, output_dir, dataset_name):
    """Save results to CSV files and summary to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save detailed results
    df = pd.DataFrame(results)
    df.to_csv(f"{output_dir}/{dataset_name}_detailed.csv", index=False)
    
    # Save summary
    with open(f"{output_dir}/{dataset_name}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Save individual metric files
    for metric in ["accuracy", "rouge_l", "bertscore", "hvi"]:
        df[[metric]].to_csv(f"{output_dir}/{dataset_name}_{metric}.csv", index=False)

def main():
    parser = argparse.ArgumentParser(description="Comprehensive AKGC Evaluation")
    parser.add_argument("--datasets", nargs="+", 
                       default=["halu_eval", "hotpotqa", "custom"],
                       help="Datasets to evaluate")
    parser.add_argument("--max_samples", type=int, default=1000,
                       help="Maximum samples per dataset")
    parser.add_argument("--output_dir", type=str, default="results/comprehensive",
                       help="Output directory for results")
    parser.add_argument("--device", type=str, default="auto",
                       help="Device to use (auto, cpu, cuda)")
    
    args = parser.parse_args()
    
    # Setup device
    if args.device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
    
    print(f"Using device: {device}")
    
    # Load models
    print("Loading models...")
    config = load_config()
    model, tokenizer = load_model(config["model"], device)
    llm, llm_tokenizer = load_llm(device)
    print("Models loaded successfully!")
    
    # Dataset paths
    dataset_paths = {
        "halu_eval": "data/halu_eval/qa.json",
        "hotpotqa": "data/hotpotqa/hotpot_dev.json",
        "custom": "data/custom/custom_dataset.json"
    }
    
    all_summaries = []
    
    # Evaluate each dataset
    for dataset_name in args.datasets:
        if dataset_name not in dataset_paths:
            print(f"Warning: Unknown dataset {dataset_name}, skipping...")
            continue
        
        dataset_path = dataset_paths[dataset_name]
        if not os.path.exists(dataset_path):
            print(f"Warning: Dataset {dataset_path} not found, skipping...")
            continue
        
        try:
            print(f"\nLoading {dataset_name} dataset...")
            dataset = load_dataset(dataset_path)
            
            results, summary = evaluate_dataset(
                model, tokenizer, llm, llm_tokenizer, dataset, device,
                dataset_name, args.max_samples
            )
            
            save_results(results, summary, args.output_dir, dataset_name)
            all_summaries.append(summary)
            
        except Exception as e:
            print(f"Error evaluating {dataset_name}: {e}")
            continue
    
    # Create overall summary
    if all_summaries:
        overall_summary = {
            "evaluation_date": datetime.now().isoformat(),
            "device": device,
            "datasets": all_summaries,
            "overall_accuracy": sum(s["accuracy"] for s in all_summaries) / len(all_summaries),
            "overall_rouge_l": sum(s["rouge_l"] for s in all_summaries) / len(all_summaries),
            "overall_bertscore": sum(s["bertscore"] for s in all_summaries) / len(all_summaries),
            "overall_hvi": sum(s["hvi"] for s in all_summaries) / len(all_summaries)
        }
        
        with open(f"{args.output_dir}/overall_summary.json", "w") as f:
            json.dump(overall_summary, f, indent=2)
        
        print(f"\n{'='*60}")
        print("OVERALL RESULTS")
        print(f"{'='*60}")
        print(f"Overall Accuracy: {overall_summary['overall_accuracy']:.3f}")
        print(f"Overall ROUGE-L: {overall_summary['overall_rouge_l']:.3f}")
        print(f"Overall BERTScore: {overall_summary['overall_bertscore']:.3f}")
        print(f"Overall HVI: {overall_summary['overall_hvi']:.3f}")
        print(f"\nResults saved to: {args.output_dir}")

if __name__ == "__main__":
    def main():
        akgc = OptimizedAKGC()
        # ...existing code...
        for sample in dataset:
            prompt = sample["prompt"]
            ground_truth = sample.get("ground_truth", "")
            try:
                response, is_factual, hvi = akgc.adaptive_correction_optimized(
                    prompt,
                    sim_threshold=akgc.config.get("sim_threshold", 0.8),
                    hvi_threshold=akgc.config.get("hvi_threshold", 0.7)
                )
            except Exception as e:
                print(f"[ERROR] KG fetch or correction failed for prompt: '{prompt}' | Error: {e}")
                response, is_factual, hvi = "[KG fetch failed]", False, 0.0
            # ...existing code...
