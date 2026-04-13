from ariadne import convert_kwargs_to_snake_case

from .models import Post


def listPosts_resolver(obj, info):
    try:
        print('>>> listPosts_resolver')
        print('---', type(obj), obj)
        print('---', type(info), info)
        posts = [post.to_dict() for post in Post.query.all()]
        print('---', posts)
        print(info.field_name)
        return {"success": True, "posts": posts}
    except Exception as error:
        return {"success": False, "errors": [str(error)]}


@convert_kwargs_to_snake_case
def getPost_resolver(obj, info, id):
    try:
        print('>>> listPosts_resolver')
        print('---', type(obj), obj)
        print('---', type(info), info.path.typename, info.field_name)
        print('---', type(id), id)
        post = Post.query.get(id)
        print('---', post)
        return {"success": True, "post": post.to_dict()}
    except Exception as error:
        return {"success": False, "errors": [str(error)]}
