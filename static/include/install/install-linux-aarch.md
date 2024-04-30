`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies.

To install `viam-server` :

1. Go to the [Viam app](https://app.viam.com) and add a new machine by providing a name in the **New machine** field and clicking **Add machine**.
   If this is your first time using the Viam app, you must create an account first.

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**.
   Click **View setup instructions** to open the setup instructions.
   Select **Linux** as your system's OS, **Aarch64** as your Linux architecture, and **RDK** as the RDK type.

1. Follow the instructions listed to install `viam-server` on your Linux computer.

1. Once you have followed the setup instructions, `viam-server` is installed and running.
   Wait for confirmation that your computer has successfully connected.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/get-started/installation/manage/) if desired.
