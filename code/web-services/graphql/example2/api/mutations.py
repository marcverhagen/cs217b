from datetime import date

import sqlalchemy

from api import db
from api.models import Post


def create_post_resolver(obj, info, title, description):
    try:
        today = date.today()
        post = Post(title=title, description=description, created_at=today)
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


def delete_posts_resolver(obj, info, title):
    try:
        posts = Post.query.filter_by(title=title).all()
        for post in posts:
            db.session.delete(post)
        db.session.commit()
        return {"success": True, "message": f"Deleted {len(posts)} posts"}
    except Exception:
        return {
            "success": False,
            "errors": ["Something went wrong"] }
