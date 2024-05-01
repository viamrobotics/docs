### CreateDataset

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: create_dataset

Create a new dataset.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required) The name of the dataset being created.:
- `name`- `organization_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required) The ID of the organization where the dataset is being created.:
- `organization_id`

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The dataset ID of the created dataset.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.create_dataset).

``` python {class="line-numbers linkable-line-numbers"}
name = await data_client.create_dataset(
    name="<dataset-name>",
    organization_id="<your-org-id>"
)
print(name)

```

\{\{% /tab %}}

\{\{% tab name="Flutter" %}\}

Flutter Method: CreateDataset

