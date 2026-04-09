"""

Query and analyze sentiment data from Azure Table Storage.

Run this after process_reviews.py to explore the data.

"""

import os, sys
from collections import Counter

from dotenv import load_dotenv

from azure.data.tables import TableServiceClient, TableClient, TableEntity
from azure.core.exceptions import ResourceExistsError


load_dotenv()

ENDPOINT = os.environ['AZURE_ENDPOINT']
KEY = os.environ['AZURE_KEY']
CONNECTION = os.environ['AZURE_CONNECTION']
TABLE_NAME = "reviews"


def get_all_reviews() -> list[TableEntity]:
    """
    Retrieve all reviews from the database
    
    Returns:
        List of review entities
    """
    table_service = TableServiceClient.from_connection_string(CONNECTION)
    table_client = table_service.get_table_client(TABLE_NAME)
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
    table_service = TableServiceClient.from_connection_string(CONNECTION)
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
    table_service = TableServiceClient.from_connection_string(CONNECTION)
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
        print(type(all_reviews[0]))
        print(all_reviews[0])

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
        print("Make sure CONNECTION is set correctly!")
        return
    
    print("\n" + "=" * 80)
    print("Analysis complete! ✓")


class AzureTableService:

    """An Azure table service set up for a particular account. It is a wrapper
    around a TableServiceClient instance in which you can create a TableClient
    for a particular table (only one table at the time)."""

    def __init__(self, connection_string: str):
        """Initialize the table service from the Azure connection string."""
        self.table_service = \
            TableServiceClient.from_connection_string(connection_string)
        self.table : TableClient = None

    def get_table_client(self, table_name: str) -> TableClient:
        """Set a TableClient given a table name, which is assumed to exist."""
        self.table = self.table_service.get_table_client(table_name)
        return self.table

    @property
    def tables(self) -> list:
        return self.table_service.list_tables()

    @property
    def table_names(self) -> list[str]:
        return [t.name for t in self.tables]

    @property
    def url(self):
        return self.table_service.url

    @property
    def account_name(self):
        return self.table_service.account_name
    
    def create_table(self, table_name: str):
        try:
            table_item = self.table_service.create_table(table_name)
            print(f'>>> created table {table_item.table_name}')
            print(type(table_item), table_item)
        except ResourceExistsError as e:
            print(f'>>> table {table_name} already exists')

    def delete_table(self, table_name: str):
        self.table_service.delete_table(table_name)

    def create_entity(self, entity: dict):
        try:
            self.table.create_entity(entity)
        except ResourceExistsError as e:
            print('\n>>> Could no create entity')
            print('>>>', type(e))
            print(e)


def test():

    # Get the table service client, which lets you print some info
    ts = AzureTableService(CONNECTION)
    print(f'>>> service client url:     {ts.url}')
    print(f'>>> service client account: {ts.account_name}')
    print('>>> tables:', ' '.join(ts.table_names))
    
    #ts.create_table('test3')
    
    # Get the table client (an instance of TableClient) for TABLE_NAME
    table_client = ts.get_table_client(TABLE_NAME)
    print(f'>>> table name:        {table_client.table_name}')
    print(f'>>> table client url:  {table_client.url}')

    # Getting all entities
    entities = table_client.list_entities()
    print(f'>>> table has {len(list(entities))} entities')

    # Getting one row
    rowkey = '012d8104-3e62-47cb-8a89-b3c3c1f4e2cb'
    my_filter = f"RowKey eq '{rowkey}'"
    result = table_client.query_entities(query_filter=my_filter)
    for e in result:
        print(e)

    # Using both keys. Note that the above may have given you more rows if
    # there were multiple partitions. Here we use both keys and we use a
    # parameter dictionary.
    parameters = {"pk": "movies", "rk": rowkey}
    query_filter = "PartitionKey eq @pk and RowKey eq @rk"
    result = table_client.query_entities(query_filter, parameters=parameters)
    for e in result:
        print(e)

    # Using get_entity()
    entity = table_client.get_entity(partition_key='movies', row_key=rowkey)
    print(entity)

    # Adding an entity to the new test table
    entity = {
        'PartitionKey': 'movies',
        'RowKey': 'm001',
        'title': 'Thelma and Louise' }
    test_table = ts.get_table_client('test')
    #test_table.create_entity(entity)
    #print(f'>>> added {entity}')
    ts.create_entity(entity)


def main():
    test()
    #analyze_data()
    #query_by_sentiment()
    #uery_high_confidence()



if __name__ == "__main__":

    main()
