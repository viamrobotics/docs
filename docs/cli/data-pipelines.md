---
linkTitle: "Data pipelines"
title: "Data pipelines with the CLI"
weight: 40
layout: "docs"
type: "docs"
description: "Create and manage scheduled data pipelines from the command line."
---

Create data pipelines that run MQL aggregations on your captured data on a schedule, transforming raw sensor readings or image metadata into precomputed summaries you can query efficiently.

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.

You also need captured tabular data in the Viam cloud.
See [Capture and sync data](/data/capture-sync/capture-and-sync-data/) to get started.
{{< /expand >}}

## Find your IDs

To find your organization ID:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

To find pipeline IDs for existing pipelines:

```sh {class="command-line" data-prompt="$"}
viam datapipelines list --org-id=<org-id>
```

## Create a pipeline

A pipeline needs a name, a cron schedule, an MQL query, and whether to backfill historical data:

```sh {class="command-line" data-prompt="$"}
viam datapipelines create \
  --org-id=<org-id> \
  --name=hourly-temp-avg \
  --schedule="0 * * * *" \
  --data-source-type=standard \
  --mql='[{"$match":{"component_name":"my-sensor"}},{"$group":{"_id":"$part_id","avg_temp":{"$avg":"$data.readings.temperature"}}}]' \
  --enable-backfill=false
```

On success, the CLI prints the pipeline name and ID:

```sh {class="command-line" data-prompt="$" data-output="1"}
hourly-temp-avg (ID: abcdef12-3456-7890-abcd-ef1234567890) created.
```

Save the pipeline ID for management commands.

For complex queries, put the MQL in a JSON file:

```sh {class="command-line" data-prompt="$"}
viam datapipelines create \
  --org-id=<org-id> \
  --name=hourly-temp-avg \
  --schedule="0 * * * *" \
  --data-source-type=standard \
  --mql-path=./pipeline-query.json \
  --enable-backfill=false
```

| Flag                    | Required     | Description                                                   |
| ----------------------- | ------------ | ------------------------------------------------------------- |
| `--name`                | Yes          | Pipeline name                                                 |
| `--schedule`            | Yes          | Cron expression for when the pipeline runs                    |
| `--enable-backfill`     | Yes          | `true` to run over historical data, `false` for new data only |
| `--org-id`              | No           | Your organization ID (uses default if set)                    |
| `--data-source-type`    | No           | `standard` (default) or `hotstorage` (hot data store)         |
| `--mql` or `--mql-path` | One required | MQL query as inline JSON or path to a JSON file               |

## List pipelines

```sh {class="command-line" data-prompt="$"}
viam datapipelines list --org-id=<org-id>
```

## Get pipeline details

```sh {class="command-line" data-prompt="$"}
viam datapipelines describe --id=<pipeline-id>
```

## Enable and disable pipelines

Disable a pipeline without deleting it:

```sh {class="command-line" data-prompt="$"}
viam datapipelines disable --id=<pipeline-id>
```

Re-enable it:

```sh {class="command-line" data-prompt="$"}
viam datapipelines enable --id=<pipeline-id>
```

## Rename a pipeline

```sh {class="command-line" data-prompt="$"}
viam datapipelines rename --id=<pipeline-id> --name=new-pipeline-name
```

## Delete a pipeline

```sh {class="command-line" data-prompt="$"}
viam datapipelines delete --id=<pipeline-id>
```

## Related pages

- [Create a data pipeline](/data/pipelines/create-a-pipeline/) for step-by-step pipeline creation with the Viam app and SDKs
- [Pipeline examples and MQL tips](/data/pipelines/examples/) for common MQL patterns
- [Query pipeline results](/data/pipelines/query-results/) for querying pipeline output
- [CLI reference](/cli/#datapipelines) for the complete `datapipelines` command reference
