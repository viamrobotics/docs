### SubmitTrainingJob

Submit a training job.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the id of the org to submit the training job to.
- `dataset_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the id of the dataset.
- `model_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the model name.
- `model_version` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the model version.
- `model_type` (viam.proto.app.mltraining.ModelType.ValueType) (required): the model type.
- `tags` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): the tags.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): the id of the training job.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.submit_training_job).

{{% /tab %}}
{{< /tabs >}}

### GetTrainingJob

Get training job metadata.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the id of the requested training job.

**Returns:**

- ([viam.proto.app.mltraining.TrainingJobMetadata](https://python.viam.dev/autoapi/viam/proto/app/mltraining/index.html#viam.proto.app.mltraining.TrainingJobMetadata)): training job data.

**Example:**

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

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the id of the org to request training job data from.
- `training_status` ([viam.proto.app.mltraining.TrainingStatus.ValueType](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.TrainingStatus)) (optional): status of training jobs to filter the list by. If unspecified, all training jobs will be returned.

**Returns:**

- ([List[viam.proto.app.mltraining.TrainingJobMetadata]](https://python.viam.dev/autoapi/viam/proto/app/mltraining/index.html#viam.proto.app.mltraining.TrainingJobMetadata)): a list of training job data.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
jobs_metadata = await ml_training_client.list_training_jobs(
    org_id="INSERT YOUR ORG ID")

first_job_id = jobs_metadata[1].id
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.list_training_jobs).

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

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the id of the job to be canceled.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await ml_training_client.cancel_training_job(
    id="INSERT YOUR JOB ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.cancel_training_job).

{{% /tab %}}
{{< /tabs >}}

### DeleteCompletedTrainingJob

Delete a completed training job from the database, whether the job succeeded or failed.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required)

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.delete_completed_training_job).

{{% /tab %}}
{{< /tabs >}}
