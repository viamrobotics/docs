---
title: "Get Started Programming your Robot with Viam's SDKs"
linkTitle: "Run Code"
weight: 50
type: "docs"
description: "Execute the logic you've written to control your robot or fleet."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---


## Run Your Code

After saving your boilerplate code sample and adding control logic with Viam's API methods, run your program to control your Viam-connected robot.

For example:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 ~/myCode/myViamFile.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go run ~/myCode/myViamFile.py
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

For an example, see [this execution demo.](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples/vanilla)

{{% /tab %}}
{{< /tabs >}}

### Run Code Locally

If you need to run [PID control loops](https://en.wikipedia.org/wiki/PID_controller) or other on-robot code, you can run control code on the same board that is running `viam-server`.

To ensure intermittent internet connectivity does not interfere with the code's execution, there are some special steps you need to follow:

{{< alert title="Note" color="note" >}}
Currently, this only works with Python code which is running on the same board that `viam-server` is running on.
{{< /alert >}}

1. Change the `connect()` method to disable {{< glossary_tooltip term_id="webrtc" >}} and add the auth_entity in the DialOptions and use `localhost:8080`:

    ```python {class="line-numbers linkable-line-numbers" data-line="5"}
    async def connect():
      creds = Credentials(type='robot-location-secret', payload=PAYLOAD_SECRET)
      opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(
            credentials=creds,
            disable_webrtc=True,
            auth_entity=ROBOT_NAME
        )
      )
      return await RobotClient.at_address('localhost:8080', opts)
    ```

2. Replace the `ROBOT_NAME` with your robot's Viam cloud address and the `PAYLOAD_SECRET` with your robot secret.
   Your localhost can now make a secure connection to `viam-server` locally.
   SSL will now check the server hostname against the `auth_entity` required by {{< glossary_tooltip term_id="grpc" >}} from the `auth_entity` dial options.

   This ensures that you can send commands to the robot through localhost without internet connectivity.
   Note that all commands will be sent using {{< glossary_tooltip term_id="grpc" >}} only without {{< glossary_tooltip term_id="webrtc" >}}.