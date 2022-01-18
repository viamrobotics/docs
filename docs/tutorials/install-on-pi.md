---
title: Install VIAM on Raspberry Pi
summary: Instructions for getting the viam-server binary up and running on a fresh Raspberry Pi.
authors:
    - Matt Dannenberg
date: 2022-01-18
---
# Installing Viam RDK Server on Raspberry Pi

Before installing the Viam RDK, you’ll need a Raspberry Pi running a 64-bit linux distribution. If you do not have linux installed on your Raspberry Pi, skip ahead to [Installing Raspian on the Raspberry Pi](install-on-pi.md#installing-raspian-on-the-raspberry-pi). If you already have a Raspberry Pi with linux installed on it, check if the linux installation on your Raspberry Pi is 64-bit. First, `ssh` into your pi and then run `lscpu`. Example output:
![lscpu-output](img/lscpu-output.png)
If the line of output which reads “Architecture:     <value>” has a value which ends in 64, skip ahead to [Installing viam-server](install-on-pi.md#installing-viam-server). Otherwise continue to [Installing Raspian on the Raspberry Pi](install-on-pi.md#installing-raspian-on-the-raspberry-pi).

# Installing Raspian on the Raspberry Pi
A Raspberry Pi boots from a microSD card. Our first step is to set up a linux installation on that microSD card. 

Since we need a 64-bit version of linux, you’ll need to download the raspberry pi OS 64-bit beta image [here](https://downloads.raspberrypi.org/raspios_lite_arm64/images/).
![top-level-64-bit](img/top-level-64-bit.png)

Select and click on the most recent folder listed:
![single-version-64-bit](img/single-version-64-bit.png)


Now that you've got the viam-server running, why not plug it into a Yahboom 4WD Rover and set that up by following [these instructions](yahboom-rover.md)?
