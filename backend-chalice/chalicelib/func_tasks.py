import copy
import uuid

from chalicelib.common_modules import common_func
from chalicelib.common_modules.const import const
from chalicelib.common_modules.entity.task import Task


def main(params: dict) -> dict:
    try:
        headers: dict = params[const.headers]
        id_token: str = headers.get(const.authorization)

        if not id_token:
            common_func.no_authorization_header()

        payload = common_func.decode_id_token(id_token)

        if not payload.get(const.team_id):
            err_params = {
                const.exception: f"no permissions: no {const.team_id}",
                const.status_code: 403,
            }
            raise Exception(err_params)

        user_id = payload[const.user_id]
        team_id = payload[const.team_id]

        params.update({
            const.user_id: user_id,
            const.team_id: team_id,
        })

        res = None
        status_code = 200

        method = params[const.method]

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
        task_id: str = query_params.get(const.task_id)
        team_id: str = params[const.team_id]

        if not db_client:
            db_client = common_func.dynamodb_client(const.tasks_backapp)

        Key = common_func.get_dynamodb_key()

        if task_id:
            result = db_client.query(
                KeyConditionExpression=Key(const.team_id).eq(team_id) & Key(const.task_id).eq(task_id)
            )
            rows: list[dict] = result.get("Items", [])

        else:
            result: dict = db_client.query(
                KeyConditionExpression=Key(const.team_id).eq(team_id)
            )
            rows: list[dict] = result.get("Items", [])

        rows = [Task(**i).to_dict() for i in rows]
        rows = sorted(rows, key=lambda x: x[const.limit])

        return {const.contents: rows}

    except Exception as e:
        raise e


def post(params: dict) -> dict:
    try:
        body: dict = params[const.body]
        content = Task(
            task_id=str(uuid.uuid4()),
            team_id=params[const.team_id],
            user_id=body.get(const.user_id),
            task=body.get(const.task),
            detail=body.get(const.detail),
            status=body.get(const.status),
            limit=body.get(const.limit),
        )
        content.validation()

        db_client = common_func.dynamodb_client(const.tasks_backapp)
        db_client.put_item(Item=content.to_dict())

        return content.to_dict()

    except Exception as e:
        raise e


def put(params: dict) -> dict:
    try:
        body: dict = params[const.body]
        query_params: dict = params[const.query_params]

        if not query_params.get(const.task_id):
            err_params = {
                const.exception: f"not provide {const.task_id}",
                const.status_code: 400,
            }
            raise Exception(err_params)

        db_client = common_func.dynamodb_client(const.tasks_backapp)

        r_params = copy.deepcopy(params)
        row = get(r_params, db_client)

        if len(row[const.contents]) == 0:
            err_params = {
                const.exception: f"not found {query_params[const.task_id]}",
                const.status_code: 404,
            }
            raise Exception(err_params)

        task_item = row[const.contents][0]
        task = Task(**task_item)

        if body.get(const.user_id):
            task.user_id = body[const.user_id]
        if body.get(const.task):
            task.task = body[const.task]
        if body.get(const.detail):
            task.detail = body[const.detail]
        if body.get(const.status):
            task.status = body[const.status]
        if body.get(const.limit):
            task.limit = body[const.limit]

        task.validation()

        db_client.update_item(
            Key={const.task_id: task.task_id, const.team_id: task.team_id},
            UpdateExpression='set #task = :task, #detail = :detail, #user_id = :user_id, #status = :status, #limit = :limit',
            ExpressionAttributeNames={
                '#task': 'task',
                '#detail': 'detail',
                '#user_id': 'user_id',
                '#status': 'status',
                '#limit': 'limit',
            },
            ExpressionAttributeValues={
                ':task': task.task,
                ':detail': task.detail,
                ':user_id': task.user_id,
                ':status': task.status,
                ':limit': task.limit,
            }
        )

        return task.to_dict()

    except Exception as e:
        raise e


def delete(params: dict) -> dict:
    try:
        query_params: dict = params[const.query_params]

        if not query_params.get(const.task_id):
            err_params = {
                const.exception: f"not provide {const.task_id}",
                const.status_code: 400,
            }
            raise Exception(err_params)

        content = Task(
            task_id=query_params[const.task_id],
            team_id=params[const.team_id],
        )

        db_client = common_func.dynamodb_client(const.tasks_backapp)

        r_params = copy.deepcopy(params)
        r_params[const.query_params].update({const.task_id: content.task_id})
        row = get(r_params, db_client)

        if len(row[const.contents]) == 0:
            err_params = {
                const.exception: f"not found {content.task_id}",
                const.status_code: 404,
            }
            raise Exception(err_params)

        db_client.delete_item(Key={const.task_id: content.task_id, const.team_id: content.team_id})

        pre_content = row[const.contents][0]
        content.task = pre_content[const.task]
        content.detail = pre_content[const.detail]
        content.status = pre_content[const.status]
        content.limit = pre_content[const.limit]
        return content.to_dict()

    except Exception as e:
        raise e


def delete_tasks(team_id: str, db_client=None) -> None:
    try:
        if not db_client:
            db_client = common_func.dynamodb_client(const.tasks_backapp)

        params = {
            const.team_id: team_id,
            const.query_params: {},
        }

        tasks = get(params, db_client)[const.contents]
        for i in tasks:
            db_client.delete_item(Key={const.team_id: team_id, const.task_id: i[const.task_id]})

    except Exception as e:
        raise e
