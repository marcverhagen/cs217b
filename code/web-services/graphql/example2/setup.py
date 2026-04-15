"""

Setting up the database and loading one post into the table.

"""


from datetime import datetime

from api import app, db
from api.models import Post


with app.app_context():
	db.create_all()
	current_date = datetime.today().date()
	new_post = Post(title="A new morning", description="A new morning details", created_at=current_date)
	db.session.add(new_post)
	db.session.commit()
