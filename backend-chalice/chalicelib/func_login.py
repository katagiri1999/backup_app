from urllib import parse

import requests

from chalicelib import func_users
from chalicelib.common_modules import common_func, config
from chalicelib.common_modules.const import const


def main(params: dict) -> dict:
    try:
        body: dict = params[const.body]
        authorization_code: str = body.get(const.authorization_code)

        if not authorization_code:
            err_params = {
                const.exception: f"not provide {const.authorization_code}",
                const.status_code: 401,
            }
            raise Exception(err_params)

        # url decode
        authorization_code = parse.unquote(authorization_code)

        user_id = code_to_email(authorization_code)

        id_token = common_func.generate_jwt(user_id, "", "")

        res = {
            const.id_token: id_token,
            const.user_id: user_id,
        }

        return common_func.response_handler(body=res, status_code=200)

    except Exception as e:
        return common_func.error_handler(e)


def code_to_email(authorization_code: str) -> str:
    try:
        TOKEN_ENDPOINT = "https://accounts.google.com/o/oauth2/token"
        USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
        data = {
            const.code: authorization_code,
            const.grant_type: const.authorization_code,
            const.client_id: config.GCP_CLIENT_ID,
            const.client_secret: config.GCP_CLIENT_SECRET,
            const.redirect_uri: config.APP_URL,
        }
        res1 = requests.post(url=TOKEN_ENDPOINT, data=data)

        if res1.status_code != 200:
            err_params = {
                const.exception: f"invalid {const.authorization_code}",
                const.status_code: 401,
            }
            raise Exception(err_params)

        access_token: str = res1.json()["access_token"]
        headers = {const.authorization: f"Bearer {access_token}"}
        res2 = requests.get(USERINFO_ENDPOINT, headers=headers)
        email: str = res2.json()["email"]

        if email != config.ADMIN_EMAIL:
            common_func.mail_2_admin("User Login", f"user login: {email}")

        return email

    except Exception as e:
        raise e
