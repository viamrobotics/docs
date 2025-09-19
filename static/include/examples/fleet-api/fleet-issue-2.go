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

	//  ISSUE 2: Add role
	// User ID: d3bcb264-1a60-406b-8a79-9e43da4f3c9d
	// 2025-09-02T10:31:21.526Z	ERROR	client	fleet-api/fleet-issues.go:113	rpc error: code = InvalidArgument desc = requestID=9806ca33a0007d462e545f16a7cc0ec0: provided invalid authorization id 'location_owner' for resource type 'location' and authorization type 'owner'

	memberList, _, err := cloud.ListOrganizationMembers(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}

	// Add role
	userID := memberList[1].UserID
	fmt.Println("User ID:", userID)

	err = cloud.AddRole(
		ctx,
		ORG_ID,
		userID,
		app.AuthRoleOwner,
		app.AuthResourceTypeLocation,
		LOCATION_ID,
	)
	if err != nil {
		logger.Fatal(err)
	}

	// Change role
    fmt.Printf(userID)
	err = cloud.ChangeRole(ctx, &app.Authorization{}, ORG_ID, userID, app.AuthRoleOwner, app.AuthResourceTypeOrganization, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}

	// d3bcb264-1a60-406b-8a79-9e43da4f3c9d2025-09-02T10:33:43.956Z	ERROR	client	fleet-api/fleet-issues.go:122	rpc error: code = InvalidArgument desc = requestID=df8a74809aad4dfd156a7c2bad698d23: missing required 'identity_id'

}
