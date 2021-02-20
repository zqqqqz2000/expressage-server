from typing import *
from global_var import s
from flask import request


ReqCallback = Callable[[Optional[Dict]], Any]


def get_token_data(token: str) -> Optional[Dict]:
    try:
        data = s.loads(token.encode())
    except Exception:
        return None
    return data


def generate_token(context: Dict):
    return s.dumps(context).decode("ascii")


def with_token(func: ReqCallback) -> ReqCallback:
    def inner_func():
        data = request.get_json(silent=True)
        token = data['token']
        token_data = get_token_data(token)
        if not token_data:
            return {'success': False, 'info': '登录信息失效，清重新登录'}
        return func(token_data)

    inner_func.__name__ = func.__name__

    return inner_func


def check_token_role(role: str) -> Callable[[ReqCallback], ReqCallback]:
    def callback(func: ReqCallback) -> ReqCallback:
        def inner_func():
            data = request.get_json(silent=True)
            token = data['token']
            token_data = get_token_data(token)
            if not token_data:
                return {'success': False, 'info': '登录信息失效，清重新登录'}
            if 'role' not in token_data or token_data['role'] != role:
                return {'success': False, 'info': '身份验证失败，请以准许的身份登录此页面'}
            return func(token_data)

        inner_func.__name__ = func.__name__

        return inner_func
    return callback
