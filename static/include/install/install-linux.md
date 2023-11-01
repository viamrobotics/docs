`viam-server` is distributed for Linux as an AppImage.
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies (except for FUSE, which is required by the AppImage format).

To install `viam-server` on a Linux computer:

1. Determine if FUSE version 2 is installed on your Linux system:

   ```sh {class="command-line" data-prompt="$"}
   find /usr -name libfuse.so.2
   ```

   If the above command does not return a path to the `libfuse.so.2` file, install FUSE version 2 according to your Linux platform:

   - If installing `viam-server` on a Raspberry Pi running Raspberry Pi OS (Debian GNU/Linux 12 bookworm or later), install FUSE version 2 with the following command:

     ```sh {class="command-line" data-prompt="$"}
     sudo apt install libfuse2
     ```

   - If installing `viam-server` on Ubuntu, install FUSE version 2 with the following commands:

     ```sh {class="command-line" data-prompt="$"}
     sudo add-apt-repository universe
     sudo apt install libfuse2
     ```

   - If installing `viam-server` on other Linux distributions, or for more information, see [FUSE troubleshooting](/appendix/troubleshooting/#appimages-require-fuse-to-run).

   **Do not** install the `fuse` package (that is, without a version number).
   `viam-server` requires FUSE version 2 specifically (`libfuse2`).

1. Go to the [Viam app](https://app.viam.com) and add a new robot by providing a name in the **New Robot** field and clicking **Add robot**.
   If this is your first time using the Viam app, you must create an account first.

   ![The 'First Location' page on the Viam app with a new robot name in the New Robot field and the Add robot button next to the field highlighted.](/fleet/app-usage/create-robot.png)

1. On the **Setup** tab, select `Linux (Aarch64)` or `Linux (x86_64)` for the appropriate **Architecture** for your computer.
   On most Linux operating systems, you can run `uname -m` to confirm your computer's architecture.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your Linux computer.

1. Once you have followed the steps on the **Setup** tab, `viam-server` is installed and running.
   Return to the **Setup** page on the Viam app and wait for confirmation that your computer has successfully connected.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/get-started/installation/manage/) if desired.
