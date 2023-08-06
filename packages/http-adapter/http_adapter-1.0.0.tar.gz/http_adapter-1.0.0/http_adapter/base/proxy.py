# -*- coding: utf-8 -*-

import logging

from requests.models import Response
from requests import get, post, put, delete

NORMAL_REQUEST_CODE = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
                       300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310]
BAD_REQUEST_CODE = [400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]

EXCEPTION_REQUEST_CODE = [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512]

logger = logging.getLogger(__name__)


class HttpProxy:

    def __init__(self, host: str = '127.0.0.1', protocol: str = 'http', port: int = 80):
        self.port = port
        self._url = ''
        self._body = dict()
        self.is_auth = False
        self._params = dict()
        self._headers = dict()
        self.host = host.strip()
        self.protocol = protocol.strip()

    def _set_url(self, url_path: str, *args):
        if self.protocol not in ["http", "https"]:
            raise ValueError(
                f"This <{self.protocol}> protocol is not currently supported, Only supports <http, https>")
        url_prefix = f"{self.protocol}://{self.host}"
        if self.port:
            url_prefix = f"{url_prefix}:{self.port}"
        # 如果path中，有传递动参，需要格式化
        if url_path.find("{}") != -1:
            if args:
                url_path = url_path.format(*args)
            else:
                raise ValueError("Missing parameter <args>.")
        self._url = f"{url_prefix}{url_path}"

    @classmethod
    def _get_method(cls, method: str = 'get'):
        if method == "get":
            _method = get
        elif method == "post":
            _method = post
        elif method == "put":
            _method = put
        elif method == "delete":
            _method = delete
        else:
            raise ValueError(f"This <{method}> method is not currently supported, "
                             f"Only supports <get, post, put, delete>.")
        return _method

    @classmethod
    def _kwargs_lowercase(cls, **kwargs) -> dict:
        kwargs = {key.lower(): value for key, value in kwargs.items()}
        return kwargs

    def _add_current_login_user(self, **kwargs):
        kwargs = self._kwargs_lowercase(**kwargs)
        if "current_login_user" in kwargs.keys() or "current-login-user" in kwargs.keys():
            self._headers.update(
                {"current-login-user": kwargs.get("current-login-user") or kwargs.get("current_login_user")})

    def _init_args(self, **kwargs):
        if kwargs:
            kwargs_1 = self._kwargs_lowercase(**kwargs)
            if kwargs_1.get("position"):
                args = kwargs_1.get("args")
                if kwargs_1.get("position") == "params":
                    self._set_params(**args)
                elif kwargs_1.get("position") == "headers":
                    self._set_headers(**args)
                elif kwargs_1.get("position") == "body":
                    self._set_body(**args)
                else:
                    raise ValueError(f"Args position <{kwargs_1.get('position')}> is not currently supported, "
                                     f"Only supports <params, headers, body>.")
            else:
                raise ValueError("Args info missing parameter <position>.")

    def _set_params(self, **kwargs):
        self._add_current_login_user(**kwargs)
        self._params.update(kwargs)

    def _set_body(self, **kwargs):
        self._add_current_login_user(**kwargs)
        self._body.update(kwargs)

    def _set_headers(self, **kwargs):
        self._add_current_login_user(**kwargs)
        self._headers.update(kwargs)

    def get_response(self, url_path: str = '/', method: str = 'get', args_info: dict = None, *args) -> tuple:
        method = self._get_method(method=method)
        self._set_url(url_path=url_path, *args)
        self._init_args(**args_info)
        response = method(self._url, params=self._params, headers=self._headers, json=self._body, verify=False)
        return self._parse_response(response=response)

    def _parse_response(self, response: Response) -> tuple:
        flag = True
        result = dict(code=200101, message="Get data successful。", data=None)
        status_code = response.status_code
        response_json = response.json(encoding='utf-8')
        if status_code in NORMAL_REQUEST_CODE:
            if isinstance(response_json, dict) or isinstance(response_json, list) or isinstance(response_json, str):
                if isinstance(response_json, dict):
                    result_new = self._kwargs_lowercase(**response_json)
                    if "code" in result_new.keys() and "data" in result_new.keys():
                        if str(result_new.get("code")).find("200") != -1:
                            result['data'] = result_new.get("data")
                        else:
                            result['message'] = result_new.get("msg") or result_new.get("message")
                    elif "ret" in result_new.keys() and "data" in result_new.keys():
                        data = result.get("data") if result.get("data") else list()
                        if data:
                            result['data'] = data
                        else:
                            result['message'] = result.get("msg")
                    else:
                        result['data'] = result
                else:
                    result['data'] = response_json
            else:
                raise ValueError(f"<{response_json}> Unparseable data format.")
        else:
            flag = False
            result['message'] = response.raise_for_status()
            if response_json.get("message") or response_json.get("msg"):
                result['message'] = response_json.get("message") or response_json.get("msg")
            if status_code in BAD_REQUEST_CODE:
                result['code'] = 400101
            elif status_code in EXCEPTION_REQUEST_CODE:
                result['code'] = 500101
            else:
                raise ValueError(f"Unparseable http response.")
        return flag, result
