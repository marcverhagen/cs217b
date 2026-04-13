"""

This is the first example from the Ariadne introduction at
https://ariadnegraphql.org/server/Docs/intro.

$ pip install uvicorn ariadne
$ python ariadne_hello:app

From GraphiQL:

    { hello }

"""

from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL


# The schema define the special type Query that GraphQL services use as an entry
# point for all reading operations. We  specify a single field, named hello, that
# returns a value of type String, and that it will never return null (indicated
# by the exclamation mark).

type_defs = gql("type Query { hello: String! }")

# Create type instance for Query type defined in our schema...
query = QueryType()

# ...and assign our resolver function to its "hello" field.
@query.field("hello")
def resolve_hello(_, info):
    # The default GraphQL server implementation provided by Ariadne defines
    # info.context as a Python dictionary containing a single key named request
    # containing a request object.
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent

# In Ariadne the process of adding the Python logic to GraphQL schema is called
# binding to schema, and special types that are passed in are called bindables.
# QueryType is one of many bindables provided by Ariadne, often you will see a
# list that includes mutations and others.
schema = make_executable_schema(type_defs, query)

# Finally create an instance of ariadne.asgi.GraphQL that can be run in an ASGI
# server like uvicorn.
app = GraphQL(schema, debug=True)
