from dao.management import Management
from dao.warehouse import Warehouse
from utils.token import generate_token, with_token
from flask import request, Blueprint
from typing import *
from global_var import db

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
    location: str = data['location']
    lng: float = data['lng']
    lat: float = data['lat']
    warehouse = Warehouse(location=location, lng=lng, lat=lat)
    db.session.add(warehouse)
    db.session.commit()
