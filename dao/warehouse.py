from dao.wi import WI
from global_var import db
from typing import *

from utils.jsonify_helper import JsonifyModel


class Warehouse(JsonifyModel):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    lng = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120))
    specific_location = db.Column(db.String(120))

    @classmethod
    def get_page(cls, page: int, per_page: int) -> List['Warehouse']:
        return cls.query.paginate(page, per_page=per_page, error_out=False).items

    @classmethod
    def len(cls):
        return cls.query.count()

    @classmethod
    def get_inventoried_warehouse(cls, iid: int) -> List[Tuple['Warehouse', int]]:
        wi_query = db.session.query(
            WI.wid,
            WI.number.label('number')
        ).filter_by(iid=iid).subquery()
        warehouse_with_num = db.session.query(
            cls,
            wi_query.c.number
        ).join(wi_query, isouter=True).all()
        return [(d[0], 0 if not d[1] else d[1]) for d in warehouse_with_num]
