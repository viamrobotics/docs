---
title: "Access APIs from within a module"
linkTitle: "Use platform APIs"
weight: 25
layout: "docs"
type: "docs"
description: "Write your validate and reconfigure functions to handle dependencies in your custom modular resource."
---

To use the platform or machine APIs, you must authenticate using API keys.

- [Use platform APIs from a module](#use-platform-apis-from-a-module)
- [Use the machine management API from a module](#use-the-machine-management-api-from-a-module)

## Use platform APIs from a module

The following steps show you how to use the following APIs from a module:

- [Fleet management (`app_client`)](/dev/reference/apis/fleet/)
- [Data client (`data_client`)](/dev/reference/apis/data-client/)
- [ML training (`ml_training_client`)](/dev/reference/apis/ml-training-client/)
- [Billing (`billing_client`)](/dev/reference/apis/billing-client/)

{{< tabs >}}
{{% tab name="Python" %}}

1. Add the following imports and the `create_viam_client_from_module` method:

   ```python {class="line-numbers linkable-line-numbers"}
   import os
   from viam.rpc.dial import DialOptions, Credentials
   from viam.app.viam_client import ViamClient
   from viam.app.app_client import AppClient
   from viam.app.data_client import DataClient
   from viam.app.ml_training_client import MLTrainingClient
   from viam.app.billing_client import BillingClient

   async def create_viam_client_from_module():
       # Get API credentials from module environment variables
       api_key = os.environ.get("VIAM_API_KEY")
       api_key_id = os.environ.get("VIAM_API_KEY_ID")

       if not api_key or not api_key_id:
           raise Exception("VIAM_API_KEY and VIAM_API_KEY_ID " +
                           "environment variables are required")

       # Create dial options with API key authentication
       dial_options = DialOptions(
           credentials=Credentials(
               type="api-key",
               payload=api_key,
           ),
           auth_entity=api_key_id
       )

       # Create ViamClient and get app_client
       viam_client = await ViamClient.create_from_dial_options(dial_options)

       return viam_client
   ```

1. Add the `viam_client` or other clients to the resource class:

   ```python {class="line-numbers linkable-line-numbers"}
   class TestSensor(Sensor, EasyResource):
       viam_client: Optional[ViamClient] = None
       app_client: Optional[AppClient] = None
       data_client: Optional[DataClient] = None
       ml_training_client: Optional[MLTrainingClient] = None
       billing_client: Optional[BillingClient] = None

       # ...
   ```

1. Initialize the clients and use them:

   ```python {class="line-numbers linkable-line-numbers"}
   async def some_module_function(self):
      # Ensure there is only one viam_client connection
      if not self.viam_client:
          self.viam_client = await create_viam_client_from_module()

      self.app_client = self.viam_client.app_client
      self.data_client = self.viam_client.data_client
      self.ml_training_client = self.viam_client.ml_training_client
      self.billing_client = self.viam_client.billing_client
      # Use the clients in your module
      locations = await self.app_client.list_locations(os.environ.get("VIAM_PRIMARY_ORG_ID"))
   ```

{{% /tab %}}
{{< /tabs >}}

The [module environment variables](/operate/get-started/other-hardware/module-configuration/) `VIAM_API_KEY` and `VIAM_API_KEY_ID` provide [machine owner access](/manage/manage/rbac/) for the machine the module is running on.

If you need a higher level of access, you can pass API keys as part of the module configuration:

1. Create an API key with the appropriate [permissions](/manage/manage/rbac/) from your organization settings page.
1. Add the API key and API key ID values to the module configuration:

   ```json
   {
     "modules": [
       {
         "type": "registry",
         "name": "example-module",
         "module_id": "naomi:example-module",
         "version": "latest",
         "env": {
           "VIAM_API_KEY": "abcdefg987654321abcdefghi",
           "VIAM_API_KEY_ID": "1234abcd-123a-987b-1234567890abc"
         }
       }
     ]
   }
   ```

   This changes the environment variables `VIAM_API_KEY` and `VIAM_API_KEY_ID` from the default to the provided ones.

## Use the machine management API from a module

To use the [machine management (`robot_client`) API](/dev/reference/apis/robot/), you must get the machine's FQDN and API keys from the module environment variables.

{{< tabs >}}
{{% tab name="Python" %}}

1. Add the following imports and the `create_robot_client_from_module` method:

   ```python {class="line-numbers linkable-line-numbers"}
   # Add imports
   import os
   from viam.robot.client import RobotClient

   # For robot client, you can also use the machine's FQDN:
   async def create_robot_client_from_module():
       # Get API credentials from module environment variables
       api_key = os.environ.get("VIAM_API_KEY")
       api_key_id = os.environ.get("VIAM_API_KEY_ID")
       machine_fqdn = os.environ.get("VIAM_MACHINE_FQDN")

       if not api_key or not api_key_id or not machine_fqdn:
           raise Exception("VIAM_API_KEY, VIAM_API_KEY_ID, and " +
                           "VIAM_MACHINE_FQDN " +
                           "environment variables are required")

       # Create robot client options with API key authentication
       opts = RobotClient.Options.with_api_key(
           api_key=api_key,
           api_key_id=api_key_id
       )

       # Create RobotClient using the machine's FQDN
       robot_client = await RobotClient.at_address(machine_fqdn, opts)

       return robot_client
   ```

1. Add the `robot_client` or other clients to the resource class:

   ```python {class="line-numbers linkable-line-numbers"}
   class TestSensor(Sensor, EasyResource):
       robot_client: Optional[RobotClient] = None
       # ...
   ```

1. Initialize the client and use it:

   ```python {class="line-numbers linkable-line-numbers"}
   async def some_module_function(self):
       # Ensure there is only one robot client
       if not self.robot_client:
           self.robot_client = await create_robot_client_from_module()
       # Use the robot client
       resources = [str(name) for name in self.robot_client.resource_names]
   ```

{{% /tab %}}

<!--
TODO: TEST.
```go {class="line-numbers linkable-line-numbers"}
func createRobotClientFromModule(ctx context.Context) (client.RobotClient, error) {
    // Get API credentials and machine FQDN from module environment variables
    apiKey := os.Getenv("VIAM_API_KEY")
    apiKeyID := os.Getenv("VIAM_API_KEY_ID")
    machineFQDN := os.Getenv("VIAM_MACHINE_FQDN")

    if apiKey == "" || apiKeyID == "" || machineFQDN == "" {
        return nil, fmt.Errorf("VIAM_API_KEY, VIAM_API_KEY_ID, and " +
            "VIAM_MACHINE_FQDN environment variables are required")
    }

    logger := logging.NewLogger("client")

    // Create robot client with API key authentication
    robotClient, err := client.New(
        ctx,
        machineFQDN,
        logger,
        client.WithDialOptions(rpc.WithEntityCredentials(
            apiKeyID,
            rpc.Credentials{
                Type:    rpc.CredentialsTypeAPIKey,
                Payload: apiKey,
            })),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to create robot client: %w", err)
    }

    return robotClient, nil
}

func NewMySensor(ctx context.Context,deps resource.Dependencies,
   name resource.Name, conf *Config, logger logging.Logger) (sensor.Sensor, error) {

   cancelCtx, cancelFunc := context.WithCancel(context.Background())

    s := &myModuleMySensor{
     name:       name,
     logger:     logger,
     cfg:        conf,
     cancelCtx:  cancelCtx,
     cancelFunc: cancelFunc,
   }

   robotClient, err := &createRobotClientFromModule()
   if err != nil {
     return nil, errors.New("failed to get robot client")
   }
   s.robotClient = robotClient

   return s, nil
 }

func (c *Component) SomeModuleFunction(ctx context.Context) error {
    // Use the robot client
    resources := robotClient.ResourceNames()
}
``` -->

{{% /tabs %}}

The [module environment variables](/operate/get-started/other-hardware/module-configuration/) `VIAM_API_KEY` and `VIAM_API_KEY_ID` provide [machine owner access](/manage/manage/rbac/) for the machine the module is running on.

If you need a higher level of access to access other machines, you can pass API keys as part of the module configuration:

1. Create an API key with the appropriate [permissions](/manage/manage/rbac/) from your organization settings page.
1. Add the API key and API key ID values to the module configuration:

   ```json
   {
     "modules": [
       {
         "type": "registry",
         "name": "example-module",
         "module_id": "naomi:example-module",
         "version": "latest",
         "env": {
           "VIAM_API_KEY": "abcdefg987654321abcdefghi",
           "VIAM_API_KEY_ID": "1234abcd-123a-987b-1234567890abc"
         }
       }
     ]
   }
   ```

   This changes the environment variables `VIAM_API_KEY` and `VIAM_API_KEY_ID` from the default to the provided ones.
