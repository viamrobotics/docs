---
title: "Add Audio Classification as a Modular Service"
linkTitle: "Add Audio Classification as a Modular Service"
weight: 70
type: "docs"
description: "Add a custom MLModel modular-resource-based service which uses TensorFlow Lite to classify audio samples."
tags: ["ml", "model training", "services"]
# SMEs: Andrew Morrow
---

Viam provides an example of a [custom module](extend/modular-resources) written in the Viam C++ SDK that extends the [ML model](/services/ml/) service to support audio classification.

The example files can be found in the [Viam C++ SDK](https://github.com/viamrobotics/viam-cpp-sdk):

- [`example_mlmodelservice_tflite.cpp`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/examples/modules/example_mlmodelservice_tflite.cpp) - a custom module that provides an example `MLModelService` instance which runs TensorFlow Lite models.
- [`example_audio_classification_client.cpp`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/examples/mlmodel/example_audio_classification_client.cpp) - an example client instance which generates audio samples and invokes the `example_mlmodelservice_tflite` custom module to classify those samples.

This tutorial walks you through everything you need to start using these example files with your robot, including building the C++ SDK, procuring the necessary support files, configuring your robot and installing `viam-server`, and running the compiled binary example.

## Build the C++ SDK

To build the Viam C++ SDK, you will need a macOS or Linux computer.
Follow the instructions below for your platform:

{{< tabs >}}
{{% tab name="macOS" %}}

Follow the [Viam C++ SDK build instructions](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md) to build the SDK on your macOS computer using the `brew` package manager.

While your specific build steps may differ slightly, your installation should generally resemble the following:

1. Install the mandatory and optional dependencies to support the Viam C++ SDK:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   brew install abseil cmake boost grpc protobuf xtensor pkg-config ninja buf
   ```

1. Clone the Viam C++ SDK to your computer:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   mkdir -p ~/example_workspace
   cd ~/example_workspace
   git clone git@github.com:viamrobotics/viam-cpp-sdk.git
   ```

1. Create a `build` directory to house the build target:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   cd viam-cpp-sdk/
   mkdir build
   cd build
   ```

1. Determine the version of `openssl` you are running on your macOS computer:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   brew list | grep openssl
   ```

   If the command returns `openssl@1.1`, proceed to the next step. If the command returns a different `openssl` version, install the correct version first:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   brew install openssl@1.1
   ```

1. Create an environment variable `PKG_CONFIG_PATH` which points to the version of `openssl` we will use for the Viam C++ SDK build:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   export PKG_CONFIG_PATH="/opt/homebrew/opt/openssl@1.1/lib/pkgconfig"
   ```

1. Build the C++ SDK.
   We are using two flags to help us compile successfully: [`VIAMCPPSDK_USE_DYNAMIC_PROTOS`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md#viamcppsdk_use_dynamic_protos) to request that proto generation happen along with the build, and [`CMAKE_INSTALL_PREFIX`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md#cmake_install_prefix) to install to `/usr/local/` instead of the default `./install` location.
   To write to the restricted location `/usr/local/`, we'll also need to use `sudo` for the second `ninja` invocation:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   cmake .. -DVIAMCPPSDK_USE_DYNAMIC_PROTOS=ON -DCMAKE_INSTALL_PREFIX=/usr/local -G Ninja
   ninja all
   sudo ninja install
   ```

{{% /tab %}}
{{% tab name="Linux" %}}

TODO: Linux instructions here. Currently failing at requiring tflite C headers: I have not yet been able to successfully [build the tflite headers on Linux](https://www.tensorflow.org/lite/guide/build_cmake#build_tensorflow_lite_c_library).

{{% /tab %}}
{{< /tabs >}}

## Download the `yamnet/classification` model file

This example uses the `yamnet/classification` TensorFlow Lite model for audio classification.
We are using a pre-trained model for this example, but you can also [train your own model](/manage/ml/train-model/).

1. Download the `yamnet/classification` TensorFlow Lite model file: [yamnet classification tflite model](https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1).

1. Copy the downloaded file into a more permanent location.
   For this example, place the model file in the `~/example_workspace` directory from earlier:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   cp ~/Downloads/lite-model_yamnet_classification_tflite_1.tflite ~/example_workspace/
   ```

1. Extract the labels file <file>yamnet_label_list.txt</file> from the downloaded model file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   unzip ~/example_workspace/lite-model_yamnet_classification_tflite_1.tflite
   ```

   The labels file provides pre-populated labels for the calculated scores, so that output scores can be associated and returned with their matching labels.
   You can omit this file if desired, which will cause the client to return the computed scores without labels.

## Install `viam-server`

Next, install `viam-server` on your robot, if you have not done so already.

1. Navigate to [the Viam app](https://app.viam.com) in your browser and [add a new robot](/manage/fleet/robots/#add-a-new-robot).

1. Switch to the **Setup** tab, and select your platform from the **Mode** selection at the top.
   If you are installing on a Linux system, additionally select your system's **Architecture**.

1. Follow the steps listed under the **Setup** tab to install `viam-server` on your system.

1. Once complete, verify that step 3 on the **Setup** tab indicates that your robot has successfully connected.

## Generate your robot configuration

When you built the C++ SDK, the build process also built the `example_audio_classification_client` binary.
The `example_audio_classification_client` binary includes a `--generate` function which determines and creates the necessary robot configuration to support this example.

To generate your robot's configuration using `example_audio_classification_client`:

1. First, determine the full path to the `yamnet/classification` model you just downloaded.
   If you followed the instructions above, this path is: <file>~/example_workspace/lite-model_yamnet_classification_tflite_1.tflite</file>.

1. Next, determine the full path to the `example_mlmodelservice_tflite` modular resource example provided with the Viam C++ SDK.
   If you followed the instructions above, this path is: <file>/usr/local/bin/example_mlmodelservice_tflite</file>.

1. Run the `example_audio_classification_client` binary, proving both paths to the `--generate` function in the following fashion:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   example_audio_classification_client --generate --model-path ~/example_workspace/lite-model_yamnet_classification_tflite_1.tflite --tflite-module-path /usr/local/bin/example_mlmodelservice_tflite > ~/example_workspace/viam-example-mlmodel-config.json
   ```

   If you did not use the [`CMAKE_INSTALL_PREFIX`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md#cmake_install_prefix) option when building the C++ SDK, you may need to provide the full path to the `example_audio_classification_client` binary for this step.

1. Verify that the resulting configuration file was created successfully:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   cat ~/example_workspace/viam-example-mlmodel-config.json
   ```

1. Copy the contents of this file.
   Then return to your robot's page on [the Viam app](https://app.viam.com), select the **Config** tab, select **Raw JSON**, and paste the configuration into the text area.

1. Click the **Save config** button at the bottom of the page.
   Now, when you switch back to **Builder** mode, you can see the new configuration settings under the **Services** and **Modules** subtabs.

This generated configuration features the minimum required configuration to support this tutorial: a `services` definition for the [ML model](/services/ml/) service and a `modules` definition for our `example_mlmodelservice_tflite` [custom module](extend/modular-resources/#configure-your-modular-resource).

## Run the inference client

With everything configured and running, we can now run the inference client that connects to `viam-server` and uses the `example_mlmodelservice_tflite` custom module.

1. First, determine your robot address and location secret. To do so, navigate to [the Viam app](https://app.viam.com), select the **Code sample** tab, and toggle **Include secret**.
   The location secret resembles `abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234` and the robot address resembles `my-robot-main.abcdefg123.viam.cloud`.

   {{%  snippet "secret-share.md" %}}

1. On the command line of the system you built the Viam C++ SDK on, run the following to start the inference client, providing the necessary access credentials and the path to the labels file we extracted earlier:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   example_audio_classification_client --model-label-path ~/example_workspace/yamnet_label_list.txt --robot-host my-robot-main.abcdefg123.viam.cloud --robot-secret abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234
   ```

   The command should return output similar to:

   ```sh {id="terminal-prompt" class="command-line"}
   0: Static                               0.5
   1: Noise                                0.332031
   2: White noise                          0.261719
   3: Cacophony                            0.109375
   4: Pink noise                           0.0585938

   Measuring inference latency ...
   Inference latency (seconds), Mean: 0.012795
   Inference latency (seconds), Var : 0.000164449
   ```

   The labels shown in the example output require that you have provided the <file>yamnet_label_list.txt</file> labels file to the `example_audio_classification_client` client using the `--model-label-path` flag.
   If you have omitted the labels file, the computed scores will be returned without labels.

## Understanding the client

The code in `src/viam/examples/mlmodel/example_audio_classification_client.cpp` is richly commented to explain each step it takes in generating and analyzing the data provided. What follows is a high-level overview of the steps it takes when executed:

1. The inference client generates two signals that meet the input requirements of the `yamnet/classification` model: the first signal is silence, while the second is noise.
   As written, the example analyzes only the noise signal, but you can change which signal is classified by changing which is assigned to the `samples` variable in the code.

1. The client then populates an input tensor named `sample` as a `tensor_view` over the provided sample data.
   The tensor must be named according to the configured value under `tensor_name_remappings` in your robot configuration.
   If you followed the instructions above to [generate your robot configuration](#generate-your-robot-configuration), the value `sample` is already pre-populated for you.

1. The client invokes the `infer` method provided by the `MLModelService` custom module, providing it with the `sample` input tensor data it generated earlier.

1. The `MLModelService` custom module returns a map of response tensors as a result.

1. The client validates the result, including its expected type: a vector of `float` values.
   The expected output must be defined under `tensor_name_remappings` in your robot configuration for validation to succeed.
   If you followed the instructions above to [generate your robot configuration](#generate-your-robot-configuration), the value `categories` is already pre-populated for you.

1. If a labels file was provided, labels are read in as a vector of `string` values and the top 5 scores are associated with their labels.

1. Finally, the client runs 100 rounds of inference using the determined label and score pairs, and returns the results of the rounds, including mean and variance values.

Similarly, the custom module that provides the `MLModelService` model can be found at `src/viam/examples/modules/example_mlmodelservice_tflite.cpp` and also offers rich comments explaining its features and considerations.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/), and additional reference material in the [C++ SDK Documentation](https://cpp.viam.dev/).

{{< snippet "social.md" >}}
