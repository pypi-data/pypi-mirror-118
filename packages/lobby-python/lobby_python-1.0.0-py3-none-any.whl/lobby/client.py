import requests
import json
from typing import List


class LobbyException(Exception):
    pass


class Lobby:
    """
    This client use Lobby's REST API and can obtain information gathered by the daemon. It can also update runtime labels of the destination instance.
    """
    _proto: str = "http"
    _host: str = "localhost"
    _port: int = 1313
    _token: str = ""

    def __init__(self, host: str = "localhost", port: int = 1313, token: str = "", proto: str = "http") -> None:
        self._host = host
        self._port = port
        self._token = token
        self._proto = proto.lower()

        assert self._port > 0 and self._port < 2**16, "port value is not in the right range"
        assert self._proto in (
            "http", "https"), "protocol can be only http and https"

    def _call(self, method: str, path: str, body: str = "") -> str:
        """
        Generic HTTP call used internally.
        """
        method = method.lower()

        headers = {}
        if self._token:
            headers.update({"Authorization": "Token {}".format(self._token)})

        if method == "get":
            response = requests.get(
                "{}://{}:{}{}".format(self._proto, self._host, self._port, path), headers=headers)
            if response.status_code != 200:
                raise LobbyException(
                    "backend returned error: {}", response.text)
            return response.text
        elif method == "post":
            response = requests.post(
                "{}://{}:{}{}".format(self._proto, self._host, self._port, path), data=body, headers=headers)
            if response.status_code != 200:
                raise LobbyException(
                    "backend returned error: {}", response.text)
            return response.text
        elif method == "delete":
            response = requests.delete(
                "{}://{}:{}{}".format(self._proto, self._host, self._port, path), data=body, headers=headers)
            if response.status_code != 200:
                raise LobbyException(
                    "backend returned error: {}", response.text)
            return response.text
        else:
            raise LobbyException("unknown method {}".format(method))

    def get_discovery(self) -> dict:
        """
        Returns discovery packet of the destination instance.
        """
        body = self._call("get", "/v1/discovery")
        return json.loads(body)

    def get_discoveries(self) -> List[dict]:
        """
        Returns all registered discovery packets.
        """
        body = self._call("get", "/v1/discoveries")
        return json.loads(body)

    def add_labels(self, labels: List[str]) -> str:
        """
        Adds runtime labels to the destination instance. This can't affect the labels 
        added via environment variables or labels added extra files in the config directory.
        """
        return self._call("post", "/v1/labels", "\n".join(labels))

    def delete_labels(self, labels: List[str]) -> str:
        """
        Removes runtime labels from the destination instance. This can't affect the labels 
        added via environment variables or labels added extra files in the config directory.
        """
        return self._call("delete", "/v1/labels", "\n".join(labels))
