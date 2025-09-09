// :snippet-start: add-metadata
package main

import (
	"context"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/utils/rpc"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	// :remove-end:

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	machine, err := client.New(
		context.Background(),
		machineAddress,
		logger,
		client.WithDialOptions(rpc.WithEntityCredentials(
			apiKeyID,
			rpc.Credentials{
				Type:    rpc.CredentialsTypeAPIKey,
				Payload: apiKey,
			})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	appClient := viamClient.AppClient()
	metadata, err := machine.CloudMetadata(ctx)
	if err != nil {
		logger.Fatal(err)
	}
	machineID := metadata.MachineID
	appClient.UpdateRobotMetadata(ctx, machineID, map[string]interface{}{
		"TEST_API_KEY": "ABC123",
	})

	// :remove-start:
	metadata1, err := appClient.GetRobotMetadata(ctx, machineID)
	if err != nil {
		logger.Fatal(err)
	}

	// Print the current metadata
	if metadata1["TEST_API_KEY"] != "ABC123" {
		logger.Fatal("Metadata mismatch")
	}
	appClient.UpdateRobotMetadata(ctx, machineID, map[string]interface{}{})
	metadata2, err := appClient.GetRobotMetadata(ctx, machineID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(metadata2) != 0 {
		logger.Fatal("Metadata mismatch")
	}
	// :remove-end:
}
// :snippet-end: