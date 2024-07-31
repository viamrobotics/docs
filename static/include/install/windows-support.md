{{% alert title="Windows Support Notice" color="note" %}}

You can install `viam-server` on Windows Subsystem for Linux (WSL) to test your code or machine configuration.
However, WSL itself does not currently support exposing many types of Windows hardware to the embedded Linux kernel in WSL.
This means that some hardware, such as a USB webcam connected to your Windows computer, may not be available to `viam-server` when run in WSL, even though it is fully supported for native Linux systems.

Although you cannot access all hardware if you run `viam-server` on your personal computer with WSL, you can [run code to control a machine](/sdks/#run-code) on your personal computer with WSL if you install `viam-server` on a single-board computer running Linux.

{{% /alert %}}
