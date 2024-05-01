### CancelTrainingJob

{{< tabs >}}
{{% tab name="Python" %}}

Cancels the specified training job.

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): the id of the job to be canceled.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.cancel_training_job).

``` python {class="line-numbers linkable-line-numbers"}
await ml_training_client.cancel_training_job(
    id="INSERT YOUR JOB ID")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/cancelTrainingJob.html).

{{% /tab %}}
{{< /tabs >}}
