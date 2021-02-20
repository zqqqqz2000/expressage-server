from utils.jsonify_helper import JsonifyModel
from global_var import db
from hashlib import md5
from typing import *


class Deliveryman(JsonifyModel):
    __tablename__ = 'deliveryman'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    lng = db.Column(db.Float, nullable=True)
    lat = db.Column(db.Float, nullable=True)

    @classmethod
    def try_login(cls, username: str, password: str) -> Union[Tuple[int, str], bool]:
        m = md5()
        m.update(password.encode())
        pass_with_hash = m.hexdigest()
        query_res: Deliveryman = cls.query.filter_by(
            username=username,
            password=pass_with_hash
        ).first()
        if query_res is None:
            return False
        else:
            return query_res.id, query_res.name

    @classmethod
    def get_page(cls, page: int, per_page: int) -> List['Deliveryman']:
        return cls.query.paginate(page, per_page=per_page, error_out=False).items

    @classmethod
    def len(cls):
        return cls.query.count()

    @classmethod
    def update_position(cls, did: int, lng: float, lat: float) -> bool:
        query_res: Deliveryman = cls.query.filter_by(id=did).first()
        if not query_res:
            return False
        query_res.lat = lat
        query_res.lng = lng
        db.session.commit()
        return True
