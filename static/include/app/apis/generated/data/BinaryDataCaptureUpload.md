### BinaryDataCaptureUpload

{{< tabs >}}
{{% tab name="Python" %}}

Upload binary sensor data.

**Parameters:**

- `binary_data` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes-objects) (required): The data to be uploaded, represented in bytes.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Part ID of the component used to capture the data.
- `component_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Type of the component used to capture the data (e.g., “movement_sensor”).
- `component_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the component used to capture the data.
- `method_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the method used to capture the data.
- `file_extension` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The file extension of binary data including the period, e.g. .jpg, .png, .pcd. The backend will route the binary to its corresponding mime type based on this extension. Files with a .jpeg, .jpg, or .png extension will be saved to the images tab.
- `method_parameters` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Optional dictionary of method parameters. No longer in active use.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>) (optional): Optional list of tags to allow for tag-based data filtering when retrieving data.
- `data_request_times` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>) (optional): Optional tuple containing `datetime`s objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): the file_id of the uploaded data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload).

``` python {class="line-numbers linkable-line-numbers"}
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.binary_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='camera',
    component_name='my_camera',
    method_name='GetImages',
    method_parameters=None,
    tags=["tag_1", "tag_2"],
    data_request_times=[time_requested, time_received],
    file_extension=".jpg",
    binary_data=b"Encoded image bytes"
)
```

{{% /tab %}}
{{< /tabs >}}
