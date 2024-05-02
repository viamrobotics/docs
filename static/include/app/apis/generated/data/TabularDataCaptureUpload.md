### TabularDataCaptureUpload

{{< tabs >}}
{{% tab name="Python" %}}

Upload tabular sensor data.

**Parameters:**

- `tabular_data` [(List[Mapping[str, Any]])](<INSERT PARAM TYPE LINK>) (required): List of the data to be uploaded, represented tabularly as a collection of dictionaries.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Part ID of the component used to capture the data.
- `component_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Type of the component used to capture the data (e.g., “movement_sensor”).
- `component_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the component used to capture the data.
- `method_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the method used to capture the data.
- `method_parameters` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Optional dictionary of method parameters. No longer in active use.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>) (optional): Optional list of tags to allow for tag-based data filtering when retrieving data.
- `data_request_times` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>) (optional): Optional list of tuples, each containing datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor. Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the same metadata.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): the file_id of the uploaded data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload).

``` python {class="line-numbers linkable-line-numbers"}
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.tabular_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    tags=["tag_1", "tag_2"],
    data_request_times=[(time_requested, time_received)],
    tabular_data=[{'PowerPCT': 0, 'IsPowered': False}]
)
```

{{% /tab %}}
{{< /tabs >}}
