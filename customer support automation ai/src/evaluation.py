"""
Model evaluation module with comprehensive metrics.
"""
import pandas as pd
import numpy as np
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from rouge_score import rouge_scorer
from bert_score import score as bert_score
import json
import os
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

class ModelEvaluator:
    """Comprehensive evaluation of the customer support AI model."""
    
    def __init__(self, model_path='models/customer_support_gpt2'):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    def load_model(self):
        """Load trained model and tokenizer."""
        if not os.path.exists(self.model_path):
            print(f"Warning: Model not found at {self.model_path}")
            return False
        
        print(f"Loading model from {self.model_path}")
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_path)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_path)
        self.model.to(self.device)
        self.model.eval()
        return True
    
    def generate_response(self, query, max_length=200, temperature=0.7):
        """Generate response for evaluation."""
        prompt = f"Query: {query} Response:"
        inputs = self.tokenizer.encode(prompt, return_tensors='pt').to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + max_length,
                temperature=temperature,
                top_p=0.9,
                top_k=50,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "Response:" in generated_text:
            response = generated_text.split("Response:")[-1].strip()
        else:
            response = generated_text[len(prompt):].strip()
        
        return response
    
    def calculate_rouge_scores(self, generated_responses, reference_responses):
        """Calculate ROUGE scores."""
        print("Calculating ROUGE scores...")
        rouge_scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}
        
        for gen, ref in tqdm(zip(generated_responses, reference_responses), 
                           total=len(generated_responses), desc="ROUGE"):
            scores = self.rouge_scorer.score(ref, gen)
            rouge_scores['rouge1'].append(scores['rouge1'].fmeasure)
            rouge_scores['rouge2'].append(scores['rouge2'].fmeasure)
            rouge_scores['rougeL'].append(scores['rougeL'].fmeasure)
        
        return {
            'rouge1': {
                'mean': np.mean(rouge_scores['rouge1']),
                'std': np.std(rouge_scores['rouge1']),
                'scores': rouge_scores['rouge1']
            },
            'rouge2': {
                'mean': np.mean(rouge_scores['rouge2']),
                'std': np.std(rouge_scores['rouge2']),
                'scores': rouge_scores['rouge2']
            },
            'rougeL': {
                'mean': np.mean(rouge_scores['rougeL']),
                'std': np.std(rouge_scores['rougeL']),
                'scores': rouge_scores['rougeL']
            }
        }
    
    def calculate_bert_score(self, generated_responses, reference_responses):
        """Calculate BERTScore."""
        print("Calculating BERTScore...")
        try:
            P, R, F1 = bert_score(
                generated_responses,
                reference_responses,
                lang='en',
                verbose=True,
                device=self.device
            )
            return {
                'precision': {
                    'mean': P.mean().item(),
                    'std': P.std().item(),
                    'scores': P.tolist()
                },
                'recall': {
                    'mean': R.mean().item(),
                    'std': R.std().item(),
                    'scores': R.tolist()
                },
                'f1': {
                    'mean': F1.mean().item(),
                    'std': F1.std().item(),
                    'scores': F1.tolist()
                }
            }
        except Exception as e:
            print(f"Error calculating BERTScore: {e}")
            return None
    
    def calculate_custom_metrics(self, generated_responses, reference_responses):
        """Calculate custom metrics."""
        print("Calculating custom metrics...")
        
        metrics = {}
        
        # Length metrics
        gen_lengths = [len(r.split()) for r in generated_responses]
        ref_lengths = [len(r.split()) for r in reference_responses]
        
        metrics['length'] = {
            'generated_mean': np.mean(gen_lengths),
            'generated_std': np.std(gen_lengths),
            'reference_mean': np.mean(ref_lengths),
            'reference_std': np.std(ref_lengths),
            'length_ratio': np.mean(gen_lengths) / np.mean(ref_lengths) if np.mean(ref_lengths) > 0 else 0
        }
        
        # Word overlap
        overlaps = []
        for gen, ref in zip(generated_responses, reference_responses):
            gen_words = set(gen.lower().split())
            ref_words = set(ref.lower().split())
            if len(ref_words) > 0:
                overlap = len(gen_words & ref_words) / len(ref_words)
                overlaps.append(overlap)
        
        metrics['word_overlap'] = {
            'mean': np.mean(overlaps),
            'std': np.std(overlaps)
        }
        
        # Response quality indicators
        quality_keywords = ['help', 'assist', 'resolve', 'apologize', 'thank', 'understand']
        quality_scores = []
        for response in generated_responses:
            score = sum(1 for keyword in quality_keywords if keyword in response.lower())
            quality_scores.append(score)
        
        metrics['quality_keywords'] = {
            'mean': np.mean(quality_scores),
            'std': np.std(quality_scores)
        }
        
        return metrics
    
    def evaluate(self, test_data_path='data/processed/preprocessed_dataset.csv', 
                 sample_size=100):
        """Comprehensive model evaluation."""
        print("="*70)
        print("MODEL EVALUATION")
        print("="*70)
        
        if not self.load_model():
            print("Cannot evaluate: Model not found.")
            return None
        
        # Load test data
        print(f"\nLoading test data from {test_data_path}...")
        if not os.path.exists(test_data_path):
            print(f"Error: {test_data_path} not found.")
            return None
        
        df = pd.read_csv(test_data_path)
        
        # Sample test data
        if len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42)
        
        print(f"Evaluating on {len(df)} samples...")
        
        # Generate responses
        print("\nGenerating responses...")
        generated_responses = []
        for query in tqdm(df['query'].tolist(), desc="Generating"):
            response = self.generate_response(query)
            generated_responses.append(response)
        
        reference_responses = df['response'].tolist()
        
        # Calculate metrics
        print("\n" + "="*70)
        print("CALCULATING METRICS")
        print("="*70)
        
        results = {}
        
        # ROUGE scores
        results['rouge'] = self.calculate_rouge_scores(generated_responses, reference_responses)
        
        # BERTScore
        bert_results = self.calculate_bert_score(generated_responses, reference_responses)
        if bert_results:
            results['bertscore'] = bert_results
        
        # Custom metrics
        results['custom'] = self.calculate_custom_metrics(generated_responses, reference_responses)
        
        # Save results
        self.save_results(results, generated_responses, reference_responses, df)
        
        # Print summary
        self.print_summary(results)
        
        return results
    
    def save_results(self, results, generated_responses, reference_responses, df):
        """Save evaluation results."""
        os.makedirs('reports', exist_ok=True)
        
        # Save metrics
        with open('reports/evaluation_metrics.json', 'w') as f:
            # Convert numpy types to native Python types for JSON serialization
            def convert_to_serializable(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {key: convert_to_serializable(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_to_serializable(item) for item in obj]
                return obj
            
            json.dump(convert_to_serializable(results), f, indent=2)
        
        # Save sample predictions
        sample_df = pd.DataFrame({
            'query': df['query'].tolist()[:20],
            'generated_response': generated_responses[:20],
            'reference_response': reference_responses[:20]
        })
        sample_df.to_csv('reports/sample_predictions.csv', index=False)
        
        print(f"\nResults saved to:")
        print(f"  - reports/evaluation_metrics.json")
        print(f"  - reports/sample_predictions.csv")
    
    def print_summary(self, results):
        """Print evaluation summary."""
        print("\n" + "="*70)
        print("EVALUATION SUMMARY")
        print("="*70)
        
        # ROUGE scores
        print("\nROUGE Scores:")
        rouge = results['rouge']
        print(f"  ROUGE-1: {rouge['rouge1']['mean']:.4f} (±{rouge['rouge1']['std']:.4f})")
        print(f"  ROUGE-2: {rouge['rouge2']['mean']:.4f} (±{rouge['rouge2']['std']:.4f})")
        print(f"  ROUGE-L: {rouge['rougeL']['mean']:.4f} (±{rouge['rougeL']['std']:.4f})")
        
        # BERTScore
        if 'bertscore' in results:
            print("\nBERTScore:")
            bs = results['bertscore']
            print(f"  Precision: {bs['precision']['mean']:.4f} (±{bs['precision']['std']:.4f})")
            print(f"  Recall: {bs['recall']['mean']:.4f} (±{bs['recall']['std']:.4f})")
            print(f"  F1: {bs['f1']['mean']:.4f} (±{bs['f1']['std']:.4f})")
        
        # Custom metrics
        print("\nCustom Metrics:")
        custom = results['custom']
        print(f"  Average Generated Length: {custom['length']['generated_mean']:.1f} words")
        print(f"  Average Reference Length: {custom['length']['reference_mean']:.1f} words")
        print(f"  Length Ratio: {custom['length']['length_ratio']:.2f}")
        print(f"  Word Overlap: {custom['word_overlap']['mean']:.4f} (±{custom['word_overlap']['std']:.4f})")
        print(f"  Quality Keywords: {custom['quality_keywords']['mean']:.2f} (±{custom['quality_keywords']['std']:.2f})")
        
        print("\n" + "="*70)

if __name__ == "__main__":
    evaluator = ModelEvaluator()
    results = evaluator.evaluate(sample_size=100)

