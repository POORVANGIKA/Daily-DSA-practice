"""
Model training module for generative AI customer support automation.
"""
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    GPT2LMHeadModel, GPT2Tokenizer, GPT2Config,
    Trainer, TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import Dataset as HFDataset
import json
import os
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

class CustomerSupportDataset(Dataset):
    """Custom dataset for customer support queries and responses."""
    
    def __init__(self, queries, responses, tokenizer, max_length=512):
        self.queries = queries
        self.responses = responses
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.queries)
    
    def __getitem__(self, idx):
        query = str(self.queries[idx])
        response = str(self.responses[idx])
        
        # Format as: "Query: {query} Response: {response}"
        text = f"Query: {query} Response: {response}"
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': encoding['input_ids'].flatten()
        }

class CustomerSupportModel:
    """Generative AI model for customer support automation."""
    
    def __init__(self, model_name='gpt2', max_length=512):
        self.model_name = model_name
        self.max_length = max_length
        self.tokenizer = None
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
    
    def load_tokenizer(self):
        """Load tokenizer."""
        print(f"Loading tokenizer: {self.model_name}")
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = 'left'
        return self.tokenizer
    
    def load_model(self):
        """Load or initialize model."""
        print(f"Loading model: {self.model_name}")
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.to(self.device)
        return self.model
    
    def prepare_data(self, df, train_split=0.8):
        """Prepare training and validation datasets."""
        print("Preparing datasets...")
        
        # Split data
        n_train = int(len(df) * train_split)
        train_df = df.iloc[:n_train]
        val_df = df.iloc[n_train:]
        
        print(f"Training samples: {len(train_df)}")
        print(f"Validation samples: {len(val_df)}")
        
        # Create datasets
        train_dataset = CustomerSupportDataset(
            train_df['query'].tolist(),
            train_df['response'].tolist(),
            self.tokenizer,
            self.max_length
        )
        
        val_dataset = CustomerSupportDataset(
            val_df['query'].tolist(),
            val_df['response'].tolist(),
            self.tokenizer,
            self.max_length
        )
        
        return train_dataset, val_dataset
    
    def train(self, train_dataset, val_dataset, output_dir='models/customer_support_gpt2',
              num_epochs=3, batch_size=4, learning_rate=5e-5):
        """Train the model."""
        print("\nStarting training...")
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir=f'{output_dir}/logs',
            logging_steps=50,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            learning_rate=learning_rate,
            fp16=torch.cuda.is_available(),
            report_to="none"
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator
        )
        
        # Train
        trainer.train()
        
        # Save model
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        print(f"\nModel saved to {output_dir}")
        
        return trainer
    
    def generate_response(self, query, max_length=200, temperature=0.7, top_p=0.9, top_k=50):
        """Generate a response to a customer query."""
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer must be loaded first.")
        
        # Format input
        prompt = f"Query: {query} Response:"
        
        # Tokenize
        inputs = self.tokenizer.encode(prompt, return_tensors='pt').to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + max_length,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )
        
        # Decode
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract response
        if "Response:" in generated_text:
            response = generated_text.split("Response:")[-1].strip()
        else:
            response = generated_text[len(prompt):].strip()
        
        return response
    
    def batch_generate(self, queries, **kwargs):
        """Generate responses for multiple queries."""
        responses = []
        for query in tqdm(queries, desc="Generating responses"):
            response = self.generate_response(query, **kwargs)
            responses.append(response)
        return responses

def train_model(data_path='data/processed/preprocessed_dataset.csv',
                model_output_dir='models/customer_support_gpt2',
                num_epochs=3):
    """Main training function."""
    print("="*70)
    print("CUSTOMER SUPPORT AI MODEL TRAINING")
    print("="*70)
    
    # Load data
    print("\n1. Loading data...")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run data_preprocessing.py first.")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records")
    
    # Initialize model
    print("\n2. Initializing model...")
    model = CustomerSupportModel(model_name='gpt2', max_length=512)
    model.load_tokenizer()
    model.load_model()
    
    # Prepare data
    print("\n3. Preparing datasets...")
    train_dataset, val_dataset = model.prepare_data(df, train_split=0.8)
    
    # Train
    print("\n4. Training model...")
    trainer = model.train(
        train_dataset,
        val_dataset,
        output_dir=model_output_dir,
        num_epochs=num_epochs,
        batch_size=4,
        learning_rate=5e-5
    )
    
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)
    
    return model, trainer

if __name__ == "__main__":
    # Train the model
    model, trainer = train_model(num_epochs=3)
    
    if model:
        # Test generation
        print("\n" + "="*70)
        print("TESTING MODEL GENERATION")
        print("="*70)
        
        test_queries = [
            "I can't log into my account. What should I do?",
            "I was charged twice for my subscription.",
            "What features are included in the premium plan?"
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            response = model.generate_response(query)
            print(f"Response: {response}")

