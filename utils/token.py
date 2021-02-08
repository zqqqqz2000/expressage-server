from typing import *
from global_var import s


def get_token_data(token: Dict) -> Union[Dict, bool]:
    try:
        data = s.loads(token)
    except Exception:
        return False
    return data


def generate_token(context: Dict):
    return s.dumps(context).decode("ascii")
