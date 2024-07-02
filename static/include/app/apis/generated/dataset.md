### CreateDataset

Create a new dataset.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the dataset being created.
- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization where the dataset is being created. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The dataset ID of the created dataset.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
name = await data_client.create_dataset(
    name="<dataset-name>",
    organization_id="<your-org-id>"
)
print(name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.create_dataset).

{{% /tab %}}
{{< /tabs >}}

### DeleteDataset

Delete a dataset.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await data_client.delete_dataset(
    id="abcd-1234xyz-8765z-123abc"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_dataset).

{{% /tab %}}
{{< /tabs >}}

### RenameDataset

Rename a dataset specified by the dataset ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The new name of the dataset.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await data_client.rename_dataset(
    id="abcd-1234xyz-8765z-123abc",
    name="<dataset-name>"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.rename_dataset).

{{% /tab %}}
{{< /tabs >}}

### ListDatasetsByOrganizationID

Get the datasets in an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- ([Sequence[viam.proto.app.dataset.Dataset]](https://python.viam.dev/autoapi/viam/proto/app/dataset/index.html#viam.proto.app.dataset.Dataset)): The list of datasets in the organization.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
datasets = await data_client.list_dataset_by_organization_id(
    organization_id=[""a12b3c4e-1234-1abc-ab1c-ab1c2d345abc""]
)
print(datasets)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_datasets_by_organization_id).

{{% /tab %}}
{{< /tabs >}}

### ListDatasetsByIDs

Get a list of datasets using their IDs.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): The IDs of the datasets being called for. To retrieve these IDs, navigate to your dataset’s page in the Viam app, click … in the left-hand menu, and click Copy dataset ID.

**Returns:**

- ([Sequence[viam.proto.app.dataset.Dataset]](https://python.viam.dev/autoapi/viam/proto/app/dataset/index.html#viam.proto.app.dataset.Dataset)): The list of datasets.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
datasets = await data_client.list_dataset_by_ids(
    ids=["abcd-1234xyz-8765z-123abc"]
)
print(datasets)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_dataset_by_ids).

{{% /tab %}}
{{< /tabs >}}
