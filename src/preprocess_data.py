import argparse
import json
import os

def preprocess_dataset(input_path, output_path):
    """Preprocess HaluEval dataset to standardize format."""
    try:
        data = []
        # Read JSONL format (one JSON object per line)
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding line in {input_path}: {line[:100]}... Error: {e}")
                        continue
        
        processed = []
        for item in data:
            # Handle different field names across datasets
            prompt = item.get("question", item.get("prompt", ""))
            if "dialogue_history" in item:
                prompt = item.get("dialogue_history", "")
            elif "document" in item:
                prompt = item.get("document", "")
            elif "user_query" in item:
                prompt = item.get("user_query", "")
            
            knowledge = item.get("knowledge", item.get("answer", item.get("document", "")))
            
            # Handle different field names for correct/hallucinated answers
            right_answer = item.get("right_answer", 
                                   item.get("right_response", 
                                           item.get("right_summary", "")))
            hallucinated_answer = item.get("hallucinated_answer", 
                                          item.get("hallucinated_response", 
                                                  item.get("hallucinated_summary", "")))
            
            # Handle general dataset format (single response with hallucination label)
            if "chatgpt_response" in item and "hallucination" in item:
                response = item.get("chatgpt_response", "")
                is_hallucination = item.get("hallucination", "").lower() == "yes"
                
                processed_item = {
                    "prompt": prompt,
                    "ground_truth": knowledge,
                    "answer": response,
                    "is_hallucination": is_hallucination
                }
                processed.append(processed_item)
            else:
                # Create two examples for each item: one correct, one hallucinated
                if right_answer:
                    # Correct answer example
                    correct_item = {
                        "prompt": prompt,
                        "ground_truth": knowledge,
                        "answer": right_answer,
                        "is_hallucination": False
                    }
                    processed.append(correct_item)
                
                if hallucinated_answer:
                    # Hallucinated answer example
                    hallucinated_item = {
                        "prompt": prompt,
                        "ground_truth": knowledge,
                        "answer": hallucinated_answer,
                        "is_hallucination": True
                    }
                    processed.append(hallucinated_item)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write processed data with UTF-8 encoding
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(processed, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully processed {len(processed)} items from {input_path} to {output_path}")
    
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess dataset")
    parser.add_argument("--input", type=str, required=True, help="Input dataset path")
    parser.add_argument("--output", type=str, required=True, help="Output JSON path")
    args = parser.parse_args()
    
    preprocess_dataset(args.input, args.output)