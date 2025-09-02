package main

import (
	"context"
	"fmt"
	"os"

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
	MACHINE_ID = "" // Machine ID, find or create in your organization settings
	MACHINE_PART_ID = "" // Part ID, find or create in your organization settings
)

func main() {
  // :remove-start:
  ORG_ID = os.Getenv("TEST_ORG_ID")
  API_KEY = os.Getenv("VIAM_API_KEY")
  API_KEY_ID = os.Getenv("VIAM_API_KEY_ID")
  LOCATION_ID = "pg5q3j3h95"
  MACHINE_ID = "5ec7266e-f762-4ea8-9c29-4dd592718b48"
  MACHINE_PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77"
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

	orgMetadata, err := cloud.GetOrganizationMetadata(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	// The metadata is a map, not a struct, so we can't access OrganizationID field
	// Let's just check if the metadata is not nil
	if orgMetadata == nil {
		logger.Fatal("Organization metadata should not be nil")
	}

	err = cloud.UpdateOrganizationMetadata(
		ctx,
		ORG_ID,
		map[string]interface{}{
			"key": "value",
		})
	if err != nil {
		logger.Fatal(err)
	}

	testUpdatedOrgMetadata, err := cloud.GetOrganizationMetadata(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if testUpdatedOrgMetadata["key"] != "value" {
		logger.Fatal("Organization metadata value mismatch")
	}

	err = cloud.UpdateLocationMetadata(
		ctx,
		LOCATION_ID,
		map[string]interface{}{
			"key": "value",
		})
	if err != nil {
		logger.Fatal(err)
	}

	testUpdatedLocationMetadata, err := cloud.GetLocationMetadata(ctx, LOCATION_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if testUpdatedLocationMetadata["key"] != "value" {
		logger.Fatal("Location metadata value mismatch")
	}

	testUpdatedMachineMetadata, err := cloud.GetRobotMetadata(ctx, MACHINE_ID)
	if err != nil {
		logger.Fatal(err)
	}

	err = cloud.UpdateRobotMetadata(
		ctx,
		MACHINE_ID,
		map[string]interface{}{
			"key": "value",
		})
	if err != nil {
		logger.Fatal(err)
	}

	testUpdatedMachineMetadata, err = cloud.GetRobotMetadata(ctx, MACHINE_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if testUpdatedMachineMetadata["key"] != "value" {
		logger.Fatal("Machine metadata value mismatch")
	}

	testUpdatedMachinePartMetadata, err := cloud.GetRobotPartMetadata(ctx, MACHINE_PART_ID)
	if err != nil {
		logger.Fatal(err)
	}

	err = cloud.UpdateRobotPartMetadata(
		ctx,
		MACHINE_PART_ID,
		map[string]interface{}{
			"key": "value",
		})
	if err != nil {
		logger.Fatal(err)
	}

	testUpdatedMachinePartMetadata, err = cloud.GetRobotPartMetadata(ctx, MACHINE_PART_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if testUpdatedMachinePartMetadata["key"] != "value" {
		logger.Fatal("Machine part metadata value mismatch")
	}

	err = cloud.OrganizationSetSupportEmail(ctx, ORG_ID, "test@test.com")
	if err != nil {
		logger.Fatal(err)
	}

	email, err := cloud.OrganizationGetSupportEmail(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if email != "test@test.com" {
		logger.Fatal("Support email mismatch")
	}

	err = cloud.OrganizationSetSupportEmail(ctx, ORG_ID, "none")
	if err != nil {
		logger.Fatal(err)
	}

	// err = cloud.EnableBillingService(ctx, ORG_ID, &app.BillingAddress{
	// 	AddressLine1: "123 Test Street",
	// 	AddressLine2: stringPtr("Company Name"),
	// 	City:         "Test City",
	// 	State:        "Test State",
	// 	Zipcode:      "12345",
	// })
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	// _, err = cloud.GetBillingServiceConfig(ctx, ORG_ID)

	// if err != nil {
	// 	logger.Fatal(err)
	// }

	// err = cloud.DisableBillingService(ctx, ORG_ID)
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	// Upload organization logo
	logoData, err := os.ReadFile("fleet-api/logoipsum-395.png")
	if err != nil {
		logger.Fatal(err)
	}

	err = cloud.OrganizationSetLogo(ctx, ORG_ID, logoData)
	if err != nil {
		logger.Fatal(err)
	}
	_, err = cloud.OrganizationGetLogo(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}

	_, err = cloud.ListOAuthApps(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Println("All tests passed successfully!")
}

// Helper function to create string pointers
func stringPtr(s string) *string {
	return &s
}

// Helper function to create bool pointers
func boolPtr(b bool) *bool {
	return &b
}
