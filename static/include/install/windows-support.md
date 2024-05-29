{{% alert title="Windows Support Notice" color="note" %}}

You can install `viam-server` on Windows Subsystem for Linux (WSL) to test your code or machine configuration.
However, WSL itself does not currently support exposing many types of Windows hardware to the embedded Linux kernel in WSL.
This means that some hardware, such as a USB webcam connected to your Windows computer, may not be available to `viam-server` when run in WSL, even though they are fully supported for native Linux systems.

You can absolutely [run Viam SDK code](/build/program/run/#run-code-remotely) on your personal computer with WSL; if you install `viam-server` on a single-board computer running Linux, or [remotely borrow a Try Viam rover](/get-started/try-viam/), you can control hardware with code running on your Windows computer.

{{% /alert %}}
