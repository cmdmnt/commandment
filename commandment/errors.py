from typing import Optional, Dict
from flask import jsonify


class JSONAPIError(Exception):

    def __init__(self, title: str, status: int = 500, code: Optional[str] = None, detail: Optional[str] = None,
                 source: Optional[Dict[str, str]] = None, meta=None, id=None):
        self.title = title
        self.status = status
        self.code = code
        self.detail = detail
        self.source = source
        self.meta = meta
        self.id = id

    def to_dict(self) -> Dict[str, any]:
        res = {'errors': []}
        error = {'title': self.title, 'status': self.status}
        if self.code is not None:
            error['code'] = self.code

        if self.detail is not None:
            error['detail'] = self.detail

        res['errors'].append(error)
        return res
