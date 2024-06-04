---
title: "Work with ML Training Jobs with Viam's ML Training API"
linkTitle: "ML Training Client"
weight: 10
type: "docs"
description: "Use the ML training client API to manage ML training jobs taking place in Viam's cloud app."
tags: ["cloud", "sdk", "viam-server", "networking", "apis", "ml model", "ml"]
aliases:
  - /program/apis/ml_training-client/
---

The ML training API allows you to get information about and cancel ML training jobs taking place on the [Viam app](https://app.viam.com).

{{% alert title="Support Notice" color="note" %}}

ML training client API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam ML training client API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`MLTrainingClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient.ml_training_client).
See the following example for reference.

<!-- After sveltekit migration we should also be able to get a key from the UI-->

Select **Include secret** on the **Code sample** page of the **CONNECT** tab of the [Viam app](https://app.viam.com) to obtain your API key and API key ID values.

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an MLTrainingClient to run ML training client API methods on
    ml_training_client = viam_client.ml_training_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated an `MLTrainingClient`, you can run the following [API methods](#api) against the `MLTrainingClient` object (named `ml_training_client` in the examples).

## API

The ML training client API supports the following methods:

{{< readfile "/static/include/services/apis/ml-training-client.md" >}}

### GetTrainingJob

Get training job metadata.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the training job you wish to get metadata from. Retrieve this value with [`ListTrainingJobs()`](#listtrainingjobs).

**Returns**:

- [(TrainingJobMetadata)](https://python.viam.dev/autoapi/viam/proto/app/mltraining/index.html#viam.proto.app.mltraining.TrainingJobMetadata): Training job metadata, including status, last modified timestamp, id, and more.

```python {class="line-numbers linkable-line-numbers"}
job_metadata = await ml_training_client.get_training_job(
    id="INSERT YOUR JOB ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.get_training_job).

{{% /tab %}}
{{< /tabs >}}

### ListTrainingJobs

Get training job metadata for all jobs within an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of your organization to request training job metadata from. Retrieve this value with the fleet management API's [`ListOrganizations()`](/build/program/apis/fleet/#listorganizations).
- `training_status` [(Optional[TrainingStatus.ValueType])](https://python.viam.dev/autoapi/viam/gen/app/mltraining/v1/ml_training_pb2/index.html#viam.gen.app.mltraining.v1.ml_training_pb2.TrainingStatus): The status of training jobs you want to filter the list by. If you leave this unspecified, all training jobs for your organization are returned.

**Returns**:

- [(List[TrainingJobMetadata])](https://python.viam.dev/autoapi/viam/proto/app/mltraining/index.html#viam.proto.app.mltraining.TrainingJobMetadata): A list of training job metadata, including status, last modified timestamp, id, and more.

```python {class="line-numbers linkable-line-numbers"}
jobs_metadata = await ml_training_client.list_training_jobs(
    org_id="INSERT YOUR ORG ID")

first_job_id = jobs_metadata[1].id
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.list_training_jobs).

{{% /tab %}}
{{< /tabs >}}

### SubmitTrainingJob

Submit a training job.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to submit the training job to. To retrieve this, expand your organization's dropdown in the top right corner of the [Viam app](https://app.viam.com/), select **Settings**, and copy **Organization ID**.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to train the ML model on. To retrieve this, navigate to your dataset's page in the [Viam app](https://app.viam.com/data/datasets), click **...** in the left-hand menu, and click **Copy dataset ID**.
- `model_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the ML model you wish to train.
- `model_version` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The version of the ML model you're training. This string must be unique from any previous versions you've set.
- `model_type` ([ModelType.ValueType](https://python.viam.dev/autoapi/viam/gen/app/mltraining/v1/ml_training_pb2/index.html#viam.gen.app.mltraining.v1.ml_training_pb2.ModelType)) (required): The type of the ML model. Options: `ModelType.MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION`, `ModelType.MODEL_TYPE_MULTI_LABEL_CLASSIFICATION`, `ModelType.MODEL_TYPE_OBJECT_DETECTION`.
- `tags` ([List(str)](https://docs.python.org/3/library/stdtypes.html#typesseq-list)) (required): The labels to train on.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The ID of the training job created.

```python {class="line-numbers linkable-line-numbers"}
job_id = await ml_training_client.submit_training_job(
  "3988fd7d-b1c0-4f36-9842-0c666f374d3c",
  "66491a0666a6c8aa4a33e43e",
  "your-model-name",
  "1",
  "ModelType.MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION",
  tags)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.submit_training_job).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `datasetId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required): The ID of the dataset to train the ML model on. To retrieve this, navigate to your dataset's page in the [Viam app](https://app.viam.com/data/datasets), click **...** in the left-hand menu, and click **Copy dataset ID**.
- `modelName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required): The name of the ML model to train.
- `modelType` [(ModelType)](https://flutter.viam.dev/viam_protos.app.ml_training/ModelType-class.html) (required): The type of the ML model. Options: `MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION`, `MODEL_TYPE_MULTI_LABEL_CLASSIFICATION`, or `MODEL_TYPE_OBJECT_DETECTION`.
- `modelVersion` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required): The version of the ML model you're training. This string must be unique from any previous versions you've set.
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required): The ID of the organization to submit the training job to. To retrieve this, expand your organization's dropdown in the top right corner of the [Viam app](https://app.viam.com/), select **Settings**, and copy **Organization ID**.
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required): The labels to train on.

**Returns:**

- [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required): The ID of the training job created.

```dart {class="line-numbers linkable-line-numbers"}
final tags = <String>['A', 'B', 'C']; // Creates list of tags.

String jobID = ml_training.submitTrainingJob("66491a0666a6c8aa4a33e43e", "your-model-name", "MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION", "1", "3988fd7d-b1c0-4f36-9842-0c666f374d3c", tags);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/submitTrainingJob.html).

{{% /tab %}}
{{< /tabs >}}

### CancelTrainingJob

Cancel the specified training job.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the training job you wish to get metadata from. Retrieve this value with [`ListTrainingJobs()`](#listtrainingjobs).

**Returns**:

- None

**Raises**:

- `GRPCError`: If no training job exists with the given ID or cancellation was otherwise unsuccessful.

```python {class="line-numbers linkable-line-numbers"}
await ml_training_client.cancel_training_job(
    id="INSERT YOUR JOB ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.cancel_training_job).

{{% /tab %}}
{{< /tabs >}}
