---
linkTitle: "Query results"
title: "Query pipeline results"
weight: 15
layout: "docs"
type: "docs"
description: "Query the output of a data pipeline from Python, Go, or TypeScript."
date: "2026-03-27"
---

Once you have [created a pipeline](/data/pipelines/create-a-pipeline/), its results land in a dedicated sink collection that is separate from your raw data. This page covers how to query that sink.

You query pipeline results the same way you query raw readings, except you specify the `pipeline_sink` data source type and the **pipeline ID** of the pipeline whose results you want. The pipeline ID is returned on creation. If you did not save it, retrieve it with:

```bash
viam datapipelines list --org-id=<org-id>
```

To see a specific pipeline and its last run:

```bash
viam datapipelines describe --id=<pipeline-id>
```

Both commands are also documented in [Manage pipelines](/data/pipelines/manage-pipelines/).

## Query with the SDK

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType

PIPELINE_ID = "YOUR-PIPELINE-ID"

# Returns a list of result documents
results = await data_client.tabular_data_by_mql(
    organization_id=ORG_ID,
    query=[
        {"$limit": 10},
    ],
    tabular_data_source_type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK,
    pipeline_id=PIPELINE_ID,
)

for entry in results:
    print(entry)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
results, err := dataClient.TabularDataByMQL(ctx, orgID,
    []map[string]interface{}{
        {"$limit": 10},
    },
    &app.TabularDataByMQLOptions{
        TabularDataSourceType: app.TabularDataSourceTypePipelineSink,
        PipelineID:            "YOUR-PIPELINE-ID",
    },
)
if err != nil {
    logger.Fatal(err)
}

for _, entry := range results {
    fmt.Printf("%v\n", entry)
}
```

{{% /tab %}}
{{< /tabs >}}

The query runs against the pipeline's output documents, not the raw readings. The fields available depend on what your pipeline's `$project` stage produces.

## What results look like

Each result document contains the fields your pipeline's `$project` stage outputs, plus metadata added automatically:

```json
{
  "_viam_pipeline_run": {
    "id": "run-id",
    "interval": {
      "start": "2025-03-15T14:00:00.000Z",
      "end": "2025-03-15T15:00:00.000Z"
    },
    "organization_id": "org-id"
  },
  "location": "warehouse-a",
  "avg_temp": 23.5,
  "count": 3600
}
```

You can use `$match` on the `_viam_pipeline_run.interval` fields to filter results by time window.

## Troubleshooting

{{< expand "Query returns empty results" >}}

- **Pipeline hasn't run yet.** Check pipeline run status with `viam datapipelines describe --id=<pipeline-id>` or see [Monitor pipeline runs](/data/pipelines/manage-pipelines/#monitor-pipeline-runs). Wait for at least one run to complete.
- **Wrong pipeline ID.** The ID is returned on creation and visible in `viam datapipelines list`.
- **Wrong data source type.** You must specify `TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK`, not `STANDARD` or `HOT_STORAGE`.

{{< /expand >}}
