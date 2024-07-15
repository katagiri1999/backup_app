# File for const

# Create the constant according to the following.
# 1. write in alphabet order.
# 2. hyphen(‐) changes to underbar(_).
# 3. keep the original character size.

class Const:
    __admin = "admin"
    __application_json = "application/json"
    __aud = "aud"
    __authorization = "authorization"
    __authorization_code = "authorization_code"
    __body = "body"
    __client_id = "client_id"
    __client_secret = "client_secret"
    __code = "code"
    __contents = "contents"
    __Content_Type = "Content-Type"
    __DELETE = "DELETE"
    __detail = "detail"
    __exception = "exception"
    __exp = "exp"
    __GET = "GET"
    __Finished = "Finished"
    __grant_type = "grant_type"
    __headers = "headers"
    __iat = "iat"
    __id_token = "id_token"
    __iss = "iss"
    __limit = "limit"
    __method = "method"
    __normal = "normal"
    __path = "path"
    __POST = "POST"
    __Processing = "Processing"
    __PUT = "PUT"
    __query_params = "query_params"
    __redirect_uri = "redirect_uri"
    __request = "request"
    __response = "response"
    __role = "role"
    __status = "status"
    __status_code = "status_code"
    __task = "task"
    __task_id = "task_id"
    __tasks_backapp = "tasks-backapp"
    __team_id = "team_id"
    __team_name = "team_name"
    __teams_backapp = "teams-backapp"
    __Untouched = "Untouched"
    __user_id = "user_id"
    __users_backapp = "users-backapp"

    @property
    def admin(self) -> str:
        return self.__admin

    @property
    def application_json(self) -> str:
        return self.__application_json

    @property
    def aud(self) -> str:
        return self.__aud

    @property
    def authorization(self) -> str:
        return self.__authorization

    @property
    def authorization_code(self) -> str:
        return self.__authorization_code

    @property
    def body(self) -> str:
        return self.__body

    @property
    def client_id(self) -> str:
        return self.__client_id

    @property
    def client_secret(self) -> str:
        return self.__client_secret

    @property
    def code(self) -> str:
        return self.__code

    @property
    def contents(self) -> str:
        return self.__contents

    @property
    def Content_Type(self) -> str:
        return self.__Content_Type

    @property
    def DELETE(self) -> str:
        return self.__DELETE

    @property
    def detail(self) -> str:
        return self.__detail

    @property
    def exception(self) -> str:
        return self.__exception

    @property
    def exp(self) -> str:
        return self.__exp

    @property
    def GET(self) -> str:
        return self.__GET

    @property
    def Finished(self) -> str:
        return self.__Finished

    @property
    def grant_type(self) -> str:
        return self.__grant_type

    @property
    def headers(self) -> str:
        return self.__headers

    @property
    def iat(self) -> str:
        return self.__iat

    @property
    def id_token(self) -> str:
        return self.__id_token

    @property
    def iss(self) -> str:
        return self.__iss

    @property
    def limit(self) -> str:
        return self.__limit

    @property
    def method(self) -> str:
        return self.__method

    @property
    def normal(self) -> str:
        return self.__normal

    @property
    def path(self) -> str:
        return self.__path

    @property
    def POST(self) -> str:
        return self.__POST

    @property
    def Processing(self) -> str:
        return self.__Processing

    @property
    def PUT(self) -> str:
        return self.__PUT

    @property
    def query_params(self) -> str:
        return self.__query_params

    @property
    def redirect_uri(self) -> str:
        return self.__redirect_uri

    @property
    def request(self) -> str:
        return self.__request

    @property
    def response(self) -> str:
        return self.__response

    @property
    def role(self) -> str:
        return self.__role

    @property
    def status(self) -> str:
        return self.__status

    @property
    def status_code(self) -> str:
        return self.__status_code

    @property
    def task(self) -> str:
        return self.__task

    @property
    def task_id(self) -> str:
        return self.__task_id

    @property
    def tasks_backapp(self) -> str:
        return self.__tasks_backapp

    @property
    def team_id(self) -> str:
        return self.__team_id

    @property
    def team_name(self) -> str:
        return self.__team_name

    @property
    def teams_backapp(self) -> str:
        return self.__teams_backapp

    @property
    def Untouched(self) -> str:
        return self.__Untouched

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def users_backapp(self) -> str:
        return self.__users_backapp


const = Const()
