import copy
import os
from typing import List, Callable, Optional

from flask import Flask

from flask_spaproxy import reverse_proxy


class SpaProxy:

    def __init__(self, app: Flask, view_decorators: Optional[List[Callable]] = None):
        """
        Initialize route to serve frontend application. If FLASK_SPA_PROXY_URL is defined,
        it will set a route that will fetch unknown resource from the url given in input.

        Otherwise, it will use the static_folder to send requested resources.

        :param app: flask web application
        :param view_decorators:
            a list of view decorator that Flask SpaProxy will use over
            the proxy route (login requirement, ...).

            It use similar order evaluation as it would use as decorator on a route method

            >>> @route("hello_world", "/")
            >>> @login_required
            >>> @audit_trail
            >>> def route():
            >>>     return "hello world"

            >>> SpaProxy(webapp, view_decorators=[login_required, audit_trail])
        """
        self._app = app
        self._spa_url = os.getenv('FLASK_SPA_PROXY_URL', None)
        if view_decorators is None:
            view_decorators = []

        if app is not None:
            self.init_app(app, view_decorators)

    def init_app(self, app: Flask, view_decorators: List[Callable]):
        if self._spa_url:
            proxy_route = self._build_decorated_views(self.proxy_route, view_decorators)

            app.add_url_rule('/<path:subpath>', 'spa_proxy', proxy_route)
            app.add_url_rule('/', 'spa_proxy', proxy_route, defaults={"subpath": ""})
        else:
            static_index = self._build_decorated_views(self.static_index, view_decorators)

            app.add_url_rule('/<path:subpath>', 'spa', static_index)
            app.add_url_rule('/', 'spa', static_index, defaults={"subpath": ""})

    def proxy_route(self, subpath: str):
        url = "/".join([self._spa_url, subpath])
        response = reverse_proxy.get(url)
        print(url)
        return response

    def static_index(self, subpath: str):
        if subpath in ["/", ""]:
            return self._app.send_static_file('index.html')

        return self._app.send_static_file(subpath)

    def _build_decorated_views(self, static_index, view_decorators):
        view_decorators = copy.copy(view_decorators)
        view_decorators.reverse()
        for view_decorator in view_decorators:
            static_index = view_decorator(static_index)
        return static_index
