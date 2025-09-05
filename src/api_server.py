#!/usr/bin/env python3
"""
Production API Server for AKGC Algorithm
RESTful API for hallucination detection and correction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import yaml
import time
import logging
from typing import Dict, List
from akgc_optimized import OptimizedAKGC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global AKGC instance
akgc_instance = None

def initialize_akgc():
    """Initialize the AKGC model."""
    global akgc_instance
    try:
        logger.info("Initializing AKGC model...")
        akgc_instance = OptimizedAKGC()
        logger.info("AKGC model initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize AKGC: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": akgc_instance is not None,
        "device": akgc_instance.device if akgc_instance else "unknown"
    })

@app.route('/detect', methods=['POST'])
def detect_hallucination():
    """Detect hallucination in a single text."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400
        
        if not akgc_instance:
            return jsonify({"error": "Model not initialized"}), 500
        
        text = data['text']
        threshold = data.get('threshold', 0.7)
        
        start_time = time.time()
        response, factual, hvi = akgc_instance.adaptive_correction_optimized(
            text, hvi_threshold=threshold
        )
        processing_time = time.time() - start_time
        
        return jsonify({
            "original_text": text,
            "corrected_text": response,
            "is_factual": factual,
            "hvi": float(hvi),
            "needs_correction": hvi < threshold,
            "processing_time": processing_time
        })
        
    except Exception as e:
        logger.error(f"Error in detect endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/batch_detect', methods=['POST'])
def batch_detect_hallucination():
    """Detect hallucinations in multiple texts."""
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({"error": "Missing 'texts' field"}), 400
        
        if not akgc_instance:
            return jsonify({"error": "Model not initialized"}), 500
        
        texts = data['texts']
        threshold = data.get('threshold', 0.7)
        
        if len(texts) > 100:  # Limit batch size
            return jsonify({"error": "Batch size too large (max 100)"}), 400
        
        start_time = time.time()
        results = akgc_instance.batch_process(texts)
        processing_time = time.time() - start_time
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "original_text": result['prompt'],
                "corrected_text": result['response'],
                "is_factual": result['factual'],
                "hvi": float(result['hvi']),
                "needs_correction": result['hvi'] < threshold
            })
        
        return jsonify({
            "results": formatted_results,
            "total_processed": len(texts),
            "processing_time": processing_time,
            "avg_time_per_text": processing_time / len(texts)
        })
        
    except Exception as e:
        logger.error(f"Error in batch_detect endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate_text():
    """Evaluate text quality and provide detailed metrics."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data or 'ground_truth' not in data:
            return jsonify({"error": "Missing 'text' or 'ground_truth' field"}), 400
        
        if not akgc_instance:
            return jsonify({"error": "Model not initialized"}), 500
        
        text = data['text']
        ground_truth = data['ground_truth']
        threshold = data.get('threshold', 0.7)
        
        start_time = time.time()
        response, factual, hvi = akgc_instance.adaptive_correction_optimized(
            text, hvi_threshold=threshold
        )
        processing_time = time.time() - start_time
        
        # Compute additional metrics
        from utils.metrics import compute_accuracy, compute_rouge_l, compute_bertscore
        
        accuracy = compute_accuracy(response, ground_truth)
        rouge_l = compute_rouge_l(response, ground_truth)
        bertscore = compute_bertscore(response, ground_truth)
        
        return jsonify({
            "original_text": text,
            "corrected_text": response,
            "ground_truth": ground_truth,
            "is_factual": factual,
            "hvi": float(hvi),
            "needs_correction": hvi < threshold,
            "metrics": {
                "accuracy": float(accuracy),
                "rouge_l": float(rouge_l),
                "bertscore": float(bertscore)
            },
            "processing_time": processing_time
        })
        
    except Exception as e:
        logger.error(f"Error in evaluate endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration."""
    if not akgc_instance:
        return jsonify({"error": "Model not initialized"}), 500
    
    return jsonify({
        "device": akgc_instance.device,
        "model_config": akgc_instance.config,
        "kg_cache_size": len(akgc_instance.kg_cache)
    })

@app.route('/config', methods=['POST'])
def update_config():
    """Update configuration parameters."""
    try:
        data = request.get_json()
        
        if not akgc_instance:
            return jsonify({"error": "Model not initialized"}), 500
        
        # Update configurable parameters
        if 'sim_threshold' in data:
            akgc_instance.config['sim_threshold'] = data['sim_threshold']
        if 'hvi_threshold' in data:
            akgc_instance.config['hvi_threshold'] = data['hvi_threshold']
        
        return jsonify({
            "message": "Configuration updated",
            "new_config": akgc_instance.config
        })
        
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

def main():
    """Main function to run the API server."""
    print("Starting AKGC API Server...")
    
    # Initialize model
    if not initialize_akgc():
        print("Failed to initialize AKGC model. Exiting...")
        return
    
    # Run server
    print("API Server ready!")
    print("Available endpoints:")
    print("  GET  /health - Health check")
    print("  POST /detect - Detect hallucination in single text")
    print("  POST /batch_detect - Detect hallucinations in multiple texts")
    print("  POST /evaluate - Evaluate text with ground truth")
    print("  GET  /config - Get current configuration")
    print("  POST /config - Update configuration")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
