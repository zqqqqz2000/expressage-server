from flask import Blueprint
from flask import request
from dao.deliveryman import Deliveryman
from utils.token import generate_token, check_token_role
from typing import *

deliveryman = Blueprint("deliveryman", __name__, url_prefix='/deliveryman')


@deliveryman.route("/login", methods=['POST'])
def login():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    login_res = Deliveryman.try_login(username, password)
    if login_res is False:
        return {'success': False, 'info': '用户名或密码错误'}
    uid, name = login_res
    return {
        'success': True,
        'token': generate_token({'did': str(uid), 'role': 'deliveryman'}),
        'info': f'登录成功，欢迎你，{name}'
    }


@deliveryman.route('/update_position', methods=['POST'])
@check_token_role('deliveryman')
def update_position(token_data: Dict):
    data: Dict = request.get_json(silent=True)
    lng: float = data['lng']
    lat: float = data['lat']
    did: int = token_data['did']
    update_res: bool = Deliveryman.update_position(did, lng, lat)
    if update_res:
        return {'success': True, 'info': '定位更新成功'}
    return {'success': False, 'info': '定位信息更新失败，请重新登录'}
