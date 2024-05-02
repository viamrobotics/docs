### DoCommand

{{< tabs >}}
{{% tab name="Python" %}}

Send/receive arbitrary commands.

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](<INSERT PARAM TYPE LINK>) (required): The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.do_command).

``` python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot, "builtin")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await motion.do_command(command=my_command)
```

{{% /tab %}}
{{< /tabs >}}
