The world state store client lives in the `viam.services.worldstatestore` module, with no underscores, even though the service and API are named `world_state_store`. Import it before you create the client:

```python {class="line-numbers linkable-line-numbers"}
from viam.services.worldstatestore import WorldStateStoreClient

worldstatestore = WorldStateStoreClient.from_robot(robot=machine, name="world_state_store")
```
