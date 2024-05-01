### DeleteOrganizationMember

{{< tabs >}}
{{% tab name="Python" %}}

Remove a member from the organization.

**Parameters:**

- `user_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The ID of the user to remove.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_member).

``` python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await cloud.list_organization_members()
first_user_id = member_list[0].user_id

await cloud.delete_organization_member(first_user_id)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `userId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteOrganizationMember.html).

{{% /tab %}}
{{< /tabs >}}
