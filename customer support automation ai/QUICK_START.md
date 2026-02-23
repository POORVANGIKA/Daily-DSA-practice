# Quick Start Guide

## Step-by-Step Execution

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Complete Pipeline

```bash
python main.py
```

This will:
1. Generate synthetic customer support data (5,000 records)
2. Preprocess and analyze the data
3. Train the generative AI model
4. Evaluate model performance
5. Demonstrate personalization
6. Generate comprehensive reports

### 3. View Results

After execution, check the following:

- **Data**: `data/processed/preprocessed_dataset.csv`
- **Visualizations**: `reports/visualizations/`
- **Model**: `models/customer_support_gpt2/`
- **Evaluation**: `reports/evaluation_metrics.json`
- **Report**: `reports/comprehensive_report.md`

## Individual Module Usage

### Generate Data Only

```bash
python src/data_generation.py
```

### Preprocess and Analyze

```bash
python src/data_preprocessing.py
```

### Train Model

```bash
python src/model_training.py
```

### Evaluate Model

```bash
python src/evaluation.py
```

### Test Personalization

```bash
python src/personalization.py
```

## Expected Outputs

1. **Data Files**
   - `data/raw/customer_support_dataset.csv` (5,000 records)
   - `data/raw/customer_profiles.json` (1,000 profiles)
   - `data/processed/preprocessed_dataset.csv`

2. **Visualizations** (in `reports/visualizations/`)
   - 4 PNG files with analysis charts
   - 1 HTML interactive dashboard

3. **Model** (in `models/customer_support_gpt2/`)
   - Trained model files
   - Tokenizer files

4. **Reports** (in `reports/`)
   - `comprehensive_report.md`
   - `presentation_summary.md`
   - `evaluation_metrics.json`
   - `data_analysis_insights.txt`
   - `sample_predictions.csv`

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Make sure you're in the project root directory and dependencies are installed.

### Issue: CUDA out of memory
**Solution**: Reduce batch size in `model_training.py` or use CPU (will be slower).

### Issue: Data not found
**Solution**: Run data generation first: `python src/data_generation.py`

### Issue: Model not found during evaluation
**Solution**: Train the model first: `python src/model_training.py`

## Time Estimates

- Data Generation: ~1-2 minutes
- Preprocessing: ~2-3 minutes
- Model Training: ~30-60 minutes (depends on hardware)
- Evaluation: ~5-10 minutes
- Report Generation: ~1 minute

**Total**: ~40-75 minutes for complete pipeline

## Hardware Requirements

- **Minimum**: CPU with 8GB RAM
- **Recommended**: GPU with 16GB+ VRAM for faster training
- **Storage**: ~2GB for models and data

