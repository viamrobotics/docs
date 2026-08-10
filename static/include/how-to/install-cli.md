{{< tabs >}}
{{% tab name="macOS" %}}

To download the Viam CLI on a macOS computer, install [brew](https://brew.sh/) and run the following commands:

```sh {class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew trust viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Linux aarch64" %}}

On Debian-based distributions (Debian, Ubuntu, Raspberry Pi OS 64-bit), install the Viam CLI from Viam's apt repository so `apt upgrade` keeps it up to date:

```sh {class="command-line" data-prompt="$"}
curl -fsSL https://us-apt.pkg.dev/doc/repo-signing-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/viam.gpg
echo "deb [signed-by=/usr/share/keyrings/viam.gpg] https://us-apt.pkg.dev/projects/static-file-server-310021 viam main" | sudo tee /etc/apt/sources.list.d/viam.list
sudo apt update && sudo apt install viam-cli
```

The package is named `viam-cli`; the installed command is `viam` (a `viam-cli` alias also works).

On other distributions, download the binary directly:

```sh {class="command-line" data-prompt="$"}
sudo curl --compressed -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-arm64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

On Debian-based distributions (Debian, Ubuntu), install the Viam CLI from Viam's apt repository so `apt upgrade` keeps it up to date:

```sh {class="command-line" data-prompt="$"}
curl -fsSL https://us-apt.pkg.dev/doc/repo-signing-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/viam.gpg
echo "deb [signed-by=/usr/share/keyrings/viam.gpg] https://us-apt.pkg.dev/projects/static-file-server-310021 viam main" | sudo tee /etc/apt/sources.list.d/viam.list
sudo apt update && sudo apt install viam-cli
```

The package is named `viam-cli`; the installed command is `viam` (a `viam-cli` alias also works).

On other distributions, download the binary directly:

```sh {class="command-line" data-prompt="$"}
sudo curl --compressed -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="Windows" %}}

[Download the binary](https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-windows-amd64.exe) and run it directly to use the Viam CLI on a Windows computer.

{{% /tab %}}
{{% tab name="Source" %}}

If you have [Go installed](https://go.dev/doc/install), you can build the Viam CLI from source. Clone the repository and build it with `make`:

```sh {class="command-line" data-prompt="$"}
git clone --depth 1 https://github.com/viamrobotics/rdk.git
cd rdk
make cli
sudo cp "bin/$(go env GOOS)-$(go env GOARCH)/viam-cli" /usr/local/bin/viam
```

To confirm `viam` is installed and ready to use, run `viam version` from your terminal.

{{< alert title="Why not `go install`?" color="caution" >}}
The RDK module replaces one of its dependencies, and Go refuses `go install <package>@<version>` for a module carrying replace directives.
{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

For more information see [install the Viam CLI](/cli/).
