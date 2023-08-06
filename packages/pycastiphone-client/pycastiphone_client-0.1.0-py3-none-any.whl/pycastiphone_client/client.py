import logging
import requests
import json

from pycastiphone_client import exceptions, helpers


logger = logging.getLogger(__name__)


class Client(object):
    """Client class
    This class manages the HTTP requests and this class only can send a request.
    """

    def __init__(self, token=None):
        self.baseurl = "https://bezeroak.onaro.eus/api"
        self.client_credentials = helpers.getenv_or_fail("CASTIPHONE_CLIENT_ID")
        self.token = token

    def post(self, route, body=None):
        """Send a POST HTTP requests

        Args:
            route (str): String with the route to the endpoint
            body (dict): Dict with the body of the request to send

        Return:
            **response**: Return the response object
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = 'grant_type=client_credentials&client_id={}'.format(self.client_credentials)
        return self._send_request(
            verb="POST",
            url=self._format_url(route),
            payload=body,
            extra_headers=headers,
        )

    def put(self, route, body):
        """Send a PUT HTTP requests

        Args:
            route (str): String with the route to the endpoint
            body (dict): Dict with the body of the request to send

        Return:
            **response**: Return the response object
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.token,
        }
        return self._send_request(
            verb="PUT",
            url=self._format_url(route),
            payload=body,
            extra_headers=headers,
        )

    def _format_url(self, path):
        return "{url}{path_prefix}{path}".format(
            url=self.baseurl, path_prefix="/api", path=path
        )

    def _send_request(self, verb, url, payload, extra_headers={}):
        """send the API request using the *requests.request* method

        Args:
            payload (dict)

        Raises:
            HTTPError:
            ArgumentMissingError

        Returns:
            **requests.Response**: Response received after sending the request.

        .. note::
            Supported HTTP Methods: DELETE, GET, HEAD, PATCH, POST, PUT
        """
        headers = {
            "Accept": "application/json",
        }
        if extra_headers:
            headers.update(extra_headers)

        if headers.get("Content-Type") == "application/json":
            payload = json.dumps(payload)

        logger.info(
            "{verb} {url} \n {body}".format(verb=verb, url=url, body=payload)
        )

        try:
            response = requests.request(
                verb.upper(), url, headers=headers, data=payload
            )

        except Exception as err:
            raise exceptions.HTTPError(err)
        if response.status_code == 500:
            raise exceptions.HTTPError(response.reason)
        if response.status_code not in [200, 201]:
            raise exceptions.NotSuccessfulRequest(response.status_code)
        return response.json()
