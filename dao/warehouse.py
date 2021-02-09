from global_var import db
from typing import *

from utils.jsonify_helper import JsonifyModel


class Warehouse(JsonifyModel):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    lng = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120))

    @classmethod
    def get_page(cls, page: int, per_page: int) -> List['Warehouse']:
        return cls.query.paginate(page, per_page=per_page)

    @classmethod
    def len(cls):
        return cls.query.count()
