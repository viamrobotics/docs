### ListAuthorizations

{{< tabs >}}
{{% tab name="Python" %}}

List all authorizations under a specific resource (or resources) within the currently authed-to organization. If no resource IDs are provided, all resource authorizations within the organizations are returned.

**Parameters:**

- `resource_ids` [(List[str])](<INSERT PARAM TYPE LINK>) (optional): IDs of the resources to retrieve authorizations from. If None, defaults to all resources.

**Returns:**

- [(List[viam.proto.app.Authorization])](INSERT RETURN TYPE LINK): The list of authorizations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_authorizations).

``` python {class="line-numbers linkable-line-numbers"}
list_of_auths = await cloud.list_authorizations(
    resource_ids=["1a123456-x1yz-0ab0-a12xyzabc"])
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `resourceIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listAuthorizations.html).

{{% /tab %}}
{{< /tabs >}}
