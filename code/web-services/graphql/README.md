# GraphQL

[GraphQL](https://graphql.org/) positions itself as the query language for modern APIs. 

This directory has a couple of GraphQL examples.

First we have two simple examples using Ariadne, a Python library for implementing GraphQL servers.

- [Retrieve a list of people](example1/ariadne_example.md). This example is used in the readme file of the  [Ariadne's GitHub repository](https://github.com/mirumee/ariadne).
- [Print the user agent from the request](example1/ariadne_hello.py). This is the first example from the Ariadne introduction at [https://ariadnegraphql.org/server/Docs/intro](https://ariadnegraphql.org/server/Docs/intro) and it is one of the few examples in the introduction that work without some massaging.

Here is [a more involved example](example2/readme.md) that embeds GrapQL in a Flask server, uses an SQLAlchemy database of posts and allows a far wider range of operations than the examples above: listing all posts, selecting a post, creating a post, updating a post and deleting one or more posts.