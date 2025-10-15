Install `viam-server` on the computer or single-board computer (SBC) that is directly connected to your hardware (for example sensors, cameras, or motors).

1. Make sure your computer or SBC is powered on and connected to the internet.

1. Create a Viam account on [app.viam.com](https://app.viam.com).
   You can configure and manage devices and data collection in the web UI.

1. Create a new [_{{< glossary_tooltip term_id="machine" text="machine" >}}_](/operate/hello-world/quickstart/#machines) using the **Add machine** button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. On your machine's page, click **View setup instructions**.

1. Select the appropriate architecture for your machine: **Linux / Aarch64**, **Linux / x86_64**, or **Linux / Armv7l**.

   On most Linux operating systems, you can run `uname -m` to confirm your computer's architecture.

   If you selected **Linux / Aarch 64** or **Linux / x86** also select your installation method:

   - `viam-agent` (recommended): installs viam-agent, which will automatically install (and update) viam-server **and** provide additional functionality such as [provisioning](/manage/fleet/provision/setup/) and operating system update configuration.
   - `manual`: installs only `viam-server` on your machine.

1. Follow the instructions on the page to install `viam-server` and connect it to the cloud with your machine’s unique credentials.

1. After you install `viam-server`, a secure connection is automatically established between your machine and Viam.
   When you update your machine's configuration, `viam-server` automatically gets the updates.

   You are ready to [configure supported hardware](/operate/modules/supported-hardware/) on your machine.
