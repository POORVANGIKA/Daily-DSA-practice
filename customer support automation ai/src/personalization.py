"""
Personalization module for tailoring responses based on customer data.
"""
import pandas as pd
import json
import os
from typing import Dict, Optional

class ResponsePersonalizer:
    """Personalize customer support responses based on customer profile."""
    
    def __init__(self, profiles_path='data/raw/customer_profiles.json'):
        self.profiles_path = profiles_path
        self.profiles = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Load customer profiles."""
        if os.path.exists(self.profiles_path):
            with open(self.profiles_path, 'r') as f:
                self.profiles = json.load(f)
            print(f"Loaded {len(self.profiles)} customer profiles")
        else:
            print(f"Warning: {self.profiles_path} not found. Personalization will be limited.")
    
    def get_customer_profile(self, customer_id: str) -> Optional[Dict]:
        """Get customer profile by ID."""
        return self.profiles.get(customer_id, None)
    
    def personalize_response(self, base_response: str, customer_id: str, 
                           query_category: str = None, 
                           customer_tier: str = None,
                           sentiment: str = None) -> str:
        """
        Personalize a response based on customer data.
        
        Args:
            base_response: The base generated response
            customer_id: Customer identifier
            query_category: Category of the query
            customer_tier: Customer tier (Basic, Pro, Premium, Enterprise)
            sentiment: Customer sentiment (positive, neutral, negative)
        
        Returns:
            Personalized response string
        """
        personalized = base_response
        
        # Get customer profile
        profile = self.get_customer_profile(customer_id)
        
        # Personalization based on communication style
        if profile:
            comm_style = profile.get('preferred_communication_style', 'professional')
            
            if comm_style == 'casual':
                # Make response more casual and friendly
                personalized = personalized.replace("I can help you", "I'd be happy to help you")
                personalized = personalized.replace("I apologize", "Sorry about that")
            elif comm_style == 'formal':
                # Make response more formal
                personalized = personalized.replace("I'd", "I would")
                personalized = personalized.replace("Let's", "Let us")
                personalized = personalized.replace("can't", "cannot")
        
        # Personalization based on customer tier
        if customer_tier:
            if customer_tier in ['Premium', 'Enterprise']:
                # Add premium touches
                if not any(word in personalized.lower() for word in ['priority', 'immediately', 'dedicated']):
                    personalized = f"Thank you for being a {customer_tier} customer. " + personalized
                    personalized += " I'll prioritize this for you."
            elif customer_tier == 'Basic':
                # Keep it simple and helpful
                personalized = personalized.replace("I'll prioritize this", "I'll handle this")
        
        # Personalization based on sentiment
        if sentiment:
            if sentiment == 'negative':
                # Add empathy and urgency
                if "I apologize" not in personalized and "I'm sorry" not in personalized:
                    personalized = "I sincerely apologize for the inconvenience. " + personalized
                personalized = personalized.replace("I can help", "I'll immediately help")
            elif sentiment == 'positive':
                # Acknowledge positive sentiment
                personalized = "I'm glad to hear from you! " + personalized
        
        # Personalization based on query category
        if query_category:
            if query_category == 'billing' and profile:
                # Add billing-specific personalization
                if 'total_spent' in profile:
                    personalized += f" As a valued customer, I want to ensure this is resolved quickly."
            elif query_category == 'technical':
                # Add technical support touches
                if profile and 'preferred_channels' in profile:
                    channels = profile['preferred_channels']
                    if 'phone' in channels:
                        personalized += " If you'd prefer, I can have a technical specialist call you."
        
        # Add customer name if available (simulated)
        if profile and customer_tier in ['Premium', 'Enterprise']:
            # In real scenario, we'd have customer name
            personalized = personalized.replace("you", "you", 1)  # First occurrence
        
        return personalized
    
    def personalize_batch(self, responses: list, customer_ids: list, 
                         query_categories: list = None,
                         customer_tiers: list = None,
                         sentiments: list = None) -> list:
        """Personalize a batch of responses."""
        personalized_responses = []
        
        for i, (response, customer_id) in enumerate(zip(responses, customer_ids)):
            category = query_categories[i] if query_categories else None
            tier = customer_tiers[i] if customer_tiers else None
            sentiment = sentiments[i] if sentiments else None
            
            personalized = self.personalize_response(
                response, customer_id, category, tier, sentiment
            )
            personalized_responses.append(personalized)
        
        return personalized_responses
    
    def get_personalization_summary(self, customer_id: str) -> Dict:
        """Get a summary of personalization factors for a customer."""
        profile = self.get_customer_profile(customer_id)
        
        if not profile:
            return {"status": "No profile found", "customer_id": customer_id}
        
        summary = {
            "customer_id": customer_id,
            "tier": profile.get('tier', 'Unknown'),
            "communication_style": profile.get('preferred_communication_style', 'professional'),
            "preferred_language": profile.get('preferred_language', 'English'),
            "customer_since": profile.get('customer_since', 'Unknown'),
            "total_spent": profile.get('total_spent', 0),
            "preferred_channels": profile.get('preferred_channels', []),
            "personalization_applied": True
        }
        
        return summary

def demonstrate_personalization():
    """Demonstrate personalization capabilities."""
    print("="*70)
    print("PERSONALIZATION DEMONSTRATION")
    print("="*70)
    
    personalizer = ResponsePersonalizer()
    
    # Example base responses
    base_responses = [
        "I can help you with that. Let me check your account.",
        "I'll investigate this issue and get back to you.",
        "Thank you for contacting us. I can assist you with this."
    ]
    
    # Example customer scenarios
    scenarios = [
        {
            "customer_id": "CUST_10000",
            "tier": "Premium",
            "category": "billing",
            "sentiment": "negative"
        },
        {
            "customer_id": "CUST_10001",
            "tier": "Basic",
            "category": "technical",
            "sentiment": "neutral"
        },
        {
            "customer_id": "CUST_10002",
            "tier": "Enterprise",
            "category": "product",
            "sentiment": "positive"
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        print(f"\n{'='*70}")
        print(f"Scenario {i+1}:")
        print(f"Customer ID: {scenario['customer_id']}")
        print(f"Tier: {scenario['tier']}")
        print(f"Category: {scenario['category']}")
        print(f"Sentiment: {scenario['sentiment']}")
        print(f"{'='*70}")
        
        base_response = base_responses[i % len(base_responses)]
        print(f"\nBase Response:\n{base_response}")
        
        personalized = personalizer.personalize_response(
            base_response,
            scenario['customer_id'],
            scenario['category'],
            scenario['tier'],
            scenario['sentiment']
        )
        
        print(f"\nPersonalized Response:\n{personalized}")
        
        summary = personalizer.get_personalization_summary(scenario['customer_id'])
        print(f"\nPersonalization Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    demonstrate_personalization()

