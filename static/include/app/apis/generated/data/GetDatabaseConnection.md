### GetDatabaseConnection

{{< tabs >}}
{{% tab name="Python" %}}

Get a connection to access a MongoDB Atlas Data federation instance.

**Parameters:**

- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Organization to retrieve the connection for.


**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The hostname of the federated database.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_database_connection).

``` python {class="line-numbers linkable-line-numbers"}
data_client.get_database_connection(org_id="a12b3c4e-1234-1abc-ab1c-ab1c2d345abc")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/getDatabaseConnection.html).

{{% /tab %}}
{{< /tabs >}}
