from test.common import id_token, id_token_no_admin, id_token_no_team, printer

import pytest

import test_config
from chalicelib import func_users
from chalicelib.common_modules.const import const

WHITE = test_config.WHITE
RED = test_config.RED
USER_ID = test_config.USER_ID
TEAM_ID = test_config.TEAM_ID


def test_users_get1(id_token):
    print(f"\n{RED}--- get users ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.GET,
        const.query_params: {},
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_users_get2(id_token):
    print(f"\n{RED}--- get users ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.GET,
        const.query_params: {const.user_id: USER_ID},
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_users_get3(id_token):
    print(f"\n{RED}--- get users ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.GET,
        const.query_params: {const.user_id: "noexist@gmail.com"},
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_users_get_error1(id_token_no_team):
    print(f"\n{RED}--- get users (no permissions) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_team,
        },
        const.method: const.GET,
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 403


def test_users_post1(id_token):
    print(f"\n{RED}--- post users ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.body: {
            const.user_id: "temp@gmail.com",
            const.role: const.admin,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_users_post_errro1(id_token):
    print(f"\n{RED}--- post users (duplicated user) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.body: {
            const.user_id: "temp@gmail.com",
            const.role: const.admin,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 409


def test_users_post_errro2(id_token):
    print(f"\n{RED}--- post users (invalid params) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.body: {},
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_users_post_errro3(id_token_no_admin):
    print(f"\n{RED}--- post users (no permissions) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_admin,
        },
        const.method: const.POST,
        const.body: {
            const.user_id: USER_ID,
            const.role: const.admin,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 403


def test_users_post_errro4(id_token_no_team):
    print(f"\n{RED}--- post users (no permissions) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_team,
        },
        const.method: const.POST,
        const.body: {
            const.user_id: USER_ID,
            const.role: const.admin,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 403


def test_users_put_1(id_token):
    print(f"\n{RED}--- put users ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.query_params: {const.user_id: "temp@gmail.com"},
        const.body: {
            const.role: const.normal,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_users_put_error1(id_token):
    print(f"\n{RED}--- put users (no exist user) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.query_params: {const.user_id: "noexist@gmail.com"},
        const.body: {
            const.role: const.normal,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 404


def test_users_put_error2(id_token_no_admin):
    print(f"\n{RED}--- put users (no permissions) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_admin,
        },
        const.method: const.PUT,
        const.query_params: {const.user_id: USER_ID},
        const.body: {
            const.role: const.normal,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 403


def test_users_put_error3(id_token_no_team):
    print(f"\n{RED}--- put users (no permissions) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_team,
        },
        const.method: const.PUT,
        const.query_params: {const.user_id: USER_ID},
        const.body: {
            const.role: const.normal,
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 403


def test_users_put_error4(id_token):
    print(f"\n{RED}--- put users (no permissions) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.query_params: {const.user_id: USER_ID},
        const.body: {
            const.role: "hogehoge",
        },
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_users_delete_1(id_token):
    print(f"\n{RED}--- delete users ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.DELETE,
        const.query_params: {const.user_id: "temp@gmail.com"},
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_users_delete_error1(id_token):
    print(f"\n{RED}--- delete users (no exist user) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.DELETE,
        const.query_params: {const.user_id: "noexist@gmail.com"},
    }
    res = func_users.main(params)
    printer(res)
    assert res["status_code"] == 404


if __name__ == "__main__":
    pytest.main()
