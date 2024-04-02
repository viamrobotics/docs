{{< tabs name="different-architectures" >}}
{{% tab name="Aarch64"%}}

```sh {class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage -o viam-server && chmod 755 viam-server && sudo ./viam-server --aix-install
```

You can also use the latest version with [https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage](https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage).

{{% /tab %}}
{{% tab name="X86_64"%}}

```sh {class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage -o viam-server && chmod 755 viam-server && sudo ./viam-server --aix-install
```

You can also use the latest version with [https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage](https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage).

{{% /tab %}}
{{< /tabs >}}
