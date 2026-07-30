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

The package is named `viam-cli`; the installed command is `viam`.

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

The package is named `viam-cli`; the installed command is `viam`.

On other distributions, download the binary directly:

```sh {class="command-line" data-prompt="$"}
sudo curl --compressed -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod a+rx /usr/local/bin/viam
```

You can also install the Viam CLI using [brew](https://brew.sh/) on Linux `amd64` (Intel `x86_64`):

```sh {class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew trust viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Windows" %}}

[Download the binary](https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-windows-amd64.exe) and run it directly to use the Viam CLI on a Windows computer.

{{% /tab %}}
{{% tab name="Source" %}}

If you have [Go installed](https://go.dev/doc/install), you can build the Viam CLI directly from source using the `go install` command:

```sh {class="command-line" data-prompt="$"}
go install go.viam.com/rdk/cli/viam@latest
```

To confirm `viam` is installed and ready to use, issue the _viam_ command from your terminal.
If you see help instructions, everything is correctly installed.
If you do not see help instructions, add your local <file>go/bin/\*</file> directory to your `PATH` variable.
If you use `bash` as your shell, you can use the following command:

```sh {class="command-line" data-prompt="$"}
echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
```

{{% /tab %}}
{{< /tabs >}}

For more information see [install the Viam CLI](/cli/).
