`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies (except for FUSE, which is required by the AppImage format).

To install `viam-server` on a Linux computer:

1. Install FUSE version 2 if it is not already installed on your Linux system.
   For example, on Ubuntu (including Raspberry Pi OS), run the following commands:

   ```sh {class="command-line" data-prompt="$"}
   sudo add-apt-repository universe
   sudo apt install libfuse2
   ```

   **Do not** install the `fuse` package (that is, without a version number).
   Only install the `libfuse2` package.

   For other linux distributions, or for more information, see [FUSE troubleshooting](/appendix/troubleshooting/#appimages-require-fuse-to-run).

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Linux (Aarch64)` or `Linux (x86_64)` for the appropriate **Architecture** for your computer.
   On most Linux operating systems, you can run `uname -m` to confirm your computer's architecture.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your Linux computer.

2. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/installation/manage/) if desired.
