/// This is the BaseScreen, which allows us to control a Base.

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