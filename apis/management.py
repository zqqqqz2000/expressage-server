from dao.management import Management
from utils.token import get_token_data
from flask import request, Blueprint

management = Blueprint("management", __name__, url_prefix='/management')


@management.route("/login", methods=['POST'])
def login():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    login_res = Management.try_login(username, password)
    if login_res is False:
        return {'success': False, 'info': '用户名或密码错误'}
    return {'success': True, 'token': get_token_data({'uid': str(login_res)})}
