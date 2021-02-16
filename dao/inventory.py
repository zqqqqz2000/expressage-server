from utils.jsonify_helper import JsonifyModel
from global_var import db
from typing import *
from sqlalchemy import func
from .wi import WI


class Inventory(JsonifyModel):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, index=True, unique=True)
    comment = db.Column(db.String(128))

    @classmethod
    def change_inventory_num(cls, inventory_id: int, warehouse_id: int, number: int):
        wi_query: Optional[WI] = WI.query.filter_by(iid=inventory_id, wid=warehouse_id).first()
        if wi_query:
            if wi_query.number + number < 0:
                raise Exception
            if wi_query.number + number == 0:
                db.session.delete(wi_query)
            else:
                wi_query.number += number
        else:
            if number < 0:
                raise Exception
            wi_new = WI(iid=inventory_id, wid=warehouse_id, number=number)
            db.session.add(wi_new)
        db.session.commit()

    @classmethod
    def get_page(cls, page: int, per_page: int) -> List[Tuple['Inventory', int]]:
        query_in_wi = db.session.query(
            WI.iid,
            func.sum(WI.number).label('total_number')
        ).group_by(WI.iid).subquery()
        left_join_inventory = db.session.query(
            Inventory,
            query_in_wi.c.total_number
        ).join(query_in_wi, isouter=True)
        res: List[Tuple['Inventory', Optional[int]]] = left_join_inventory.paginate(
            page,
            per_page=per_page,
            error_out=False
        ).items
        return [(inv, 0 if num is None else num) for inv, num in res]

    @classmethod
    def len(cls):
        return cls.query.count()
