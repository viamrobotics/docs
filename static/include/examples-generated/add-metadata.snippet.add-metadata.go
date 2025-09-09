package main

import (
	"context"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/utils/rpc"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""


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

}
