import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';
import 'location_screen.dart';

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
      _locations = await _viam.appClient.listLocations(_organization.id);

      // in Flutter, setState tells the UI to rebuild the widgets whose state has changed,
      // this is how you change from showing a loading screen to a list of values
      setState(() {
        _loading = false;
      });
    } catch (e) {
      print(e);
    }
  }

  /// This method will navigate to a specific [Location].
  void _navigateToLocation(Location location) {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (_) => LocationScreen(_viam, location)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Locations')),
      // If the list is loading, show a loading indicator.
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