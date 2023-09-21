---
title: "Run SDK Code"
linkTitle: "Run Code"
weight: 50
type: "docs"
description: "Execute the logic you've written to control your robot or fleet."
images: ["/services/icons/sdk.svg"]
tags: ["client", "sdk", "application", "sdk", "fleet", "program"]
---

After saving your [code sample](/program/#hello-world-the-code-sample-tab) and adding control logic with [Viam's SDKs](/program/apis/), run your program to control your Viam-connected robot.

### Authentication

You must reference a robot's location secret to authenticate yourself to the robot.
However, the app hides the robot location secret from the sample by default for your security.

To copy the robot location secret, select **Include Secret** on the **Code sample** tab of your robot's page on the [Viam app](https://app.viam.com).
Paste it into your SDK code as directed by the code sample.

You must also include the robot's remote address, like `12345.somerobot-main.viam.cloud`, as an external or public address to connect to your robot.
The code sample includes this address at default.
You can find it at the top of the robot's **Control** tab.

{{% snippet "secret-share.md" %}}

## Run Code Remotely

Most of the time, as long as both you and your robot are connected to the internet, you will want to run code on your robot remotely.
The advantage of this method is that your robot and your computer do not have to be connected to the same WAN/LAN to issue control commands.
You can remotely control your robot with any application you implement from anywhere in the world.
After editing your code to include your robot's [authentication credentials](#authentication), run a command to execute the program in the terminal of a machine with the appropriate programming language and Viam SDK installed:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {class="command-line" data-prompt="$"}
python3 ~/myCode/myViamFile.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
go run ~/myCode/myViamFile.py
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

For an example, see [this execution demo.](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples/vanilla)

{{% /tab %}}
{{% tab name="C++" %}}

For information on running C++ code see [the instructions on GitHub](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{% tab name="Flutter" %}}

```sh {class="command-line" data-prompt="$"}
flutter run <DART_FILE>
```

{{% /tab %}}
{{< /tabs >}}

This is useful because as long as that computer is able to establish a network connection with the robot's computer, your control logic will be executed on the robot.

## Run Code On-Robot

{{< alert title="Info" color="info" >}}
This method of running code locally is only implemented on the Viam Python SDK.
{{< /alert >}}

In case your robots have intermittent internet connectivity, you can ensure this does not interfere with the code's execution.
If you need to run [PID control loops](https://en.wikipedia.org/wiki/PID_controller) or other on-robot code, you can run control code on the same board that is running `viam-server`.

In the `connect()` method of your control code, make the following changes:

1. Set `disable_webrtc=True` to disable {{< glossary_tooltip term_id="webrtc" >}}.
2. Set `auth_entity` to your robot's [configured](/manage/configuration/) `name`.
3. Replace the remote address in `RobotClient.at_address` with `localhost:8080`

Your SDK code should now look like:

```python {class="line-numbers linkable-line-numbers"}
async def connect():
  creds = Credentials(type='robot-location-secret', payload=YOUR_LOCATION_SECRET)
  opts = RobotClient.Options(
    refresh_interval=0,
    dial_options=DialOptions(
        credentials=creds,
        disable_webrtc=True,
        auth_entity="<YOUR_ROBOT_NAME>"
    )
  )
  return await RobotClient.at_address('localhost:8080', opts)
```

Your localhost can now make a secure connection to `viam-server` locally.
SSL will check the server hostname against the `auth_entity` required by {{< glossary_tooltip term_id="grpc" >}} from the `auth_entity` `DialOptions`.

This ensures that you can send commands to the robot through localhost without internet connectivity.
Note that all commands will be sent using {{< glossary_tooltip term_id="grpc" >}} only without {{< glossary_tooltip term_id="webrtc" >}}.
