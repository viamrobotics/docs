### UpdateOrganizationInviteAuthorizations

{{< tabs >}}
{{% tab name="Python" %}}

Update the authorizations attached to an organization invite that has already been created.

**Parameters:**

- `email` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Email of the user the invite was sent to.
- `add_authorizations` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization) (optional): Optional list of authorizations to add to the invite.
- `remove_authorizations` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization) (optional): Optional list of authorizations to remove from the invite.


**Returns:**

- [(viam.proto.app.OrganizationInvite)](INSERT RETURN TYPE LINK): The updated invite.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization_invite_authorizations).

``` python {class="line-numbers linkable-line-numbers"}
from viam.proto.app import Authorization

authorization_to_add = Authorization(
    authorization_type="some type of auth",
    authorization_id="identifier",
    resource_type="abc",
    resource_id="resource-identifier123",
    identity_id="id12345",
    organization_id="org_id_123"
)

update_invite = await cloud.update_organization_invite_authorizations(
    email="notarealemail@viam.com",
    add_authorizations =[authorization_to_add]
)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `addAuthorizations` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)> (required):
- `email` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)> (required):
- `organizationId` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)> (required):
- `removeAuthorizations` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateOrganizationInviteAuthorizations.html).

{{% /tab %}}
{{< /tabs >}}
