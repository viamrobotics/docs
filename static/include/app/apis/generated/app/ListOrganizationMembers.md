### ListOrganizationMembers

{{< tabs >}}
{{% tab name="Python" %}}

List the members and invites of the currently authed-to organization.


**Returns:**

- [(Tuple[List[viam.proto.app.OrganizationMember], List[viam.proto.app.OrganizationInvite]])](INSERT RETURN TYPE LINK): A tuple containing two lists; the first [0] of organization members, and the second [1] of organization invites.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

``` python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await cloud.list_organization_members()

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listOrganizationMembers.html).

{{% /tab %}}
{{< /tabs >}}
