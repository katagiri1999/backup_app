from test.common import id_token, id_token_no_admin, id_token_no_team, printer

import pytest

import test_config
from chalicelib import func_login, func_refresh
from chalicelib.common_modules.const import const

WHITE = test_config.WHITE
RED = test_config.RED
USER_ID = test_config.USER_ID
TEAM_ID = test_config.TEAM_ID


def test_login_error1():
    print(f"\n{RED}--- invalid code, redirect_uri ---{WHITE}")
    params = {
        const.headers: {const.Content_Type: const.application_json},
        const.body: {
            const.authorization_code: "hogehoge",
            const.redirect_uri: "hogehoge"
        },
    }
    res = func_login.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_login_error2():
    print(f"\n{RED}--- invalid code, redirect_uri ---{WHITE}")
    params = {
        const.headers: {const.Content_Type: const.application_json},
        const.body: {},
    }
    res = func_login.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_refresh1(id_token):
    print(f"\n{RED}--- refresh ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.body: {}
    }
    res = func_refresh.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_refresh2(id_token_no_team):
    print(f"\n{RED}--- refresh ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_team,
        },
        const.body: {
            const.team_id: TEAM_ID
        }
    }
    res = func_refresh.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_refresh_error1():
    print(f"\n{RED}--- refresh (invalid team_id) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: "hogehoge",
        }
    }
    res = func_refresh.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_refresh_error2():
    print(f"\n{RED}--- refresh (invalid token) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: "hogehoge",
        }
    }
    res = func_refresh.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_refresh_error3():
    print(f"\n{RED}--- refresh (no token) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: "",
        }
    }
    res = func_refresh.main(params)
    printer(res)
    assert res["status_code"] == 401


if __name__ == "__main__":
    pytest.main()
