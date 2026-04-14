# Simple Ariadne GraphQL Server

This example, based on [https://github.com/mirumee/ariadne](https://github.com/mirumee/ariadne), creates an API defining a *Person* type and a single query field *people* returning a list of two persons. It also starts a local server with GraphiQL on [http://127.0.0.1:8000](http://127.0.0.1:8000).

Requires the ariadne and uvicorn modules:

```bash
pip install ariadne uvicorn
```

Start the server

```bash
uvicorn ariadne_example:app
```

And in the GraphiQL widonw you can put in a query like this:

```javascript
query { people { fullName }}
```
```json
{
  "data": {
    "people": [
      { "fullName": "John Doe" },
      { "fullName": "Bob Boberson" } ]
  }
}
```

Or ask for more fields to be returned:

```javascript
{ people { firstName, lastName, age }}
```

Here, we did not add "query" to the beginning of the statement since it is implied anyway.

You can even do this, which will expand to using all fields:

```javascript
{ people }
```

Why can I not do the following?

```javascript
{ person(firstName : "John") { fullName} } 
```

This is even though it seems to be exactly what is suggested at the GraphQL homepage at [https://graphql.org](https://graphql.org).

> Insert the answer here, probably along the lines that there is no resolver set up for this.


### Notes on the code

Define types using the Schema Definition Language [https://graphql.org/learn/schema/](https://graphql.org/learn/schema/)

Resolvers are functions mediating between API consumers and the application's domain logic. Here we have

```python
@query.field("people")
def resolve_people(*_):
    return [
        {"firstName": "John", "lastName": "Doe", "age": 21},
        {"firstName": "Bob", "lastName": "Boberson", "age": 24} ]

```

Typically, resolvers take at least two arguments, the query's parent object and the query's execution info, which usually has a context attribute. Above we do not use the two arguments and blindly return a list of people. 

