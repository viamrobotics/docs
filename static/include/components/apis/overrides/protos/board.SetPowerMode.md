Set the board to the indicated `PowerMode`.

{{% alert title="Info" color="info" %}}

This method may not receive a successful response from gRPC when you set the board to the offline power mode `PowerMode.POWER_MODE_OFFLINE_DEEP`.

When this is the case for your board model, the call is returned with an error specifying that the remote procedure call timed out or that the endpoint is no longer available.
This is expected: the board has been successfully powered down and can no longer respond to messages.

{{% /alert %}}
