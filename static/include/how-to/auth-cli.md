{{< tabs >}}
{{% tab name="Personal access token" %}}

```sh {class="command-line" data-prompt="$"}
viam login
```

This will open a new browser window with a prompt to start the authentication process. If a browser window does not open, the CLI will present a URL for you to manually open in your browser. Follow the instructions to complete the authentication process.

{{% /tab %}}
{{% tab name="API key" %}}

Use your organization, location, or machine part API key and corresponding API key ID in the following command:

```sh {class="command-line" data-prompt="$"}
viam login api-key --key-id <api-key-id> --key <organization-api-key-secret>
```

{{% /tab %}}
{{< /tabs >}}
