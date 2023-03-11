---
title: "Microcontroller Setup: the Micro-RDK"
linkTitle: "Microcontroller Setup"
weight: 50
simple_list: false
type: docs
icon: "img/thumbnails/viam-icon-sdk.png"
# SMEs: Nicolas Menard
---

The micro-RDK is a lightweight version of Viam's [Robot Development Kit](https://github.com/viamrobotics/rdk). The micro-RDK allows you to run a smaller version of `viam-server` on microcontroller resource-limited embedded systems.

The micro-RDK supports:

- Viam app connectivity
- Component control

The only microcontroller the micro-RDK currently supports is the [ESP32](https://www.espressif.com/en/products/socs/esp32).

See [GitHub](https://github.com/viamrobotics/micro-rdk) for code examples and more information about the micro-RDK.

## Getting Started

A guide to getting started with using an [Expressif ESP32 microcontroller](https://www.espressif.com/en/products/socs/esp32) to control your robot with Viam's micro-RDK.

To install the micro-RDK on your Expressif ESP32 microcontroller, you first need to install the ESP-IDF development framework on your development machine.

To establish a connection with the ESP32 board as your new robot, you also need to install Rust, the Rust ESP Toolchain, `cargo-generate`, and `cargo-espflash`, generate a new project from Viam's micro-RDK template, and upload the project to your ESP32.
Then, to program and control your new ESP32 robot, you must configure it as a remote of another robot running `viam-server`.

You need the following hardware to upload a new project on an ESP32 with the micro-RDK:

- An Expressif ESP32 microcontroller.
Viam recommends purchasing the ESP32 with a development board: see development kit options [here](https://www.espressif.com/en/products/devkits).
- A USB-C cable for connecting the ESP32 to your development machine (included with ESP32 DevKits).
- A Micro-USB (recommended, included with ESP32 DevKits), 5V/GND header pin or 3V3/GND header pin power supply.

### Install ESP-IDF

ESP-IDF is the development framework for Espressif SoCs (System-on-Chips), supported on Windows, Linux and macOS.
Start by completing Step 1 of [these instructions](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html), following the appropriate steps for your development machine's architecture, and then return here.

Clone Viam's fork of the ESP-IDF:

``` shell
mkdir -p ~/esp
cd ~/esp
git clone https://github.com/npmenard/esp-idf
cd esp-idf
git checkout v4.4.1
git submodule update --init --recursive
```

Then, install the required tools for ESP-IDF:

``` shell
cd ~/esp/esp-idf
./install.sh esp32
```

To activate ESP-IDF, run the following command to source (`.`) the activation script `export.sh`:

``` shell
. $HOME/esp/esp-idf/export.sh
```

To avoid conflicts with other toolchains, adding this command to your `.bashrc` or `.zshrc` is not recommended.
Save this command to run in any future terminal session where you need to activate the ESP-IDF development framework.

### Install Rust

#### MacOS & Linux

If you don't already have the Rust programming language installed on your development machine, run the following command to download Rustup and install Rust:

``` shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

See [Rust](https://www.rust-lang.org/tools/install) for more information and other installation methods.

### Install the Rust ESP Toolchain and Activate the ESP-RS Virtual Environment

To install the Rust ESP toolchain, run the following command:

``` shell
curl -LO https://github.com/esp-rs/rust-build/releases/download/v1.64.0.0/install-rust-toolchain.sh
chmod a+x install-rust-toolchain.sh
./install-rust-toolchain.sh
```

This command will prompt you to add two variables to your `.zshrc` or `.bashrc` if you want to activate the ESP-RS environment automatically in every terminal session:

``` shell
IMPORTANT!
 The following environment variables need to be updated:
export LIBCLANG_PATH= ...
```

Doing so is not recommended, as this may cause conflicts with other toolchains.
As an alternative, the script prompts you to save the export script `export-esp.sh`.

Run the following command to save `./export-esp.sh` at `$HOME/esp/esp-idf/export-esp-rs.sh`:

``` shell
mv ./export-esp.sh $HOME/esp/esp-idf/export-esp-rs.sh
```

After doing so, run the following command to source (`.`) this file, activating the ESP-RS Virtual Environment:

``` shell
. $HOME/esp/esp-idf/export-esp-rs.sh
```

Save this source command to run in any future terminal session where you need to activate the ESP-RS Virtual Environment.

### Install `cargo-generate` with `cargo`

 `cargo` installs automatically when downloading Rust with Rustup.

If you need to install `cargo`, run the following command, or see the [Rust Documentation](https://doc.rust-lang.org/cargo/getting-started/installation.html) for other installation methods:

``` shell
curl https://sh.rustup.rs -sSf | sh
```

Run the following command to install `cargo-generate`:

``` shell
cargo install cargo-generate
```

### Install or Update `cargo-espflash`

Run the following command to install `cargo-espflash` in Viam's recommended version:

``` shell
cargo install cargo-espflash@2.0.0-rc.1
```

## Your First ESP32 Robot

### Create a New Robot

Navigate to [the Viam app](https://app.viam.com) and create a new robot in your desired location.
Leave your `Mode` and `Architecture` selections at default, and skip the instructions in the **SETUP** tab for now, as `viam-server` instantiation is not supported on the ESP32.

### Generate a New Project from the Micro-RDK Template

Using [this template](https://github.com/viamrobotics/micro-rdk-template.git), create a new micro-RDK project to upload to your ESP32.

Run the following command to generate a new project with `cargo`:

``` shell
cargo generate --git https://github.com/viamrobotics/micro-rdk-template.git
```

If you would like, you can use `mkdir` to initialize a new repository in the directory you created by running `cargo-generate`, to track any changes you make to the generated project.

You will be prompted to paste your Viam robot configuration information (`viam.json`) into the terminal.

To obtain this, navigate to [the Viam app](https://app.viam.com).
Click the **COPY VIAM-SERVER CONFIG** button on the right side of the **SETUP** tab of your robot to copy the text for the config file.
Paste this into your terminal.

{{< alert title="Caution" color="caution" >}}

All of the generated files should be safe to commit as a project on Github, with the exception of `viam.json`, since it contains a secret key.

{{% /alert %}}

### Upload the Project and Connect to your ESP32 Board

Modify the contents of <file>src/main.rs</file> to your liking and run:

``` shell
make upload
```

While running `make upload`, you may be presented with an interactive menu of different serial port options to use to connect to the ESP32 board.
Once you have identified the correct choice for your environment, you may bypass the menu by providing the correct port as a command line argument to future invocations of `make upload`:

``` shell
make ESPFLASH_FLASH_ARGS="-p /dev/cu.usbserial-130" upload
```

If successful, `make upload` will retain a serial connection to the board until `Ctrl-C` is pressed.
To manage this connection, consider running it within a dedicated terminal session, or under `tmux` or `screen`.
While the serial connection is live, you can also restart the currently flashed image with `Ctrl-R`.

If everything went well, your ESP32 will be programmed so that you will be able to see your robot live on [the Viam app](https://app.viam.com).

{{< alert title="Note" color="note" >}}

If you encounter a crash due to stack overflow, you may need to increase the stack available to the main task.

In the generated <file>sdkconfig.defaults</file> set the `CONFIG_ESP_MAIN_TASK_STACK_SIZE` to `32768`. The diff of your changes should look like this:

``` diff
diff --git a/sdkconfig.defaults b/sdkconfig.defaults
index f75b465..2b0ba9c 100644
--- a/sdkconfig.defaults
+++ b/sdkconfig.defaults
@@ -1,5 +1,5 @@
 # Rust often needs a bit of an extra main task stack size compared to C (the default is 3K)
-CONFIG_ESP_MAIN_TASK_STACK_SIZE=24576
+CONFIG_ESP_MAIN_TASK_STACK_SIZE=32768
 CONFIG_ESP_MAIN_TASK_AFFINITY_CPU1=y
 # Use this to set FreeRTOS kernel tick frequency to 1000 Hz (100 Hz by default).
```

{{% /alert %}}

## Program your ESP32 Robot

### Configure the ESP32 as a Remote

To programmatically control the robot now running on the ESP32, you need to connect it to another robot that is running the full-featured `viam-server` software, as the microcontroller lacks the required processing power to do so.
This second "robot" can be as simple as an instance of `viam-server` running on your development machine.

By configuring the ESP32 robot as a remote of a robot running `viam-server`, you can establish a secure connection between the two robots.

Navigate to [the Viam app](https://app.viam.com).
Create and configure a new robot, or select an existing robot that you want to add the ESP32 to.

Add the ESP32-backed robot as a remote of your new or existing robot:

<p style="max-width:800px;"><img src="../img/esp32-setup/esp32-remote-creation.png" alt="Adding the ESP32 as a remote in the Viam app Config builder." ></p>

1. Navigate to the **CONTROL** tab of the robot and copy its `Remote Address`.
2. Navigate to the **CONFIG** tab, select the `Remotes` tab, and create a new remote.
3. Set the `Address` field of the new remote to be the `Remote Address` you copied above.
4. Set `TLS` for the remote to `Enabled`.

Ensure that the controlling robot is live in [the Viam app](https://app.viam.com).
If the connection is present, the ESP32-backed robot is now programmatically available.

### Modify the Generated Template

You can find the declaration of the robot in the generated file `src/main.rs`.
This example exposes one GPIO pin (pin 18), and one analog reader attached to GPIO pin 34.

#### Expose Other GPIO Pins

Once you have selected an appropriate GPIO pin, according to the pinout diagram included with your ESP32, you can add to the collection of exposed pins.

For example, to expose GPIO pin 21, change the line:

``` rust
let pins = vec![PinDriver::output(periph.pins.gpio18.downgrade_output())?];
```

to

``` rust
let pins = vec![PinDriver::output(periph.pins.gpio18.downgrade_output())?,
    PinDriver::output(periph.pins.gpio21.downgrade_output())?,];
```

Now you can change and read the state of pin 21 from [the Viam app](https://app.viam.com).

#### Add a New Analog Reader

Adding a new analog reader requires a few more steps.
First, identify a pin capable of analog reading.

In the pinout diagram of the ESP32, the pins are labeled like this:

- `ADCn_y`: where `n` is the adc number (1 or 2, note that 2 cannot be used with WiFi enabled), and `y` is the channel number.

Once you have identified an appropriate pin, follow these steps to add it.
In this example, we want to add GPIO pin 35, which is labeled `ADC1_7` in the pinout diagram:

1. Create a new ADC channel:

    ``` rust
    let my_analog_channel = adc_chan: AdcChannelDriver<_, Atten11dB<adc::ADC1>> =
                AdcChannelDriver::new(periph.pins.gpio35)?;
    ```

2. Create the actual Analog reader:

    ``` rust
    let my_analog_reader = Esp32AnalogReader::new("A2".to_string(), my_analog_channel, adc1.clone());
    ```

3. Finally, add the collection of analog readers:

    ``` rust
    let analog_readers = vec![
                Rc::new(RefCell::new(analog1)),
                Rc::new(RefCell::new(my_analog_reader)),
            ];
    ```

## Next Steps

To continue developing your robot with an ESP32 microcontroller, Viam suggests utilizing Espressif's QEMU ESP32 machine and userspace emulator and virtualizer.
Follow these instructions to install and build the emulator.

### Install Espressif's QEMU ESP32 Emulator

Espressif maintains a good QEMU emulator supporting the ESP32.
See [here](https://github.com/espressif/qemu) for more information.

{{< tabs >}}
{{% tab name="MacOS" %}}

Run the following command to install the QEMU ESP32 Emulator:

``` shell
git clone https://github.com/espressif/qemu
cd qemu
./configure --target-list=xtensa-softmmu \
    --enable-gcrypt \
    --enable-debug --enable-sanitizers \
    --disable-strip --disable-user \
    --disable-capstone --disable-vnc \
    --disable-sdl --disable-gtk --extra-cflags="-I/opt/homebrew/Cellar/libgcrypt/1.10.1/include -I/opt/homebrew//include/"
cd build && ninja
```

{{% /tab %}}
{{% tab name="Linux" %}}

On Ubuntu or Debian, first make sure you have the `libgcrypt` library and headers installed by running the following command:

``` shell
sudo apt-get install libgcrypt20 libgcrypt20-dev
```

Then, run the following command to install QEMU:

``` shell
git clone https://github.com/espressif/qemu
cd qemu
./configure --target-list=xtensa-softmmu     --enable-gcrypt \
    --enable-debug --enable-sanitizers  --disable-strip --disable-user \
    --disable-capstone --disable-vnc --disable-sdl --disable-gtk
cd build && ninja
```

{{% /tab %}}
{{% /tabs %}}

Add `export QEMU_ESP32_XTENSA=<path-to-clone-qemu>/build/` to your `.zshrc` or `.bashrc`, or save this command to run in your terminal every session you wish to use the QEMU emulator.

### Build with the QEMU ESP32 Emulator

Navigate to the root of the Micro-RDK repository.
Once you've `cd`'d to the correct repository, run `. $HOME/esp/esp-idf/export.sh` if you haven't done so already in this terminal session.

You will need to comment out two lines from the file `sdkconfig.defaults`:

``` editorconfig
CONFIG_ESPTOOLPY_FLASHFREQ_80M=y
CONFIG_ESPTOOLPY_FLASHMODE_QIO=y
```

You can then run:

``` shell
make sim-local
```

Or, if you want to connect a debugger:

``` shell
make debug-local
```

### Troubleshooting

If you are unable to connect to the ESP32-backed robot as a remote, try adding `:4545` to the end of the value set in the remote's `Address` field.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
