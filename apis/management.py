from typing import *
from flask import jsonify
from flask import request, Blueprint
from sqlalchemy.exc import DatabaseError

from dao.inventory import Inventory
from dao.management import Management
from dao.warehouse import Warehouse
from global_var import db
from utils.token import generate_token, with_token

management = Blueprint("management", __name__, url_prefix='/management')


@management.route("/login", methods=['POST'])
def login():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    login_res = Management.try_login(username, password)
    if login_res is False:
        return {'success': False, 'info': '用户名或密码错误'}
    return {'success': True, 'token': generate_token({'uid': str(login_res)}), 'info': '登录成功'}


@management.route("/get_warehouses", methods=['POST'])
@with_token
def get_warehouses(_):
    data: Dict = request.get_json(silent=True)
    page: int = data['page']
    per_page: int = data['per_page']
    columns: List[Warehouse] = Warehouse.get_page(page, per_page)
    total_column = Warehouse.len()
    total_page: int = total_column // per_page + bool(total_column % per_page)
    return {'success': True, 'total_page': total_page, 'columns': [column.jsonify('all') for column in columns]}


@management.route("/add_warehouse", methods=['POST'])
@with_token
def add_warehouse(_):
    data: Dict = request.get_json(silent=True)
    name: str = data['name']
    location: str = data['location']
    lng: float = data['lng']
    lat: float = data['lat']
    specific_location: str = data['specific_location']
    warehouse = Warehouse(
        location=location,
        lng=lng,
        lat=lat,
        name=name,
        specific_location=specific_location
    )
    db.session.add(warehouse)
    try:
        db.session.commit()
    except DatabaseError:
        return {'success': False, 'info': '仓库名称可能重复或未知的数据库错误'}
    return {'success': True, 'info': '添加仓库成功'}


@management.route('/remove_warehouse', methods=['POST'])
@with_token
def remove_warehouse(_):
    data: Dict = request.get_json(silent=True)
    id_: int = data['id']
    query_res: Optional[Warehouse] = Warehouse.query.filter_by(id=id_).first()
    if not query_res:
        return {'success': False, 'info': '删除失败，该仓库不存在或已被删除'}
    db.session.delete(query_res)
    db.session.commit()
    return {'success': True, 'info': '成功删除仓库'}


@management.route('/add_inventory', methods=['POST'])
@with_token
def add_inventory(_):
    data: Dict = request.get_json(silent=True)
    name: str = data['name']
    comment: str = data['comment']
    inventory = Inventory(name=name, comment=comment)
    db.session.add(inventory)
    try:
        db.session.commit()
    except DatabaseError:
        return {'success': False, 'info': '货物名重复'}
    return {'success': True, 'info': '添加货物成功'}


@management.route('/get_inventory', methods=['POST'])
@with_token
def get_inventory(_):
    data: Dict = request.get_json(silent=True)
    page = data['page']
    per_page = data['per_page']
    inventories: List[Tuple[Inventory, int]] = Inventory.get_page(page, per_page)
    total_column = Inventory.len()
    total_page: int = total_column // per_page + bool(total_column % per_page)
    return {
        'total_page': total_page,
        'columns': [
            {
                'id': res[0].id,
                'name': res[0].name,
                'comment': res[0].comment,
                'total_number': res[1]
            }
            for res in inventories
        ]
    }


@management.route('remove_inventory', methods=['POST'])
@with_token
def remove_inventory(_):
    data: Dict = request.get_json(silent=True)
    id_ = data['id']
    inventory_req: Optional[Inventory] = Inventory.query.filter_by(id=id_).first()
    if inventory_req:
        db.session.delete(inventory_req)
        db.session.commit()
        return {'success': True, 'info': '删除货品成功'}
    return {'success': False, 'info': '货品不存在或已被删除'}


@management.route('get_inventory_in_warehouse', methods=['POST'])
@with_token
def get_inventory_in_warehouse(_):
    data: Dict = request.get_json(silent=True)
    id_ = data['id']
    warehouse_with_inventory = Warehouse.get_inventoried_warehouse(id_)
    return jsonify([
        {
            'id': warehouse.id,
            'name': warehouse.name,
            'lng': warehouse.lng,
            'lat': warehouse.lat,
            'number': number
        } for warehouse, number in warehouse_with_inventory
    ])


@management.route('change_inventory_num', methods=['POST'])
@with_token
def change_inventory_num(_):
    data: Dict = request.get_json(silent=True)
    iid: int = data['iid']
    wid: int = data['wid']
    number: int = data['number']
    try:
        Inventory.change_inventory_num(iid, wid, number)
    except Exception:
        return {'success': False, 'info': '库存数量变更失败，请勿使最终库存为负'}
    return {'success': True, 'info': '库存数量变更成功'}
