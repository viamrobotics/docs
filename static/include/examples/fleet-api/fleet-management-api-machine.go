package main

import (
	"context"
	"fmt"
	"os"
	"time"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

// Configuration constants – replace with your actual values
var (
	API_KEY     = "" // API key, find or create in your organization settings
	API_KEY_ID  = "" // API key ID, find or create in your organization settings
	ORG_ID      = "" // Organization ID, find or create in your organization settings
	EMAIL_ADDRESS = "" // Email address of the user to get the user id for
	LOCATION_ID = "" // Location ID, find or create in your organization settings
)

func main() {
	// :remove-start:
	ORG_ID = os.Getenv("TEST_ORG_ID")
	API_KEY = os.Getenv("VIAM_API_KEY")
	API_KEY_ID = os.Getenv("VIAM_API_KEY_ID")
	LOCATION_ID = "pg5q3j3h95"
	// :remove-end:
	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	// Make a ViamClient
	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, API_KEY, API_KEY_ID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	// Instantiate an AppClient called "cloud"
	// to run fleet management API methods on
	cloud := viamClient.AppClient()

	// Test constants
	MACHINE_ID := "5ec7266e-f762-4ea8-9c29-4dd592718b48"
	PART_ID := "deb8782c-7b48-4d35-812d-2caa94b61f77"

	// Get robot
	robot, err := cloud.GetRobot(ctx, MACHINE_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if robot.ID != MACHINE_ID {
		logger.Fatal("Robot ID mismatch")
	}

	// Get robot API keys
	apiKeys, err := cloud.GetRobotAPIKeys(ctx, MACHINE_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(apiKeys) < 1 {
		logger.Fatal("Expected at least 1 API key")
	}
	if apiKeys[0].Authorizations[0].ResourceID != MACHINE_ID {
		logger.Fatal("API key resource ID mismatch")
	}

	// Get robot parts
	listOfParts, err := cloud.GetRobotParts(ctx, MACHINE_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfParts) != 1 {
		logger.Fatal("Expected 1 robot part")
	}
	if listOfParts[0].ID != PART_ID {
		logger.Fatal("Robot part ID mismatch")
	}

	// Get robot part
	myRobotPart, _, err := cloud.GetRobotPart(ctx, PART_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if myRobotPart.ID != PART_ID {
		logger.Fatal("Robot part ID mismatch")
	}


    filter := ""
    pageToken := ""
    startTime := time.Now().Add(-720 * time.Hour)
    endTime := time.Now()
    limit := 5
    source := ""
	partLogs, _, err := cloud.GetRobotPartLogs(
        ctx,
        PART_ID,
        &app.GetRobotPartLogsOptions{
			Filter: &filter,
			PageToken: &pageToken,
			Levels: []string{"INFO", "WARN", "ERROR"},
			Start: &startTime,
			End: &endTime,
			Limit: &limit,
			Source: &source,
		})
	if err != nil {
		logger.Fatal(err)
	}
	if len(partLogs) != 5 {
		logger.Fatal("Expected 5 log entries")
	}

	// Tail robot part logs
	logFilter := "error"
	logsStream, err := cloud.TailRobotPartLogs(ctx, PART_ID, false, &app.TailRobotPartLogsOptions{
		Filter: &logFilter,
	})
	if err != nil {
		logger.Fatal(err)
	}
	if logsStream == nil {
		logger.Fatal("Logs stream should not be nil")
	}

	// Get robot part history
	partHistory, err := cloud.GetRobotPartHistory(ctx, PART_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(partHistory) < 1 {
		logger.Fatal("Expected at least 1 history entry")
	}

	// Create new robot part
	newPartID, err := cloud.NewRobotPart(ctx, MACHINE_ID, "new-part")
	if err != nil {
		logger.Fatal(err)
	}
	if newPartID == "" {
		logger.Fatal("New part ID should not be empty")
	}

	listOfParts, err = cloud.GetRobotParts(ctx, MACHINE_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfParts) != 2 {
		logger.Fatal("Expected 2 robot parts after creation")
	}

	robotConfig := map[string]interface{}{
		"components": []map[string]interface{}{
			{
				"name":       "camera-1",
				"api":        "rdk:component:camera",
				"model":      "rdk:builtin:fake",
				"attributes": map[string]interface{}{},
			},
		},
	}

	updatedPart, err := cloud.UpdateRobotPart(ctx, PART_ID, "test-part", robotConfig)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Println(updatedPart)
	if updatedPart.Name != "test-part" {
		logger.Fatal("Updated part name mismatch")
	}

	// Mark part as main
	err = cloud.MarkPartAsMain(ctx, newPartID)
	if err != nil {
		logger.Fatal(err)
	}

	newMachinePart, _, err := cloud.GetRobotPart(ctx, newPartID)
	if err != nil {
		logger.Fatal(err)
	}
	if !newMachinePart.MainPart {
		logger.Fatal("New machine part should be main part")
	}

	err = cloud.MarkPartAsMain(ctx, PART_ID)
	if err != nil {
		logger.Fatal(err)
	}

	oldMachinePart, _, err := cloud.GetRobotPart(ctx, PART_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if !oldMachinePart.MainPart {
		logger.Fatal("Old machine part should be main part")
	}

	// Mark part for restart
	err = cloud.MarkPartForRestart(ctx, newPartID)
	if err != nil {
		logger.Fatal(err)
	}

	// Create robot part secret
	partWithNewSecret, err := cloud.CreateRobotPartSecret(ctx, newPartID)
	if err != nil {
		logger.Fatal(err)
	}
	if partWithNewSecret == nil {
		logger.Fatal("Part with new secret should not be nil")
	}
	if partWithNewSecret.ID != newPartID {
		logger.Fatal("Part secret ID mismatch")
	}

	// Delete robot part secret
    fmt.Printf("Deleting robot part secret: %+v\n", partWithNewSecret.Secrets[0].ID)
	err = cloud.DeleteRobotPartSecret(ctx, newPartID, partWithNewSecret.Secrets[0].ID)
	if err != nil {
		logger.Fatal(err)
	}

	// Delete robot part
	err = cloud.DeleteRobotPart(ctx, newPartID)
	if err != nil {
		logger.Fatal(err)
	}

	listOfParts, err = cloud.GetRobotParts(ctx, MACHINE_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfParts) != 1 {
		logger.Fatal("Expected 1 robot part after deletion")
	}

	// List robots
	listOfMachines, err := cloud.ListRobots(ctx, LOCATION_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfMachines) != 1 {
		logger.Fatal("Expected 1 machine")
	}
	if listOfMachines[0].ID != MACHINE_ID {
		logger.Fatal("Machine ID mismatch")
	}

	// Create new robot
	newMachineID, err := cloud.NewRobot(ctx, "test-robot", LOCATION_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if newMachineID == "" {
		logger.Fatal("New machine ID should not be empty")
	}

	listOfMachines, err = cloud.ListRobots(ctx, LOCATION_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfMachines) != 2 {
		logger.Fatal("Expected 2 machines after creation")
	}

	// Update robot
	updatedMachine, err := cloud.UpdateRobot(ctx, newMachineID, "test-robot-new-name", LOCATION_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if updatedMachine.Name != "test-robot-new-name" {
		logger.Fatal("Updated machine name mismatch")
	}

	// Delete robot
	err = cloud.DeleteRobot(ctx, newMachineID)
	if err != nil {
		logger.Fatal(err)
	}

	listOfMachines, err = cloud.ListRobots(ctx, LOCATION_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfMachines) != 1 {
		logger.Fatal("Expected 1 machine after deletion")
	}

	fmt.Println("All tests passed successfully!")
}

// Helper function to create string pointers
func stringPtr(s string) *string {
	return &s
}

// Helper function to create int pointers
func intPtr(i int) *int {
	return &i
}
