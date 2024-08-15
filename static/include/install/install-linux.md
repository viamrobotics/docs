`viam-server` is distributed for Linux as an AppImage.
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies (except for FUSE, which is required by the AppImage format).

To install `viam-server` on a Linux computer:

1. Go to the [Viam app](https://app.viam.com). Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly created machine](/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions.

1. Select the appropriate architecture for your machine: **Linux (Aarch64)**, **Linux (x86_64)**, or **Armv7l**.
   On most Linux operating systems, you can run `uname -m` to confirm your computer's architecture.

1. Select **RDK** as your RDK type.

1. Follow the steps shown to install `viam-server` on your Linux computer.

1. Once you have followed the steps on the setup instructions, `viam-server` is installed and running.
   Wait for confirmation that your machine has successfully connected.

   On your machine's page on [the Viam app](https://app.viam.com), your machine will show that it's **Live**.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/installation/manage-viam-server/) if desired.
