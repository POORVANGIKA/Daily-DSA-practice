"""
Example usage script demonstrating how to use the trained model.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.model_training import CustomerSupportModel
from src.personalization import ResponsePersonalizer

def example_basic_generation():
    """Example: Basic response generation."""
    print("="*70)
    print("EXAMPLE 1: Basic Response Generation")
    print("="*70)
    
    # Load model
    model = CustomerSupportModel(model_name='gpt2')
    model.load_tokenizer()
    
    # Try to load trained model, fallback to base model
    try:
        model.model = CustomerSupportModel(model_name='models/customer_support_gpt2').load_model()
        print("Loaded trained model")
    except:
        print("Trained model not found. Using base GPT-2 model.")
        model.load_model()
    
    # Example queries
    queries = [
        "I can't log into my account. What should I do?",
        "I was charged twice for my subscription.",
        "What features are included in the premium plan?"
    ]
    
    print("\nGenerating responses...\n")
    for query in queries:
        print(f"Query: {query}")
        response = model.generate_response(query, max_length=150)
        print(f"Response: {response}\n")

def example_personalized_generation():
    """Example: Personalized response generation."""
    print("="*70)
    print("EXAMPLE 2: Personalized Response Generation")
    print("="*70)
    
    # Initialize personalizer
    personalizer = ResponsePersonalizer()
    
    # Example scenario
    base_response = "I can help you with that. Let me check your account and resolve this issue for you."
    
    scenarios = [
        {
            "customer_id": "CUST_10000",
            "tier": "Premium",
            "category": "billing",
            "sentiment": "negative",
            "description": "Premium customer with billing issue (negative sentiment)"
        },
        {
            "customer_id": "CUST_10001",
            "tier": "Basic",
            "category": "technical",
            "sentiment": "neutral",
            "description": "Basic customer with technical question (neutral sentiment)"
        }
    ]
    
    print("\nPersonalizing responses...\n")
    for scenario in scenarios:
        print(f"Scenario: {scenario['description']}")
        print(f"Customer ID: {scenario['customer_id']}")
        print(f"Tier: {scenario['tier']}")
        print(f"\nBase Response:\n{base_response}")
        
        personalized = personalizer.personalize_response(
            base_response,
            scenario['customer_id'],
            scenario['category'],
            scenario['tier'],
            scenario['sentiment']
        )
        
        print(f"\nPersonalized Response:\n{personalized}")
        print("\n" + "-"*70 + "\n")

def example_batch_processing():
    """Example: Batch processing with personalization."""
    print("="*70)
    print("EXAMPLE 3: Batch Processing")
    print("="*70)
    
    personalizer = ResponsePersonalizer()
    
    # Batch of base responses
    base_responses = [
        "I'll investigate this issue and get back to you.",
        "Thank you for contacting us. I can assist you with this.",
        "I can help you resolve this problem."
    ]
    
    customer_ids = ["CUST_10000", "CUST_10001", "CUST_10002"]
    tiers = ["Premium", "Basic", "Enterprise"]
    categories = ["billing", "technical", "product"]
    sentiments = ["negative", "neutral", "positive"]
    
    print("\nProcessing batch...\n")
    personalized_responses = personalizer.personalize_batch(
        base_responses,
        customer_ids,
        query_categories=categories,
        customer_tiers=tiers,
        sentiments=sentiments
    )
    
    for i, (base, personalized) in enumerate(zip(base_responses, personalized_responses)):
        print(f"Example {i+1}:")
        print(f"  Customer: {customer_ids[i]} ({tiers[i]})")
        print(f"  Base: {base}")
        print(f"  Personalized: {personalized}\n")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CUSTOMER SUPPORT AI - USAGE EXAMPLES")
    print("="*70)
    
    # Note: These examples assume the model has been trained
    # For basic generation, you can still use the base GPT-2 model
    
    try:
        example_basic_generation()
        print("\n")
        example_personalized_generation()
        print("\n")
        example_batch_processing()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: Make sure you have:")
        print("  1. Generated the data (python src/data_generation.py)")
        print("  2. Trained the model (python src/model_training.py)")
        print("  3. Or use the base GPT-2 model for basic examples")

