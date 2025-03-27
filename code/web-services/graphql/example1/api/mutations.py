from datetime import date

from ariadne import convert_kwargs_to_snake_case
import sqlalchemy

from api import db
from api.models import Post


@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title, description):
    try:
        today = date.today()
        post = Post(title=title, description=description, created_at=today)
        print('>>>', type(obj), obj)
        print('>>>', type(info), info)
        db.session.add(post)
        db.session.commit()
        return {
            "success": True,
            "post": post.to_dict() }
    except sqlalchemy.exc.StatementError as e:
        return {
            "success": False,
            "errors": [f"StatementError: {e}"] }
    except Exception as e:
        return {
            "success": False,
            "errors": [f"{type(e)}: {e}"] }


@convert_kwargs_to_snake_case
def update_post_resolver(obj, info, id, title, description):
    try:
        post = Post.query.get(id)
        if post:
            post.title = title
            post.description = description
        db.session.add(post)
        db.session.commit()
        return {
            "success": True,
            "post": post.to_dict() }
    except AttributeError:  # todo not found
        return {
            "success": False,
            "errors": ["item matching id {id} not found"] }


@convert_kwargs_to_snake_case
def delete_post_resolver(obj, info, id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return {"success": True, "post": post.to_dict()}
    except AttributeError:
        return {
            "success": False,
            "errors": ["Not found"] }
