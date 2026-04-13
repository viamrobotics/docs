---
linkTitle: "Tutorial: Flutter app with widgets"
title: "Build a Flutter app with widgets"
weight: 110
layout: "docs"
type: "docs"
description: "Build a cross-platform Flutter app for a single Viam machine. Uses prebuilt widgets for the camera feed, sensor display, and motor control."
date: "2026-04-10"
---

In this tutorial, you will build a Flutter app for a single Viam machine using the widgets that ship with the Flutter SDK. The finished app shows:

- A live camera feed (`ViamCameraStreamView`)
- A live sensor readings table (`ViamSensorWidget`)
- A motor control widget (`ViamMotorWidget`)

You will learn the Flutter SDK's widget-driven pattern, which is faster than writing stream and polling logic by hand. You will also see that the same Flutter app builds and runs on iOS, Android, and desktop from one codebase.

This tutorial uses the Flutter-specific widget path rather than the raw SDK pattern. For a comparison using raw SDK calls, see [the TypeScript dashboard tutorial](./tutorial-dashboard/).

## What you need

- A configured Viam machine with a camera, a sensor, and a motor. Any models work. If you do not have the physical hardware, add fake components in the Viam app's **CONFIGURE** tab: `fake:camera`, `fake:sensor`, and `fake:motor`.
- A completed [Flutter setup](/build-apps/setup/flutter/). You should have a Flutter project with `viam_sdk` and `flutter_dotenv` installed, a `.env` file holding your machine credentials, and the iOS/Android platform configuration applied.
- A target platform to run the app on: an iOS simulator, an Android emulator, a physical device, or a desktop target (macOS, Linux, Windows).

Before continuing, confirm your setup by running `flutter run` and verifying that the app from the setup step shows `Connected. Found N resources.` If it does not, go back to [Flutter setup](/build-apps/setup/flutter/) and fix the connection before continuing.

## Step 1: Set up the app skeleton

