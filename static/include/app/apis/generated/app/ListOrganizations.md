### ListOrganizations

{{< tabs >}}
{{% tab name="Python" %}}

List the organization(s) the user is an authorized owner of.

**Parameters:**

- None.

**Returns:**

- [(List[viam.proto.app.Organization])](INSERT RETURN TYPE LINK): The list of organizations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organizations).

``` python {class="line-numbers linkable-line-numbers"}
org_list = await cloud.list_organizations()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**


**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listOrganizations.html).

{{% /tab %}}
{{< /tabs >}}
