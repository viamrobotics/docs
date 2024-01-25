---
title: "Build a Flutter App that Integrates with Viam"
linkTitle: "Build a Flutter App"
type: "docs"
description: "Use Viam's Flutter SDK to build a custom mobile app to show your machines and their components."
webmSrc: "/tutorials/flutter-app/demo.webm"
mp4Src: "/tutorials/flutter-app/demo.mp4"
videoAlt: "An example Viam-integrated Flutter app."
tags: ["sdk", "flutter"]
authors: ["Clint Purser"]
languages: ["flutter"]
viamresources: ["base"]
level: "Intermediate"
date: "2024-01-17"
cost: "0"
---

<div class="td-max-width-on-larger-screens">
 <div class="alignleft" style="max-width:250px; margin-right:40px">
  {{<gif webm_src="/tutorials/flutter-app/demo.webm" mp4_src="/tutorials/flutter-app/demo.mp4" alt="Rendering of the mobile app. Log in is clicked, then all Clint's locations are shown, Clint's Desk it clicked, all its smart machines are listed, and then desk-robot is clicked, showing a list of components and services belonging to that smart machine.">}}
  </div>
</div>

Flutter is Google's user interface toolkit for building applications for mobile, web, and desktop from a single codebase.
If the existing [Viam mobile app](/fleet/#the-viam-mobile-app) doesn't fit your needs, you can use Viam's [Flutter SDK](https://flutter.viam.dev/) to build a custom app to interact with your smart machines that run on Viam.

This tutorial guides you through creating a mobile app that shows your machines and their components.
As you work through this project you will learn the following:

- The basics of how Flutter works
- How to create _layouts_ in Flutter
- How to connect user interactions (such as button presses) to app behavior
- The basics of using Viam's Flutter SDK

## Requirements

You do not need any hardware for this tutorial other than a computer running macOS or a 64-bit Linux operating system.

This tutorial assumes you already have a smart machine [configured](/build/configure/) on the [Viam web app](https://app.viam.com).

## Set up your Flutter environment

To make this documentation as straightforward as possible, this tutorial assumes you are using [Visual Studio Code](https://code.visualstudio.com/download) (VS Code) as your development environment (IDE).
It's free, works on all major platforms, and has great integrations with Flutter.
You can use a different editor, but it will be easier to follow along using VS Code.

### Choose a development target

Flutter can compile and run on many different platforms.
For the purpose of this tutorial, we will be developing for iOS.

You can always run your app on another platform later.
It's just easier to have a clear development target in mind; it makes the next step smoother.

### Install Flutter

Install Flutter according to [the Flutter documentation](https://docs.flutter.dev/get-started/install).
The instructions on the Flutter website cover not only the installation of the SDK itself, but also the development target-related tools and the editor plugins.
For this walkthrough, you only need to install the following:

- Flutter SDK
- Visual Studio Code with the [Flutter extension](https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter)
- The software required by your chosen development target.
  For example:
  - [Xcode](https://developer.apple.com/xcode/) to target macOS
    - When prompted, do install Cocoapods.
      You need it to support the iOS simulator.
  - [Visual Studio](https://visualstudio.microsoft.com/) to target Windows

## Create a project

### Create your first Flutter project

1. Launch VS Code and open the [command palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) (with `F1` or `Ctrl+Shift+P` or `Shift+Cmd+P`).

2. Start typing "flutter new."
   Select the **Flutter: New Project** command.

{{<imgproc src="/tutorials/flutter-app/flutter-new-project.png" resize="1200x" style="max-width:800px" declared-dimensions="true" alt="Creating a new project in VS Code.">}}

3. Next, select **Application** and then choose a folder in which to create your project.
   This could be your home directory, or something like <file>C:\\src\\</file>.
4. Finally, name your project something like <file>smart_machine_app</file>.

{{<imgproc src="/tutorials/flutter-app/project-name.png" resize="1200x" style="max-width:800px" declared-dimensions="true" alt="Entering the name for the project in VS Code: 'smart_machine_app'.">}}

Flutter now creates your project folder for you and VS Code opens it.

In the next steps, you'll overwrite the contents of three files with a basic scaffold of the app.

### Copy and paste the initial app

1. In the left pane of VS Code, make sure that **Explorer** is selected, and open the <file>pubspec.yaml</file> file.
   This file specifies basic information about your app, such as its current version, its dependencies, and the assets with which it will ship.

2. Replace the contents of your <file>pubspec.yaml</file> with the following:

   ```yaml {class="line-numbers linkable-line-numbers"}
   name: smart_machine_app
   description: "A new Flutter project."

   publish_to: "none" # Remove this line if you wish to publish to pub.dev

   version: 1.0.0+1

   environment:
     sdk: ">=3.2.3 <4.0.0"

   dependencies:
     flutter:
       sdk: flutter
     flutter_dotenv: ^5.1.0
     image: ^4.0.17
     cupertino_icons: ^1.0.2
     viam_sdk: ^0.0.9

   dev_dependencies:
     flutter_test:
       sdk: flutter

     flutter_lints: ^2.0.0

   flutter:
     uses-material-design: true
   ```

   {{% alert title="Note" color="note" %}}

   If you named your app something other than `smart_machine_app`, you need to change the `name` value in the first line of the <file>pubspec.yaml</file> file to the name you gave your app during setup.

   {{% /alert %}}

   3. Next, open the <file>analysis_options.yaml</file> configuration file.
      This file determines how strict Flutter should be when analyzing your code.
      For this tutorial, you will use a less strict analyzer configuration to start, but you can always tune this later.
      As you get closer to publishing an actual production app, you will likely want to increase the strictness of the analyzer, especially before publishing and sharing your app with others.

   4. Replace the contents of this file with the following:

   ```yaml {class="line-numbers linkable-line-numbers"}
   include: package:flutter_lints/flutter.yaml

   linter:
     rules:
       avoid_print: false
       prefer_const_constructors_in_immutables: false
       prefer_const_constructors: false
       prefer_const_literals_to_create_immutables: false
       prefer_final_fields: false
       unnecessary_breaks: true
       use_key_in_widget_constructors: false
   ```

### Configure iOS-specific code

Now you'll update some configurations in the iOS-specific code to support the [Viam Flutter SDK](https://flutter.viam.dev/).

1. Open <file>ios/Podfile</file>.
   If Podfile does not exist in that directory, you can generate it by running `flutter pub get` in the root directory of your app.

   At the top of the file you will see the following lines:

   ```{class="line-numbers linkable-line-numbers"}
   # Uncomment this line to define a global platform for your project
   # platform :ios, '11.0'
   ```

   Update that code to match the following:

   ```{class="line-numbers linkable-line-numbers"}
   # Uncomment this line to define a global platform for your project
   platform :ios, '13.0'
   ```

2. Open <file>ios/Runner/Info.plist</file>.
   It will look something like this:

   {{<imgproc src="/tutorials/flutter-app/info-plist.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="The info.plist file open in VS Code. The second line includes 'doctype plist public' and an Apple URL. The fourth line is a dict tag. The fifth line is a key, and subsequent lines contain keys, strings and arrays.">}}

3. Insert this code into the first line after the `<dict>`:

   ```{class="line-numbers linkable-line-numbers"}
     <key>NSLocalNetworkUsageDescription</key>
     <string>Smart Machine App requires access to your device's local network to connect to your devices.</string>
     <key>NSBonjourServices</key>
     <array>
         <string>_rpc._tcp</string>
     </array>
   ```

   {{<imgproc src="/tutorials/flutter-app/info-plist-insert.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="The info.plist file open in VS Code. An arrow labeled 'insert here' indicates that you should insert the code right after the fourth line in the file.">}}

   The file should now look like the following:

   {{<imgproc src="/tutorials/flutter-app/info-plist-pasted.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="The resulting file. After the non-indented <dict> tag on the fourth line, the pasted key, string, key, and array (containing an indented string) are indented inside the dict tag, spanning lines five through ten. The pasted content is at the same level of indentation as the rest of the keys and strings below it.">}}

### Create the main file

1. Open the <file>lib/main.dart</file> file.

2. Replace the contents of this file with the following code to make up the login screen for your app:

   ```{class="line-numbers linkable-line-numbers"}
   import 'package:flutter/material.dart';
   import 'package:flutter_dotenv/flutter_dotenv.dart';

   void main() async {
      await dotenv.load();
     runApp(MyApp());
   }

   class MyApp extends StatelessWidget {
     const MyApp({super.key});

     @override
     Widget build(BuildContext context) {
       return MaterialApp(
         title: 'Smart Machine App',
         theme: ThemeData(
           colorScheme: ColorScheme.fromSeed(seedColor: Colors.purple),
         ),
         home: MyHomePage(),
       );
     }
   }

   class MyHomePage extends StatelessWidget {
     @override
     Widget build(BuildContext context) {
       return Scaffold(
         body: Center(
           child: Column(
             mainAxisAlignment: MainAxisAlignment.center,
             children: [
               Text('Smart Machine App'),
               SizedBox(height: 16),
               ElevatedButton(onPressed: null, child: Text('Login')),
             ],
           ),
         ),
       );
     }
   }


   ```

   If you chose a name other than `Smart Machine App` for your project, edit lines 13 and 30 with your own app title.

### Launch the app

In this section of the tutorial we'll build the app and see what it looks like so far.

1. Open <file>lib/main.dart</file>.
   In the bottom right corner of VS Code, find the button that shows the current target device.
   Click the button to change your target device.
   Make sure that you have your target device selected before you continue.

   {{<imgproc src="/tutorials/flutter-app/target-device-button.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="A VS Code window with main.dart open. In the bottom right corner, there is a target device button labeled 'iPhone 14 (ios simulator)'.">}}

2. With <file>lib/main.dart</file> still open, find the "Start Debugging" button in the upper right corner of the VS Code window.
   Click the button to build and render your app

   {{<imgproc src="/tutorials/flutter-app/main-play.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="A VS Code window with main.dart open. In the top right corner, there is a button labeled 'Start Debugging' with an icon of a bug and a 'play' symbol.">}}

   A window should open up, displaying a rendering of your smart machine app:

   {{<imgproc src="/tutorials/flutter-app/render1.png" resize="1200x" style="max-width:300px" declared-dimensions="true" alt="Rendering of an iPhone with the app open on the screen. The screen is white with the words 'Smart Machine App' in the middle, above a grayed-out login button.">}}

## Add app navigation

### Add a new screen

Great work so far!
Your app is successfully running, with a single screen and an inactive button.
Next you will add a new screen that pulls in some information from your {{< glossary_tooltip term_id="organization" text="organization" >}} in Viam, and then navigate to that screen from the login button.

In the VS Code file explorer on the left-hand side, right click <file>lib/</file> and click **New File**, then name the new file <file>home_screen.dart</file>.

Paste the following code into the <file>home_screen.dart</file> file you just created:

```{class="line-numbers linkable-line-numbers"}
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Viam _viam;
  late Organization _organization;
  List<Location> _locations = [];
  bool _loading = true;

  @override
  void initState() {
    _getData();
    super.initState();
  }

  void _getData() async {
    try {
      _viam = await Viam.withApiKey(dotenv.env['API_KEY_ID']?? '', dotenv.env['API_KEY']?? '');
      _organization = (await _viam.appClient.listOrganizations()).first;
      _locations = await _viam.appClient.listLocations(_organization);

      // in Flutter setState tells the UI to rebuild the widgets whose state has changed,
      // this is how we change from showing a loading screen to a list of values
      setState(() {
        _loading = false;
      });
    } catch (e) {
      print(e);
    }
  }

  /// This method will navigate to a specific [Location].
  void _navigateToLocation(Location location) {
    // Navigator.of(context)
    //     .push(MaterialPageRoute(builder: (_) => LocationScreen(_viam, location)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Locations')),
      // If we are loading, show a loading indicator.
      // Otherwise, show a list of [Locations]s.
      body: _loading
          ? Center(
              child: const CircularProgressIndicator.adaptive(),
            )
          : // Build a list from the [_locations] state.
          ListView.builder(
              itemCount: _locations.length,
              itemBuilder: (_, index) {
                final location = _locations[index];
                return ListTile(
                  title: Text(location.name),
                  onTap: () => _navigateToLocation(location),
                  trailing: const Icon(Icons.chevron_right),
                );
              },
            ),
    );
  }
}
```

### Get the Viam API key

Notice in the file the following line:

```{class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(dotenv.env['API_KEY_ID']?? '', dotenv.env['API_KEY']?? '');
```

This line in the code defines how your Flutter app authenticates to the Viam platform, by referencing two environment variables that together comprise your Viam API key.

Follow the steps below to get your API key and create an environment variables file to store them in:

1. In your project folder, create a file to store your API keys.
   Name it <file>.env</file>.
   Copy and paste these two lines into the file:

   ```{class="line-numbers linkable-line-numbers"}
   API_KEY_ID="PASTE YOUR API KEY ID HERE"
   API_KEY="PASTE YOUR API KEY HERE"
   ```

2. Go to the [Viam app](https://app.viam.com) and log in.

3. Click the organization dropdown menu on the right side of the top banner.
   If you're not already in the organization you want to connect to, click the correct organization name to navigate to it.

   {{<imgproc src="/tutorials/flutter-app/org-dropdown.png" resize="1200x" style="max-width:800px" declared-dimensions="true" alt="The Viam web app with the organization dropdown labeled 'Clint's Org' highlighted.">}}

4. Click the organization dropdown menu again and click **Settings**.

5. Scroll to the **API Keys** section.
   You can find and use an existing API key for your smart machine, or you can create a new one for this application.
   For this tutorial we will create a new one:

   1. Click **Generate key**.
   2. Give the key a name like "flutter-app-my-org-name."
   3. Click the **Resource** dropdown and select your organization.
   4. Set **Role** to **Owner**.
   5. Click **Generate key**.
   6. Find your new key at the bottom of the list.

6. Use the copy buttons next to the API key ID and API key to copy each of them and paste them into your <file>.env</file> file.

{{< readfile "/static/include/snippet/secret-share.md" >}}

### Connect the login button to the home screen

In VS Code, reopen <file>main.dart</file>.

Add the following line to the imports at the top of the file:

```{class="line-numbers linkable-line-numbers"}
import 'home_screen.dart';
```

Change `ElevatedButton` in the `Column` to the following:

```{class="line-numbers linkable-line-numbers"}
            ElevatedButton(
                onPressed: () => Navigator.of(context)
                    .push(MaterialPageRoute(builder: (_) => HomeScreen())),
                child: Text('Login'),
            ),
```

Run the mobile application simulator again to see how your changes have taken effect.
Now, when you tap the login button, the app uses the API key to get the list of locations in your organization.
It displays the names of the locations on a new screen:

{{<gif webm_src="/tutorials/flutter-app/locations-list.webm" mp4_src="/tutorials/flutter-app/locations-list.mp4" alt="Rendering of a mobile app. Log in is clicked, and then all the locations in Clint's organization are shown. One of them is clicked, but nothing changes because there is no screen associated with that button yet." max-width="300px">}}

## Add more screens

### Add a location screen

So far, you have an app that displays a list of {{< glossary_tooltip term_id="location" text="locations" >}}, but nothing happens when you tap a location name.
In this step you will add functionality so that tapping a location name brings you to the list of {{< glossary_tooltip term_id="smart machine" text="smart machines" >}} in that location.

In VS Code create a new file in the same folder as <file>main.dart</file> and <file>home_screen.dart</file>.
Name it <file>location_screen.dart</file>.

Paste the following code into the file:

```{class="line-numbers linkable-line-numbers"}
import 'package:flutter/material.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';

import 'robot_screen.dart';

class LocationScreen extends StatefulWidget {
  /// The authenticated Viam instance.
  /// See previous screens for more details.
  final Viam _viam;

  /// The [Location] to show details for
  final Location location;

  const LocationScreen(this._viam, this.location, {super.key});

  @override
  State<LocationScreen> createState() => _LocationScreenState();
}

class _LocationScreenState extends State<LocationScreen> {
  /// Similar to previous screens, start with [_isLoading] to true.
  bool _isLoading = true;

  /// A list of [Robot]s available in this [Location].
  List<Robot> robots = [];

  @override
  void initState() {
    super.initState();
    // Call our own _initState method to initialize our state.
    _initState();
  }

  /// This method will get called when the widget initializes its state.
  /// It exists outside the overridden [initState] function since it's async.
  Future<void> _initState() async {
    // Using the authenticated [Viam] client received as a parameter,
    // we can obtain a list of smart machines (robots) within this location.
    final robots = await widget._viam.appClient.listRobots(widget.location);
    setState(() {
      // Once we have the list of robots, we can set the state.
      this.robots = robots;
      _isLoading = false;
    });
  }

  void _navigateToRobot(Robot robot) {
    Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => RobotScreen(widget._viam, robot)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.location.name),
      ),
      // If we are loading, show a loading indicator.
      // Otherwise, show a list of [Robot]s.
      body: _isLoading
          ? const CircularProgressIndicator.adaptive()
          : // Build a list from the [locations] state.
          ListView.builder(
              itemCount: robots.length,
              itemBuilder: (_, index) {
                final robot = robots[index];
                return ListTile(
                  title: Text(robot.name),
                  onTap: () => _navigateToRobot(robot),
                  trailing: const Icon(Icons.chevron_right),
                );
              }),
    );
  }
}

```

### Add a robot screen

Create a new file named <file>robot_screen.dart</file> and paste the following into the file:

```{class="line-numbers linkable-line-numbers"}
/// This is the screen that shows the resources available on a robot (or smart machine).
/// It takes in a Viam app client instance, as well as a robot client.
/// It then uses the Viam client instance to create a connection to that robot client.
/// Once the connection is established, we can view the resources available
/// and send commands to them.

import 'package:flutter/material.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';

class RobotScreen extends StatefulWidget {
  final Viam _viam;
  final Robot robot;

  const RobotScreen(this._viam, this.robot, {super.key});

  @override
  State<RobotScreen> createState() => _RobotScreenState();
}

class _RobotScreenState extends State<RobotScreen> {
  /// Similar to previous screens, start with [_isLoading] to true.
  bool _isLoading = true;

  /// This is the [RobotClient], which allows you to access
  /// all the resources of a Viam Smart Machine.
  /// This differs from the [Robot] provided to us in the widget constructor
  /// in that the [RobotClient] contains a direct connection to the Smart Machine
  /// and its resources. The [Robot] object simply contains information about
  /// the Smart Machine, but is not actually connected to the machine itself.
  ///
  /// This is initialized late because it requires an asynchronous
  /// network call to establish the connection.
  late RobotClient client;

  @override
  void initState() {
    super.initState();
    // Call our own _initState method to initialize our state.
    _initState();
  }

  @override
  void dispose() {
    // You should always close the [RobotClient] to free up resources.
    // Calling [RobotClient.close] will clean up any tasks and
    // resources created by Viam.
    client.close();
    super.dispose();
  }

  /// This method will get called when the widget initializes its state.
  /// It exists outside the overridden [initState] function since it's async.
  Future<void> _initState() async {
    // Using the authenticated [Viam] the received as a parameter,
    // we can obtain a connection to the Robot.
    // There is a helpful convenience method on the [Viam] instance for this.
    final robotClient = await widget._viam.getRobotClient(widget.robot);
    setState(() {
      client = robotClient;
      _isLoading = false;
    });
  }

  /// A computed variable that returns the available [ResourceName]s of
  /// this robot in an alphabetically sorted list.
  List<ResourceName> get _sortedResourceNames {
    return client.resourceNames..sort((a, b) => a.name.compareTo(b.name));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text(widget.robot.name)),
        body: _isLoading
            ? const Center(child: CircularProgressIndicator.adaptive())
            : ListView.builder(
                itemCount: client.resourceNames.length,
                itemBuilder: (_, index) {
                  final resourceName = _sortedResourceNames[index];
                  return ListTile(
                    title: Text(resourceName.name),
                    subtitle: Text(
                        '${resourceName.namespace}:${resourceName.type}:${resourceName.subtype}'),
                  );
                }));
  }
}

```

### Connect the screens together

Now that you have the code for the screens in place, you can enable navigation between them.

Connect the home screen to the locations screen by un-commenting the following two lines in <file>home_screen.dart</file>:

```{class="line-numbers linkable-line-numbers" data-line="3-4"}
 /// This method will navigate to a specific [Location]. <-- Leave this commented!
 void _navigateToLocation(Location location) {
    Navigator.of(context)                              <-- Un-comment this
        .push(MaterialPageRoute(builder: (_) => LocationScreen(_viam, location))); <-- And un-comment this
 }
```

Add the following import to the top of the file:

```{class="line-numbers linkable-line-numbers"}
import 'location_screen.dart';
```

The whole <file>home_screen.dart</file> should now look like this:

```{class="line-numbers linkable-line-numbers"}
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';

import 'location_screen.dart';          // <---- Added import

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  late Viam _viam;
  late Organization _organization;
  List<Location> _locations = [];
  bool _loading = true;

  @override
  void initState() {
    _getData();
    super.initState();
  }

  void _getData() async {
    try {
      _viam = await Viam.withApiKey(dotenv.env['API_KEY_ID']?? '', dotenv.env['API_KEY']?? '');
      _organization = (await _viam.appClient.listOrganizations()).first;
      _locations = await _viam.appClient.listLocations(_organization);

      // in Flutter setState tells the UI to rebuild the widgets whos state has changed,
      // this is how we change from showing a loading screen to a list of values
      setState(() {
        _loading = false;
      });
    } catch (e) {
      print(e);
    }
  }

  /// This method will navigate to a specific [Location].
  void _navigateToLocation(Location location) {
    Navigator.of(context).push(                                                                // <-- uncommented
        MaterialPageRoute(builder: (_) => LocationScreen(_viam, location)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('Locations')),
        // If we are loading, show a loading indicator.
        // Otherwise, show a list of [Locations]s.
        body: _loading
            ? Center(
                child: const CircularProgressIndicator.adaptive(),
              )
            : // Build a list from the [_locations] state.
            ListView.builder(
                itemCount: _locations.length,
                itemBuilder: (_, index) {
                  final location = _locations[index];
                  return ListTile(
                    title: Text(location.name),
                    onTap: () => _navigateToLocation(location),
                    trailing: const Icon(Icons.chevron_right),
                  );
                }));
  }
}
```

Try running your app.
Now, when you tap a location, you'll see a list of the smart machines in that location.
When you tap one of them, you'll see a list of that machine's {{< glossary_tooltip term_id="resource" text="resources" >}}:

{{<gif webm_src="/tutorials/flutter-app/demo.webm" mp4_src="/tutorials/flutter-app/demo.mp4" alt="Rendering of the mobile app. Log in is clicked, then all Clint's locations are shown, Clint's Desk it clicked, all its smart machines are listed, and then desk-robot is clicked, showing a list of components and services belonging to that smart machine." max-width="300px">}}

## Next steps

Congratulations!
You have successfully made a Flutter app integrated with Viam!

At this point you could customize the robot screen to have more functionality to control the machine or to show data from the robot in neat ways.
The Viam GitHub repo contains [more example apps](https://github.com/viamrobotics/viam-flutter-sdk/tree/main/example) for your reference.

Flutter is a very powerful tool for building user interfaces.
You can stylize the look and feel of your app to match your brand.
Look around [the Flutter documentation](https://docs.flutter.dev/) to learn how.

Before releasing your app to the app stores you’ll need to add an authentication flow to your app instead of adding API keys as environment variables.
If you need assistance with this, reach out to us on our Discord and we’ll be happy to help.

When you’re ready to publish your app to the app stores you can follow these articles from Flutter on the subject:

- [iOS](https://docs.flutter.dev/deployment/ios)
- [Android](https://docs.flutter.dev/deployment/android)
