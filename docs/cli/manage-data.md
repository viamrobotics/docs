---
linkTitle: "Manage data"
title: "Manage data with the CLI"
weight: 20
layout: "docs"
type: "docs"
description: "Export, tag, delete, and query your machine data from the command line."
---

Export captured data to your local machine, organize it with tags, delete old data, and configure database access for direct queries.

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.
{{< /expand >}}

## Find your IDs

Many data commands require an organization ID, location ID, or part ID.
To look up these values:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

```sh {class="command-line" data-prompt="$"}
viam locations list
```

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --location=<location-id>
```

```sh {class="command-line" data-prompt="$"}
viam machines part list --machine=<machine-id>
```

## Export data

### Export images and binary files

Export all binary data from an organization:

```sh {class="command-line" data-prompt="$"}
viam data export binary filter \
  --destination=./my-data \
  --org-ids=<org-id>
```

The CLI downloads files into the destination directory and prints progress as it goes.

Narrow the export with filters:

```sh {class="command-line" data-prompt="$"}
viam data export binary filter \
  --destination=./my-data \
  --org-ids=<org-id> \
  --mime-types=image/jpeg,image/png \
  --machine-id=<machine-id> \
  --start=2026-01-01T00:00:00Z \
  --end=2026-02-01T00:00:00Z
```

Available filters:

| Filter                | Flag                                   | Example                             |
| --------------------- | -------------------------------------- | ----------------------------------- |
| By machine            | `--machine-id` or `--machine-name`     | `--machine-id=abc123`               |
| By part               | `--part-id` or `--part-name`           | `--part-id=def456`                  |
| By location           | `--location-ids`                       | `--location-ids=loc1,loc2`          |
| By time range         | `--start`, `--end`                     | `--start=2026-01-01T00:00:00Z`      |
| By component          | `--component-name`, `--component-type` | `--component-name=my-camera`        |
| By MIME type          | `--mime-types`                         | `--mime-types=image/jpeg,image/png` |
| By tag                | `--tags`                               | `--tags=defective,reviewed`         |
| By bounding box label | `--bbox-labels`                        | `--bbox-labels=screw,bolt`          |

Export specific files by their binary data IDs:

```sh {class="command-line" data-prompt="$"}
viam data export binary ids \
  --destination=./my-data \
  --binary-data-ids=aaa,bbb,ccc
```

### Export sensor and tabular data

Tabular exports require a part ID and resource identifier:

```sh {class="command-line" data-prompt="$"}
viam data export tabular \
  --destination=./sensor-data \
  --part-id=<part-id> \
  --resource-name=my-sensor \
  --resource-subtype=rdk:component:sensor \
  --method=Readings
```

Output is written to a `data.ndjson` file (one JSON object per line).
You can also filter by time range with `--start` and `--end`.

## Tag data

Tags help you organize data for filtering, dataset creation, and search.

### Add tags by ID

Add tags to specific files by their binary data IDs:

```sh {class="command-line" data-prompt="$"}
viam data tag ids add \
  --tags=reviewed,approved \
  --binary-data-ids=aaa,bbb
```

Remove tags from specific files:

```sh {class="command-line" data-prompt="$"}
viam data tag ids remove \
  --tags=reviewed \
  --binary-data-ids=aaa,bbb
```

### Add tags by filter

{{< alert title="Note" color="note" >}}
The filter-based tag commands (`tag filter add` and `tag filter remove`) use deprecated underlying APIs.
They still work but may be removed in a future release.
Prefer the ID-based commands above when possible.
{{< /alert >}}

Add tags to all data matching a filter:

```sh {class="command-line" data-prompt="$"}
viam data tag filter add \
  --tags=reviewed,approved \
  --org-ids=<org-id> \
  --location-ids=<location-id> \
  --mime-types=image/jpeg
```

Remove tags by filter:

```sh {class="command-line" data-prompt="$"}
viam data tag filter remove \
  --tags=reviewed \
  --org-ids=<org-id>
```

## Delete data

### Delete binary data

Delete binary data matching a filter.
Both `--start` and `--end` are required:

```sh {class="command-line" data-prompt="$"}
viam data delete binary \
  --org-ids=<org-id> \
  --mime-types=image/jpeg \
  --start=2026-01-01T00:00:00Z \
  --end=2026-02-01T00:00:00Z
```

### Delete tabular data

Delete tabular data older than a specified number of days.
Pass `0` to delete all tabular data for your organization.

```sh {class="command-line" data-prompt="$"}
viam data delete tabular --org-id=<org-id> --delete-older-than-days=90
```

{{< alert title="Caution" color="caution" >}}
Passing `--delete-older-than-days=0` deletes **all** tabular data in the organization. This command has no component or location filter.
{{< /alert >}}

## Configure database access

To query synced data directly with MongoDB-compatible tools like `mongosh` or Grafana, set up a database user:

```sh {class="command-line" data-prompt="$"}
viam data database configure --org-id=<org-id> --password=<password>
```

{{< alert title="Caution" color="caution" >}}
If you already have database credentials configured, changing the password breaks existing connections from dashboards and integrations that use the old password.
{{< /alert >}}

Get the connection hostname:

```sh {class="command-line" data-prompt="$"}
viam data database hostname --org-id=<org-id>
```

Use the returned hostname with your MongoDB client.
See [Visualize data](/data/visualize-data/) for Grafana setup instructions.

## Manage data indexes

Create custom indexes to speed up queries on large datasets.
The `--collection-type` flag specifies the target: `hot-storage` for hot data store collections, or `pipeline-sink` for data pipeline output collections (requires `--pipeline-name`).

The `--index-path` flag takes a JSON file defining the index using [MongoDB index specification format](https://www.mongodb.com/docs/manual/reference/command/createIndexes/):

```json
{
  "key": { "meta.captured_at": 1, "tags": 1 },
  "name": "captured-at-tags"
}
```

```sh {class="command-line" data-prompt="$"}
viam data index create \
  --collection-type=hot-storage \
  --index-path=./my-index.json
```

List existing indexes:

```sh {class="command-line" data-prompt="$"}
viam data index list --collection-type=hot-storage
```

Delete an index:

```sh {class="command-line" data-prompt="$"}
viam data index delete --collection-type=hot-storage --index-name=my-index
```

## Related pages

- [Export data](/data/export-data/) for step-by-step export instructions with the Viam app
- [Data pipelines with the CLI](/cli/data-pipelines/) for scheduled data transformations
- [Datasets and training with the CLI](/cli/datasets-and-training/) for managing ML datasets
- [CLI reference](/cli/#data) for the complete `data` command reference
