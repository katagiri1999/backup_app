import copy

from chalicelib.common_modules import common_func
from chalicelib.common_modules.const import const
from chalicelib.common_modules.entity.user import User


def main(params: dict) -> dict:
    try:
        headers: dict = params[const.headers]
        id_token: str = headers.get(const.authorization)

        if not id_token:
            common_func.no_authorization_header()

        payload = common_func.decode_id_token(id_token)

        if not payload.get(const.team_id) or not payload.get(const.role):
            err_params = {
                const.exception: f"no permissions: no {const.team_id} or {const.role}",
                const.status_code: 403,
            }
            raise Exception(err_params)

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
        if method in [const.POST, const.PUT, const.DELETE] and role != const.admin:
            err_params = {
                const.exception: f"no permissions: not {const.admin}",
                const.status_code: 403,
            }
            raise Exception(err_params)

        if method == const.GET:
            res = get(params)
        elif method == const.POST:
            res = post(params)
        elif method == const.PUT:
            res = put(params)
        elif method == const.DELETE:
            res = delete(params)

        return common_func.response_handler(body=res, status_code=status_code)

    except Exception as e:
        return common_func.error_handler(e)


def get(params: dict, db_client=None) -> dict:
    try:
        query_params: dict = params[const.query_params]
        user_id: str = query_params.get(const.user_id)
        team_id: str = params[const.team_id]

        if not db_client:
            db_client = common_func.dynamodb_client(const.users_backapp)

        Key = common_func.get_dynamodb_key()

        if user_id:
            result = db_client.query(
                KeyConditionExpression=Key(const.team_id).eq(team_id) & Key(const.user_id).eq(user_id)
            )
            rows: list[dict] = result.get("Items", [])

        else:
            result = db_client.query(
                KeyConditionExpression=Key(const.team_id).eq(team_id)
            )
            rows: list[dict] = result.get("Items", [])

        rows = [User(**i).to_dict() for i in rows]
        rows = sorted(rows, key=lambda x: x[const.user_id])

        return {const.contents: rows}

    except Exception as e:
        raise e


def post(params: dict) -> dict:
    try:
        body: dict = params[const.body]
        team_id: str = params[const.team_id]
        content = User(
            user_id=body.get(const.user_id),
            team_id=team_id,
            role=body.get(const.role),
        )
        content.validation()

        db_client = common_func.dynamodb_client(const.users_backapp)

        r_params = copy.deepcopy(params)
        r_params.update({const.query_params: {const.user_id: content.user_id}})
        row = get(r_params, db_client)

        if len(row[const.contents]) > 0:
            err_params = {
                const.exception: f"duplicated {const.user_id}",
                const.status_code: 409,
            }
            raise Exception(err_params)

        db_client.put_item(Item=content.to_dict())

        return content.to_dict()

    except Exception as e:
        raise e


def put(params: dict) -> dict:
    try:
        body: dict = params[const.body]
        query_params: dict = params[const.query_params]
        team_id: str = params[const.team_id]

        if not query_params.get(const.user_id):
            err_params = {
                const.exception: f"not provide {const.user_id}",
                const.status_code: 400,
            }
            raise Exception(err_params)

        content = User(
            user_id=query_params[const.user_id],
            team_id=team_id,
            role=body.get(const.role),
        )
        content.validation()

        db_client = common_func.dynamodb_client(const.users_backapp)

        r_params = copy.deepcopy(params)
        row = get(r_params, db_client)

        if len(row[const.contents]) == 0:
            err_params = {
                const.exception: f"not found {content.user_id}",
                const.status_code: 404,
            }
            raise Exception(err_params)

        db_client.update_item(
            Key={const.user_id: content.user_id, const.team_id: content.team_id},
            UpdateExpression='set #role = :role',
            ExpressionAttributeNames={
                '#role': 'role',
            },
            ExpressionAttributeValues={
                ':role': content.role,
            }
        )

        return content.to_dict()

    except Exception as e:
        raise e


def delete(params: dict) -> dict:
    try:
        query_params: dict = params[const.query_params]
        team_id: str = params[const.team_id]

        if not query_params.get(const.user_id):
            err_params = {
                const.exception: f"not provide {const.user_id}",
                const.status_code: 400,
            }
            raise Exception(err_params)

        content = User(
            user_id=query_params[const.user_id],
            team_id=team_id,
        )

        db_client = common_func.dynamodb_client(const.users_backapp)

        r_params = copy.deepcopy(params)
        row = get(r_params, db_client)

        if len(row[const.contents]) == 0:
            err_params = {
                const.exception: f"not found {content.user_id}",
                const.status_code: 404,
            }
            raise Exception(err_params)

        db_client.delete_item(Key={const.team_id: content.team_id, const.user_id: content.user_id})

        pre_content = row[const.contents][0]
        content.role = pre_content[const.role]
        return content.to_dict()

    except Exception as e:
        raise e


def get_users(user_id: str, db_client=None) -> list[dict]:
    try:
        Key = common_func.get_dynamodb_key()

        if not db_client:
            db_client = common_func.dynamodb_client(const.users_backapp)

        result = db_client.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key(const.user_id).eq(user_id)
        )

        rows: list[dict] = result.get("Items", [])
        rows = [User(**i).to_dict() for i in rows]
        return rows

    except Exception as e:
        raise e


def delete_users(team_id: str, db_client=None) -> None:
    try:
        if not db_client:
            db_client = common_func.dynamodb_client(const.users_backapp)

        params = {
            const.team_id: team_id,
            const.query_params: {},
        }

        users = get(params, db_client)[const.contents]
        for i in users:
            db_client.delete_item(Key={const.team_id: team_id, const.user_id: i[const.user_id]})

    except Exception as e:
        raise e
