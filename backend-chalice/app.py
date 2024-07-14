import json

from chalice import Chalice
from chalice.app import Request, Response

from chalicelib import (func_login, func_refresh, func_tasks, func_teams,
                        func_users)
from chalicelib.common_modules.const import const

app = Chalice(app_name='back-app-main')
app.log.setLevel("INFO")


def http_request_handler(params: Request) -> dict:
    try:
        r_params = {
            const.method: params.method.upper(),
            const.path: params.path,
            const.headers: dict(params.headers),
            const.query_params: dict(params.query_params) if params.query_params else {},
            const.body: dict(params.json_body) if params.raw_body else {},
        }
        app.log.info(f"{const.request}: {json.dumps(r_params)}")
        return r_params

    except Exception as e:
        raise e


def http_response_handler(params: dict) -> Response:
    try:
        app.log.info(f"{const.response}: {json.dumps(params)}")
        res = Response(
            body=params[const.body],
            headers=params[const.headers],
            status_code=params[const.status_code]
        )
        return res

    except Exception as e:
        raise e


@app.route("/login", methods=[const.POST], content_types=[const.application_json], cors=True)
def login_api_handler():
    params = http_request_handler(app.current_request)
    res = func_login.main(params)
    return http_response_handler(res)


@app.route("/refresh", methods=[const.POST], content_types=[const.application_json], cors=True)
def session_api_handler():
    params = http_request_handler(app.current_request)
    res = func_refresh.main(params)
    return http_response_handler(res)


@app.route("/tasks", methods=[const.GET, const.POST, const.PUT, const.DELETE], content_types=[const.application_json], cors=True)
def contents_api_handler():
    params = http_request_handler(app.current_request)
    res = func_tasks.main(params)
    return http_response_handler(res)


@app.route("/teams", methods=[const.GET, const.POST, const.PUT, const.DELETE], content_types=[const.application_json], cors=True)
def contents_api_handler():
    params = http_request_handler(app.current_request)
    res = func_teams.main(params)
    return http_response_handler(res)


@app.route("/users", methods=[const.GET, const.POST, const.PUT, const.DELETE], content_types=[const.application_json], cors=True)
def contents_api_handler():
    params = http_request_handler(app.current_request)
    res = func_users.main(params)
    return http_response_handler(res)
