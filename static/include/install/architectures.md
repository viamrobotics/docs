{{< tabs name="different-architectures" >}}
   {{% tab name="Aarch64"%}}

   ```bash
   curl http://packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage -o viam-server && chmod 755 viam-server && sudo ./viam-server --aix-install
   ```

   You can also use the latest version with [http://packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage](http://packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage).

   {{% /tab %}}
   {{% tab name="X86_64"%}}

   ```bash
   curl http://packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage -o viam-server && chmod 755 viam-server && sudo ./viam-server --aix-install
   ```

   You can also use the latest version with [http://packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage](http://packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage).

  {{% /tab %}}
{{< /tabs >}}