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

        id_token = common_func.generate_jwt(user_id, team_id)

        res = {
            const.id_token: id_token,
            const.user_id: user_id,
            const.team_id: team_id,
        }

        return common_func.response_handler(body=res, status_code=200)

    except Exception as e:
        return common_func.error_handler(e)
