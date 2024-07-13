import json

import pytest

from chalicelib import func_login, func_refresh, func_tasks
from chalicelib.common_modules import common_func
from chalicelib.common_modules.const import const

WHITE = "\033[39m"
RED = "\033[32m"
USER_ID = "test@gmail.com"
TEAM_ID = "test_team"

def printer(x):
    res = json.dumps(x, indent=2, ensure_ascii=False)
    print(res)


@pytest.fixture()
def id_token():
    return common_func.generate_jwt(USER_ID, TEAM_ID)


@pytest.fixture()
def id_token_no_team():
    return common_func.generate_jwt(USER_ID, "")


def test_login_error1():
    print(f"\n{RED}--- invalid code ---{WHITE}")
    code = "aaa"
    params = {
        const.headers: {const.Content_Type: const.application_json},
        const.body: {const.authorization_code: code},
    }
    res = func_login.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_refresh1(id_token):
    print(f"\n{RED}--- refresh ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        }
    }
    res = func_refresh.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_refresh_error1():
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


def test_refresh_error2():
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


def test_tasks_get1(id_token):
    print(f"\n{RED}--- get tasks ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.GET,
        const.query_params: {},
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_tasks_get_error1():
    print(f"\n{RED}--- get tasks (invalid token) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: "hogehoge",
        },
        const.method: const.GET,
        const.query_params: {},
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_tasks_get_error2():
    print(f"\n{RED}--- get tasks (no token) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: "",
        },
        const.method: const.GET,
        const.query_params: {},
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 401


def test_tasks_get_error3(id_token_no_team):
    print(f"\n{RED}--- get tasks (no team_id) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token_no_team,
        },
        const.method: const.GET,
        const.query_params: {},
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_tasks_post1(id_token):
    print(f"\n{RED}--- post tasks ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.query_params: {},
        const.body: {
            const.task: "test_task",
            const.memo: "memomemo",
            const.status: const.Finished,
            const.limit: "2022/02/02"
        }
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_tasks_post_error2(id_token):
    print(f"\n{RED}--- post tasks (invalid content) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.query_params: {},
        const.body: {
            const.task: "",
            const.memo: "",
            const.status: "",
            const.limit: ""
        }
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_tasks_put1(id_token):
    print(f"\n{RED}--- put tasks ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.query_params: {},
        const.body: {
            const.task: "test_task",
            const.memo: "memomemo",
            const.status: const.Finished,
            const.limit: "2022/02/02"
        }
    }
    task_id = func_tasks.main(params)[const.body][const.task_id]

    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.query_params: {const.task_id: task_id},
        const.body: {
            const.task: "test_task2",
            const.memo: "memomemo",
            const.status: const.Finished,
            const.limit: "2022/02/02"
        }
    }
    task_id = func_tasks.main(params)[const.body][const.task_id]

    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.query_params: {const.task_id: task_id},
        const.body: {
            const.task: "test_task3",
            const.memo: "memomemomemomemo2",
            const.status: const.Processing,
            const.limit: "2022/02/02"
        }
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_tasks_put_error1(id_token):
    print(f"\n{RED}--- put tasks (no content) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.query_params: {const.task_id: "hogehoge"},
        const.body: {
            const.task: "not exist",
            const.memo: "memomemomemomemo",
            const.status: const.Processing,
            const.limit: "2022/02/02"
        }
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 404


def test_tasks_put_error2(id_token):
    print(f"\n{RED}--- put tasks (invalid content) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.query_params: {const.task_id: "hogehoge"},
        const.body: {
            const.task: "",
            const.memo: "",
            const.status: "",
            const.limit: ""
        }
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_tasks_put_error3(id_token):
    print(f"\n{RED}--- put tasks (no query params) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.PUT,
        const.query_params: {const.task_id: ""},
        const.body: {
            const.task: "hogehoge",
            const.memo: "hogehoge",
            const.status: const.Processing,
            const.limit: "2022/02/02"
        }
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 400


def test_tasks_delete1(id_token):
    print(f"\n{RED}--- delete tasks ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.POST,
        const.query_params: {},
        const.body: {
            const.task: "test_task",
            const.memo: "memomemo",
            const.status: const.Finished,
            const.limit: "2022/02/02"
        }
    }
    task_id = func_tasks.main(params)[const.body][const.task_id]

    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.DELETE,
        const.query_params: {const.task_id: task_id},
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 200


def test_tasks_delete_error1(id_token):
    print(f"\n{RED}--- delete tasks (no content) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.DELETE,
        const.query_params: {const.task_id: "hogehoge",},
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 404


def test_tasks_delete_error2(id_token):
    print(f"\n{RED}--- delete tasks (no query params) ---{WHITE}")
    params = {
        const.headers: {
            const.Content_Type: const.application_json,
            const.authorization: id_token,
        },
        const.method: const.DELETE,
        const.query_params: {const.task_id: "",},
    }
    res = func_tasks.main(params)
    printer(res)
    assert res["status_code"] == 400


if __name__ == "__main__":
    pytest.main()
