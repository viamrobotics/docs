### UpdateOrganization

{{< tabs >}}
{{% tab name="Python" %}}

Updates organization details.

**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>) (optional): If provided, updates the org’s name.
- `public_namespace` [(str)](<INSERT PARAM TYPE LINK>) (optional): If provided, sets the org’s namespace if it hasn’t already been set.
- `region` [(str)](<INSERT PARAM TYPE LINK>) (optional): If provided, updates the org’s region.
- `cid` [(str)](<INSERT PARAM TYPE LINK>) (optional): If provided, update’s the org’s CRM ID.


**Returns:**

- [(viam.proto.app.Organization)](INSERT RETURN TYPE LINK): The updated organization.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cid` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `publicNamespace` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `region` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateOrganization.html).

{{% /tab %}}
{{< /tabs >}}
