package main

import (
	"context"
	"fmt"

	"go.viam.com/rdk/components/camera"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/referenceframe"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/spatialmath"
	"go.viam.com/rdk/utils"
)

func main() {
	logger := logging.NewLogger("client")
	machine, err := client.New(
		context.Background(),
		"<YOUR-REMOTE-ADDRESS>",
		logger,
		client.WithDialOptions(utils.WithEntityCredentials(
			// Replace "<API-KEY-ID>" (including brackets) with your machine's
			// API Key ID
			"<API-KEY-ID>",
			utils.Credentials{
				Type: utils.CredentialsTypeAPIKey,
				// Replace "<API-KEY>" (including brackets) with your machine's API key
				Payload: "<API-KEY>",
			})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	logger.Info("Resources:")
	logger.Info(machine.ResourceNames())

	defer machine.Close(context.Background())

	q := resource.NewDiscoveryQuery(camera.API, resource.Model{Name: "webcam", Family: resource.DefaultModelFamily})

	// Define a list of discovery queries and get potential component configurations with these queries.
	out, err := machine.DiscoverComponents(context.Background(), []resource.DiscoveryQuery{q})
	logger.Info(out)

	frameSystem, err := machine.FrameSystemConfig(context.Background())
	fmt.Println(frameSystem)

	boardOrigin := referenceframe.NewPoseInFrame("board-1", spatialmath.NewZeroPose())
	cameraToBoard, err := machine.TransformPose(context.Background(), boardOrigin, "camera-1", nil)
	if err != nil {
		logger.Error("Error transforming components:", err)
		return
	}
	fmt.Println(cameraToBoard)

	status, err := machine.Status(context.Background(), nil)
	fmt.Println(status)

	err = machine.StopAll(context.Background(), nil)

	metadata, err := machine.CloudMetadata(context.Background())
	fmt.Println("test")
	fmt.Println(metadata)

	primary_org_id := metadata.PrimaryOrgID
	location_id := metadata.LocationID
	machine_id := metadata.MachineID
	machine_part_id := metadata.MachinePartID

	fmt.Println(machine_id, machine_part_id, primary_org_id, location_id)

	err = machine.Shutdown(context.Background())
	err = machine.Close(context.Background())

}
