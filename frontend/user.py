from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, profile_pic):
        self.id = id_
        self.name = name
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], profile_pic=user[2]
        )
        return user

    @staticmethod
    def create(id_, username, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO users (id, name, profile_pic) "
            "VALUES (?, ?, ?)",
            (id_, username, email, profile_pic),
        )
        db.commit()
