import copy

from chalicelib import func_users
from chalicelib.common_modules import common_func
from chalicelib.common_modules.const import const


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

        body: dict = params[const.body]
        if body.get(const.team_id):
            r_params = copy.deepcopy(params)
            r_params.update({
                const.team_id: body[const.team_id],
                const.query_params: {const.user_id: user_id},
            })
            users = func_users.get(r_params)[const.contents]

            if len(users) == 0:
                err_params = {
                    const.exception: f"invalid {const.team_id}",
                    const.status_code: 401,
                }
                raise Exception(err_params)

            team_id = users[0][const.team_id]
            role = users[0][const.role]

        id_token = common_func.generate_jwt(user_id, team_id, role)

        res = {
            const.id_token: id_token,
            const.user_id: user_id,
            const.team_id: team_id,
            const.role: role,
        }

        return common_func.response_handler(body=res, status_code=200)

    except Exception as e:
        return common_func.error_handler(e)
