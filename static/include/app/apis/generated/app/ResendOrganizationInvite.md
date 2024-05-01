### ResendOrganizationInvite

{{< tabs >}}
{{% tab name="Python" %}}

Re-sends a pending organization invite email.

**Parameters:**

- `email` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The email address associated with the invite.


**Returns:**

- [(viam.proto.app.OrganizationInvite)](INSERT RETURN TYPE LINK)

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.resend_organization_invite).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.resend_organization_invite("youremail@email.com")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `email` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/resendOrganizationInvite.html).

{{% /tab %}}
{{< /tabs >}}
