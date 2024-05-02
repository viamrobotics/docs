### GetOrganization

{{< tabs >}}
{{% tab name="Python" %}}

Return details about the requested organization.

**Parameters:**

- `org_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the organization to query. If None, defaults to the currently-authed org.

**Returns:**

- [(viam.proto.app.Organization)](INSERT RETURN TYPE LINK): The requested organization.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getOrganization.html).

{{% /tab %}}
{{< /tabs >}}
