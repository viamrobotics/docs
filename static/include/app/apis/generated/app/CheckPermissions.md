### CheckPermissions

{{< tabs >}}
{{% tab name="Python" %}}

Checks validity of a list of permissions.

**Parameters:**

- `permissions` [(List[viam.proto.app.AuthorizedPermissions])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.AuthorizedPermissions) (required): the permissions to validate (e.g., “read_organization”, “control_robot”)


**Returns:**

- [(List[viam.proto.app.AuthorizedPermissions])](INSERT RETURN TYPE LINK): The permissions argument, with invalid permissions filtered out.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.check_permissions).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app import AuthorizedPermissions

# Check whether the entity you're currently authenticated to has permission to control and/or
# read logs from robots in the "organization-identifier123" org
permissions = [AuthorizedPermissions(resource_type="organization",
                                     resource_id="organization-identifier123",
                                     permissions=["control_robot",
                                                  "read_robot_logs"])]

filtered_permissions = await cloud.check_permissions(permissions)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `permissions` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[AuthorizedPermissions](https://flutter.viam.dev/viam_protos.app.app/AuthorizedPermissions-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/checkPermissions.html).

{{% /tab %}}
{{< /tabs >}}
