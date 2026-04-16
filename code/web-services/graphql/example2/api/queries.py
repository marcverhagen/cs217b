
from .models import Post


def listPosts_resolver(obj, info):
    try:
        posts = [post.to_dict() for post in Post.query.all()]
        return {"success": True, "posts": posts}
    except Exception as error:
        return {"success": False, "errors": [str(error)]}


def getPost_resolver(obj, info, id):
    try:
        post = Post.query.get(id)
        return {"success": True, "post": post.to_dict()}
    except Exception as error:
        return {"success": False, "errors": [str(error)]}
