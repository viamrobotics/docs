<!-- preserve-formatting -->
The precision and reliability metrics of the movement sensor, which vary depending on model.
  This type contains the following fields:

  - `AccuracyMap` [(map[string]float32)](https://pkg.go.dev/builtin#string): A mapping of specific measurement parameters to their accuracy values.
    The keys are string identifiers for each measurement (for example, "Hdop", "Vdop"), and the values are their corresponding accuracy levels as float32.
  - `Hdop` [(float32)](https://pkg.go.dev/builtin#float32): Horizontal Dilution of Precision (HDOP) value.
    It indicates the level of accuracy of horizontal measurements.
    Lower values indicate improved reliability of positional measurements.
  - `Vdop` [(float32)](https://pkg.go.dev/builtin#float32): Vertical Dilution of Precision (VDOP) value.
    Similar to HDOP, it denotes the accuracy level of vertical measurements.
    Lower values indicate improved reliability of positional measurements.
  - `NmeaFix` [(int32)](https://pkg.go.dev/builtin#int32): An integer value representing the quality of the NMEA fix.
    See [Novatel documentation](https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm#GPSQualityIndicators) for the meaning of each fix value.
  - `CompassDegreeError` [(float32)](https://pkg.go.dev/builtin#float32): The estimated error in compass readings, measured in degrees.
    This signifies the deviation or uncertainty in the sensor's compass measurements.
    A lower value implies a more accurate compass direction.
