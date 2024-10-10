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
    // you can obtain a list of smart machines (robots) within this location.
    final robots = await widget._viam.appClient.listRobots(widget.location.id);
    setState(() {
      // Once you have the list of robots, you can set the state.
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
      // If the list is loading, show a loading indicator.
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