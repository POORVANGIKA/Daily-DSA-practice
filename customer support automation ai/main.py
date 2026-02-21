"""
Main execution script for Customer Support Automation AI.
"""
import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def run_data_generation():
    """Generate synthetic customer support data."""
    print("\n" + "="*70)
    print("STEP 1: DATA GENERATION")
    print("="*70)
    from src.data_generation import generate_customer_support_dataset, generate_customer_profiles
    
    generate_customer_support_dataset(n_samples=5000)
    generate_customer_profiles()
    print("\n✓ Data generation complete!")

def run_preprocessing():
    """Preprocess and analyze data."""
    print("\n" + "="*70)
    print("STEP 2: DATA PREPROCESSING AND ANALYSIS")
    print("="*70)
    from src.data_preprocessing import DataPreprocessor
    
    preprocessor = DataPreprocessor()
    if preprocessor.load_data():
        preprocessor.preprocess()
        preprocessor.analyze_data()
        preprocessor.create_visualizations()
        preprocessor.generate_insights_report()
        print("\n✓ Data preprocessing and analysis complete!")
    else:
        print("Error: Could not load data. Please run data generation first.")

def run_training():
    """Train the generative AI model."""
    print("\n" + "="*70)
    print("STEP 3: MODEL TRAINING")
    print("="*70)
    from src.model_training import train_model
    
    model, trainer = train_model(num_epochs=3)
    if model:
        print("\n✓ Model training complete!")
    else:
        print("Error: Model training failed.")

def run_evaluation():
    """Evaluate the trained model."""
    print("\n" + "="*70)
    print("STEP 4: MODEL EVALUATION")
    print("="*70)
    from src.evaluation import ModelEvaluator
    
    evaluator = ModelEvaluator()
    results = evaluator.evaluate(sample_size=100)
    if results:
        print("\n✓ Model evaluation complete!")
    else:
        print("Error: Model evaluation failed.")

def run_personalization_demo():
    """Demonstrate personalization capabilities."""
    print("\n" + "="*70)
    print("STEP 5: PERSONALIZATION DEMONSTRATION")
    print("="*70)
    from src.personalization import demonstrate_personalization
    
    demonstrate_personalization()
    print("\n✓ Personalization demonstration complete!")

def run_report_generation():
    """Generate comprehensive report."""
    print("\n" + "="*70)
    print("STEP 6: REPORT GENERATION")
    print("="*70)
    from src.report_generator import generate_comprehensive_report
    
    generate_comprehensive_report()
    print("\n✓ Report generation complete!")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Customer Support Automation AI')
    parser.add_argument('--step', type=str, choices=['all', 'data', 'preprocess', 'train', 'evaluate', 'personalize', 'report'],
                       default='all', help='Which step to run')
    parser.add_argument('--skip-data', action='store_true', help='Skip data generation if data exists')
    
    args = parser.parse_args()
    
    print("="*70)
    print("CUSTOMER SUPPORT AUTOMATION AI - MAIN PIPELINE")
    print("="*70)
    
    if args.step == 'all':
        # Check if data exists
        if not args.skip_data and not os.path.exists('data/raw/customer_support_dataset.csv'):
            run_data_generation()
        elif args.skip_data:
            print("\nSkipping data generation (--skip-data flag set)")
        else:
            print("\nData already exists. Skipping data generation.")
        
        run_preprocessing()
        run_training()
        run_evaluation()
        run_personalization_demo()
        run_report_generation()
        
        print("\n" + "="*70)
        print("ALL STEPS COMPLETE!")
        print("="*70)
        print("\nDeliverables:")
        print("  ✓ Preprocessed and analyzed datasets with visualizations")
        print("  ✓ Trained generative AI model")
        print("  ✓ Personalization module")
        print("  ✓ Model evaluation results")
        print("  ✓ Comprehensive report")
        print("\nCheck the 'reports' directory for all outputs.")
    
    elif args.step == 'data':
        run_data_generation()
    elif args.step == 'preprocess':
        run_preprocessing()
    elif args.step == 'train':
        run_training()
    elif args.step == 'evaluate':
        run_evaluation()
    elif args.step == 'personalize':
        run_personalization_demo()
    elif args.step == 'report':
        run_report_generation()

if __name__ == "__main__":
    main()

