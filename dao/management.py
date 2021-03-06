from global_var import db
from typing import *
from hashlib import md5

from utils.jsonify_helper import JsonifyModel


class Management(JsonifyModel):
    __tablename__ = 'management'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)

    @classmethod
    def try_login(cls, username: str, password: str) -> Union[Tuple[int, str], bool]:
        m = md5()
        m.update(password.encode())
        pass_with_hash = m.hexdigest()
        query_res: Management = cls.query.filter_by(
            username=username,
            password=pass_with_hash
        ).first()
        if query_res is None:
            return False
        else:
            return query_res.id, query_res.username
