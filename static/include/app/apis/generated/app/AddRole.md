### AddRole

{{< tabs >}}
{{% tab name="Python" %}}

Add a role under the currently authed-to organization.

**Parameters:**

- `identity_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the entity the role belongs to (e.g., a user ID).
- `role` [(Literal[owner] | Literal[operator])](<INSERT PARAM TYPE LINK>) (required): The role to add.
- `resource_type` [(Literal[organization] | Literal[location] | Literal[robot])](<INSERT PARAM TYPE LINK>) (required): Type of the resource to add role to. Must match resource_id.
- `resource_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.add_role).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.add_role(
    identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    role="owner",
    resource_type="location",
    resource_id="111ab12345")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `authorization` [(Authorization)](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/addRole.html).

{{% /tab %}}
{{< /tabs >}}
