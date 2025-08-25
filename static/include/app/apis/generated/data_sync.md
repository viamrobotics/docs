### BinaryDataCaptureUpload

Upload binary data collected on your machine through a specific component and the relevant metadata to [Viam](https://app.viam.com).
Uploaded binary data can be found under the **Images**, **Point clouds**, or **Files** subtab of the [**Data** tab](https://app.viam.com/data), depending on the type of data that you upload.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `binary_data` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): The data to be uploaded, represented in bytes.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the component used to capture the data.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Type of the component used to capture the data (for example, “movement_sensor”).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the component used to capture the data.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the method used to capture the data.
- `file_extension` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The file extension of binary data, including the period, for example .jpg, .png, .pcd. The backend routes the binary to its corresponding mime type based on this extension. Files with a .jpeg, .jpg, or .png extension will appear in the Images tab.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of method parameters. No longer in active use.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based data filtering when retrieving data.
- `dataset_ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of datasets to add the data to.
- `data_request_times` (Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html)]) (optional): Optional tuple containing datetime objects denoting the times this data was requested [0] by the robot and received [1] from the appropriate sensor.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The binary data ID of the uploaded data.

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
    binary_data=b"Encoded image bytes",
    dataset_ids=["dataset_1", "dataset_2"]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `binaryData` (Uint8Array) (required): The data to be uploaded, represented in bytes.
- `partId` (string) (required): The part ID of the component used to capture the data.
- `componentType` (string) (required): The type of the component used to capture the data
  (for example, "movementSensor").
- `componentName` (string) (required): The name of the component used to capture the data.
- `methodName` (string) (required): The name of the method used to capture the data.
- `fileExtension` (string) (required): The file extension of binary data including the
  period, for example .jpg, .png, or .pcd. The backend will route the
  binary to its corresponding mime type based on this extension. Files with
  a .jpeg, .jpg, or .png extension will be saved to the images tab.
- `dataRequestTimes` (Date) (required): Tuple containing `Date` objects denoting the times
  this data was requested\[0] by the robot and received\[1] from the
  appropriate sensor.
- `tags` (string) (optional): The list of tags to allow for tag\-based filtering when
  retrieving data.
- `datasetIds` (string) (optional)

**Returns:**

- (Promise<string>): The binary data ID of the uploaded data.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const binaryDataId = await dataClient.binaryDataCaptureUpload(
  binaryData,
  '123abc45-1234-5678-90ab-cdef12345678',
  'rdk:component:camera',
  'my-camera',
  'ReadImage',
  '.jpg',
  [new Date('2025-03-19'), new Date('2025-03-19')]
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#binarydatacaptureupload).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `binaryData` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)\> (required)
- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `fileExtension` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `componentType` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `componentName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodParameters` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), Any\>? (optional)
- `dataRequestTimes` ([DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html), [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html))? (optional)
- `datasetIds` [Iterable](https://api.flutter.dev/flutter/dart-core/Iterable-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (optional)
- `tags` [Iterable](https://api.flutter.dev/flutter/dart-core/Iterable-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 try {
   final imageBytes = getPNGasBytes(); // Replace with your image bytes getter

   (DateTime, DateTime) dataRequestTimes = (
     DateTime(2025, 1, 15, 10, 30), // Start time
     DateTime(2025, 1, 15, 14, 45)  // End time
   );

   final binaryDataId = await dataClient.binaryDataCaptureUpload(
     imageBytes,
     "<YOUR-PART-ID>",
     ".png",
     componentType: "rdk:component:camera",
     componentName: "camera-1",
     methodName: "ReadImage",
     dataRequestTimes: dataRequestTimes);

   print('Successfully uploaded binary data with binaryDataId: $binaryDataId');
 } catch (e) {
   print('Error uploading binary data: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/binaryDataCaptureUpload.html).

{{% /tab %}}
{{< /tabs >}}

### TabularDataCaptureUpload

Upload tabular data collected on your machine through a specific {{< glossary_tooltip term_id="component" text="component" >}} to [Viam](https://app.viam.com).
Uploaded tabular data can be found under the **Sensors** subtab of the [**Data** tab](https://app.viam.com/data).

{{< alert title="Size limit" color="note" >}}
Viam enforces a maximum size of 4MB for any single reading for tabular data.
{{< /alert >}}
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `tabular_data` (List[Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]]) (required): List of the data to be uploaded, represented tabularly as a collection of dictionaries. Must include the key readings for sensors.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the component used to capture the data.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Type of the component used to capture the data (for example, rdk:component:movement_sensor).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the component used to capture the data.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the method used to capture the data.
- `data_request_times` (List[Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html)]]) (required): List of tuples, each containing datetime objects denoting the times this data was requested [0] by the robot and received [1] from the appropriate sensor. Pass a list of tabular data and timestamps with length n > 1 to upload n datapoints, all with the same metadata.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of method parameters. No longer in active use.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based data filtering when retrieving data.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The file ID of the uploaded data.

**Raises:**

- (GRPCError): If an invalid part ID is passed.
- (ValueError): If the provided list of Timestamp objects has a length that does not match the length of the list of tabular data.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from datetime import datetime

time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)
file_id = await data_client.tabular_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='rdk:component:movement_sensor',
    component_name='my_movement_sensor',
    method_name='Readings',
    tags=["sensor_data"],
    data_request_times=[(time_requested, time_received)],
    tabular_data=[{
        'readings': {
            'linear_velocity': {'x': 0.5, 'y': 0.0, 'z': 0.0},
            'angular_velocity': {'x': 0.0, 'y': 0.0, 'z': 0.1}
        }
    }]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `tabularData` (Record) (required): The list of data to be uploaded, represented tabularly
  as an array.
- `partId` (string) (required): The part ID of the component used to capture the data.
- `componentType` (string) (required): The type of the component used to capture the data
  (for example, "movementSensor").
- `componentName` (string) (required): The name of the component used to capture the data.
- `methodName` (string) (required): The name of the method used to capture the data.
- `dataRequestTimes` (Date) (required): Array of Date tuples, each containing two `Date`
  objects denoting the times this data was requested\[0] by the robot and
  received\[1] from the appropriate sensor. Passing a list of tabular data
  and Timestamps with length n \> 1 will result in n datapoints being
  uploaded, all tied to the same metadata.
- `tags` (string) (optional): The list of tags to allow for tag\-based filtering when
  retrieving data.

**Returns:**

- (Promise<string>): The file ID of the uploaded data.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const fileId = await dataClient.tabularDataCaptureUpload(
  [
    {
      readings: {
        timestamp: '2025-03-26T10:00:00Z',
        value: 10,
      },
    },
  ],
  '123abc45-1234-5678-90ab-cdef12345678',
  'rdk:component:sensor',
  'my-sensor',
  'Readings',
  [
    [
      new Date('2025-03-26T10:00:00Z'),
      new Date('2025-03-26T10:00:00Z'),
    ],
  ]
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#tabulardatacaptureupload).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `tabularData` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\> (required)
- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `componentType` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `componentName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodParameters` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), Any\>? (optional)
- `dataRequestTimes` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<([DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html), [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html))\>? (optional)
- `tags` [Iterable](https://api.flutter.dev/flutter/dart-core/Iterable-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );

 try {
   // Define tabular data
   final List<Map<String, dynamic>> tabularData;
   tabularData = [{
     'readings': {
       "altitude_m": 50.2,
       "coordinate": {
         "latitude": 40.5,
         "longitude": -72.98
      }
     }
   }];

  // Define date request times
  final List<(DateTime, DateTime)> timeSpan = [(DateTime(2025, 1, 23, 11), DateTime(2025, 1, 23, 11, 0, 3))];

  // Upload captured tabular data
  final fileId = await dataClient.tabularDataCaptureUpload(
    tabularData,
    "<YOUR-PART-ID>",
    componentType: "rdk:component:movement_sensor",
    componentName: "movement_sensor-1",
    methodName: "Position",
    dataRequestTimes: timeSpan,
    tags: ["tag_1", "tag_2"]
  );
   print('Successfully uploaded captured tabular data: $fileId');
 } catch (e) {
   print('Error uploading captured tabular data: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/tabularDataCaptureUpload.html).

{{% /tab %}}
{{< /tabs >}}

### FileUpload

Upload arbitrary files stored on your machine to Viam by file name.
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
- `file_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the file. The empty string "" will be assigned as the file name if one isn’t provided.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of the method parameters. No longer in active use.
- `file_extension` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional file extension. The empty string "" will be assigned as the file extension if one isn’t provided. Files with a .jpeg, .jpg, or .png extension will be saved to the Images tab.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based filtering when retrieving data.
- `dataset_ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of datasets to add the data to.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Binary data ID of the new file.

**Raises:**

- (GRPCError): If an invalid part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload(
    data=b"Encoded image bytes",
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    file_name="your-file",
    file_extension=".txt",
    dataset_ids=["dataset_1", "dataset_2"]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `path` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `fileName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `componentType` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `componentName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodParameters` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), Any\>? (optional)
- `datasetIds` [Iterable](https://api.flutter.dev/flutter/dart-core/Iterable-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (optional)
- `tags` [Iterable](https://api.flutter.dev/flutter/dart-core/Iterable-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
import 'package:file_picker/file_picker.dart';
import 'package:cross_file/cross_file.dart';

_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
);
final dataClient = _viam.dataClient;

// File picker function
Future<XFile?> pickTextFile() async {
  FilePickerResult? result = await FilePicker.platform.pickFiles(
    type: FileType.custom,
    allowedExtensions: ['txt', 'md', 'json', 'csv'],  // Add any other text file extensions you want to support
  );
 if (result != null) {
   return XFile(result.files.single.path!);
 }
   return null;
 }

// Upload text file function. Call this in onPressed in a button in your application.
Future<void> uploadTextFile() async {
  final file = await pickTextFile();
  if (file == null) return;

  try {
    // Get file name
    final fileName = file.name;

    // Upload the file
    final result = await _viam.dataClient.uploadFile(
      file.path,
      fileName: fileName,
      "<YOUR-PART-ID>",
      tags: ["text_file", "document"],
      datasetIds: ["datasetId"]
    );
    print('Upload success: $result');
  } catch (e) {
    print('Upload error: $e');
  }
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/uploadFile.html).

{{% /tab %}}
{{< /tabs >}}

### FileUploadFromPath

Upload files stored on your machine to [Viam](https://app.viam.com) by filepath.
Uploaded files can be found under the **Files** subtab of the [**Data** tab](https://app.viam.com/data).
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
- `dataset_ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of datasets to add the data to.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): Binary data ID of the new file.

**Raises:**

- (GRPCError): If an invalid part ID is passed.
- (FileNotFoundError): If the provided filepath is not found.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload_from_path(
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    dataset_ids=["dataset_1", "dataset_2"],
    filepath="/Users/<your-username>/<your-directory>/<your-file.txt>"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path).

{{% /tab %}}
{{< /tabs >}}

### StreamingDataCaptureUpload

Upload the contents of streaming binary data and the relevant metadata to [Viam](https://app.viam.com).
Uploaded streaming data can be found under the [**Data** tab](https://app.viam.com/data).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `data` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): The data to be uploaded.
- `part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Part ID of the resource associated with the file.
- `file_ext` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): File extension type for the data. required for determining MIME type.
- `component_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional type of the component associated with the file (for example, “movement_sensor”).
- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the component associated with the file.
- `method_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional name of the method associated with the file.
- `method_parameters` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional dictionary of the method parameters. No longer in active use.
- `data_request_times` (Tuple[[datetime.datetime](https://docs.python.org/3/library/datetime.html), [datetime.datetime](https://docs.python.org/3/library/datetime.html)]) (optional): Optional tuple containing datetime objects denoting the times this data was requested [0] by the robot and received [1] from the appropriate sensor.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of tags to allow for tag-based filtering when retrieving data.
- `dataset_ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): Optional list of datasets to add the data to.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The binary data ID of the uploaded data.

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
    data_request_times=[time_requested, time_received],
    tags=["tag_1", "tag_2"],
    dataset_ids=["dataset_1", "dataset_2"]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.streaming_data_capture_upload).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `bytes` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)\> (required)
- `partId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `fileExtension` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `componentType` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `componentName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html)? (optional)
- `methodParameters` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), Any\>? (optional)
- `dataRequestTimes` ([DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html), [DateTime](https://api.flutter.dev/flutter/dart-core/DateTime-class.html))? (optional)
- `datasetIds` [Iterable](https://api.flutter.dev/flutter/dart-core/Iterable-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (optional)
- `tags` [Iterable](https://api.flutter.dev/flutter/dart-core/Iterable-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
import 'package:file_picker/file_picker.dart';
import 'dart:typed_data';

Future<Uint8List> pickVideoAsBytes() async {
  try {
    // Open file picker
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.video,
      allowMultiple: false,
    );

    if (result == null || result.files.isEmpty) {
      throw Exception('No file selected');
    }

    // For mobile, we get the file path and read it
    final String? filePath = result.files.first.path;
    if (filePath == null) {
      throw Exception('Invalid file path');
    }

    // Read the file as bytes
    final File file = File(filePath);
    final Uint8List bytes = await file.readAsBytes();

    if (bytes.isEmpty) {
      throw Exception('File is empty');
    }

    print('Successfully read file: ${bytes.length} bytes');

    return bytes;
  } catch (e, stackTrace) {
    print('Error picking video: $e');
    print('Stack trace: $stackTrace');
    rethrow;
  }
}

void _uploadData() async {
  _viam = await Viam.withApiKey(
       dotenv.env['API_KEY_ID'] ?? '',
       dotenv.env['API_KEY'] ?? ''
   );
   final dataClient = _viam.dataClient;

   try {
     Uint8List video = await pickVideoAsBytes();

     (DateTime, DateTime) dataRequestTimes = (
       DateTime(2025, 1, 15, 10, 30), // Start time
       DateTime(2025, 1, 15, 14, 45)  // End time
     );

     final binaryDataId = await dataClient.streamingDataCaptureUpload(
       video,
       "<YOUR-PART-ID>",
       ".mp4", // Replace with your desired file format
       componentType: "rdk:component:camera",
       componentName: "camera-1",
       dataRequestTimes: dataRequestTimes);

     print('Successfully uploaded streaming binary data with binaryDataId: $binaryDataId');
   } catch (e) {
     print('Error uploading streaming binary data: $e');
   }
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/streamingDataCaptureUpload.html).

{{% /tab %}}
{{< /tabs >}}
