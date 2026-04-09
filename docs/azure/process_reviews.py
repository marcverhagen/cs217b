"""

Process multiple movie reviews and save results to Azure Table Storage.

This script reads reviews from a file, analyzes it (at the moment just for sentiment
and key phrases), and stores results.

"""

import os
import uuid
from datetime import datetime, UTC

from dotenv import load_dotenv

from azure.ai import textanalytics
from azure.core.credentials import AzureKeyCredential
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ServiceRequestError, ClientAuthenticationError

DEBUG = False

# The .env file should have endpoint, key and connection strings from the
# Azure portal
load_dotenv()

ENDPOINT = os.environ['AZURE_ENDPOINT']
KEY = os.environ['AZURE_KEY']
CONNECTION = os.environ['AZURE_CONNECTION']
TABLE_NAME = "reviews"


class Sentiment:

    """This is a proxy to the textanalytics.AnalyzeSentimentResult class that
    offers some extra properties, most notably the confidence property. At the
    same time it hides many of the properties of the embedded object."""

    def __init__(self, result: textanalytics.AnalyzeSentimentResult):
        self.data = result

    @property
    def id(self):
        return self.data.id

    @property
    def sentiment(self):
        return self.data.sentiment

    @property
    def confidence(self):
        # Get the highest confidence score (handles 'mixed' sentiment correctly)
        return max(
            self.data.confidence_scores.positive,
            self.data.confidence_scores.negative,
            self.data.confidence_scores.neutral)

    def __str__(self):
        return (
            f'<{self.__class__.__name__} id={self.id}'
            f' sentiment={self.sentiment} confidence={self.confidence}>')


def get_sample_reviews() -> list[str]:
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


def get_client() ->textanalytics.TextAnalyticsClient:
    return textanalytics.TextAnalyticsClient(
        endpoint=ENDPOINT, 
        credential=AzureKeyCredential(KEY))


def debug_result(review, sentiment, presult):
    if DEBUG:
        print(review)
        print('  ', sentiment)
        print(f'    key_phrases={presult.key_phrases}>')


def analyze_reviews(reviews: list[str], batch_size=10):
    """
    Analyze reviews.

    Args:
        reviews: List of review strings
        batch_size: size of batches, the maximum for the API is 10
        
    Returns:
        List of (review, sentiment, confidence) tuples
    """
    client = get_client()
    results = []    
    for i in range(0, len(reviews), batch_size):
        batch = reviews[i:i + batch_size]
        print(f"Processing reviews {i+1} to {i+len(batch)}...")
        sentiment_results = client.analyze_sentiment(batch)
        phrase_results = client.extract_key_phrases(batch)
        for review, sresult, presult in zip(batch, sentiment_results, phrase_results):
            sentiment = Sentiment(sresult)
            debug_result(review, sentiment, presult)
            results.append({
                'text': review,
                'sentiment': sentiment.sentiment,
                'confidence': sentiment.confidence,
                'keyphrases': presult['key_phrases'] })
    return results


def save_to_database(results):
    """
    Save sentiment results to Azure Table Storage
    
    Args:
        results: List of dicts with text, sentiment, confidence
    """
    # Connect to Table Storage
    table_service = TableServiceClient.from_connection_string(CONNECTION)
    table_client = table_service.get_table_client(TABLE_NAME)
    print(f"Saving {len(results)} reviews to database...")
    for i, result in enumerate(results):
        # Create entity for Table Storage
        # PartitionKey and RowKey are required fields
        entity = {
            'PartitionKey': 'movies',     # Group all movie reviews together
            'RowKey': str(uuid.uuid4()),  # Unique ID for this review
            'text': result['text'],
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'timestamp': datetime.now(UTC).isoformat(),        # Azure will do this
            'keyphrases': ' :: '.join(result['keyphrases']) }  # cannot be a list 
        # Insert into table
        table_client.create_entity(entity)
        if (i + 1) % 5 == 0:
            print(f"  Saved {i+1}/{len(results)} reviews...")
    print(f"✓ All {len(results)} reviews saved to database!")


def main():
    
    # Step 1: Get reviews
    print("\n1. Loading reviews...")
    reviews = get_sample_reviews()
    print(f"   Loaded {len(reviews)} reviews")
    
    # Step 2: Analyze sentiment
    print("\n2. Analyzing sentiment with Azure AI Language...")
    try:
        results = analyze_reviews(reviews)
        print(f"✓ Analyzed {len(results)} reviews")
        sentiments = [r['sentiment'] for r in results]
        print(f"  <Summary pos={sentiments.count('positive')}"
              f" neg={sentiments.count('negative')}"
              f" neutral={sentiments.count('neutral')}>")
    except ServiceRequestError as e:
        exit(f'>>> ERROR\n{e.message}')
    except ClientAuthenticationError as e:
        exit(f'>>> ERROR\n{e.message}')
    
    # Step 3: Save to database
    print("\n3. Saving to Azure Table Storage...")
    try:
        save_to_database(results)
    except Exception as e:
        print(f">>> Error saving to database: {e}")
        print("    Make sure STORAGE_CONNECTION_STRING is set correctly")
        print("    Also check that the table exists in Azure Portal")
        return
    
    print("\n✓ Pipeline complete")
    print("  Run query_reviews.py to analyze the data\n")



if __name__ == "__main__":

    main()
