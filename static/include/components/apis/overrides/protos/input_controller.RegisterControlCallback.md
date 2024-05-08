Defines a callback function to execute whenever one of the [EventTypes](#eventtype-field) selected occurs on the given [Control](#control-field).

You can only register one callback function per [Event](#event-object) for each [Control](#control-field).
A second call to register a callback function for a [EventType](#eventtype-field) on a [Control](#control-field) replaces any function that was already registered.

You can pass a `nil` function here to "deregister" a callback.

{{% alert title="Tip" color="tip" %}}
Registering a callback for the `ButtonChange` [EventType](#eventtype-field) is merely a convenience for filtering.
Doing so registers the same callback to both `ButtonPress` and `ButtonRelease`, but `ButtonChange` is not reported in an actual [Event Object](#event-object).
{{% /alert %}}
