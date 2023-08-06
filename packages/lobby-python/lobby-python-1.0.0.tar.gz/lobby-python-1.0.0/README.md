# lobby-python

This is a simple wrapper for Lobby's REST API interface that allows to list discovered
servers and their labels and also update labels of the destination instance.

Check [Lobby](https://gitea.ceperka.net/cx/lobby) for more information.

## Example

```python
from lobby import Lobby
import json

lobby = Lobby(host="localhost", port=1313, token="", proto="http")

response = lobby.add_labels(["service:ns", "service:smtp", "service:node", "backup:/srv/apps", "backup:/etc"])
print(response)

response = lobby.delete_labels(["service:node"])
print(response)

response = lobby.get_discovery()
print(json.dumps(response, indent=2))

response = lobby.get_discoveries()
print(json.dumps(response, indent=2))
```
