---
linkTitle: "Tag data"
title: "Tag captured data"
weight: 25
layout: "docs"
type: "docs"
description: "Apply tags to captured binary data so you can filter it, build datasets, or scope a delete operation."
---

Tags are short labels you attach to captured items.
Use them to mark which items have been reviewed, group items by source or condition, build a dataset for ML training, or narrow the scope of a delete operation.

A few important boundaries:

- **Binary data only.** You can tag images, point clouds, audio, and other binary uploads. Tabular data (sensor readings) does not support post-capture tagging.
- **Different from bounding boxes and labels.** Tags apply to a whole item. Bounding boxes mark regions of an image and are used for object-detection training. See [Annotate images](/train/annotate-images/) for both classification tags and bounding boxes in the ML training context.
- **Different from tabular `tags` capture attributes.** The `tags` field in a [data capture method config](/data/reference/#capture_methods) attaches a fixed list of tags at capture time. The operations on this page apply tags after data is captured.

## Apply tags to binary data

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On your organization's **DATA** page, click an item to open the side panel.
1. Open the **Actions** tab.
1. In the **Tags** section, type a tag name and press Enter.

Repeat to add more tags. Click the **x** next to a tag to remove it.

The Viam app applies tags one item at a time.
To tag many items in a single operation, use the CLI or the SDK.

{{% /tab %}}
{{% tab name="CLI" %}}

Tag specific items by their binary data IDs:

```sh {class="command-line" data-prompt="$"}
viam data tag ids add \
  --tags=reviewed,approved \
  --binary-data-ids=<id1>,<id2>
```

Remove tags from specific items:

```sh {class="command-line" data-prompt="$"}
viam data tag ids remove \
  --tags=reviewed \
  --binary-data-ids=<id1>,<id2>
```

Tag every item that matches a filter (organization, location, MIME type, time range, and more):

```sh {class="command-line" data-prompt="$"}
viam data tag filter add \
  --tags=reviewed,approved \
  --org-ids=<org-id> \
  --location-ids=<location-id> \
  --mime-types=image/jpeg
```

{{< alert title="Note" color="note" >}}
The filter-based tag commands (`tag filter add` and `tag filter remove`) use deprecated underlying APIs.
They still work but may be removed in a future release.
Prefer the ID-based commands when possible.
{{< /alert >}}

For the full list of flags, see the [`viam data tag` CLI reference](/cli/manage-data/#tag-data).

To find binary data IDs, run `viam data export binary filter` and read the IDs from the JSON metadata file each download produces, or query through the SDK with `BinaryDataByFilter`.

{{% /tab %}}
{{% tab name="Python" %}}

```python
binary_ids = ["binary-data-id-1", "binary-data-id-2"]

await data_client.add_tags_to_binary_data_by_ids(
    tags=["reviewed", "approved"],
    binary_ids=binary_ids,
)
```

The [data client API](/reference/apis/data-client/) also supports adding and removing tags by filter, removing tags by ID, and listing the distinct tags that match a filter.

{{% /tab %}}
{{% tab name="Go" %}}

```go
binaryIDs := []string{"binary-data-id-1", "binary-data-id-2"}

err := dataClient.AddTagsToBinaryDataByIDs(
    ctx,
    []string{"reviewed", "approved"},
    binaryIDs,
)
```

The [data client API](/reference/apis/data-client/) also supports adding and removing tags by filter, removing tags by ID, and listing the distinct tags that match a filter.

{{% /tab %}}
{{< /tabs >}}

## Use tags downstream

Once data is tagged, you can use those tags to:

- **Filter the DATA page.** Use the tag filter at the top of the page to view only items with a given tag.
- **Build a dataset.** Add tagged items to a dataset for ML training. See [Create a dataset](/train/create-a-dataset/).
- **Scope an export.** Pass `--tags` to [`viam data export binary filter`](/cli/manage-data/#export-data) to download only items with a given tag, or `--tags=tagged` and `--tags=untagged` to scope to all tagged or all untagged items.

## Related pages

- [Annotate images](/train/annotate-images/) for classification tags and bounding boxes used in ML training
- [Manage data with the CLI](/cli/manage-data/) for the full CLI reference
- [Data client API](/reference/apis/data-client/) for SDK methods
