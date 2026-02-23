"""
Data preprocessing and analysis module with visualizations.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class DataPreprocessor:
    def __init__(self, data_path='data/raw/customer_support_dataset.csv', 
                 profiles_path='data/raw/customer_profiles.json'):
        self.data_path = data_path
        self.profiles_path = profiles_path
        self.df = None
        self.profiles = None
        self.processed_df = None
        
    def load_data(self):
        """Load raw data files."""
        print("Loading data...")
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df)} records from {self.data_path}")
        else:
            print(f"Warning: {self.data_path} not found. Please run data_generation.py first.")
            return False
            
        if os.path.exists(self.profiles_path):
            with open(self.profiles_path, 'r') as f:
                self.profiles = json.load(f)
            print(f"Loaded {len(self.profiles)} customer profiles from {self.profiles_path}")
        else:
            print(f"Warning: {self.profiles_path} not found.")
            
        return True
    
    def preprocess(self):
        """Preprocess the dataset."""
        if self.df is None:
            print("Please load data first.")
            return None
            
        print("\nPreprocessing data...")
        df = self.df.copy()
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.day_name()
        
        # Text preprocessing
        df['query_length'] = df['query'].str.len()
        df['response_length'] = df['response'].str.len()
        df['query_word_count'] = df['query'].str.split().str.len()
        df['response_word_count'] = df['response'].str.split().str.len()
        
        # Encode categorical variables
        df['category_encoded'] = pd.Categorical(df['category']).codes
        df['tier_encoded'] = pd.Categorical(df['customer_tier']).codes
        df['segment_encoded'] = pd.Categorical(df['customer_segment']).codes
        
        # Handle missing values
        df['satisfaction_score'] = df['satisfaction_score'].fillna(df['satisfaction_score'].median())
        
        # Create interaction features
        df['is_high_priority'] = (df['priority'].isin(['High', 'Urgent'])).astype(int)
        df['is_premium_customer'] = (df['customer_tier'].isin(['Premium', 'Enterprise'])).astype(int)
        
        self.processed_df = df
        
        # Save processed data
        output_path = 'data/processed/preprocessed_dataset.csv'
        df.to_csv(output_path, index=False)
        print(f"Preprocessed data saved to {output_path}")
        
        return df
    
    def analyze_data(self):
        """Perform comprehensive data analysis."""
        if self.processed_df is None:
            print("Please preprocess data first.")
            return
        
        df = self.processed_df
        print("\n" + "="*50)
        print("DATA ANALYSIS SUMMARY")
        print("="*50)
        
        # Basic statistics
        print("\n1. Dataset Overview:")
        print(f"   Total Records: {len(df)}")
        print(f"   Unique Customers: {df['customer_id'].nunique()}")
        print(f"   Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        # Category distribution
        print("\n2. Category Distribution:")
        print(df['category'].value_counts())
        
        # Customer tier distribution
        print("\n3. Customer Tier Distribution:")
        print(df['customer_tier'].value_counts())
        
        # Priority distribution
        print("\n4. Priority Distribution:")
        print(df['priority'].value_counts())
        
        # Sentiment distribution
        print("\n5. Sentiment Distribution:")
        print(df['sentiment'].value_counts())
        
        # Average satisfaction
        print(f"\n6. Average Satisfaction Score: {df['satisfaction_score'].mean():.2f}")
        
        # Text statistics
        print(f"\n7. Text Statistics:")
        print(f"   Average Query Length: {df['query_length'].mean():.0f} characters")
        print(f"   Average Response Length: {df['response_length'].mean():.0f} characters")
        print(f"   Average Query Words: {df['query_word_count'].mean():.1f}")
        print(f"   Average Response Words: {df['response_word_count'].mean():.1f}")
    
    def create_visualizations(self):
        """Create comprehensive visualizations."""
        if self.processed_df is None:
            print("Please preprocess data first.")
            return
        
        df = self.processed_df
        print("\nGenerating visualizations...")
        
        # Create output directory
        os.makedirs('reports/visualizations', exist_ok=True)
        
        # 1. Category Distribution
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Category pie chart
        category_counts = df['category'].value_counts()
        axes[0, 0].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title('Query Category Distribution', fontsize=14, fontweight='bold')
        
        # Customer Tier Distribution
        tier_counts = df['customer_tier'].value_counts()
        axes[0, 1].bar(tier_counts.index, tier_counts.values, color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'])
        axes[0, 1].set_title('Customer Tier Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Customer Tier')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Priority Distribution
        priority_counts = df['priority'].value_counts()
        axes[1, 0].barh(priority_counts.index, priority_counts.values, color=['#95a5a6', '#3498db', '#f39c12', '#e74c3c'])
        axes[1, 0].set_title('Priority Level Distribution', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Count')
        
        # Sentiment Distribution
        sentiment_counts = df['sentiment'].value_counts()
        axes[1, 1].bar(sentiment_counts.index, sentiment_counts.values, 
                      color=['#2ecc71', '#95a5a6', '#e74c3c'])
        axes[1, 1].set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Sentiment')
        axes[1, 1].set_ylabel('Count')
        
        plt.tight_layout()
        plt.savefig('reports/visualizations/01_basic_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: 01_basic_distributions.png")
        
        # 2. Temporal Analysis
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Queries over time
        daily_counts = df.groupby('date').size()
        axes[0, 0].plot(daily_counts.index, daily_counts.values, linewidth=2, color='#3498db')
        axes[0, 0].set_title('Daily Query Volume', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Number of Queries')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Hourly distribution
        hourly_counts = df.groupby('hour').size()
        axes[0, 1].bar(hourly_counts.index, hourly_counts.values, color='#2ecc71')
        axes[0, 1].set_title('Query Volume by Hour of Day', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Hour')
        axes[0, 1].set_ylabel('Number of Queries')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Day of week distribution
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = df['day_of_week'].value_counts().reindex(day_order)
        axes[1, 0].bar(day_counts.index, day_counts.values, color='#f39c12')
        axes[1, 0].set_title('Query Volume by Day of Week', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Day of Week')
        axes[1, 0].set_ylabel('Number of Queries')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Category over time
        category_time = df.groupby(['date', 'category']).size().unstack(fill_value=0)
        for category in category_time.columns:
            axes[1, 1].plot(category_time.index, category_time[category], 
                           label=category, linewidth=2, alpha=0.7)
        axes[1, 1].set_title('Query Categories Over Time', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Number of Queries')
        axes[1, 1].legend()
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('reports/visualizations/02_temporal_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: 02_temporal_analysis.png")
        
        # 3. Customer Analysis
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Customer Lifetime Value Distribution
        axes[0, 0].hist(df['customer_lifetime_value'], bins=50, color='#3498db', edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Customer Lifetime Value Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Customer Lifetime Value ($)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Interaction Count Distribution
        axes[0, 1].hist(df['interaction_count'], bins=30, color='#2ecc71', edgecolor='black', alpha=0.7)
        axes[0, 1].set_title('Customer Interaction Count Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Number of Interactions')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Satisfaction Score by Tier
        satisfaction_by_tier = df.groupby('customer_tier')['satisfaction_score'].mean().sort_values()
        axes[1, 0].barh(satisfaction_by_tier.index, satisfaction_by_tier.values, color='#f39c12')
        axes[1, 0].set_title('Average Satisfaction Score by Customer Tier', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Average Satisfaction Score')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # CLV by Tier
        clv_by_tier = df.groupby('customer_tier')['customer_lifetime_value'].mean().sort_values()
        axes[1, 1].bar(clv_by_tier.index, clv_by_tier.values, color='#e74c3c')
        axes[1, 1].set_title('Average Customer Lifetime Value by Tier', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Customer Tier')
        axes[1, 1].set_ylabel('Average CLV ($)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('reports/visualizations/03_customer_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: 03_customer_analysis.png")
        
        # 4. Text Analysis
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Query Length Distribution
        axes[0, 0].hist(df['query_length'], bins=50, color='#3498db', edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Query Length Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Query Length (characters)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Response Length Distribution
        axes[0, 1].hist(df['response_length'], bins=50, color='#2ecc71', edgecolor='black', alpha=0.7)
        axes[0, 1].set_title('Response Length Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Response Length (characters)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Query vs Response Length
        axes[1, 0].scatter(df['query_length'], df['response_length'], alpha=0.5, color='#f39c12', s=20)
        axes[1, 0].set_title('Query vs Response Length', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Query Length (characters)')
        axes[1, 0].set_ylabel('Response Length (characters)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Average Response Length by Category
        response_by_category = df.groupby('category')['response_length'].mean().sort_values()
        axes[1, 1].barh(response_by_category.index, response_by_category.values, color='#e74c3c')
        axes[1, 1].set_title('Average Response Length by Category', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Average Response Length (characters)')
        axes[1, 1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('reports/visualizations/04_text_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: 04_text_analysis.png")
        
        # 5. Interactive Plotly Dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Query Volume Over Time', 'Category Distribution', 
                          'Customer Tier vs Satisfaction', 'Regional Distribution'),
            specs=[[{"secondary_y": False}, {"type": "pie"}],
                   [{"type": "box"}, {"type": "bar"}]]
        )
        
        # Time series
        daily_counts = df.groupby('date').size()
        fig.add_trace(
            go.Scatter(x=daily_counts.index, y=daily_counts.values, 
                      mode='lines', name='Daily Queries', line=dict(color='#3498db', width=2)),
            row=1, col=1
        )
        
        # Pie chart
        category_counts = df['category'].value_counts()
        fig.add_trace(
            go.Pie(labels=category_counts.index, values=category_counts.values, 
                  name="Categories"),
            row=1, col=2
        )
        
        # Box plot
        for tier in df['customer_tier'].unique():
            tier_data = df[df['customer_tier'] == tier]['satisfaction_score']
            fig.add_trace(
                go.Box(y=tier_data, name=tier, boxmean='sd'),
                row=2, col=1
            )
        
        # Regional distribution
        region_counts = df['region'].value_counts()
        fig.add_trace(
            go.Bar(x=region_counts.index, y=region_counts.values, 
                  marker_color='#2ecc71', name='Queries by Region'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Customer Support Analytics Dashboard", 
                         showlegend=False)
        fig.write_html('reports/visualizations/05_interactive_dashboard.html')
        print("  ✓ Saved: 05_interactive_dashboard.html")
        
        print("\nAll visualizations generated successfully!")
    
    def generate_insights_report(self):
        """Generate a text report with key insights."""
        if self.processed_df is None:
            print("Please preprocess data first.")
            return
        
        df = self.processed_df
        
        report = []
        report.append("="*70)
        report.append("CUSTOMER SUPPORT DATA ANALYSIS - KEY INSIGHTS")
        report.append("="*70)
        report.append("")
        
        # Key Metrics
        report.append("KEY METRICS:")
        report.append(f"  • Total Support Interactions: {len(df):,}")
        report.append(f"  • Unique Customers: {df['customer_id'].nunique():,}")
        report.append(f"  • Average Satisfaction Score: {df['satisfaction_score'].mean():.2f}/5.0")
        report.append(f"  • Average Response Time: {df['response_length'].mean():.0f} characters")
        report.append("")
        
        # Category Insights
        report.append("CATEGORY INSIGHTS:")
        category_dist = df['category'].value_counts(normalize=True) * 100
        for cat, pct in category_dist.items():
            report.append(f"  • {cat.capitalize()}: {pct:.1f}% of all queries")
        report.append("")
        
        # Customer Tier Insights
        report.append("CUSTOMER TIER INSIGHTS:")
        tier_clv = df.groupby('customer_tier')['customer_lifetime_value'].mean()
        for tier, clv in tier_clv.items():
            report.append(f"  • {tier} customers: Average CLV ${clv:.2f}")
        report.append("")
        
        # Priority Insights
        report.append("PRIORITY DISTRIBUTION:")
        priority_dist = df['priority'].value_counts(normalize=True) * 100
        for priority, pct in priority_dist.items():
            report.append(f"  • {priority}: {pct:.1f}%")
        report.append("")
        
        # Temporal Insights
        report.append("TEMPORAL INSIGHTS:")
        busiest_hour = df.groupby('hour').size().idxmax()
        busiest_day = df['day_of_week'].value_counts().idxmax()
        report.append(f"  • Busiest Hour: {busiest_hour}:00")
        report.append(f"  • Busiest Day: {busiest_day}")
        report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS:")
        report.append("  1. Focus on the most common query categories for training")
        report.append("  2. Prioritize high-value customer segments")
        report.append("  3. Optimize response templates for common scenarios")
        report.append("  4. Consider staffing adjustments based on temporal patterns")
        report.append("")
        report.append("="*70)
        
        report_text = "\n".join(report)
        
        # Save report
        os.makedirs('reports', exist_ok=True)
        with open('reports/data_analysis_insights.txt', 'w') as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\nInsights report saved to reports/data_analysis_insights.txt")

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    
    if preprocessor.load_data():
        preprocessor.preprocess()
        preprocessor.analyze_data()
        preprocessor.create_visualizations()
        preprocessor.generate_insights_report()
        print("\n✓ Data preprocessing and analysis complete!")

