from test.common import id_token, id_token_no_admin, id_token_no_team, printer

import pytest

import test_config
from chalicelib import func_teams
from chalicelib.common_modules import common_func
from chalicelib.common_modules.const import const

WHITE = test_config.WHITE
RED = test_config.RED
USER_ID = test_config.USER_ID
TEAM_ID = test_config.TEAM_ID


def test_teams_get1(id_token):
    print(f"\n{RED}--- get teams ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.GET,
        const.query_params: {},
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_teams_get2(id_token_no_admin):
    print(f"\n{RED}--- get teams (no admin) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_admin,
        },
        const.method: const.GET,
        const.query_params: {},
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_teams_get3(id_token):
    print(f"\n{RED}--- get teams ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.GET,
        const.query_params: {const.team_id: TEAM_ID},
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_teams_get4(id_token_no_admin):
    print(f"\n{RED}--- get teams (no exist) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_admin,
        },
        const.method: const.GET,
        const.query_params: {const.team_id: "hogehoge"},
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_teams_get_error1():
    print(f"\n{RED}--- get teams (no token) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: "",
        },
        const.method: const.GET,
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_teams_get_error2():
    print(f"\n{RED}--- get teams (invalid token) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: "hogehoge",
        },
        const.method: const.GET,
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_teams_post1(id_token):
    print(f"\n{RED}--- post teams ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.body: {
            const.team_name: "temp_team"
        }
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_teams_post_error1(id_token):
    print(f"\n{RED}--- post teams ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.body: {
            const.team_name: ""
        }
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_teams_put1(id_token):
    print(f"\n{RED}--- put teams ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.body: {
            const.team_name: "test1"
        }
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_teams_put_error1(id_token):
    print(f"\n{RED}--- put teams (invalid team_name) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.body: {
            const.team_name: ""
        }
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_teams_put_error2(id_token_no_admin):
    print(f"\n{RED}--- put teams (not admin) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_admin,
        },
        const.method: const.PUT,
        const.query_params: {const.team_id: TEAM_ID},
        const.body: {
            const.team_name: "test1"
        }
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 403


def test_teams_delete1(id_token):
    print(f"\n{RED}--- delete teams ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.body: {
            const.team_name: "temp_team"
        }
    }
    team_id = func_teams.main(params)[const.body][const.team_id]

    id_token = common_func.generate_jwt(USER_ID, team_id, const.admin)

    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.DELETE,
        const.query_params: {const.team_id: team_id},
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_teams_delete_error1(id_token_no_admin):
    print(f"\n{RED}--- delete teams (not admin) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_admin,
        },
        const.method: const.DELETE,
    }
    res = func_teams.main(params)
    printer(res)
    assert res["status_code"] == 403


if __name__ == "__main__":
    pytest.main()
