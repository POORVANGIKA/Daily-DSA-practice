# Customer Support Automation AI

An intelligent customer support automation system powered by generative AI that can generate automated responses and personalize messages based on customer data.

## Project Overview

This project implements a complete pipeline for customer support automation, including:

- **Data Generation & Preprocessing**: Synthetic dataset creation and comprehensive data analysis
- **Generative AI Model**: Fine-tuned GPT-2 model for automated response generation
- **Personalization Engine**: Tailors responses based on customer profiles, tier, sentiment, and preferences
- **Comprehensive Evaluation**: Multiple metrics including ROUGE, BERTScore, and custom metrics
- **Visualizations & Insights**: Data analysis with interactive dashboards
- **Documentation**: Complete reports and presentation materials

## Project Structure

```
customer support automation ai/
├── data/
│   ├── raw/              # Raw datasets
│   ├── processed/        # Preprocessed datasets
│   └── generated/        # Generated/simulated data
├── src/
│   ├── data_generation.py       # Generate synthetic customer support data
│   ├── data_preprocessing.py    # Data preprocessing and analysis
│   ├── model_training.py        # Model training pipeline
│   ├── personalization.py       # Personalization module
│   ├── evaluation.py            # Model evaluation
│   └── report_generator.py      # Report generation
├── models/               # Trained model checkpoints
├── notebooks/            # Jupyter notebooks for analysis
├── reports/              # Generated reports and presentations
│   └── visualizations/   # Data visualization outputs
├── requirements.txt      # Python dependencies
└── main.py              # Main execution script
```

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data (if needed):**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage

### Quick Start (Run All Steps)

Run the complete pipeline:
```bash
python main.py
```

This will execute all steps:
1. Data generation
2. Data preprocessing and analysis
3. Model training
4. Model evaluation
5. Personalization demonstration
6. Report generation

### Run Individual Steps

You can also run individual steps:

```bash
# Generate data only
python main.py --step data

# Preprocess and analyze data
python main.py --step preprocess

# Train the model
python main.py --step train

# Evaluate the model
python main.py --step evaluate

# Demonstrate personalization
python main.py --step personalize

# Generate reports
python main.py --step report
```

### Skip Data Generation

If data already exists:
```bash
python main.py --skip-data
```

## Deliverables

### ✅ 1. Preprocessed and Analyzed Datasets

- **Location**: `data/processed/preprocessed_dataset.csv`
- **Features**: 
  - Temporal features (hour, day, date)
  - Text statistics (length, word count)
  - Encoded categorical variables
  - Customer metrics (CLV, interaction count)

### ✅ 2. Visualizations

All visualizations are saved in `reports/visualizations/`:

- `01_basic_distributions.png` - Category, tier, priority, sentiment distributions
- `02_temporal_analysis.png` - Time series, hourly patterns, day-of-week analysis
- `03_customer_analysis.png` - CLV, interactions, satisfaction by tier
- `04_text_analysis.png` - Query/response length distributions
- `05_interactive_dashboard.html` - Interactive Plotly dashboard

### ✅ 3. Trained Generative AI Model

- **Location**: `models/customer_support_gpt2/`
- **Capabilities**:
  - Generate automated responses to customer queries
  - Context-aware response generation
  - Support for multiple query categories

### ✅ 4. Personalization Module

- **Location**: `src/personalization.py`
- **Features**:
  - Tier-based personalization (Basic, Pro, Premium, Enterprise)
  - Communication style adaptation
  - Sentiment-aware responses
  - Category-specific tailoring

### ✅ 5. Model Evaluation

- **Location**: `reports/evaluation_metrics.json`
- **Metrics**:
  - ROUGE-1, ROUGE-2, ROUGE-L scores
  - BERTScore (Precision, Recall, F1)
  - Custom metrics (length, word overlap, quality keywords)
- **Sample Predictions**: `reports/sample_predictions.csv`

### ✅ 6. Comprehensive Report

- **Location**: `reports/comprehensive_report.md`
- **Contents**:
  - Executive summary
  - Methodology
  - Results and findings
  - Deliverables checklist
  - Future improvements

- **Presentation Summary**: `reports/presentation_summary.md`

## Key Features

### Data Analysis
- Comprehensive exploratory data analysis
- Temporal pattern identification
- Customer segmentation analysis
- Text characteristic analysis

### Model Training
- Fine-tuned GPT-2 model
- Custom dataset class
- Training with validation
- Model checkpointing

### Personalization
- Customer profile integration
- Multi-factor personalization
- Dynamic response adaptation
- Batch personalization support

### Evaluation
- Multiple evaluation metrics
- Statistical analysis
- Sample prediction comparison
- Performance benchmarking

## Technical Details

### Model Architecture
- **Base Model**: GPT-2 (124M parameters)
- **Input Format**: `Query: {query} Response: {response}`
- **Max Length**: 512 tokens
- **Training**: Fine-tuning on customer support dataset

### Training Configuration
- **Epochs**: 3
- **Batch Size**: 4
- **Learning Rate**: 5e-5
- **Optimizer**: AdamW
- **Train/Val Split**: 80/20

### Personalization Factors
- Customer tier
- Communication style preference
- Sentiment (positive/neutral/negative)
- Query category
- Customer lifetime value
- Interaction history

## Results Summary

The model demonstrates:
- Successful learning of customer support patterns
- Context-aware response generation
- Effective personalization capabilities
- Good performance on evaluation metrics

## Future Enhancements

1. **Model Improvements**
   - Larger model architectures
   - Few-shot learning
   - Domain-specific fine-tuning

2. **Personalization**
   - Real-time behavior integration
   - Multi-language support
   - A/B testing framework

3. **Deployment**
   - API development
   - Caching and optimization
   - Monitoring and logging

## Requirements

See `requirements.txt` for complete list. Key dependencies:
- PyTorch
- Transformers (Hugging Face)
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- ROUGE-score, BERTScore
- NLTK

## Notes

- The project uses synthetic data for demonstration purposes
- Model training may take time depending on hardware
- GPU recommended for faster training
- All outputs are saved in the `reports/` directory

## License

This project is for educational and demonstration purposes.

## Contact

For questions or issues, please refer to the code documentation or project reports.

