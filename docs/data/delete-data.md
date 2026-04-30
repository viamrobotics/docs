---
linkTitle: "Delete data"
title: "Delete captured data"
weight: 27
layout: "docs"
type: "docs"
description: "Delete captured tabular and binary data through the Viam app, the CLI, or the SDK."
aliases:
  - /data/overview/#delete-data
---

You can delete captured data through the Viam app, the CLI, or the SDK.
The SQL and MQL query editor is read-only: you cannot run `DELETE`, `DROP TABLE`, or any write operation through it.

[Retention policies](/data/reference/#platform-managed-capture-settings) can also auto-delete data in the cloud after a configured number of days, without anyone running a delete operation.

## Delete captured data

{{< tabs >}}
{{% tab name="Viam app" %}}

- **Images and binary data**: on the **DATA** page, select one or more items and click **Delete selected**, or use **Delete all** with the current filters applied. Point clouds, video, and file uploads can be deleted the same way.
- **Tabular data (sensor readings)**: the Sensors tab does not have a delete button. Use the CLI or the SDK instead.

{{% /tab %}}
{{% tab name="CLI" %}}

Delete tabular data older than a number of days:

```sh {class="command-line" data-prompt="$"}
viam data delete tabular --org-id=<org-id> --delete-older-than-days=30
```

If the organization has a [hot data store](/data/hot-data-store/), matching data is deleted from that store as well.

{{< alert title="Caution" color="caution" >}}
`--delete-older-than-days=0` deletes **all** tabular data in the organization. The CLI tabular delete has no component or location filter: it applies to the entire org.
{{< /alert >}}

Delete binary data within a time range:

```sh {class="command-line" data-prompt="$"}
viam data delete binary \
  --org-ids=<org-id> \
  --start=2026-01-01T00:00:00Z \
  --end=2026-02-01T00:00:00Z
```

The binary delete command requires `--org-ids`, `--start`, and `--end`. Narrow further with optional filters for location, machine, part, component, MIME type, and bounding-box label. For the full list, see the [`viam data delete binary` CLI reference](/cli/manage-data/#delete-data).

{{% /tab %}}
{{% tab name="Python" %}}

Delete tabular data older than a number of days:

```python
deleted = await data_client.delete_tabular_data(
    organization_id="<org-id>",
    delete_older_than_days=30,
)
```

Delete binary data matching a filter:

```python
from viam.utils import create_filter

my_filter = create_filter(
    component_name="camera-1",
    organization_ids=["<org-id>"],
)

deleted = await data_client.delete_binary_data_by_filter(my_filter)
```

Delete specific binary items by ID:

```python
deleted = await data_client.delete_binary_data_by_ids(
    ["binary-data-id-1", "binary-data-id-2"],
)
```

See the [data client API](/reference/apis/data-client/) for the full set of methods and signatures.

{{% /tab %}}
{{% tab name="Go" %}}

Delete tabular data older than a number of days:

```go
deleted, err := dataClient.DeleteTabularData(ctx, "<org-id>", 30, nil)
```

Delete binary data matching a filter:

```go
filter := &app.Filter{
    ComponentName:   "camera-1",
    OrganizationIDs: []string{"<org-id>"},
}

deleted, err := dataClient.DeleteBinaryDataByFilter(ctx, filter)
```

Delete specific binary items by ID:

```go
deleted, err := dataClient.DeleteBinaryDataByIDs(
    ctx,
    []string{"binary-data-id-1", "binary-data-id-2"},
)
```

See the [data client API](/reference/apis/data-client/) for the full set of methods and signatures.

{{% /tab %}}
{{< /tabs >}}

## Related pages

- [Manage data with the CLI](/cli/manage-data/) for the full CLI reference, including all `viam data delete` filters
- [Data client API](/reference/apis/data-client/) for SDK methods
- [Hot data store](/data/hot-data-store/) for how the hot store interacts with tabular deletes
- [Data management reference](/data/reference/#platform-managed-capture-settings) for `retention_policy` configuration
