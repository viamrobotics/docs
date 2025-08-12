### SubmitTrainingJob

Submit a training job.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to submit the training job to. To retrieve this, expand your organization's dropdown in the top right corner on [Viam](https://app.viam.com/), select **Settings**, and copy **Organization ID**.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the dataset to train the ML model on. To retrieve this, navigate to your [dataset's page](https://app.viam.com/data/datasets), click **...** in the left-hand menu, and click **Copy dataset ID**.
- `model_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the model name.
- `model_version` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The version of the ML model you're training. This string must be unique from any previous versions you've set.
- `model_type` (viam.proto.app.mltraining.ModelType.ValueType) (required): The type of the ML model. Options: `ModelType.MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION`, `ModelType.MODEL_TYPE_MULTI_LABEL_CLASSIFICATION`, `ModelType.MODEL_TYPE_OBJECT_DETECTION`.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): the labels to train the model on.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): the ID of the training job.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.mltraining import ModelType

job_id = await ml_training_client.submit_training_job(
    org_id="<organization-id>",
    dataset_id="<dataset-id>",
    model_name="<your-model-name>",
    model_version="1",
    model_type=ModelType.MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION,
    tags=["tag1", "tag2"]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.submit_training_job).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `args` [(SubmitTrainingJobArgs)](https://pkg.go.dev/go.viam.com/rdk/app#SubmitTrainingJobArgs)
- `modelType` [(ModelType)](https://pkg.go.dev/go.viam.com/rdk/app#ModelType)
- `tags` [([]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#MLTrainingClient.SubmitTrainingJob).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The organization ID.
- `datasetId` (string) (required): The dataset ID.
- `modelName` (string) (required): The model name.
- `modelVersion` (string) (required): The model version.
- `modelType` ([ModelType](https://ts.viam.dev/enums/ModelType.html)) (required): The model type.
- `tags` (string) (required): The tags.

**Returns:**

- (Promise<string>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await mlTrainingClient.submitTrainingJob(
  '<organization-id>',
  '<dataset-id>',
  '<your-model-name>',
  '1.0.0',
  ModelType.SINGLE_LABEL_CLASSIFICATION,
  ['tag1', 'tag2']
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MlTrainingClient.html#submittrainingjob).

{{% /tab %}}
{{< /tabs >}}

### SubmitCustomTrainingJob

Submit a training job from a custom training script.
Follow the guide to [Train a Model with a Custom Python Training Script](/data-ai/train/train/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to submit the training job to.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the dataset to train the model on.
- `registry_item_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the training script from the registry.
- `registry_item_version` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the version of the training script from the registry.
- `model_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the model name.
- `model_version` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the model version.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): the ID of the training job.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
job_id = await ml_training_client.submit_custom_training_job(
    org_id="<organization-id>",
    dataset_id="<dataset-id>",
    registry_item_id="viam:classification-tflite",
    registry_item_version="2024-08-13T12-11-54",
    model_name="<your-model-name>",
    model_version="1"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.submit_custom_training_job).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `args` [(SubmitTrainingJobArgs)](https://pkg.go.dev/go.viam.com/rdk/app#SubmitTrainingJobArgs)
- `registryItemID`
- `registryItemVersion` [(string)](https://pkg.go.dev/builtin#string)
- `arguments` [(map[string]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#MLTrainingClient.SubmitCustomTrainingJob).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The organization ID.
- `datasetId` (string) (required): The dataset ID.
- `registryItemId` (string) (required): The registry item ID.
- `registryItemVersion` (string) (required): The registry item version.
- `modelName` (string) (required): The model name.
- `modelVersion` (string) (required): The model version.

**Returns:**

- (Promise<string>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await mlTrainingClient.submitCustomTrainingJob(
  '<organization-id>',
  '<dataset-id>',
  'viam:classification-tflite',
  '1.0.0',
  '<your-model-name>',
  '1.0.0'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MlTrainingClient.html#submitcustomtrainingjob).

{{% /tab %}}
{{< /tabs >}}

### GetTrainingJob

Get training job metadata.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the requested training job.

**Returns:**

- ([viam.proto.app.mltraining.TrainingJobMetadata](https://python.viam.dev/autoapi/viam/proto/app/mltraining/index.html#viam.proto.app.mltraining.TrainingJobMetadata)): the training job data.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
job_metadata = await ml_training_client.get_training_job(
    id="<job-id>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.get_training_job).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*TrainingJobMetadata)](https://pkg.go.dev/go.viam.com/rdk/app#TrainingJobMetadata)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#MLTrainingClient.GetTrainingJob).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The training job ID.

**Returns:**

- (Promise<undefined | [TrainingJobMetadata](https://ts.viam.dev/classes/mlTrainingApi.TrainingJobMetadata.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const job = await mlTrainingClient.getTrainingJob('<training-job-id>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MlTrainingClient.html#gettrainingjob).

{{% /tab %}}
{{< /tabs >}}

### ListTrainingJobs

Get training job metadata for all jobs within an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to request training job data from.
- `training_status` ([viam.proto.app.mltraining.TrainingStatus.ValueType](https://python.viam.dev/autoapi/viam/gen/app/mltraining/v1/ml_training_pb2/index.html#viam.gen.app.mltraining.v1.ml_training_pb2.TrainingStatus)) (optional): the status to filter the training jobs list by. If unspecified, all training jobs will be returned.

**Returns:**

- ([List[viam.proto.app.mltraining.TrainingJobMetadata]](https://python.viam.dev/autoapi/viam/proto/app/mltraining/index.html#viam.proto.app.mltraining.TrainingJobMetadata)): the list of training job data.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
jobs_metadata = await ml_training_client.list_training_jobs(
    org_id="<org-id>")

first_job_id = jobs_metadata[1].id
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.list_training_jobs).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)
- `status` [(TrainingStatus)](https://pkg.go.dev/go.viam.com/rdk/app#TrainingStatus)

**Returns:**

- [([]*TrainingJobMetadata)](https://pkg.go.dev/go.viam.com/rdk/app#TrainingJobMetadata)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#MLTrainingClient.ListTrainingJobs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The organization ID.
- `status` ([TrainingStatus](https://ts.viam.dev/enums/TrainingStatus.html)) (required): The training job status.

**Returns:**

- (Promise<[TrainingJobMetadata](https://ts.viam.dev/classes/mlTrainingApi.TrainingJobMetadata.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const jobs = await mlTrainingClient.listTrainingJobs(
  '<organization-id>',
  TrainingStatus.RUNNING
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MlTrainingClient.html#listtrainingjobs).

{{% /tab %}}
{{< /tabs >}}

### CancelTrainingJob

Cancel the specified training job.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the training job you wish to get metadata from. Retrieve this value with [`ListTrainingJobs()`](#listtrainingjobs).

**Returns:**

- None.

**Raises:**

- (GRPCError): if no training job exists with the given ID.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await ml_training_client.cancel_training_job(
    id="<job-id>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.cancel_training_job).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#MLTrainingClient.CancelTrainingJob).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The training job ID.

**Returns:**

- (Promise<null>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await mlTrainingClient.cancelTrainingJob('<training-job-id>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MlTrainingClient.html#canceltrainingjob).

{{% /tab %}}
{{< /tabs >}}

### DeleteCompletedTrainingJob

Delete a completed training job from the database, whether the job succeeded or failed.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the training job to delete.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await ml_training_client.delete_completed_training_job(
    id="<job-id>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.delete_completed_training_job).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#MLTrainingClient.DeleteCompletedTrainingJob).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The training job ID.

**Returns:**

- (Promise<null>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await mlTrainingClient.deleteCompletedTrainingJob('<training-job-id>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MlTrainingClient.html#deletecompletedtrainingjob).

{{% /tab %}}
{{< /tabs >}}
