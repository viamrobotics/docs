<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`GetControls`](/components/input-controller/#getcontrols) | Get a list of input `Controls` that this Controller provides.
[`GetEvents`](/components/input-controller/#getevents) | Get the current state of the Controller as a map of the most recent [Event](/components/input-controller/#event-object) for each [Control](/components/input-controller/#control-field).
[`RegisterControlCallback`](/components/input-controller/#registercontrolcallback) | Define a callback function to execute whenever one of the [`EventTypes`](/components/input-controller/#eventtype-field) selected occurs on the given [Control](/components/input-controller/#control-field).
[`GetGeometries`](/components/input-controller/#getgeometries) | Get all the geometries associated with the input controller in its current configuration, in the [frame](/services/frame-system/) of the input controller.
[`DoCommand`](/components/input-controller/#docommand) | Send or receive model-specific commands.
