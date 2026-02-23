"""
Generate synthetic customer support dataset for training and evaluation.
"""
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random

def generate_customer_support_dataset(n_samples=5000, output_path='data/raw/customer_support_dataset.csv'):
    """
    Generate a synthetic customer support dataset with customer queries and responses.
    """
    np.random.seed(42)
    random.seed(42)
    
    # Customer support scenarios
    scenarios = {
        'billing': {
            'queries': [
                "I was charged twice for my subscription. Can you help?",
                "Why is my bill higher than expected?",
                "I need to update my payment method.",
                "Can you explain the charges on my invoice?",
                "I want to cancel my subscription and get a refund.",
                "My payment failed. What should I do?",
                "I didn't receive my invoice this month.",
                "Can I change my billing cycle?"
            ],
            'responses': [
                "I apologize for the inconvenience. I'll investigate the duplicate charge and process a refund within 3-5 business days.",
                "Let me review your account. The increase is due to [specific reason]. I can help you understand each charge.",
                "I can help you update your payment method. Please provide your new card details securely.",
                "I'd be happy to explain your invoice. The charges include [breakdown]. Would you like more details?",
                "I understand. I can process your cancellation and refund request. Your refund will be processed within 7-10 business days.",
                "Let's resolve this. Please verify your card details and ensure sufficient funds. I can also help set up an alternative payment method.",
                "I'll resend your invoice immediately. Please check your email, including spam folder.",
                "Yes, absolutely! I can help you change your billing cycle. What frequency would you prefer?"
            ]
        },
        'technical': {
            'queries': [
                "I can't log into my account. What should I do?",
                "The app keeps crashing on my phone.",
                "I forgot my password. How do I reset it?",
                "I'm experiencing slow loading times.",
                "How do I enable two-factor authentication?",
                "My data seems to be missing. Can you help?",
                "I need help setting up the integration.",
                "The feature I need isn't working as expected."
            ],
            'responses': [
                "I can help you regain access. Let's verify your account details and reset your password if needed.",
                "I'm sorry for the trouble. Let's troubleshoot this. What device and OS version are you using?",
                "No problem! I'll send you a password reset link to your registered email address.",
                "Let me investigate the performance issue. This could be due to [reason]. I'll check your account settings.",
                "I'll guide you through setting up 2FA. It's a great security feature. Let's start with the authentication app setup.",
                "I'll investigate immediately. Can you tell me when you last saw the data? I'll check our backup systems.",
                "I'd be happy to help you set up the integration. Let's start by connecting your account.",
                "I understand your concern. Let me check the feature status and help you get it working properly."
            ]
        },
        'product': {
            'queries': [
                "What features are included in the premium plan?",
                "How do I upgrade my account?",
                "Can I get a demo of the new feature?",
                "What's the difference between Basic and Pro plans?",
                "I want to add more users to my team.",
                "Is there a mobile app available?",
                "Can I export my data?",
                "How do I customize my dashboard?"
            ],
            'responses': [
                "The premium plan includes [features]. Would you like a detailed comparison with your current plan?",
                "I can help you upgrade! The process is quick and your new features will be available immediately.",
                "Absolutely! I can schedule a personalized demo for you. When would be a good time?",
                "The main differences are [comparison]. I can help you choose the best plan for your needs.",
                "Great! I can help you add team members. How many users would you like to add?",
                "Yes! We have mobile apps for both iOS and Android. I can send you the download links.",
                "Yes, you can export your data in multiple formats. I'll guide you through the export process.",
                "I'll show you how to customize your dashboard. You can rearrange widgets, change themes, and more."
            ]
        },
        'general': {
            'queries': [
                "Thank you for your help!",
                "How do I contact support?",
                "What are your business hours?",
                "I have a general question about your service.",
                "Can you help me understand your refund policy?",
                "I want to provide feedback about my experience.",
                "How do I unsubscribe from marketing emails?",
                "Where can I find your terms of service?"
            ],
            'responses': [
                "You're very welcome! I'm glad I could help. Is there anything else you need?",
                "You can reach us through this chat, email at support@company.com, or phone at 1-800-SUPPORT.",
                "Our support team is available Monday-Friday, 9 AM - 6 PM EST. We also offer 24/7 emergency support for premium customers.",
                "I'd be happy to answer your question. What would you like to know?",
                "Our refund policy allows returns within 30 days of purchase. I can provide more specific details based on your situation.",
                "Thank you for your feedback! I'd love to hear about your experience. How can we improve?",
                "I can help you update your email preferences. You'll be unsubscribed immediately.",
                "You can find our terms of service at [link]. I can also answer any specific questions about them."
            ]
        }
    }
    
    # Customer profiles
    customer_tiers = ['Basic', 'Pro', 'Premium', 'Enterprise']
    customer_segments = ['New', 'Active', 'At-Risk', 'Churned']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Other']
    
    data = []
    
    for i in range(n_samples):
        # Select random scenario
        category = random.choice(list(scenarios.keys()))
        scenario = scenarios[category]
        
        # Select query and response
        idx = random.randint(0, len(scenario['queries']) - 1)
        query = scenario['queries'][idx]
        response = scenario['responses'][idx]
        
        # Generate customer profile
        customer_id = f"CUST_{10000 + i}"
        tier = random.choice(customer_tiers)
        segment = random.choice(customer_segments)
        region = random.choice(regions)
        
        # Generate timestamps
        days_ago = random.randint(0, 365)
        timestamp = datetime.now() - timedelta(days=days_ago)
        
        # Generate sentiment (for analysis)
        sentiment = random.choice(['positive', 'neutral', 'negative'])
        
        # Generate priority
        priority = random.choice(['Low', 'Medium', 'High', 'Urgent'])
        
        # Generate customer lifetime value (for personalization)
        clv = np.random.normal(500, 200) if tier in ['Premium', 'Enterprise'] else np.random.normal(200, 100)
        clv = max(0, clv)  # Ensure non-negative
        
        # Generate interaction history count
        interaction_count = random.randint(1, 50)
        
        data.append({
            'customer_id': customer_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'query': query,
            'response': response,
            'customer_tier': tier,
            'customer_segment': segment,
            'region': region,
            'sentiment': sentiment,
            'priority': priority,
            'customer_lifetime_value': round(clv, 2),
            'interaction_count': interaction_count,
            'satisfaction_score': random.randint(1, 5) if random.random() > 0.3 else None
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Generated {n_samples} customer support records and saved to {output_path}")
    return df

def generate_customer_profiles(output_path='data/raw/customer_profiles.json'):
    """
    Generate customer profile data for personalization.
    """
    np.random.seed(42)
    random.seed(42)
    
    profiles = {}
    customer_tiers = ['Basic', 'Pro', 'Premium', 'Enterprise']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Other']
    
    for i in range(1000):
        customer_id = f"CUST_{10000 + i}"
        tier = random.choice(customer_tiers)
        
        profiles[customer_id] = {
            'customer_id': customer_id,
            'tier': tier,
            'region': random.choice(regions),
            'preferred_language': random.choice(['English', 'Spanish', 'French', 'German', 'Chinese']),
            'preferred_communication_style': random.choice(['formal', 'casual', 'friendly', 'professional']),
            'customer_since': (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime('%Y-%m-%d'),
            'total_spent': round(np.random.normal(500 if tier == 'Basic' else 1500 if tier == 'Pro' else 3000, 500), 2),
            'average_response_time_preference': random.choice(['immediate', 'within_hour', 'within_day']),
            'preferred_channels': random.sample(['email', 'chat', 'phone', 'ticket'], k=random.randint(1, 3)),
            'interests': random.sample(['product_updates', 'tutorials', 'best_practices', 'case_studies'], 
                                     k=random.randint(1, 3))
        }
    
    with open(output_path, 'w') as f:
        json.dump(profiles, f, indent=2)
    
    print(f"Generated {len(profiles)} customer profiles and saved to {output_path}")
    return profiles

if __name__ == "__main__":
    print("Generating customer support dataset...")
    df = generate_customer_support_dataset(n_samples=5000)
    
    print("\nGenerating customer profiles...")
    profiles = generate_customer_profiles()
    
    print("\nData generation complete!")

