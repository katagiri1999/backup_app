import json

import pytest

import test_config
from chalicelib.common_modules import common_func
from chalicelib.common_modules.const import const

WHITE = test_config.WHITE
RED = test_config.RED
USER_ID = test_config.USER_ID
TEAM_ID = test_config.TEAM_ID


def printer(x):
    res = json.dumps(x, indent=2, ensure_ascii=False)
    print(res)


@pytest.fixture()
def id_token():
    return common_func.generate_jwt(USER_ID, TEAM_ID, const.admin)


@pytest.fixture()
def id_token_no_admin():
    return common_func.generate_jwt(USER_ID, TEAM_ID, const.normal)


@pytest.fixture()
def id_token_no_team():
    return common_func.generate_jwt(USER_ID, "", "")
