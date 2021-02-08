from typing import *
from global_var import db


class JsonifyModel(db.Model):
    __abstract__ = True

    def jsonify(self, parameters: Union[List[str], str]) -> Dict:
        if isinstance(parameters, str) and parameters.lower() == 'all':
            parameters: Iterable[str] = filter(self._is_inner_name, dir(self))
        return {
            parameter: self.__getattribute__(parameter)
            for parameter in parameters
        }

    def _is_inner_name(self, attr_name: str):
        inner = {'query_class', 'query'}
        if attr_name in inner or attr_name.startswith('_'):
            return False
        attr = self.__getattribute__(attr_name)
        if isinstance(attr, Callable):
            return False
        return True
