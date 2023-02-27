---
title: "Install viam-server on macOS"
linkTitle: "macOS Install"
weight: 35
type: "docs"
aliases:
    - /getting-started/macos-install/
    - /installation/macos-install/
# SME: James
---
`viam-server` is available for macOS users through [Homebrew](https://docs.brew.sh).
You should install `viam-server` on your Mac if you are using a Mac as the basis for your robot.
If your robot runs a Linux-based OS, then be sure to follow the [installing `viam-server` on Linux](../linux-install/) guide.

## How to install `viam-server`

In short, you must ensure that you have Homebrew installed and go to the **SETUP** page of your robot on the [Viam app](https://app.viam.com).
There you will find setup instructions that are auto-populated with your robot's unique ID.
Let's explore the installation process in detail:

Before you proceed, ensure that you have Homebrew installed ([https://docs.brew.sh/Installation](https://docs.brew.sh/Installation)) and add `viamrobotics` to Homebrew.

1. **Install `viam-server` on your Mac**

   ```bash
   brew tap viamrobotics/brews && brew install viam-server
   ```

2. **Download the Viam app config to your Mac.** This config file tells the robot where to look on app.viam.com to pull its configuration information and allows you to monitor and control your robot from the Viam app.
You can download your robot's config file from the **SETUP** tab of your robot on the Viam app.

3. **Start `viam-server` on your Mac.** Run viam-server locally on your Mac with the config you just downloaded.
   Be sure that you replace `<YOUR_ROBOT_NAME>` with the name of your robot from the Viam app.

   ```bash
   viam-server -config ~/Downloads/viam-<YOUR_ROBOT_NAME>-main.json
   ```

4. **Connect and configure.** Go to the **SETUP** page on the Viam app and wait for confirmation that your robot has successfully connected.

### Next Steps

Continue to our [Managing viam-server Guide](/installation/manage/) to learn about running viam-server.
