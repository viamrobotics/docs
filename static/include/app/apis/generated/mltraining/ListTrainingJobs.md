### ListTrainingJobs

{{< tabs >}}
{{% tab name="Python" %}}

Returns training job data for all jobs within an org.

**Parameters:**

- `org_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): the id of the org to request training job data from.
- `training_status` [(viam.proto.app.mltraining.TrainingStatus.ValueType)](https://python.viam.dev/autoapi/viam/gen/app/mltraining/v1/ml_training_pb2/index.html#viam.gen.app.mltraining.v1.ml_training_pb2.TrainingStatus) (optional): status of training jobs to filter the list by. If unspecified, all training jobs will be returned.

**Returns:**

- [(List[viam.proto.app.mltraining.TrainingJobMetadata])](INSERT RETURN TYPE LINK): a list of training job data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.list_training_jobs).

``` python {class="line-numbers linkable-line-numbers"}
jobs_metadata = await ml_training_client.list_training_jobs(
    org_id="INSERT YOUR ORG ID")

first_job_id = jobs_metadata[1].id
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `status` [(TrainingStatus)](https://flutter.viam.dev/viam_protos.app.ml_training/TrainingStatus-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/listTrainingJobs.html).

{{% /tab %}}
{{< /tabs >}}
