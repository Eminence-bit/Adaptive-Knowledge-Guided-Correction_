#!/usr/bin/env python3
"""
HaluEval Dataset Downloader
Downloads HaluEval dataset from HuggingFace for AKGC testing
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datasets import load_dataset


class HaluEvalDownloader:
    """Downloads and prepares HaluEval dataset from HuggingFace."""
    
    def __init__(self, output_dir: str = "data/halueval"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.dataset_name = "pminervini/HaluEval"
        
        # Available subsets in HaluEval
        self.subsets = {
            'qa': 'Question Answering',
            'dialogue': 'Dialogue',
            'summarization': 'Summarization',
            'general': 'General'
        }
    
    def download_subset(self, subset: str, split: str = 'data') -> List[Dict]:
        """Download a subset of HaluEval dataset using datasets library."""
        
        print(f"📥 Downloading HaluEval - {self.subsets.get(subset, subset)} subset...")
        
        try:
            # Load the dataset using HuggingFace datasets library
            ds = load_dataset(self.dataset_name, subset, split=split)
            
            # Convert to list of dictionaries
            all_rows = [dict(item) for item in ds]
            
            print(f"✅ Downloaded {len(all_rows)} total rows")
            return all_rows
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return []
    
    def download_all_subsets(self) -> Dict[str, List[Dict]]:
        """Download all available subsets."""
        print("🚀 Downloading HaluEval Dataset from HuggingFace")
        print("=" * 70)
        
        all_data = {}
        
        for subset, description in self.subsets.items():
            print(f"\n📂 Subset: {description}")
            data = self.download_subset(subset)
            
            if data:
                all_data[subset] = data
                # Save individual subset
                self.save_subset(data, subset)
        
        return all_data
    
    def save_subset(self, data: List[Dict], subset: str):
        """Save subset to file."""
        output_path = self.output_dir / f"halueval_{subset}_raw.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {output_path}")
    
    def preprocess_for_akgc(self, data: List[Dict], subset: str) -> List[Dict]:
        """Preprocess HaluEval data for AKGC testing."""
        
        print(f"\n🔧 Preprocessing {subset} subset for AKGC...")
        
        processed = []
        
        for idx, item in enumerate(data, 1):
            processed_item = {
                'id': f"{subset}_{idx}",
                'subset': subset,
                'prompt': None,
                'ground_truth': None,
                'metadata': {}
            }
            
            # Handle different subset formats
            if subset == 'summarization':
                # Summarization: document, right_summary, hallucinated_summary
                if 'hallucinated_summary' in item:
                    processed_item['prompt'] = str(item['hallucinated_summary']).strip()
                if 'right_summary' in item:
                    processed_item['ground_truth'] = str(item['right_summary']).strip()
                if 'document' in item:
                    processed_item['metadata']['document'] = str(item['document']).strip()[:500]  # Truncate long docs
                    
            elif subset == 'general':
                # General: user_query, chatgpt_response, hallucination, hallucination_spans
                if 'chatgpt_response' in item:
                    processed_item['prompt'] = str(item['chatgpt_response']).strip()
                if 'user_query' in item:
                    processed_item['metadata']['user_query'] = str(item['user_query']).strip()
                if 'hallucination' in item:
                    processed_item['metadata']['hallucination'] = item['hallucination']
                if 'hallucination_spans' in item:
                    processed_item['metadata']['hallucination_spans'] = item['hallucination_spans']
                # For general, we don't have ground truth, just hallucination labels
                
            else:
                # QA and Dialogue: question, knowledge, hallucinated_answer/response, right_answer/response
                # Extract prompt (the potentially hallucinated text)
                if 'hallucinated_answer' in item:
                    processed_item['prompt'] = str(item['hallucinated_answer']).strip()
                elif 'hallucinated_response' in item:
                    processed_item['prompt'] = str(item['hallucinated_response']).strip()
                elif 'answer' in item:
                    processed_item['prompt'] = str(item['answer']).strip()
                elif 'response' in item:
                    processed_item['prompt'] = str(item['response']).strip()
                
                # Extract ground truth (the correct answer)
                if 'right_answer' in item:
                    processed_item['ground_truth'] = str(item['right_answer']).strip()
                elif 'right_response' in item:
                    processed_item['ground_truth'] = str(item['right_response']).strip()
                elif 'correct_answer' in item:
                    processed_item['ground_truth'] = str(item['correct_answer']).strip()
                
                # Add question as context if available
                if 'question' in item:
                    processed_item['metadata']['question'] = str(item['question']).strip()
                
                # Add knowledge as context if available
                if 'knowledge' in item:
                    processed_item['metadata']['knowledge'] = str(item['knowledge']).strip()
            
            # Store all other metadata
            for key, value in item.items():
                if key not in processed_item['metadata'] and key not in ['hallucinated_answer', 'hallucinated_response', 
                                                                          'right_answer', 'right_response', 
                                                                          'hallucinated_summary', 'right_summary',
                                                                          'chatgpt_response', 'document']:
                    processed_item['metadata'][key] = value
            
            # Only add if we have a prompt
            if processed_item['prompt']:
                processed.append(processed_item)
        
        print(f"✅ Preprocessed {len(processed)} items")
        return processed
    
    def save_preprocessed(self, data: List[Dict], subset: str):
        """Save preprocessed data."""
        output_path = self.output_dir / f"halueval_{subset}_preprocessed.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Preprocessed data saved to: {output_path}")
        return str(output_path)
    
    def download_and_preprocess(self, subsets: Optional[List[str]] = None) -> Dict[str, str]:
        """Complete download and preprocessing pipeline."""
        
        if subsets is None:
            subsets = list(self.subsets.keys())
        
        print("🚀 HaluEval Dataset Download & Preprocessing Pipeline")
        print("=" * 70)
        print(f"📊 Subsets to download: {', '.join(subsets)}")
        print(f"📏 Items per subset: ALL AVAILABLE")
        print()
        
        output_paths = {}
        
        for subset in subsets:
            if subset not in self.subsets:
                print(f"⚠️ Unknown subset: {subset}, skipping...")
                continue
            
            print(f"\n{'='*70}")
            print(f"Processing: {self.subsets[subset]}")
            print('='*70)
            
            # Download
            raw_data = self.download_subset(subset)
            
            if not raw_data:
                print(f"⚠️ No data downloaded for {subset}")
                continue
            
            # Save raw data
            self.save_subset(raw_data, subset)
            
            # Preprocess
            processed_data = self.preprocess_for_akgc(raw_data, subset)
            
            if processed_data:
                output_path = self.save_preprocessed(processed_data, subset)
                output_paths[subset] = output_path
        
        # Create combined dataset
        if output_paths:
            self.create_combined_dataset(output_paths)
        
        print("\n" + "=" * 70)
        print("✅ Download & Preprocessing Complete!")
        print("=" * 70)
        
        return output_paths
    
    def create_combined_dataset(self, output_paths: Dict[str, str]):
        """Combine all subsets into one dataset."""
        print("\n🔗 Creating combined dataset...")
        
        combined = []
        
        for subset, path in output_paths.items():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined.extend(data)
        
        combined_path = self.output_dir / "halueval_combined_preprocessed.json"
        
        with open(combined_path, 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Combined dataset created: {combined_path}")
        print(f"   Total items: {len(combined)}")
        
        return str(combined_path)
    
    def print_sample(self, subset: str, num_samples: int = 3):
        """Print sample data from a subset."""
        file_path = self.output_dir / f"halueval_{subset}_preprocessed.json"
        
        if not file_path.exists():
            print(f"⚠️ File not found: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n📋 Sample data from {subset} subset:")
        print("=" * 70)
        
        for i, item in enumerate(data[:num_samples], 1):
            print(f"\nSample {i}:")
            print(f"  ID: {item['id']}")
            print(f"  Prompt: {item['prompt'][:100]}...")
            if item['ground_truth']:
                print(f"  Ground Truth: {item['ground_truth'][:100]}...")
            print(f"  Metadata: {list(item['metadata'].keys())}")


def main():
    """Main function."""
    import sys
    
    # Parse arguments
    subsets = None
    
    if '--subset' in sys.argv:
        idx = sys.argv.index('--subset')
        if idx + 1 < len(sys.argv):
            subsets = [sys.argv[idx + 1]]
    
    if '--all' in sys.argv:
        subsets = None  # Download all
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
HaluEval Dataset Downloader

Usage:
  python src/download_halueval.py [options]

Options:
  --subset NAME    Download specific subset (qa, dialogue, summarization, general)
  --all            Download all subsets (default)
  --help, -h       Show this help message

Examples:
  # Download all subsets (all available items)
  python src/download_halueval.py --all

  # Download only QA subset
  python src/download_halueval.py --subset qa

  # Download only dialogue subset
  python src/download_halueval.py --subset dialogue
""")
        return
    
    # Default: download all subsets
    if subsets is None and '--subset' not in sys.argv:
        subsets = None  # Will download all
    
    try:
        downloader = HaluEvalDownloader()
        output_paths = downloader.download_and_preprocess(subsets=subsets)
        
        if output_paths:
            print("\n📂 Downloaded Files:")
            for subset, path in output_paths.items():
                print(f"   {subset}: {path}")
            
            print("\n🧪 Ready for Testing!")
            print("\nNext steps:")
            print("  # Test individual subset:")
            for subset in output_paths.keys():
                print(f"  python src/test_external_dataset.py data/halueval/halueval_{subset}_preprocessed.json")
                break  # Just show one example
            
            print("\n  # Test combined dataset:")
            print("  python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json")
            
            print("\n  # Test with ultra-optimized mode:")
            print("  python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --ultra")
            
            # Print sample
            if output_paths:
                first_subset = list(output_paths.keys())[0]
                downloader.print_sample(first_subset, num_samples=2)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
