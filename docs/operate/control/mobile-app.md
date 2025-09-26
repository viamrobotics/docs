---
linkTitle: "Create a mobile app"
title: "Create a mobile app"
weight: 20
layout: "docs"
type: "docs"
description: "Create a custom user interface for interacting with machines from a mobile device."
---

You can use Viam's [Flutter SDK](https://flutter.viam.dev/) to create a custom mobile application to interact with your devices.
The Flutter SDK includes:

- Implementation of the standard component and service APIs to control your hardware and software
- Widgets to ease the development process
- Authentication tools so users can log in securely

## Install the Flutter SDK

Run the following command in your terminal to install the Viam Flutter SDK:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
flutter pub add viam_sdk
```

## Connect to your machine

You can find sample connection code on each [machine's](/operate/install/setup/) **CONNECT** tab.
Select **Flutter** to display a code snippet with connection code as well as some calls to the APIs of the resources you've configured on your machine.

You can use the toggle to include the machine API key and API key ID, though we strongly recommend storing your API keys in environment variables to reduce the risk of accidentally sharing your API key and granting access to your machines.

If your code will connect to multiple machines or use [Platform APIs](/dev/reference/apis/#platform-apis) you can create an API key with broader access.

## Write your app

Refer to the [Viam Flutter SDK](https://flutter.viam.dev/) documentation for available methods and widgets.

### Example usage

The following code, part of [Drive a rover in a square in 2 minutes](/tutorials/control/drive-rover/), shows how you could move a robotic rover base in a square using the base API's [`moveStraight`](https://flutter.viam.dev/viam_sdk/Base/moveStraight.html) and [`spin`](https://flutter.viam.dev/viam_sdk/Base/spin.html) methods:

```dart {class="line-numbers linkable-line-numbers"}
import 'package:flutter/material.dart';
import 'package:viam_sdk/viam_sdk.dart';
import 'package:viam_sdk/widgets.dart';

class BaseScreen extends StatelessWidget {
  final Base base;

  const BaseScreen(this.base, {super.key});

  Future<void> moveSquare() async {
    for (var i=0; i<4; i++) {
      await base.moveStraight(500, 500);
      await base.spin(90, 100);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(base.name)),
      body: Center(
        child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ElevatedButton(
              onPressed: moveSquare,
              child: const Text('Move Base in Square'),
            ),
        ]))
        ,);}}
```

{{<video webm_src="/tutorials/try-viam-sdk/square-test-rover.webm" mp4_src="/tutorials/try-viam-sdk/square-test-rover.mp4" alt="An example flutter app moving a Try Viam rover in a square" poster="/tutorials/try-viam-sdk/square-test-rover.jpg">}}

See the guide for full code and instructions to get started by building a simple app to control a rented Viam rover:

{{< cards >}}
{{% card link="/tutorials/control/drive-rover/" %}}
{{< /cards >}}

For a more in-depth guide with more screens, see the following guide:

{{< cards >}}
{{% card link="/tutorials/control/flutter-app/" %}}
{{< /cards >}}

## Test your app

You can use the mobile app simulator on your development computer to test your app.
The connection code will establish communication with your machine over LAN or WAN.

## Set up user authentication through Viam

Viam uses [FusionAuth](https://fusionauth.io/) for authentication and authorization.

You can [use Viam to authenticate end users](/manage/manage/oauth/) while using a branded login screen.

## Next steps

To publish your app to the app stores when you're done testing and adding authentication, see Flutter's articles:

- [iOS](https://docs.flutter.dev/deployment/ios)
- [Android](https://docs.flutter.dev/deployment/android)
