## `network_configuration`

The `network_configuration` section configures network-related settings for the Viam Agent. This includes device information that appears during Bluetooth provisioning:

```json
{
  "network_configuration": {
    "manufacturer": "Viam Inc", // Manufacturer name shown during BT provisioning
    "model": "Robot-X1",        // Model name shown during BT provisioning  
    "fragment_id": "robot-1",   // Fragment ID shown during BT provisioning
    "wifi": [
      {
        "ssid": "MyWiFi",
        "psk": "MyPassword" 
      }
    ]
  }
}
```