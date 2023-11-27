<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`GetControls`](/build/configure/components/input-controller/#getcontrols) | Get a list of input `Controls` that this Controller provides.
[`GetEvents`](/build/configure/components/input-controller/#getevents) | Get the current state of the Controller as a map of the most recent [Event](/build/configure/components/input-controller/#event-object) for each [Control](/build/configure/components/input-controller/#control-field).
[`RegisterControlCallback`](/build/configure/components/input-controller/#registercontrolcallback) | Define a callback function to execute whenever one of the [`EventTypes`](/build/configure/components/input-controller/#eventtype-field) selected occurs on the given [Control](/build/configure/components/input-controller/#control-field).
[`GetGeometries`](/build/configure/components/input-controller/#getgeometries) | Get all the geometries associated with the input controller in its current configuration, in the [frame](/mobility/frame-system/) of the input controller.
[`TriggerEvent`](/build/configure/components/input-controller/#triggerevent) | Trigger an event on the controller.
[`DoCommand`](/build/configure/components/input-controller/#docommand) | Send or receive model-specific commands.
[`Close`](/build/configure/components/input-controller/#close) | Safely shut down the resource and prevent further use.
