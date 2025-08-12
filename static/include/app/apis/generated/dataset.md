### CreateDataset

Create a new dataset.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the dataset being created.
- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization where the dataset is being created. To find your organization ID, visit the organization settings page.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The dataset ID of the created dataset.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
dataset_id = await data_client.create_dataset(
    name="<DATASET-NAME>",
    organization_id="<YOUR-ORG-ID>"
)
print(dataset_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.create_dataset).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `name`
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.CreateDataset).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `name` (string) (required): The name of the new dataset.
- `organizationId` (string) (required): The ID of the organization the dataset is being
  created in.

**Returns:**

- (Promise<string>): The ID of the dataset.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const datasetId = await dataClient.createDataset(
  'my-new-dataset',
  '123abc45-1234-5678-90ab-cdef12345678'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#createdataset).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `orgId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 // Org ID to create dataset in
 const orgId = '<YOUR-ORG-ID>';

 try {
   // Create the dataset
   final datasetId = await dataClient.createDataset(orgId, "example-dataset");
   print('Successfully created dataset');
 } catch (e) {
   print('Error creating dataset: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/createDataset.html).

{{% /tab %}}
{{< /tabs >}}

### DeleteDataset

Delete a dataset.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset. To retrieve the dataset ID:  Navigate to the DATASETS tab of the DATA page. Click on the dataset. Click the … menu. Select Copy dataset ID.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await data_client.delete_dataset(
    id="<YOUR-DATASET-ID>"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_dataset).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DeleteDataset).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the dataset.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await dataClient.deleteDataset('12ab3de4f56a7bcd89ef0ab1');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#deletedataset).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 // Dataset ID to delete
 const datasetId = '<YOUR-DATASET-ID>';

 try {
   // Delete the dataset
   await dataClient.deleteDataset(datasetId);
   print('Successfully deleted dataset');
 } catch (e) {
   print('Error deleting dataset: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/deleteDataset.html).

{{% /tab %}}
{{< /tabs >}}

### RenameDataset

Rename a dataset specified by the dataset ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset. To retrieve the dataset ID:  Navigate to the DATASETS tab of the DATA page. Click on the dataset. Click the … menu. Select Copy dataset ID.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The new name of the dataset.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await data_client.rename_dataset(
    id="<YOUR-DATASET-ID>",
    name="MyDataset"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.rename_dataset).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id`
- `name` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.RenameDataset).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the dataset.
- `name` (string) (required): The new name of the dataset.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await dataClient.renameDataset(
  '12ab3de4f56a7bcd89ef0ab1',
  'my-new-dataset'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#renamedataset).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 // Dataset ID to rename
 const datasetId = '<YOUR-DATASET-ID>';

 try {
   // Rename the dataset
   await dataClient.renameDataset(datasetId, "new-name");
   print('Successfully renamed dataset');
 } catch (e) {
   print('Error renaming dataset: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/renameDataset.html).

{{% /tab %}}
{{< /tabs >}}

### ListDatasetsByOrganizationID

Get the datasets in an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization you’d like to retrieve datasets from. To find your organization ID, visit the organization settings page.

**Returns:**

- ([Sequence[viam.proto.app.dataset.Dataset]](https://python.viam.dev/autoapi/viam/proto/app/dataset/index.html#viam.proto.app.dataset.Dataset)): The list of datasets in the organization.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
datasets = await data_client.list_datasets_by_organization_id(
    organization_id="<YOUR-ORG-ID>"
)
print(datasets)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_datasets_by_organization_id).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*Dataset)](https://pkg.go.dev/go.viam.com/rdk/app#Dataset)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDatasetsByOrganizationID).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.

**Returns:**

- (Promise<Dataset[]>): The list of datasets in the organization.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const datasets = await dataClient.listDatasetsByOrganizationID(
  '123abc45-1234-5678-90ab-cdef12345678'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#listdatasetsbyorganizationid).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `orgId` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Dataset](https://flutter.viam.dev/viam_protos.app.dataset/Dataset-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 // Org ID to list datasets from
 const orgId = '<YOUR-ORG-ID>';

 try {
   // List datasets from org
   final datasets = await dataClient.listDatasetsByOrganizationID(orgId);
   print('Successfully retrieved list of datasets: $datasets');
 } catch (e) {
   print('Error retrieving list of datasets: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/listDatasetsByOrganizationID.html).

{{% /tab %}}
{{< /tabs >}}

### ListDatasetsByIDs

Get a list of datasets using their IDs.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): The IDs of the datasets that you would like to retrieve information about. To retrieve a dataset ID:  Navigate to the DATASETS tab of the DATA page. Click on the dataset. Click the … menu. Select Copy dataset ID.

**Returns:**

- ([Sequence[viam.proto.app.dataset.Dataset]](https://python.viam.dev/autoapi/viam/proto/app/dataset/index.html#viam.proto.app.dataset.Dataset)): The list of datasets.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
datasets = await data_client.list_dataset_by_ids(
    ids=["<YOUR-DATASET-ID-1>, <YOUR-DATASET-ID-2>"]
)
print(datasets)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_dataset_by_ids).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `ids` [([]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*Dataset)](https://pkg.go.dev/go.viam.com/rdk/app#Dataset)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDatasetsByIDs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `ids` (string) (required): The list of IDs of the datasets.

**Returns:**

- (Promise<Dataset[]>): The list of datasets.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const datasets = await dataClient.listDatasetsByIds([
  '12ab3de4f56a7bcd89ef0ab1',
]);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DataClient.html#listdatasetsbyids).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `ids` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Dataset](https://flutter.viam.dev/viam_protos.app.dataset/Dataset-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
_viam = await Viam.withApiKey(
     dotenv.env['API_KEY_ID'] ?? '',
     dotenv.env['API_KEY'] ?? ''
 );
 final dataClient = _viam.dataClient;

 const datasetIds = ["<YOUR-DATASET-ID>", "<YOUR-DATASET-ID-2>"];

 try {
   // List datasets by ids
   final datasets = await dataClient.listDatasetsByIDs(datasetIds);
   print('Successfully listed datasets by ids: $datasets');
 } catch (e) {
   print('Error retrieving datasets by ids: $e');
 }
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DataClient/listDatasetsByIDs.html).

{{% /tab %}}
{{< /tabs >}}
