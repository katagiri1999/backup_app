import hashlib
import smtplib
import time
import traceback
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

import boto3
import jwt
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import DynamoDBServiceResource

from chalicelib.common_modules import config
from chalicelib.common_modules.const import const


def error_handler(e: Exception) -> dict:
    try:
        args = e.args[0]

        status_code = None
        params = {}

        if type(args) is dict and args.get(const.status_code):
            # Expected Errors
            status_code = args[const.status_code]
            params.update({const.exception: args.get(const.exception)})

        else:
            # Unexpected error (internal error)
            status_code = 500
            traceback_str = traceback.format_exc()
            params.update({const.exception: traceback_str})

            title = "Fatal Error (From back-app)"
            text = traceback_str
            mail_2_admin(title, text)

        return response_handler(body=params, status_code=status_code)

    except Exception as e:
        raise e


def response_handler(body: dict, status_code: int = 200) -> dict:
    try:
        headers = {const.Content_Type: const.application_json}

        return {
            const.headers: headers,
            const.status_code: status_code,
            const.body: body,
        }

    except Exception as e:
        raise e


def jwt_key() -> str:
    try:
        base = datetime.utcnow().strftime("%Y%m%d")
        key = hashlib.sha256(base.encode()).hexdigest()
        return f"{config.JWT_KEY}{key}"

    except Exception as e:
        raise e


def generate_jwt(user_id: str, team_id: str = "") -> str:
    try:
        claim = {
            const.user_id: user_id,
            const.team_id: team_id,
            const.iss: config.APP_URL,
            const.aud: config.APP_URL,
            const.iat: int(time.time()),
            const.exp: int(time.time()) + 1800,
        }

        str_jwt = jwt.encode(
            payload=claim,
            key=jwt_key(),
            algorithm="HS256",
        )
        return str_jwt

    except Exception as e:
        raise e


def decode_id_token(id_token: str) -> dict:
    # decode id token
    try:
        try:
            json_payload: dict = jwt.decode(
                jwt=id_token,
                key=jwt_key(),
                algorithms="HS256",
                audience=config.APP_URL,
                issuer=config.APP_URL,
                verify=True,
            )

            return json_payload

        except jwt.ExpiredSignatureError:
            err_params = {
                const.exception: f"{const.id_token} is expired",
                const.status_code: 401,
            }
            raise Exception(err_params)

        except Exception:
            err_params = {
                const.exception: f"invalid {const.id_token}",
                const.status_code: 401,
            }
            raise Exception(err_params)

    except Exception as e:
        raise e


def no_authorization_header() -> Exception:
    try:
        err_params = {
            const.exception: f"not provide {const.id_token}",
            const.status_code: 401,
        }
        raise Exception(err_params)

    except Exception as e:
        raise e


def dynamodb_client(table_name):
    try:
        dynamodb: DynamoDBServiceResource = boto3.resource(service_name="dynamodb")

        return dynamodb.Table(table_name)

    except Exception as e:
        raise e


def get_dynamodb_key() -> Key:
    return Key


def send_mail(title: str, text: str, dest: str) -> None:
    try:
        jp_tz = timezone(timedelta(hours=9))
        now_str = datetime.now(jp_tz).strftime("%Y/%m/%d %H:%M:%S")
        subject = f"{title} {now_str}"

        text = text.replace("\n", "<br>")
        html = f'''
        <html>
        <head>
            <style>.text {{border-style: outset; padding: 3%}}</style>
        </head>
        <body>
            <h1><i>{subject}</i></h1>
            <hr><br>
            <b><i>Message From back-app</i></b>
            <p class="text">{text}</p>
            <br><hr><br>
            <b><i>※ Please do not reply directly to this email.</i></b>
        </body>
        </html>
        '''

        FROM = "backapp2024@gmail.com"
        PW = "ukhm rkcc oppv zibd"
        TO = FROM

        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.starttls()
        smtpobj.login(FROM, PW)

        msg = MIMEText(html, "html")
        msg['Subject'] = subject
        msg['To'] = TO
        msg['Bcc'] = dest

        smtpobj.send_message(msg)
        smtpobj.close()

    except Exception as e:
        raise e


def mail_2_admin(title: str, text: str) -> None:
    try:
        send_mail(title, text, config.ADMIN_EMAIL)

    except Exception as e:
        raise e
