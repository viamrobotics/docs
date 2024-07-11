### BinaryDataCaptureUpload

Upload binary data collected on your machine through a specific component and the relevant metadata to the [Viam app](https://app.viam.com).
Uploaded binary data can be found under the **Images**, **Point clouds**, or **Files** subtab of the app's [**Data** tab](https://app.viam.com/data), depending on the type of data that you upload.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_data` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): The data to be uploaded, represented in bytes.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the component used to capture the data.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Type of the component used to capture the data (for example, “movement_sensor”).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the component used to capture the data.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the method used to capture the data.
- `file_extension` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The file extension of binary data including the period, for example .jpg, .png, .pcd. The backend will route the binary to its corresponding mime type based on this extension. Files with a .jpeg, .jpg, or .png extension will be saved to the images tab.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of method parameters. No longer in active use.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based data filtering when retrieving data.
- `data_request_times` (Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html)]) (optional): Optional tuple containing datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The file_id of the uploaded data.

**Raises:**

- (GRPCError): If an invalid part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload).

{{% /tab %}}
{{< /tabs >}}

### TabularDataCaptureUpload

Upload tabular data collected on your machine through a specific [component](/components/) to the [Viam app](https://app.viam.com).
Uploaded tabular data can be found under the **Sensors** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `tabular_data` (List[Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]]) (required): List of the data to be uploaded, represented tabularly as a collection of dictionaries.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the component used to capture the data.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Type of the component used to capture the data (for example, “movement_sensor”).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the component used to capture the data.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the method used to capture the data.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of method parameters. No longer in active use.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based data filtering when retrieving data.
- `data_request_times` (List[Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html)]]) (optional): Optional list of tuples, each containing datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor. Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the same metadata.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The file_id of the uploaded data.

**Raises:**

- (GRPCError): If an invalid part ID is passed.
- (ValueError): If a list of Timestamp objects is provided and its length does not match the length of the list of tabular data.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload).

{{% /tab %}}
{{< /tabs >}}

### FileUpload

Upload arbitrary files stored on your machine to the [Viam app](https://app.viam.com) by file name.
If uploaded with a file extension of <file>.jpeg/.jpg/.png</file>, uploaded files can be found in the **Images** subtab of the app's [**Data** tab](https://app.viam.com/data).
If <file>.pcd</file>, the uploaded files can be found in the **Point clouds** subtab.
All other types of uploaded files can be found under the **Files** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the resource associated with the file.
- `data` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): Bytes representing file data to upload.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional type of the component associated with the file (for example, “movement_sensor”).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the component associated with the file.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the method associated with the file.
- `file_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the file. The empty string “” will be assigned as the file name if one isn’t provided.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of the method parameters. No longer in active use.
- `file_extension` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional file extension. The empty string “” will be assigned as the file extension if one isn’t provided. Files with a .jpeg, .jpg, or .png extension will be saved to the images tab.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based filtering when retrieving data.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ID of the new file.

**Raises:**

- (GRPCError): If an invalid part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload(
    data=b"Encoded image bytes",
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    file_name="your-file",
    file_extension=".txt"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload).

{{% /tab %}}
{{< /tabs >}}

### FileUploadFromPath

Upload files stored on your machine to the [Viam app](https://app.viam.com) by filepath.
Uploaded files can be found under the **Files** subtab of the app's [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filepath` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Absolute filepath of file to be uploaded.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the component associated with the file.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional type of the component associated with the file (for example, “movement_sensor”).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the component associated with the file.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the method associated with the file.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of the method parameters. No longer in active use.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based filtering when retrieving data.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ID of the new file.

**Raises:**

- (GRPCError): If an invalid part ID is passed.
- (FileNotFoundError): If the provided filepath is not found.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload_from_path(
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    filepath="/Users/<your-username>/<your-directory>/<your-file.txt>"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path).

{{% /tab %}}
{{< /tabs >}}

### StreamingDataCaptureUpload

Upload the contents of streaming binary data and the relevant metadata to the [Viam app](https://app.viam.com).
Uploaded streaming data can be found under the [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `data` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): the data to be uploaded.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the resource associated with the file.
- `file_ext` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): file extension type for the data. required for determining MIME type.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional type of the component associated with the file (for example, “movement_sensor”).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the component associated with the file.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the method associated with the file.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of the method parameters. No longer in active use.
- `data_request_times` (Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html)]) (optional): Optional tuple containing datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based filtering when retrieving data.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The file_id of the uploaded data.

**Raises:**

- (GRPCError): If an invalid part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.streaming_data_capture_upload(
    data="byte-data-to-upload",
    part_id="INSERT YOUR PART ID",
    file_ext="png",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    data_request_times=[(time_requested, time_received)],
    tags=["tag_1", "tag_2"]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.streaming_data_capture_upload).

{{% /tab %}}
{{< /tabs >}}
