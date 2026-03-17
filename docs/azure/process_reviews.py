"""
Process multiple movie reviews and save results to Azure Table Storage
This script reads reviews from a file, analyzes sentiment, and stores results
"""

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.data.tables import TableServiceClient
from datetime import datetime
import uuid

# TODO: Replace with your actual values from Azure Portal
ENDPOINT = "YOUR_ENDPOINT_HERE"
KEY = "YOUR_KEY_HERE"
STORAGE_CONNECTION_STRING = "YOUR_CONNECTION_STRING_HERE"
TABLE_NAME = "reviews"

def get_sample_reviews():
    """
    Return a list of sample movie reviews
    In practice, you might load these from a file or database
    """
    return [
        "The cinematography was breathtaking and the story kept me engaged throughout.",
        "Waste of money. Poor acting and a boring plot.",
        "Pretty average. Some good moments but nothing memorable.",
        "Absolutely loved it! The twist at the end was perfect.",
        "Could barely stay awake. So slow and predictable.",
        "Great performances by the cast. Well worth watching.",
        "Not my favorite but I can see why others liked it.",
        "Brilliant film! Every scene was beautifully crafted.",
        "Disappointing. Expected much more from this director.",
        "An okay movie. Nothing special but entertaining enough.",
        "One of the best movies I've ever seen. Highly recommend!",
        "Terrible pacing and weak character development.",
        "Solid film with some really touching moments.",
        "Completely forgettable. Won't be watching again.",
        "Exceeded my expectations! A real gem.",
        "The worst movie I've seen in years. Avoid at all costs.",
        "Nice visuals but the story was lacking.",
        "A masterpiece. This will be remembered for years.",
        "Meh. It was fine I guess.",
        "Absolutely hated it. Total disappointment."
    ]

def analyze_reviews(reviews):
    """
    Analyze sentiment for a batch of reviews
    
    Args:
        reviews: List of review strings
        
    Returns:
        List of (review, sentiment, confidence) tuples
    """
    client = TextAnalyticsClient(
        endpoint=ENDPOINT, 
        credential=AzureKeyCredential(KEY)
    )
    
    # API can handle batches of up to 10 documents at a time
    batch_size = 10
    results = []
    
    for i in range(0, len(reviews), batch_size):
        batch = reviews[i:i + batch_size]
        
        print(f"Processing reviews {i+1} to {i+len(batch)}...")
        
        # Call the API
        sentiment_results = client.analyze_sentiment(batch)
        
        # Combine reviews with their results
        for review, result in zip(batch, sentiment_results):
            # Get the highest confidence score (handles 'mixed' sentiment correctly)
            confidence = max(
                result.confidence_scores.positive,
                result.confidence_scores.negative,
                result.confidence_scores.neutral
            )
            
            results.append({
                'text': review,
                'sentiment': result.sentiment,
                'confidence': confidence
            })
    
    return results

def save_to_database(results):
    """
    Save sentiment results to Azure Table Storage
    
    Args:
        results: List of dicts with text, sentiment, confidence
    """
    # Connect to Table Storage
    table_service = TableServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    table_client = table_service.get_table_client(TABLE_NAME)
    
    print(f"\nSaving {len(results)} reviews to database...")
    
    for i, result in enumerate(results):
        # Create entity for Table Storage
        # PartitionKey and RowKey are required fields
        entity = {
            'PartitionKey': 'movies',  # Group all movie reviews together
            'RowKey': str(uuid.uuid4()),  # Unique ID for this review
            'text': result['text'],
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Insert into table
        table_client.create_entity(entity)
        
        if (i + 1) % 5 == 0:
            print(f"  Saved {i+1}/{len(results)} reviews...")
    
    print(f"✓ All {len(results)} reviews saved to database!")

def main():
    print("Movie Review Sentiment Analysis Pipeline")
    print("=" * 60)
    
    # Step 1: Get reviews
    print("\n1. Loading reviews...")
    reviews = get_sample_reviews()
    print(f"   Loaded {len(reviews)} reviews")
    
    # Step 2: Analyze sentiment
    print("\n2. Analyzing sentiment with Azure AI Language...")
    try:
        results = analyze_reviews(reviews)
        print(f"   ✓ Analyzed {len(results)} reviews")
        
        # Show a summary
        sentiments = [r['sentiment'] for r in results]
        print(f"\n   Summary:")
        print(f"   - Positive: {sentiments.count('positive')}")
        print(f"   - Negative: {sentiments.count('negative')}")
        print(f"   - Neutral: {sentiments.count('neutral')}")
        
    except Exception as e:
        print(f"   Error analyzing reviews: {e}")
        print("   Make sure ENDPOINT and KEY are set correctly!")
        return
    
    # Step 3: Save to database
    print("\n3. Saving to Azure Table Storage...")
    try:
        save_to_database(results)
    except Exception as e:
        print(f"   Error saving to database: {e}")
        print("   Make sure STORAGE_CONNECTION_STRING is set correctly!")
        print("   Also check that the table exists in Azure Portal!")
        return
    
    print("\n" + "=" * 60)
    print("Pipeline complete! ✓")
    print("\nNext step: Run query_reviews.py to analyze the data")

if __name__ == "__main__":
    main()
