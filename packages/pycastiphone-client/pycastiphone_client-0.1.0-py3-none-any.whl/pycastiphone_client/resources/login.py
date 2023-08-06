from pycastiphone_client.client import Client


class Login:
    _name = "login"
    _url_path = "/login"

    def __init__(
        self,
        access_token,
        token_type,
        **kwargs
    ):
        self.access_token = access_token
        self.token_type = token_type
        self.token = "{} {}".format(token_type, access_token)

    @classmethod
    def authenticate(cls):
        """
        Get auth token
        """
        response_data = Client().post("{}".format(cls._url_path))

        return cls(**response_data)
