from flask import Response
from werkzeug.exceptions import abort
import requests

def get(url: str) -> Response:
    """
    Fetch the content of the specified url to show the webpage.

    We are using this strategy in dev or to protect the access to the
    documentation
    """
    proxy_response = requests.get(url)

    if 400 <= proxy_response.status_code < 500:
        """
        raise 404 if the fetch content does not exists. This will activate
        the general handler for 404
        """
        abort(404)

    response = Response(proxy_response.content)
    response.headers.set("Content-Type", proxy_response.headers.get("Content-Type"))
    return response
