import sys
from typing import Union

from .endpoint import Endpoint
from .observer import OptimizationObserver

def ipython_info():
    ip = None
    if 'ipykernel' in sys.modules:
        ip = 'notebook'
    elif 'IPython' in sys.modules:
        ip = 'terminal'
    return ip


def openBrowser(url: str):
    if ipython_info():
        from IPython.display import Javascript, display
        display(Javascript('window.open("{url}");'.format(url=url)))


class BrowserPresenter(OptimizationObserver):
    def __init__(
        self,
        webfrontend_url: str,
    ) -> None:
        self._webfrontend_url = webfrontend_url

    def on_start(self, run_id, *args, **kwargs):
        self.openBrowser(f"run/{run_id}")

    def openBrowser(self, path):
        from urllib.parse import urljoin
        openBrowser(urljoin(self._webfrontend_url, path))

    @classmethod
    def from_endpoint(cls, endpoint: Endpoint):
        host = endpoint.host
        if host.startswith("grpc"):
            www_host = host.replace("grpc", "www")
            return BrowserPresenter(webfrontend_url=f"https://{www_host}:{endpoint.port}")
        elif host == "localhost" and endpoint.port == 9111:
            # development environment
            return BrowserPresenter(webfrontend_url="http://localhost:3000")
        else:
            return None
