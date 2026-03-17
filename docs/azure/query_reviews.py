"""
Query and analyze sentiment data from Azure Table Storage
Run this after process_reviews.py to explore the data
"""

from azure.data.tables import TableServiceClient
from collections import Counter

# TODO: Replace with your actual connection string
ENDPOINT = "YOUR_ENDPOINT_HERE"  # For consistency, though not used in this file
KEY = "YOUR_KEY_HERE"  # For consistency, though not used in this file
STORAGE_CONNECTION_STRING = "YOUR_CONNECTION_STRING_HERE"
TABLE_NAME = "reviews"

def get_all_reviews():
    """
    Retrieve all reviews from the database
    
    Returns:
        List of review entities
    """
    table_service = TableServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    table_client = table_service.get_table_client(TABLE_NAME)
    
    # Query all entities
    entities = list(table_client.list_entities())
    
    return entities

def query_by_sentiment(sentiment):
    """
    Get all reviews with a specific sentiment
    
    Args:
        sentiment: 'positive', 'negative', or 'neutral'
        
    Returns:
        List of matching entities
    """
    table_service = TableServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    table_client = table_service.get_table_client(TABLE_NAME)
    
    # Query with filter
    query = f"sentiment eq '{sentiment}'"
    entities = list(table_client.query_entities(query))
    
    return entities

def query_high_confidence(min_confidence=0.90):
    """
    Get reviews where the model is very confident
    
    Args:
        min_confidence: Minimum confidence score (0-1)
        
    Returns:
        List of high-confidence entities
    """
    table_service = TableServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    table_client = table_service.get_table_client(TABLE_NAME)
    
    # Query with filter
    query = f"confidence gt {min_confidence}"
    entities = list(table_client.query_entities(query))
    
    return entities

def analyze_data():
    """
    Run various analyses on the stored data
    """
    print("Movie Review Sentiment Analysis")
    print("=" * 80)
    
    try:
        # Get all reviews
        print("\n1. Loading all reviews from database...")
        all_reviews = get_all_reviews()
        print(f"   Found {len(all_reviews)} reviews")
        
        if len(all_reviews) == 0:
            print("\n   No reviews found! Run process_reviews.py first.")
            return
        
        # Overall sentiment distribution
        print("\n2. Overall Sentiment Distribution:")
        sentiments = [r['sentiment'] for r in all_reviews]
        sentiment_counts = Counter(sentiments)
        
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(all_reviews)) * 100
            print(f"   {sentiment.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Average confidence
        print("\n3. Average Confidence Scores:")
        avg_confidence = sum(r['confidence'] for r in all_reviews) / len(all_reviews)
        print(f"   Overall: {avg_confidence:.3f}")
        
        for sentiment in ['positive', 'negative', 'neutral']:
            sentiment_reviews = [r for r in all_reviews if r['sentiment'] == sentiment]
            if sentiment_reviews:
                avg = sum(r['confidence'] for r in sentiment_reviews) / len(sentiment_reviews)
                print(f"   {sentiment.capitalize()}: {avg:.3f}")
        
        # Most negative review
        print("\n4. Most Confidently Negative Review:")
        negative_reviews = [r for r in all_reviews if r['sentiment'] == 'negative']
        if negative_reviews:
            most_negative = max(negative_reviews, key=lambda x: x['confidence'])
            print(f"   Confidence: {most_negative['confidence']:.3f}")
            print(f"   Text: \"{most_negative['text']}\"")
        else:
            print("   No negative reviews found")
        
        # Most positive review
        print("\n5. Most Confidently Positive Review:")
        positive_reviews = [r for r in all_reviews if r['sentiment'] == 'positive']
        if positive_reviews:
            most_positive = max(positive_reviews, key=lambda x: x['confidence'])
            print(f"   Confidence: {most_positive['confidence']:.3f}")
            print(f"   Text: \"{most_positive['text']}\"")
        else:
            print("   No positive reviews found")
        
        # High confidence reviews
        print("\n6. High Confidence Reviews (>0.95):")
        high_conf = query_high_confidence(0.95)
        print(f"   Found {len(high_conf)} high-confidence predictions")
        
        for review in high_conf[:3]:  # Show first 3
            print(f"   - {review['sentiment'].upper()} ({review['confidence']:.3f}): \"{review['text'][:60]}...\"")
        
        # Low confidence / uncertain reviews
        print("\n7. Uncertain Reviews (confidence < 0.70):")
        low_conf = [r for r in all_reviews if r['confidence'] < 0.70]
        print(f"   Found {len(low_conf)} uncertain predictions")
        
        for review in low_conf[:3]:  # Show first 3
            print(f"   - {review['sentiment']} ({review['confidence']:.3f}): \"{review['text'][:60]}...\"")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure STORAGE_CONNECTION_STRING is set correctly!")
        return
    
    print("\n" + "=" * 80)
    print("Analysis complete! ✓")

def interactive_query():
    """
    Let user run custom queries
    """
    print("\nInteractive Query Mode")
    print("Try these examples:")
    print("  - Get all negative reviews: query_by_sentiment('negative')")
    print("  - Get high confidence: query_high_confidence(0.90)")
    print()

def main():
    analyze_data()
    
    # Uncomment to enable interactive mode
    # interactive_query()

if __name__ == "__main__":
    main()
