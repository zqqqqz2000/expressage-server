from utils.jsonify_helper import JsonifyModel
from global_var import db


class WI(JsonifyModel):
    __tablename__ = 'wi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wid = db.Column(db.Integer, db.ForeignKey('warehouse.id', ondelete="CASCADE"), nullable=False)
    iid = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete="CASCADE"), nullable=False)
    number = db.Column(db.Integer, db.CheckConstraint('number > 0'), nullable=False)
    wi_unique = db.UniqueConstraint(wid, iid)
