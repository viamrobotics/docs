---
title: "Add an AWS Sagemaker Modular Vision Service"
linkTitle: "AWS Sagemaker Vision Modular Service"
weight: 70
type: "docs"
description: "Add a modular vision service to access ML models deployed on cloud endpoints using AWS Sagemaker."
tags: ["vision", "model training", "ml", "services"]
# SMEs: Khari
---

Viam provides an `aws-sagemaker` model of [vision service](/services/vision) with which you can use ML models you deploy on cloud endpoints using [AWS Sagemaker](https://aws.amazon.com/sagemaker/).

Configure this vision service as a [modular resource](/modular-resources/) on your robot to access and perform inference with AWS-deployed ML models.

Usage information is also available on [GitHub](https://github.com/viam-labs/aws-sagemaker).

## Requirements

You must have a model deployed to an AWS Sagemaker endpoint.
You can do this programmatically or through the AWS console.
Follow [these instructions](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html) to do so.

Then, if you haven't done so already, create a new robot in [the Viam app](https://app.viam.com) and connect to the robot.

## Configuration

{{< tabs name="Add the AWS Sagemaker modular service">}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot’s page in the [Viam app](https://app.viam.com).
Click on the **Services** subtab and click the **Create service** button.
Search for `aws-sagemaker`, then select the version from the [Registry](https://app.viam.com/registry).
Give your resource a name of your choice and click **Create**.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the following to your `"modules"` array:

```json {class="line-numbers linkable-line-numbers"}
{
  "type": "registry",
  "name": "viam_aws-sagemaker",
  "module_id": "viam:aws-sagemaker",
  "version": "latest"
}
```

Add the following to your `"services"` array:

```json {class="line-numbers linkable-line-numbers"}
[
  {
    "name": "your-aws-sagemaker-service",
    "type": "vision",
    "namespace": "rdk",
    "model": "viam:vision:aws-sagemaker",
    "attributes": {}
  }
]
```

{{% /tab %}}
{{< /tabs >}}

### Attributes

After deploying your model to an endpoint, configure the required attributes to connect your robot to the AWS Sagemaker model performing inferences in the cloud.
The following attributes are available for the vision service `viam:vision:aws-sagemaker`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `endpoint_name` | string | **Required** | The name of the endpoint as given by AWS. |
| `aws_region` | string | **Required** | The name of the region in AWS under which the model can be found. |
| `access_json` | string | **Required** | The on-robot location of a JSON file that contains your AWS access credentials (AWS Access Key ID and Secret Access Key). Follow [these instructions](https://www.msp360.com/resources/blog/how-to-find-your-aws-access-key-id-and-secret-access-key/) to retrieve your credentials, and reference [this example JSON file containing credentials](#example-access_json). |
| `source_cams` | array | **Required** | The name of each [camera](/components/camera) you have configured on your robot that you want to use as input for the vision service. |

An example configuration would look like this, within your robot's `"services"` array:

```json {class="line-numbers linkable-line-numbers"}
[
  {
    "name": "myVisionModule",
    "type": "vision",
    "namespace": "rdk",
    "model": "viam:vision:aws-sagemaker",
    "attributes": {
      "access_json": "/Users/myname/Documents/accessfile.json",
      "endpoint_name": "jumpstart-dft-tf-ic-efficientnet-b1-classification-1",
      "aws_region": "us-east-2",
      "source_cams": ["myCam1", "myCam2"]
    }
  }
]
```

#### Example `"access_json"`

```json {class="line-numbers linkable-line-numbers"}
{
  "access_key": "UE9S0AG9KS4F3",
  "secret_access_key": "L23LKkl0d5<M0R3S4F3"
}
```

## Next steps: use your ML-enabled vision service

Now, use the `viam:vision:aws-sagemaker` modular service to perform inference with the machine learning model deployed through AWS Sagemaker on your robot.

Configure a [transform camera](/components/camera/transform/) to see classifications or detections appear in your robot's field of vision.

You can also use the following methods of the [vision service API](/services/vision/#api) to programmatically get detections and classifications with your modular vision service and camera:

- [`GetDetections()`](/services/vision/#getdetections)
- [`GetDetectionsFromCamera()`](/services/vision/#getdetectionsfromcamera)
- [`GetClassifications()`](/services/vision/#getclassifications)
- [`GetClassificationsFromCamera()`](/services/vision/#getclassificationsfromcamera)
