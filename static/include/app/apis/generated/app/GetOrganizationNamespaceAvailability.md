### GetOrganizationNamespaceAvailability

{{< tabs >}}
{{% tab name="Python" %}}

Check the availability of an organization namespace.

**Parameters:**

- `public_namespace` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Organization namespace to check. Namespaces can only contain lowercase lowercase alphanumeric and dash characters.


**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): True if the provided namespace is available.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_namespace_availability).

``` python {class="line-numbers linkable-line-numbers"}
available = await cloud.get_organization_namespace_availability(
    public_namespace="my-cool-organization")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `publicNamespace` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getOrganizationNamespaceAvailability.html).

{{% /tab %}}
{{< /tabs >}}
