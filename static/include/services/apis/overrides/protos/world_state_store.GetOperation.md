Get the Operation associated with the currently running function.

When writing custom resources, you should get the Operation by calling this function and check to see if it’s cancelled. If the Operation is cancelled, then you can perform any necessary operations such as, for example, terminating long running tasks or cleaning up connections.
