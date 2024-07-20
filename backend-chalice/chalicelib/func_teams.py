import copy
import uuid

from chalicelib import func_users
from chalicelib.common_modules import common_func
from chalicelib.common_modules.const import const
from chalicelib.common_modules.entity.team import Team


def main(params: dict) -> dict:
    try:
        headers: dict = params[const.headers]
        id_token: str = headers.get(const.authorization)

        if not id_token:
            common_func.no_authorization_header()

        payload = common_func.decode_id_token(id_token)

        user_id = payload[const.user_id]
        team_id = payload[const.team_id]
        role = payload[const.role]

        params.update({
            const.user_id: user_id,
            const.team_id: team_id,
            const.role: role,
        })

        res = None
        status_code = 200

        method = params[const.method]
        if method in [const.DELETE] and role != const.admin:
            err_params = {
                const.exception: f"no permissions: not {const.admin}",
                const.status_code: 403,
            }
            raise Exception(err_params)

        if method == const.GET:
            res = get(params)
        elif method == const.POST:
            res = post(params)
        elif method == const.DELETE:
            res = delete(params)

        return common_func.response_handler(body=res, status_code=status_code)

    except Exception as e:
        return common_func.error_handler(e)


def get(params: dict, db_client=None) -> dict:
    try:
        query_params: dict = params[const.query_params]
        team_id = query_params.get(const.team_id)
        user_id = params[const.user_id]

        if not db_client:
            db_client = common_func.dynamodb_client(const.teams_backapp)

        Attr = common_func.get_dynamodb_attr()

        users = func_users.get_users(user_id)
        team_ids = [i[const.team_id] for i in users]

        if len(team_ids) == 0:
            return {const.contents: []}

        else:
            result = db_client.scan(
                FilterExpression=Attr(const.team_id).is_in(team_ids)
            )
            rows: list[dict] = result.get("Items", [])
            rows = [Team(**i).to_dict() for i in rows]

            if len(rows) == 0:
                rows = []
            elif team_id:
                rows = [i for i in rows if i[const.team_id] == team_id]
            else:
                rows = sorted(rows, key=lambda x: x[const.team_name])

        return {const.contents: rows}

    except Exception as e:
        raise e


def post(params: dict) -> dict:
    try:
        body: dict = params[const.body]
        user_id = params[const.user_id]

        content = Team(
            team_id=str(uuid.uuid4()),
            team_name=body.get(const.team_name),
        )
        content.validation()

        db_client = common_func.dynamodb_client(const.teams_backapp)
        db_client.put_item(Item=content.to_dict())

        r_params = copy.deepcopy(params)
        r_params.update({
            const.team_id: content.team_id,
            const.body: {
                const.user_id: user_id,
                const.role: const.admin,
            }
        })
        func_users.post(r_params)

        return content.to_dict()

    except Exception as e:
        raise e


def delete(params: dict) -> dict:
    try:
        team_id = params[const.team_id]

        if not team_id:
            err_params = {
                const.exception: f"not provide {const.team_id}",
                const.status_code: 400,
            }
            raise Exception(err_params)

        content = Team(
            team_id=team_id,
        )

        db_client = common_func.dynamodb_client(const.teams_backapp)

        r_params = copy.deepcopy(params)
        r_params.update({
            const.query_params: {
                const.team_id: team_id
            }
        })
        row = get(r_params, db_client)

        if len(row[const.contents]) == 0:
            err_params = {
                const.exception: f"not found {content.team_id}",
                const.status_code: 404,
            }
            raise Exception(err_params)

        db_client.delete_item(Key={const.team_id: content.team_id})

        pre_content = row[const.contents][0]
        content.team_name = pre_content[const.team_name]
        return content.to_dict()

    except Exception as e:
        raise e
