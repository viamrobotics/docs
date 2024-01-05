---
title: "Add a TensorFlow Lite Modular Service"
linkTitle: "TensorFlow Lite Modular Service"
weight: 70
type: "docs"
description: "Add an ML model modular-resource-based service which uses TensorFlow Lite to classify audio samples."
tags: ["ml", "model training", "services"]
aliases:
  - "/extend/modular-resources/examples/tflite-module/"
  - "/modular-resources/examples/tflite-module/"
# SMEs: Andrew Morrow
---

Viam provides an example {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} written in C++ that extends the [ML model](/ml/) service to run any TensorFlow Lite model.
The example includes an inference client program as well, which generates audio samples and uses the modular resource to classify the audio samples based on a pre-trained model.

This tutorial walks you through everything necessary to start using these example files with your robot, including building the C++ SDK, configuring your robot and installing `viam-server`, and generating results with the example inference client program.

The provided example code demonstrates the design, implementation, and usage of a custom module to help you write your own.
This code is for instructional purposes only, and is not intended for production use.

You can find the example files in the [Viam C++ SDK](https://github.com/viamrobotics/viam-cpp-sdk):

- [`example_mlmodelservice_tflite.cpp`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/examples/modules/tflite/main.cpp) - an example module which provides the `MLModelService` modular resource capable of running any TensorFlow Lite model.
- [`example_audio_classification_client.cpp`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/examples/mlmodel/example_audio_classification_client.cpp) - an example inference client which generates audio samples and invokes the `example_mlmodelservice_tflite` module to classify those samples using the [`yamnet/classification` TensorFlow Lite model](https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1).

## Build the C++ SDK

To build the Viam C++ SDK, you will need a macOS or Linux computer.
Follow the instructions below for your platform:

{{< tabs >}}
{{% tab name="macOS" %}}

Follow the [Viam C++ SDK build instructions](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md) to build the SDK on your macOS computer using the `brew` package manager.

While your specific build steps may differ slightly, your installation should generally resemble the following:

1. Install all listed dependencies to support the Viam C++ SDK:

   ```sh { class="command-line" data-prompt="$"}
   brew install abseil cmake boost grpc protobuf xtensor pkg-config ninja buf
   ```

1. Create a new <file>example_workspace</file> directory for this tutorial, and create an <file>opt</file> directory within it to house the build artifacts:

   ```sh { class="command-line" data-prompt="$"}
   mkdir -p ~/example_workspace
   cd ~/example_workspace
   mkdir -p opt
   ```

1. Within the <file>~/example_workspace</file> directory, clone the Viam C++ SDK:

   ```sh { class="command-line" data-prompt="$"}
   git clone git@github.com:viamrobotics/viam-cpp-sdk.git
   ```

1. Change directory into the SDK, and create a <file>build</file> directory to house the build:

   ```sh { class="command-line" data-prompt="$"}
   cd viam-cpp-sdk/
   mkdir build
   cd build
   ```

1. Create an environment variable `PKG_CONFIG_PATH` which points to the version of `openssl` installed on your system:

   ```sh { class="command-line" data-prompt="$"}
   export PKG_CONFIG_PATH="`brew --prefix`/opt/openssl/lib/pkgconfig"
   ```

1. Build the C++ SDK by running the following commands:

   ```sh { class="command-line" data-prompt="$"}
   cmake .. -DVIAMCPPSDK_BUILD_TFLITE_EXAMPLE_MODULE=ON -DCMAKE_INSTALL_PREFIX=~/example_workspace/opt -G Ninja
   ninja all
   ninja install
   ```

   For this tutorial, the build process uses the following configuration options. See [Viam C++ SDK Build Instructions](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md) for more information:

   - `VIAMCPPSDK_BUILD_TFLITE_EXAMPLE_MODULE` to request building the example module for this tutorial.
   - [`CMAKE_INSTALL_PREFIX`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md#cmake_install_prefix) to install to <file>~/example_workspace/opt</file> instead of the default <file>./install</file> location.

{{% /tab %}}
{{% tab name="Linux" %}}

Follow the [Viam C++ SDK build instructions](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md) to build the SDK on your Linux system.

While your specific build steps may differ slightly, your installation should generally resemble the following:

1. Clone the Viam C++ SDK to your Linux system:

   ```sh { class="command-line" data-prompt="$"}
   git clone git@github.com:viamrobotics/viam-cpp-sdk.git
   ```

1. Build and run the `bullseye` development Docker container included with the SDK. If you haven't already, first [install Docker Engine](https://docs.docker.com/engine/install/).

   ```sh { class="command-line" data-prompt="$"}
   cd viam-cpp-sdk/
   docker build -t cpp . -f etc/docker/Dockerfile.debian.bullseye
   docker run --rm -it -v "$PWD":/usr/src/viam-cpp-sdk -w /usr/src/viam-cpp-sdk cpp /bin/bash
   ```

   Alternatively, you can skip running the docker container if you would prefer to use your own development environment.

1. Install all listed dependencies to support the Viam C++ SDK:

   ```sh { class="command-line" data-prompt="$"}
   sudo apt-get install git cmake build-essential libabsl-dev libboost-all-dev libgrpc++-dev libprotobuf-dev pkg-config ninja-build protobuf-compiler-grpc
   ```

1. If you are not using the `bullseye` container included with the SDK, you may need to install a newer version of `cmake` to build the SDK.
   Run the following to determine the version of `cmake` installed on your system:

   ```sh { class="command-line" data-prompt="$"}
   cmake --version
   ```

   If the version returned is `3.25` or later, skip to the next step.
   Otherwise, download and install `cmake 3.25` or later from your system's package manager.
   For example, if using Debian, you can run the following commands to add the `bullseye-backports` repository and install the version of `cmake` provided there:

   ```sh { class="command-line" data-prompt="$"}
   sudo apt-get install software-properties-common
   sudo apt-add-repository 'deb http://deb.debian.org/debian bullseye-backports main'
   sudo apt-get update
   sudo apt-get install -t bullseye-backports cmake
   ```

1. Create an <file>opt</file> directory to install the build artifacts to:

   ```sh { class="command-line" data-prompt="$"}
   mkdir -p ~/example_workspace/opt
   ```

1. Within the <file>viam-cpp-sdk</file> directory, create a <file>build</file> directory to house the build:

   ```sh { class="command-line" data-prompt="$"}
   mkdir build
   cd build
   ```

1. Build the C++ SDK by running the following commands:

   ```sh { class="command-line" data-prompt="$"}
   cmake .. -DVIAMCPPSDK_BUILD_TFLITE_EXAMPLE_MODULE=ON -DCMAKE_INSTALL_PREFIX=~/example_workspace/opt -G Ninja
   ninja all
   ninja install
   ```

   For this tutorial, the build process uses the following configuration options. See [Viam C++ SDK Build Instructions](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md) for more information:

   - `VIAMCPPSDK_BUILD_TFLITE_EXAMPLE_MODULE` to request building the example module for this tutorial.
   - [`CMAKE_INSTALL_PREFIX`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md#cmake_install_prefix) to install to <file>~/example_workspace/opt</file> instead of the default <file>./install</file> location.

{{% /tab %}}
{{< /tabs >}}

## Download the `yamnet/classification` model file

This example uses the `yamnet/classification` TensorFlow Lite model for audio classification.

1. Download the `yamnet/classification` TensorFlow Lite model file and place it in your <file>example_workspace</file> directory:

   ```sh { class="command-line" data-prompt="$"}
   curl -Lo ~/example_workspace/lite-model_yamnet_classification_tflite_1.tflite https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1?lite-format=tflite
   ```

   Alternatively, you may download the model file here: [yamnet classification tflite model](https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1).
   If you download in this fashion, move the downloaded file to your <file>~/example_workspace</file> directory.

1. Extract the labels file <file>yamnet_label_list.txt</file> from the downloaded model file:

   ```sh { class="command-line" data-prompt="$"}
   unzip ~/example_workspace/lite-model_yamnet_classification_tflite_1.tflite -d ~/example_workspace/
   ```

   The labels file provides pre-populated labels for the calculated scores, so that output scores can be associated and returned with their matching labels.
   You can omit this file if desired, which will cause the inference client to return the computed scores without labels.

## Install `viam-server`

Next, install `viam-server` on your robot, if you have not done so already:

1. Navigate to [the Viam app](https://app.viam.com) in your browser and [add a new robot](/fleet/machines/#add-a-new-robot).

1. Switch to the **Setup** tab, and select your platform from the **Architecture** selection at the top.

1. Follow the steps listed under the **Setup** tab to install `viam-server` on your system.

   {{< alert title="Important" color="note" >}}
   If you are installing `viam-server` within the `bullseye` Docker container provided with the C++ SDK, you will need to run the following command _instead_ of the command listed in step 2 **Download and install viam-server** in the Viam app:

   ```sh { class="command-line" data-prompt="$"}
   curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage -o viam-server && chmod 755 viam-server && sudo ./viam-server --appimage-extract-and-run -config /etc/viam.json
   ```

   {{< /alert >}}

1. Once complete, verify that step 3 on the **Setup** tab indicates that your robot has successfully connected.

1. Stop `viam-server` by pressing CTL-C on your keyboard from within the terminal window where you entered the commands from step 3 above.

## Generate your robot configuration

When you built the C++ SDK, the build process also built the `example_audio_classification_client` binary, which includes a `--generate` function that determines and creates the necessary robot configuration to support this example.

To generate your machine's configuration using `example_audio_classification_client`:

1. First, determine the full path to the `yamnet/classification` model you just downloaded.
   If you followed the instructions above, this path is: <file>~/example_workspace/lite-model_yamnet_classification_tflite_1.tflite</file>.

1. Next, determine the full path to the `example_mlmodelservice_tflite` modular resource example provided with the Viam C++ SDK.
   If you followed the instructions above, this path is: <file>~/example_workspace/opt/bin/example_mlmodelservice_tflite</file>.

1. Run the `example_audio_classification_client` binary, providing both paths to the `--generate` function in the following fashion:

   ```sh { class="command-line" data-prompt="$"}
   cd ~/example_workspace/opt/bin
   ./example_audio_classification_client --generate --model-path ~/example_workspace/lite-model_yamnet_classification_tflite_1.tflite --tflite-module-path ~/example_workspace/opt/bin/example_mlmodelservice_tflite > ~/example_workspace/viam-example-mlmodel-config.json
   ```

1. Verify that the resulting configuration file was created successfully:

   ```sh { class="command-line" data-prompt="$"}
   cat ~/example_workspace/viam-example-mlmodel-config.json
   ```

1. Copy the contents of this file.
   Then return to your machine's page on [the Viam app](https://app.viam.com), select the **Config** tab, select **Raw JSON**, and add the configuration into the text area.

   {{< alert title="Important" color="note" >}}
   If you already have other configured components, you will need to add each generated JSON object to the respective `modules` or `services` array.
   If you do not already have configured components, you can replace the contents in **Raw JSON** with the generated contents.
   {{< /alert >}}

1. Click the **Save config** button at the bottom of the page.
   Now, when you switch back to **Builder** mode, you can see the new configuration settings under the **Services** and **Modules** subtabs.

This generated configuration features the minimum required configuration to support this tutorial: `services` parameters for the [ML model](/ml/) service and `modules` parameters for the `example_mlmodelservice_tflite` module.

## Run the inference client

With everything configured and running, you can now run the inference client that connects to `viam-server` and uses the `example_mlmodelservice_tflite` module.

1. First, determine your robot address and API key and API key ID. To do so, navigate to [the Viam app](https://app.viam.com), select the **Code sample** tab, and toggle **Include API Key**.
   The API key resembles `abcdef1g23hi45jklm6nopqrstu7vwx8`, the API key ID resembles `a1234b5c-678d-9012-3e45-67fabc8d9efa` and the robot address resembles `my-robot-main.abcdefg123.viam.cloud`.

   {{%  snippet "secret-share.md" %}}

1. Next, start `viam-server` once more on your robot, this time as a background process:

   ```sh { class="command-line" data-prompt="$"}
   viam-server -config /etc/viam.json
   ```

   {{< alert title="Important" color="note" >}}
   If you are working within the `bullseye` Docker container on Linux, run the following command _instead_ of the above, from within the directory you installed `viam-server` to:

   ```sh { class="command-line" data-prompt="$"}
   ./viam-server --appimage-extract-and-run -config /etc/viam.json &
   ```

   {{< /alert >}}

1. Then, run the following to start the inference client, providing the necessary access credentials and the path to the labels file extracted earlier:

   ```sh { class="command-line" data-prompt="$"}
   cd ~/example_workspace/opt/bin
   ./example_audio_classification_client --model-label-path ~/example_workspace/yamnet_label_list.txt --robot-host my-robot-main.abcdefg123.viam.cloud --robot-api-key abcdef1g23hi45jklm6nopqrstu7vwx8 --robot-api-key-id a1234b5c-678d-9012-3e45-67fabc8d9efa
   ```

   The command should return output similar to:

   ```sh {}
   0: Static                               0.5
   1: Noise                                0.332031
   2: White noise                          0.261719
   3: Cacophony                            0.109375
   4: Pink noise                           0.0585938

   Measuring inference latency ...
   Inference latency (seconds), Mean: 0.012795
   Inference latency (seconds), Var : 0.000164449
   ```

   The labels shown in the example output require that you have provided the <file>yamnet_label_list.txt</file> labels file to `example_audio_classification_client` using the `--model-label-path` flag.
   If you have omitted the labels file, the computed scores will be returned without labels.

## Understanding the code

The `example_mlmodelservice_tflite` module, and the `MLModelService` modular resource it provides, extends the existing [ML model](/ml/) service to run any TensorFlow Lite model.
The `example_audio_classification_client` inference client provides sample audio data and the `yamnet/classification` TensorFlow Lite model to the `MLModelService` modular resource and interprets the results it returns.

All example code is provided in the Viam C++ SDK in the <file>src/viam/examples/</file> directory.

The code in <file>src/viam/examples/mlmodel/example_audio_classification_client.cpp</file> is richly commented to explain each step it takes in generating and analyzing the data provided.
What follows is a high-level overview of the steps it takes when executed:

1. The inference client generates two signals that meet the input requirements of the `yamnet/classification` model: the first signal is silence, while the second is noise.
   As written, the example analyzes only the noise signal, but you can change which signal is classified by changing which is assigned to the `samples` variable in the code.

1. The client then populates an input tensor named `sample` as a `tensor_view` over the provided sample data.
   The tensor must be named according to the configured value under `tensor_name_remappings` in your robot configuration.
   If you followed the instructions above to [generate your robot configuration](#generate-your-robot-configuration), the value `sample` was pre-populated for you in your generated robot configuration.

1. The client invokes the `infer` method provided by the `example_mlmodelservice_tflite` module, providing it with the `sample` input tensor data it generated earlier.

1. The `example_mlmodelservice_tflite` module returns a map of response tensors as a result.

1. The client validates the result, including its expected type: a vector of `float` values.
   The expected output must be defined under `tensor_name_remappings` in your robot configuration for validation to succeed.
   If you followed the instructions above to [generate your robot configuration](#generate-your-robot-configuration), the value `categories` was pre-populated for you in your generated robot configuration.

1. If a labels file was provided, labels are read in as a vector of `string` values and the top 5 scores are associated with their labels.

1. Finally, the client runs 100 rounds of inference using the determined label and score pairs, and returns the results of the rounds, including mean and variance values.

Similarly, the `example_mlmodelservice_tflite` module can be found at <file>src/viam/examples/modules/example_mlmodelservice_tflite.cpp</file> and also offers rich comments explaining its features and considerations.

## Next steps

This tutorial explores audio classification using the `yamnet/classification` TensorFlow Lite model, but the `MLModelService` modular resource provided by the `example_mlmodelservice_tflite` module can accept any TensorFlow Lite model so long as it fulfils the [TFLite model constraints](https://www.tensorflow.org/lite/models/build#model_design_constraints).

Once you have run the example and examined the module and client code, you might explore the following next steps:

- Write a client similar to `example_audio_classification_client` that generates a different kind of data and provides a suitable TensorFlow Lite model for that data to the `MLModelService` modular resource.
  For example, you might find a new [pre-trained TensorFlow Lite model](https://www.tensorflow.org/lite/models/trained) that analyzes [speech waveforms](https://tfhub.dev/s?deployment-format=lite&module-type=audio-speech-synthesis) and write a client to provide these waveform samples to the `MLModelService` modular resource and interpret the results returned.
- Write a client similar to `example_audio_classification_client` that [trains its own model](/ml/train-model/) on existing or incoming data, as long as that model fulfils the TFLite model constraints.
  For example, you might add a [movement sensor](/components/movement-sensor/) component to your robot that captures sensor readings to the built-in [data management service](/data/).
  Then you could write a client that trains a new model based on the collected data, provides the model and new sensor data readings to the `MLModelService` modular resource, and interprets the results returned.
- Write a module similar to `example_mlmodelservice_tflite` that accepts models for other inference engines besides TensorFlow Lite, then write a client that provides a valid model and source data for that inference engine.

## Troubleshooting and additional documentation

- If you experience issues building the C++ SDK, see [C++ SDK: Limitations, Known Issues, and Troubleshooting](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md#limitations-known-issues-and-troubleshooting).
- To customize your C++ build process or make adjustments to fit your platform or deployment requirements, see [C++ SDK: Options to Configure or Customize the Build](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md#options-to-configure-or-customize-the-build)

You can find additional reference material in the [C++ SDK documentation](https://cpp.viam.dev/).
