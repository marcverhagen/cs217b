import json

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="http://127.0.0.1:5000/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)


# Provide a simple GraphQL query, just listing the titles
query = gql('query AllPosts { listPosts { posts { title } } }')

# Execute the query on the transport
result = client.execute(query)
print(json.dumps(result))

