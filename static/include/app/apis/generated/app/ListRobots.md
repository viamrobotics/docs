### ListRobots

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of all robots under the specified location.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the location to retrieve the robots from. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- [(List[viam.proto.app.Robot])](INSERT RETURN TYPE LINK): The list of robots.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_robots).

``` python {class="line-numbers linkable-line-numbers"}
list_of_machines = await cloud.list_robots(location_id="123ab12345")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listRobots.html).

{{% /tab %}}
{{< /tabs >}}
