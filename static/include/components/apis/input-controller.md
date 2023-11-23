<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`GetControls`](/platform/build/configure/components/input-controller/#getcontrols) | Get a list of input `Controls` that this Controller provides.
[`GetEvents`](/platform/build/configure/components/input-controller/#getevents) | Get the current state of the Controller as a map of the most recent [Event](/platform/build/configure/components/input-controller/#event-object) for each [Control](/platform/build/configure/components/input-controller/#control-field).
[`RegisterControlCallback`](/platform/build/configure/components/input-controller/#registercontrolcallback) | Define a callback function to execute whenever one of the [`EventTypes`](/platform/build/configure/components/input-controller/#eventtype-field) selected occurs on the given [Control](/platform/build/configure/components/input-controller/#control-field).
[`GetGeometries`](/platform/build/configure/components/input-controller/#getgeometries) | Get all the geometries associated with the input controller in its current configuration, in the [frame](/platform/build/configure/services/frame-system/) of the input controller.
[`TriggerEvent`](/platform/build/configure/components/input-controller/#triggerevent) | Trigger an event on the controller.
[`DoCommand`](/platform/build/configure/components/input-controller/#docommand) | Send or receive model-specific commands.
[`Close`](/platform/build/configure/components/input-controller/#close) | Safely shut down the resource and prevent further use.
