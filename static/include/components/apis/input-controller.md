<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`GetControls`](/machine/components/input-controller/#getcontrols) | Get a list of input `Controls` that this Controller provides.
[`GetEvents`](/machine/components/input-controller/#getevents) | Get the current state of the Controller as a map of the most recent [Event](/machine/components/input-controller/#event-object) for each [Control](/machine/components/input-controller/#control-field).
[`RegisterControlCallback`](/machine/components/input-controller/#registercontrolcallback) | Define a callback function to execute whenever one of the [`EventTypes`](/machine/components/input-controller/#eventtype-field) selected occurs on the given [Control](/machine/components/input-controller/#control-field).
[`GetGeometries`](/machine/components/input-controller/#getgeometries) | Get all the geometries associated with the input controller in its current configuration, in the [frame](/machine/services/frame-system/) of the input controller.
[`TriggerEvent`](/machine/components/input-controller/#triggerevent) | Trigger an event on the controller.
[`DoCommand`](/machine/components/input-controller/#docommand) | Send or receive model-specific commands.
[`Close`](/machine/components/input-controller/#close) | Safely shut down the resource and prevent further use.
