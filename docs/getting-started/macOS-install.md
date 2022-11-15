---
title: "Installing Viam Server on macOS"
linkTitle: "Viam Server on macOS"
weight: 10
type: "docs"
description: "How to install and run viam-server on macOS and sync a machine with the Viam app ([https://app.viam.com](https://app.viam.com))"
# SME: James
---
`viam-server` is available for macOS users via [Homebrew](https://docs.brew.sh).
You should install `viam-server` on your Mac if you are using a Mac as the basis for your robot.
If your robot runs a Linux-based OS, then be sure to follow the [installing Viam Server on Linux](../linux-install/) guide.

## How to install viam-server using Homebrew

In short, you must ensure that you have Homebrew installed and go to the **SETUP** page of your robot on the [Viam app](https://app.viam.com). There you will find setup instructions that are auto-populated with your robot's unique ID. Let's explore the installation process in detail:

Before you proceed, ensure that you have Homebrew installed ([https://docs.brew.sh/Installation](https://docs.brew.sh/Installation)) and add `viamrobotics` to Homebrew.

1. **Install viam-server on your Mac**

```bash
brew tap viamrobotics/brews && brew install viam-server
```

2.  **Download viam-server config to your Mac.** This config file tells the robot where to look on app.viam.com to pull its configuration information and allows you to monitor and control your robot from the Viam app.
You can download your robot's config file from the **SETUP** tab of your robot on the Viam app.

3.  **Start viam-server on your Mac.** Run viam-server locally on your Mac with the config you just downloaded. Be sure that you replace `<YOUR_ROBOT_NAME>` with the name of your robot from the Viam app.

```bash
viam-server -config ~/Downloads/viam-<YOUR_ROBOT_NAME>-main.json
```

4.  **Connect and configure.** Go to the **SETUP** page on the Viam app and wait for confirmation that your robot has successfully connected.

## How to run viam-server as a service on macOS

Installing `viam-server` as a system service is not recommended for most use cases on macOS.
However, if you are looking to create a robot that runs on macOS and you want it to run `viam-server` every time your OS boots up, then you will need to run `viam-server` as a service.
Once you have `viam-server` downloaded locally from Homebrew, you will need to run:

```bash
brew services start viam-server
```

You can stop the `viam-server` service with:

```bash
brew services stop viam-server
```

Or restart the `viam-server` service with:

```bash
brew services restart viam-server
```

## How to update viam-server using Homebrew on macOS

You can upgrade to the latest version of `viam-server` using Homebrew.

```bash
brew upgrade viam-server
```

## How to troubleshoot viam-server on macOS

If you have already successfully connected `viam-server` to the Viam app, you can find all the `viam-server` logs on the **LOGS** tab of the Viam app.

You can also read viam-server's log files locally.

```bash
cat $(brew --prefix)/var/log/viam.log
```
