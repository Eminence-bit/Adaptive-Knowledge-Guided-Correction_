#!/usr/bin/env python3
"""
External Dataset Preprocessing Pipeline
Handles various dataset formats for AKGC testing
"""

import json
import csv
import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import re

class DatasetPreprocessor:
    """Preprocesses external datasets for AKGC testing."""
    
    def __init__(self, output_dir: str = "data/external"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Supported dataset formats
        self.supported_formats = ['.json', '.jsonl', '.csv', '.tsv', '.txt']
        
    def detect_format(self, file_path: str) -> str:
        """Detect the format of the input file."""
        path = Path(file_path)
        return path.suffix.lower()
    
    def load_json(self, file_path: str) -> List[Dict]:
        """Load JSON or JSONL format."""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.jsonl'):
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
            else:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
        return data
    
    def load_csv(self, file_path: str, delimiter: str = ',') -> List[Dict]:
        """Load CSV or TSV format."""
        df = pd.read_csv(file_path, delimiter=delimiter)
        return df.to_dict('records')
    
    def load_txt(self, file_path: str) -> List[Dict]:
        """Load plain text format (one statement per line)."""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    data.append({
                        'id': idx,
                        'text': line,
                        'prompt': line
                    })
        return data
    
    def load_dataset(self, file_path: str) -> List[Dict]:
        """Load dataset from file."""
        print(f"📂 Loading dataset from: {file_path}")
        
        format_type = self.detect_format(file_path)
        
        if format_type == '.json' or format_type == '.jsonl':
            data = self.load_json(file_path)
        elif format_type == '.csv':
            data = self.load_csv(file_path, delimiter=',')
        elif format_type == '.tsv':
            data = self.load_csv(file_path, delimiter='\t')
        elif format_type == '.txt':
            data = self.load_txt(file_path)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        print(f"✅ Loaded {len(data)} records")
        return data
    
    def normalize_fields(self, data: List[Dict]) -> List[Dict]:
        """Normalize field names across different datasets."""
        normalized = []
        
        # Common field name mappings
        text_fields = ['text', 'prompt', 'statement', 'claim', 'sentence', 'question', 'input']
        label_fields = ['label', 'ground_truth', 'answer', 'truth', 'correct', 'target']
        
        for idx, item in enumerate(data):
            normalized_item = {
                'id': item.get('id', idx + 1),
                'prompt': None,
                'ground_truth': None,
                'metadata': {}
            }
            
            # Find text field
            for field in text_fields:
                if field in item and item[field]:
                    normalized_item['prompt'] = str(item[field]).strip()
                    break
            
            # Find label field
            for field in label_fields:
                if field in item and item[field]:
                    normalized_item['ground_truth'] = str(item[field]).strip()
                    break
            
            # Store other fields as metadata
            for key, value in item.items():
                if key not in text_fields + label_fields + ['id']:
                    normalized_item['metadata'][key] = value
            
            if normalized_item['prompt']:
                normalized.append(normalized_item)
        
        print(f"✅ Normalized {len(normalized)} records")
        return normalized
    
    def categorize_by_domain(self, data: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize data by domain based on content."""
        domains = {
            'geography': [],
            'science': [],
            'history': [],
            'technology': [],
            'medicine': [],
            'astronomy': [],
            'general': []
        }
        
        # Domain keywords
        domain_keywords = {
            'geography': ['capital', 'country', 'city', 'continent', 'ocean', 'river', 'mountain'],
            'science': ['chemical', 'element', 'atom', 'molecule', 'physics', 'chemistry', 'biology'],
            'history': ['war', 'century', 'born', 'died', 'emperor', 'president', 'revolution'],
            'technology': ['computer', 'software', 'programming', 'internet', 'algorithm', 'code'],
            'medicine': ['disease', 'treatment', 'medical', 'health', 'patient', 'doctor', 'hospital'],
            'astronomy': ['planet', 'star', 'galaxy', 'solar', 'space', 'universe', 'orbit']
        }
        
        for item in data:
            text_lower = item['prompt'].lower()
            categorized = False
            
            for domain, keywords in domain_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    domains[domain].append(item)
                    categorized = True
                    break
            
            if not categorized:
                domains['general'].append(item)
        
        # Print distribution
        print("\n📊 Domain Distribution:")
        for domain, items in domains.items():
            if items:
                print(f"   {domain.capitalize()}: {len(items)} items")
        
        return domains
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\']', '', text)
        return text.strip()
    
    def validate_data(self, data: List[Dict]) -> List[Dict]:
        """Validate and filter data."""
        valid_data = []
        
        for item in data:
            # Check if prompt exists and is not empty
            if not item.get('prompt'):
                continue
            
            # Clean the prompt
            item['prompt'] = self.clean_text(item['prompt'])
            
            # Skip very short or very long prompts
            if len(item['prompt']) < 10 or len(item['prompt']) > 500:
                continue
            
            # Clean ground truth if exists
            if item.get('ground_truth'):
                item['ground_truth'] = self.clean_text(item['ground_truth'])
            
            valid_data.append(item)
        
        print(f"✅ Validated {len(valid_data)} records (filtered {len(data) - len(valid_data)})")
        return valid_data
    
    def save_preprocessed(self, data: List[Dict], output_name: str = "preprocessed_dataset.json"):
        """Save preprocessed data."""
        output_path = self.output_dir / output_name
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved preprocessed data to: {output_path}")
        return str(output_path)
    
    def save_by_domain(self, domains: Dict[str, List[Dict]]):
        """Save data split by domain."""
        for domain, items in domains.items():
            if items:
                output_name = f"preprocessed_{domain}.json"
                self.save_preprocessed(items, output_name)
    
    def generate_statistics(self, data: List[Dict]) -> Dict:
        """Generate dataset statistics."""
        stats = {
            'total_records': len(data),
            'with_ground_truth': sum(1 for item in data if item.get('ground_truth')),
            'avg_prompt_length': sum(len(item['prompt']) for item in data) / len(data) if data else 0,
            'unique_prompts': len(set(item['prompt'] for item in data))
        }
        
        print("\n📈 Dataset Statistics:")
        print(f"   Total Records: {stats['total_records']}")
        print(f"   With Ground Truth: {stats['with_ground_truth']}")
        print(f"   Average Prompt Length: {stats['avg_prompt_length']:.1f} characters")
        print(f"   Unique Prompts: {stats['unique_prompts']}")
        
        return stats
    
    def preprocess(self, file_path: str, categorize: bool = True) -> str:
        """Complete preprocessing pipeline."""
        print("🚀 Starting Dataset Preprocessing Pipeline")
        print("=" * 60)
        
        # Load dataset
        raw_data = self.load_dataset(file_path)
        
        # Normalize fields
        normalized_data = self.normalize_fields(raw_data)
        
        # Validate and clean
        valid_data = self.validate_data(normalized_data)
        
        if not valid_data:
            raise ValueError("No valid data after preprocessing!")
        
        # Generate statistics
        self.generate_statistics(valid_data)
        
        # Save preprocessed data
        output_path = self.save_preprocessed(valid_data)
        
        # Categorize by domain if requested
        if categorize:
            print("\n🏷️ Categorizing by domain...")
            domains = self.categorize_by_domain(valid_data)
            self.save_by_domain(domains)
        
        print("\n" + "=" * 60)
        print("✅ Preprocessing Complete!")
        print(f"📂 Output directory: {self.output_dir}")
        
        return output_path


def main():
    """Example usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python preprocess_external_dataset.py <dataset_file>")
        print("\nSupported formats: .json, .jsonl, .csv, .tsv, .txt")
        print("\nExample:")
        print("  python preprocess_external_dataset.py data/my_dataset.json")
        return
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return
    
    try:
        preprocessor = DatasetPreprocessor()
        output_path = preprocessor.preprocess(file_path, categorize=True)
        
        print(f"\n✅ Ready for testing! Use:")
        print(f"   python src/test_external_dataset.py {output_path}")
        
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
