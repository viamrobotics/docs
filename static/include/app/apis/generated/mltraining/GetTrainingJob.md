### GetTrainingJob

{{< tabs >}}
{{% tab name="Python" %}}

Gets training job data.

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): id of the requested training job.


**Returns:**

- [(viam.proto.app.mltraining.TrainingJobMetadata)](INSERT RETURN TYPE LINK): training job data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.get_training_job).

``` python {class="line-numbers linkable-line-numbers"}
job_metadata = await ml_training_client.get_training_job(
    id="INSERT YOUR JOB ID")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/getTrainingJob.html).

{{% /tab %}}
{{< /tabs >}}
