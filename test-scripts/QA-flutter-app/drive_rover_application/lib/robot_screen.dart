import 'package:flutter/material.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';

import 'base_screen.dart';

class RobotScreen extends StatefulWidget {
  final Viam _viam;
  final Robot robot;

  const RobotScreen(this._viam, this.robot, {super.key});

  @override
  State<RobotScreen> createState() => _RobotScreenState();
}

class _RobotScreenState extends State<RobotScreen> {
  bool _isLoading = true;
  late RobotClient client;

  @override
  void initState() {
    super.initState();
    _initState();
  }

  @override
  void dispose() {
    if (_isLoading == false) {
      client.close();
    }
    super.dispose();
  }

  Future<void> _initState() async {
    final robotClient = await widget._viam.getRobotClient(widget.robot);
    setState(() {
      client = robotClient;
      _isLoading = false;
    });
  }

  List<ResourceName> get _sortedResourceNames {
    return client.resourceNames..sort((a, b) => a.name.compareTo(b.name));
  }

  bool _isNavigable(ResourceName rn) {
    if (rn.subtype == Base.subtype.resourceSubtype) {
      return true;
    }
    return false;
  }

  void _navigate(ResourceName rn) {
    if (rn.subtype == Base.subtype.resourceSubtype) {
      final base = Base.fromRobot(client, rn.name);
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => BaseScreen(base)));
    }
  }

  // New function to set motor power
  Future<void> _setMotorPower() async {
    try {
      // Assuming the first motor in the list is the one we want to control
      final motorName = client.resourceNames.firstWhere(
        (rn) => rn.subtype == Motor.subtype.resourceSubtype,
        orElse: () => throw Exception('No motor found'),
      );
      
      final myMotor = Motor.fromRobot(client, motorName.name);
      // await myMotor.setPower(0.4);
      // await myMotor.setRPM(-120.5);
      // await myMotor.goFor(60, 7.2);
      // await myMotor.goTo(75, 8.3);
      // await myMotor.resetZeroPosition(0.0);
      // var position = await myMotor.position();
      // var properties = await myMotor.properties();
      // var powerState = await myMotor.powerState();
      // var powered = powerState.isOn;
      // var pct = powerState.powerPct;
      // var moving = await myMotor.isMoving();
      // await myMotor.stop();
      // const command = {'cmd': 'test', 'data1': 500};
      // var result = myMotor.doCommand(command);
      // var name = Motor.getResourceName('myMotor');

      // Assuming the first motor in the list is the one we want to control
      final msName = client.resourceNames.firstWhere(
        (rn) => rn.subtype == MovementSensor.subtype.resourceSubtype,
        orElse: () => throw Exception('No movement sensor found'),
      );

      final myMovementSensor = MovementSensor.fromRobot(client, msName.name);

      // var linVel = await myMovementSensor.linearVelocity();
      // var angVel = await myMovementSensor.angularVelocity();
      // var compassHeading = await myMovementSensor.compassHeading();
      // var orientation = await myMovementSensor.orientation();
      // var position = await myMovementSensor.position();
      // var altitude = position.altitude;
      // var coordinates = position.coordinates;
      // var props = await myMovementSensor.properties();
      // var accuracy = await myMovementSensor.accuracy();
      // var linAccel = await myMovementSensor.linearAcceleration();
      // var readings = await myMovementSensor.readings();
      // const command = {'cmd': 'test', 'data1': 500};
      // var result = myMovementSensor.doCommand(command);

      // Assuming the first ps in the list is the one we want to control
      final psName = client.resourceNames.firstWhere(
        (rn) => rn.subtype == PowerSensor.subtype.resourceSubtype,
        orElse: () => throw Exception('No power sensor found'),
      );

      final myPowerSensor = PowerSensor.fromRobot(client, psName.name);

      // var voltageObject = await myPowerSensor.voltage();
      // double voltageInVolts = voltageObject.volts;
      // bool isItAC = voltageObject.isAc;
      // var currentObject = await myPowerSensor.current();
      // double amps = currentObject.amperes;
      // bool isItAC = currentObject.isAc;
      // var power = await myPowerSensor.power();
      // var readings = await myPowerSensor.readings();
      // const command = {'cmd': 'test', 'data1': 500};
      // var result = myPowerSensor.doCommand(command);

      // Assuming the first sensor in the list is the one we want to control
      final sensorName = client.resourceNames.firstWhere(
        (rn) => rn.subtype == Sensor.subtype.resourceSubtype,
        orElse: () => throw Exception('No sensor found'),
      );

      final mySensor = Sensor.fromRobot(client, sensorName.name);

      // var readings = await mySensor.readings();
      // const command = {'cmd': 'test', 'data1': 500};
      // var result = mySensor.doCommand(command);

      // Assuming the first servo in the list is the one we want to control
      final servoName = client.resourceNames.firstWhere(
        (rn) => rn.subtype == Servo.subtype.resourceSubtype,
        orElse: () => throw Exception('No servo found'),
      );

      final myServo = Servo.fromRobot(client, servoName.name);

      // // Move the servo from its origin to the desired angle of 30 degrees.
      // await myServo.move(30);
      // var angle = await myServo.position();
      // var isItMoving = await myServo.isMoving();
      // await myServo.stop();
      const command = {'cmd': 'test', 'data1': 500};
      var result = myServo.doCommand(command);

      // Change out what's inside of content depending on what you're testing
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
           content: Text(' ${result.toString()}'),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error setting motor power: $e')),
      );
    }
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
                  onTap: () => _navigate(resourceName),
                  trailing: _isNavigable(resourceName) ? Icon(Icons.chevron_right) : SizedBox.shrink(),
                );
              }),
      floatingActionButton: FloatingActionButton(
        onPressed: _setMotorPower,
        child: Icon(Icons.power),
        tooltip: 'Set Motor Power',
      ),
    );
  }
}