Replace the contents of `lib/main.dart` with a new app skeleton that defines a home screen with space for the three widgets and a connection indicator:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:viam_sdk/viam_sdk.dart';
import 'package:viam_sdk/widgets.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My Viam Dashboard',
      theme: ThemeData(useMaterial3: true),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  RobotClient? _robot;
  String _status = 'Connecting...';

  @override
  void initState() {
    super.initState();
    _connect();
  }

  @override
  void dispose() {
    _robot?.close();
    super.dispose();
  }

  Future<void> _connect() async {
    try {
      final robot = await RobotClient.atAddress(
        dotenv.env['MACHINE_ADDRESS']!,
        RobotClientOptions.withApiKey(
          dotenv.env['API_KEY_ID']!,
          dotenv.env['API_KEY']!,
        ),
      );
      setState(() {
        _robot = robot;
        _status = 'Connected';
      });
    } catch (e) {
      setState(() {
        _status = 'Connection failed: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Viam Dashboard')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Status: $_status'),
            const SizedBox(height: 16),
            if (_robot != null) ..._buildDashboard(_robot!),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildDashboard(RobotClient robot) {
    return const [
      Text('Dashboard will go here'),
    ];
  }
}
```

Save the file and run `flutter run`. Pick your target platform when prompted. The app builds, launches, and shows the app bar with "My Viam Dashboard" and the status text switching from `Connecting...` to `Connected`. The "Dashboard will go here" placeholder appears below the status once the connection is established.

You will replace the placeholder in the next three steps.

## Step 2: Add the camera widget

Update `_buildDashboard` to include `ViamCameraStreamView`:

```dart
List<Widget> _buildDashboard(RobotClient robot) {
  final camera = Camera.fromRobot(robot, 'camera');
  final streamClient = robot.getStream('camera');

  return [
    const Text('Camera', style: TextStyle(fontSize: 20)),
    const SizedBox(height: 8),
    SizedBox(
      height: 240,
      child: ViamCameraStreamView(
        camera: camera,
        streamClient: streamClient,
      ),
    ),
  ];
}
```

The string `'camera'` is the component name you gave the camera in your machine config. Change it to match your config if you used a different name.

Save the file. Flutter's hot reload updates the app without rebuilding. The camera panel now shows a live feed. For a real camera, you see the camera's image; for `fake:camera`, you see a test pattern.

`ViamCameraStreamView` is a stateful widget that manages the `RTCVideoRenderer` lifecycle, initializes the WebRTC stream, tears it down on dispose, and displays an error state if the stream fails. You did not write any of that logic; the widget handles it all.

## Step 3: Add the sensor widget

Extend `_buildDashboard` to append a `ViamSensorWidget`:

```dart
List<Widget> _buildDashboard(RobotClient robot) {
  final camera = Camera.fromRobot(robot, 'camera');
  final streamClient = robot.getStream('camera');
  final sensor = Sensor.fromRobot(robot, 'sensor');

  return [
    const Text('Camera', style: TextStyle(fontSize: 20)),
    const SizedBox(height: 8),
    SizedBox(
      height: 240,
      child: ViamCameraStreamView(
        camera: camera,
        streamClient: streamClient,
      ),
    ),
    const SizedBox(height: 24),
    const Text('Sensor readings', style: TextStyle(fontSize: 20)),
    const SizedBox(height: 8),
    ViamSensorWidget(sensor: sensor),
  ];
}
```

Save. The app now shows a data table under the camera, populated with the sensor's current readings. The widget refreshes the table on its own; you do not need a timer or a polling loop.

Under the hood, `ViamSensorWidget` is a `ViamRefreshableDataTable` that calls `sensor.readings()` on a schedule and re-renders when new data arrives. The Flutter SDK's widget layer handles the polling so you do not have to.

## Step 4: Add the motor widget

Append a `ViamMotorWidget` to the dashboard:

```dart
List<Widget> _buildDashboard(RobotClient robot) {
  final camera = Camera.fromRobot(robot, 'camera');
  final streamClient = robot.getStream('camera');
  final sensor = Sensor.fromRobot(robot, 'sensor');
  final motor = Motor.fromRobot(robot, 'motor');

  return [
    const Text('Camera', style: TextStyle(fontSize: 20)),
    const SizedBox(height: 8),
    SizedBox(
      height: 240,
      child: ViamCameraStreamView(
        camera: camera,
        streamClient: streamClient,
      ),
    ),
    const SizedBox(height: 24),
    const Text('Sensor readings', style: TextStyle(fontSize: 20)),
    const SizedBox(height: 8),
    ViamSensorWidget(sensor: sensor),
    const SizedBox(height: 24),
    const Text('Motor', style: TextStyle(fontSize: 20)),
    const SizedBox(height: 8),
    ViamMotorWidget(motor: motor),
  ];
}
```

Save. The motor section now shows a power slider with auto-stop behavior. Drag the slider to set a power level; `ViamMotorWidget` calls `motor.setPower()` on the underlying component as you adjust it. The widget's auto-stop mode means releasing the slider calls `motor.stop()` so the motor does not continue running at the last commanded power when you let go.

Open the Viam app's **CONTROL** tab for the same machine in another window. Arrange the two side by side. When you drag the slider in your Flutter app, the motor's power slider in the Viam app's Control tab moves in sync. You just made a server-side state change from your Flutter app, visible to another client watching the same machine.

For `fake:motor`, the motor has no physical effect, but the state change is real. The same calls on a real motor would spin it.

## Step 5: Run on another platform

Stop the app and run it on a second target to see the cross-platform story. If you first ran it on an iOS simulator, try Android, or try a desktop target:

```sh {class="command-line" data-prompt="$"}
flutter run -d macos
```

Or:

```sh {class="command-line" data-prompt="$"}
flutter run -d chrome
```

Or:

```sh {class="command-line" data-prompt="$"}
flutter run -d windows
```

The same code builds and runs on each platform without modification. The widgets render with the platform's Material look, the camera stream decodes and displays on each target, the sensor data table updates, and the motor slider controls the same machine. This is the argument for Flutter over a browser-only framework when you need one app that runs across iOS, Android, and one or more desktop operating systems.

Some platform-specific notes:

- **iOS and macOS** require the `Info.plist` permissions you added in [Flutter setup](/build-apps/setup/flutter/) for WebRTC to work.
- **Android** requires minimum SDK 23 and the setup page's Kotlin version.
- **Web** support depends on whether `flutter_webrtc` has stable web behavior for your specific build. If the web target fails, fall back to native or desktop targets for now.

## What you built

You now have a Flutter app that:

- Connects to a Viam machine at startup and closes the connection on dispose
- Shows a live camera feed through `ViamCameraStreamView`
- Shows live sensor readings through `ViamSensorWidget`
- Controls a motor through `ViamMotorWidget` with auto-stop
- Builds and runs on every Flutter target platform from one codebase

The full `lib/main.dart` is around 100 lines of code, most of which is scaffolding for the app shell rather than Viam-specific logic. The three prebuilt widgets did the heavy lifting: you wrote no stream renderer, no polling timer, no motor button wiring. That is the Flutter widget advantage.

## Next steps

Extend the app in one of these directions:

- **Add a joystick for base control.** If your machine has a base configured, add a `ViamJoystickWidget` to drive it. The joystick widget converts user input into base movement commands.
- **Use the multi-camera widget.** The Flutter SDK ships `ViamMultiCameraStreamView` for showing several camera feeds at once. See the [Flutter SDK reference](https://flutter.viam.dev/) for its parameters.
- **Build a list of resources with per-resource screens.** The `viam_robot_example_app` in the Flutter SDK repo shows a pattern for enumerating the machine's resources and showing a custom screen for each. Use it as a reference for larger apps.
- **Read from the Viam cloud.** Switch from `RobotClient.atAddress` to `Viam.withApiKey` so you can use the `appClient` and `dataClient` to enumerate machines and query captured data. See [Connect to the Viam cloud](/build-apps/tasks/connect-to-cloud/).
- **Build a multi-machine version.** See [the fleet tutorial](/build-apps/app-tutorials/tutorial-fleet/) for a dashboard that aggregates data across several machines.
