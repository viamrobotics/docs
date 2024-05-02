### FileUploadFromPath

{{< tabs >}}
{{% tab name="Python" %}}

Upload arbitrary file data.

**Parameters:**

- `filepath` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Absolute filepath of file to be uploaded.
- `part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Part ID of the component associated with the file.
- `component_type` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional type of the component associated with the file (e.g., “movement_sensor”).
- `component_name` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional name of the component associated with the file.
- `method_name` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional name of the method associated with the file.
- `method_parameters` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Optional dictionary of the method parameters. No longer in active use.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>) (optional): Optional list of tags to allow for tag-based filtering when retrieving data.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ID of the new file.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path).

``` python {class="line-numbers linkable-line-numbers"}
file_id = await data_client.file_upload_from_path(
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    filepath="/Users/<your-username>/<your-directory>/<your-file.txt>"
)
```

{{% /tab %}}
{{< /tabs >}}
