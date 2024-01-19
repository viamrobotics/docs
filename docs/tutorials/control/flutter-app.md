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
  {{<gif webm_src="/tutorials/flutter-app/demo.webm" mp4_src="/tutorials/flutter-app/demo.mp4" alt="Rendering of a mobile app. Log in is clicked, and then all the robots at Clint's Desk are shown.">}}
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
For the purpose of this tutorial, pick either iOS or Android to develop with for now.

You can always run your app on another platform later.
It's just easier to have a clear development target in mind; it makes the next step smoother.

### Install Flutter

Install Flutter according to [the Flutter documentation](https://docs.flutter.dev/get-started/install).
The instructions on the Flutter website cover not only the installation of the SDK itself, but also the development target-related tools and the editor plugins.
For this walkthrough, you only need to install the following:

- Flutter SDK
- Visual Studio Code with the Flutter extension
- The software required by your chosen development target.
  For example:
  - [Xcode](https://developer.apple.com/xcode/) to target macOS
  - [Visual Studio](https://visualstudio.microsoft.com/) to target Windows

## Create a project

### Create your first Flutter project

1. Launch VS Code and open the command palette (with `F1` or `Ctrl+Shift+P` or `Shift+Cmd+P`).

2. Start typing "flutter new."
   Select the **Flutter: New Project** command.

{{<imgproc src="/tutorials/flutter-app/flutter-new-project.png" resize="1200x" style="max-width:800px" declared-dimensions="true" alt="Creating a new project in VS Code.">}}

3. Next, select **Application** and then a folder in which to create your project.
   This could be your home directory, or something like <file>C:\src\</file>.
4. Finally, name your project something like <file>smart_machine_app</file> or <file>my_awesome_smart_machine</file>.

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

   3. Next, open another configuration file in the project, <file>analysis_options.yaml</file>.
      This file determines how strict Flutter should be when analyzing your code.
      Since this is your first foray into Flutter, you're telling the analyzer to take it easy.
      You can always tune this later.
      In fact, as you get closer to publishing an actual production app, you will almost certainly want to make the analyzer stricter than this.

   4. Replace its contents with the following:

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

### Configure iOS or Android-specific code

Now you'll update some configurations in the iOS or Android-specific code to support the [Viam Flutter SDK](https://flutter.viam.dev/).

{{< tabs >}}
{{% tab name="iOS" %}}

1. Open <file>ios/Podfile</file>.
   If Podfile does not exist in that directory, you can generate it by running `flutter pub get` in the root directory of your app.

   At the top of the file you will see the following lines:

   ```{class="line-numbers linkable-line-numbers"}
   # Uncomment this line to define a global platform for your project
   # platform :ios, '11.0'
   ```

   Change that to this:

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
      <string>Smart Machine App requires access to your devices local network to connect to your devices.</string>
      <key>NSBonjourServices</key>
      <array>
          <string>_rpc._tcp</string>
      </array>
   ```

   {{<imgproc src="/tutorials/flutter-app/info-plist-insert.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="The info.plist file open in VS Code. An arrow labeled 'insert here' indicates that you should insert the code right after the fourth line in the file.">}}

   It should look like this:

   {{<imgproc src="/tutorials/flutter-app/info-plist-pasted.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="The resulting file. After the non-indented <dict> tag on the fourth line, the pasted key, string, key, and array (containing an indented string) are indented inside the dict tag, spanning lines five through ten. The pasted content is at the same level of indentation as the rest of the keys and strings below it.">}}

{{% /tab %}}
{{% tab name="Android" %}}

```{class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

### Create the main file

1. Open the <file>main.dart</file> file under the <file>lib/</file> directory.

2. Replace the contents of this file with the following code to make up the login screen for your app:

   ```{class="line-numbers linkable-line-numbers"}
   import 'package:flutter/material.dart';

   void main() {
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

   In the next section we'll build the app and see what it looks like so far, and then add the remaining pieces.

## Add app navigation

This section of the tutorial adds a new screen to your app, and makes it so that pressing the `login` button navigates to the new screen.

### Launch the app

1. Open <file>lib/main.dart</file>.
   In the bottom right corner of VS Code, you'll find a button that shows the current target device.
   Click the button to change your target device.
   Make sure that you have your target device selected before you continue.

   {{<imgproc src="/tutorials/flutter-app/target-device-button.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="A VS Code window with main.dart open. In the bottom right corner, there is a target device button labeled 'iPhone 14 (ios simulator)'.">}}

2. With <file>lib/main.dart</file> still open, find the "play" button in the upper right corner of the VS Code window.
   Click it.

   {{<imgproc src="/tutorials/flutter-app/main-play.png" resize="1200x" style="max-width:900px" declared-dimensions="true" alt="A VS Code window with main.dart open. In the top right corner, there is a play button with an icon of a bug and a 'play' symbol.">}}

   A window should open up, displaying a rendering of your smart machine app:

   {{<imgproc src="/tutorials/flutter-app/render1.png" resize="1200x" style="max-width:300px" declared-dimensions="true" alt="Rendering of an iPhone with the app open on the screen. The screen is white with the words 'Smart Machine App' in the middle, above a grayed-out login button.">}}

## Add a new screen

Great work so far!
You have your app running, with a single screen and an inactive button.
Next you will add a new screen that pulls in some information from your {{< glossary_tooltip term_id="organization" text="organization" >}} in Viam, and then navigate to that screen from the login button.
