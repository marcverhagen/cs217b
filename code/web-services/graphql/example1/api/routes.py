from flask import request, jsonify

from ariadne import load_schema_from_path, make_executable_schema
from ariadne import graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.explorer import ExplorerGraphiQL

from api import app, db, queries, mutations


query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listPosts", queries.listPosts_resolver)
query.set_field("getPost", queries.getPost_resolver)

mutation.set_field("createPost", mutations.create_post_resolver)
mutation.set_field("updatePost", mutations.update_post_resolver)
mutation.set_field("deletePost", mutations.delete_post_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation)#, snake_case_fallback_resolvers)

explorer_html = ExplorerGraphiQL().html(None)


@app.get('/')
def hello():
    return '<html>Use the <a href="graphql">Ariadne GrapiQL endpoint</a></html>'


@app.get("/graphql")
def graphql_playground():
    return explorer_html, 200


@app.post("/graphql")
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code
