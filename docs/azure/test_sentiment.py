"""
Test the Azure AI Language sentiment analysis API
Run this first to verify your API key and endpoint are working
"""

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# TODO: Replace with your actual values from Azure Portal
ENDPOINT = "YOUR_ENDPOINT_HERE"  # Example: https://your-resource.cognitiveservices.azure.com/
KEY = "YOUR_KEY_HERE"
STORAGE_CONNECTION_STRING = "YOUR_CONNECTION_STRING_HERE"  # For consistency across files

def analyze_sentiment(text):
    """
    Analyze sentiment of a single text string
    
    Args:
        text: String to analyze
        
    Returns:
        Sentiment result object
    """
    client = TextAnalyticsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))
    
    # API expects a list of documents
    documents = [text]
    
    # Call the API
    results = client.analyze_sentiment(documents)
    
    return results[0]

def main():
    # Test with a few sample reviews
    test_reviews = [
        "This movie was absolutely amazing! Best film I've seen all year.",
        "Terrible waste of time. The plot made no sense.",
        "It was okay, nothing special but not bad either."
    ]
    
    print("Testing Azure AI Language - Sentiment Analysis\n")
    print("=" * 60)
    
    for review in test_reviews:
        print(f"\nReview: {review}")
        
        try:
            result = analyze_sentiment(review)
            
            print(f"Sentiment: {result.sentiment}")
            print(f"Confidence scores:")
            print(f"  Positive: {result.confidence_scores.positive:.2f}")
            print(f"  Neutral: {result.confidence_scores.neutral:.2f}")
            print(f"  Negative: {result.confidence_scores.negative:.2f}")
            
        except Exception as e:
            print(f"Error: {e}")
            print("\nMake sure you've set ENDPOINT and KEY at the top of this file!")
            break
    
    print("\n" + "=" * 60)
    print("Test complete!")

if __name__ == "__main__":
    main()
