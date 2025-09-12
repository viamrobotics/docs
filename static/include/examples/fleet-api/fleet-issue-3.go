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

    //  ISSUE 1: CREATE & DELETE REGISTRY ITEM

	// // Create registry item
	// err = cloud.CreateRegistryItem(ctx, ORG_ID, "new-registry-item-12", app.PackageTypeMLModel)
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	// // Get number of registry items
    // registryItems, err := cloud.ListRegistryItems(
	// 	ctx,
	// 	&ORG_ID,
	// 	[]app.PackageType{app.PackageTypeMLModel},
	// 	[]app.Visibility{app.VisibilityPrivate, app.VisibilityPublic},
	// 	[]string{"linux/any"},
	// 	[]app.RegistryItemStatus{app.RegistryItemStatusPublished},
	// 	&app.ListRegistryItemsOptions{})
	// if err != nil {
	// 	logger.Fatal(err)
	// }
	// numRegistryItems := len(registryItems)
	// fmt.Println("Number of registry items:", numRegistryItems)
    // if numRegistryItems <= 0 {
	// 	logger.Fatal("Expected > 0 registry items")
	// }

	// // DOES NOT SEEM TO DELETE THE REGISTRY ITEM
	// // Delete registry item
	// err = cloud.DeleteRegistryItem(ctx, "docs-test:new-registry-item-12")
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	// // Get number of registry items
    // registryItems, err = cloud.ListRegistryItems(
	// 	ctx,
	// 	&ORG_ID,
	// 	[]app.PackageType{app.PackageTypeMLModel},
	// 	[]app.Visibility{app.VisibilityPrivate, app.VisibilityPublic},
	// 	[]string{"linux/any"},
	// 	[]app.RegistryItemStatus{app.RegistryItemStatusPublished},
	// 	&app.ListRegistryItemsOptions{})
	// if err != nil {
	// 	logger.Fatal(err)
	// }
	// fmt.Println("Number of registry items:", len(registryItems))
	// if numRegistryItems - 1 != len(registryItems) {
	// 	logger.Fatal("Expected 1 fewer registry item after deletion")
	// }

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

	// err = cloud.AddRole(
	// 	ctx,
	// 	ORG_ID,
	// 	userID,
	// 	app.AuthRoleOwner,
	// 	app.AuthResourceTypeLocation,
	// 	LOCATION_ID,
	// )
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	// Change role
    fmt.Printf(userID)
	// err = cloud.ChangeRole(ctx, &app.Authorization{}, ORG_ID, userID, app.AuthRoleOwner, app.AuthResourceTypeOrganization, ORG_ID)
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	// d3bcb264-1a60-406b-8a79-9e43da4f3c9d2025-09-02T10:33:43.956Z	ERROR	client	fleet-api/fleet-issues.go:122	rpc error: code = InvalidArgument desc = requestID=df8a74809aad4dfd156a7c2bad698d23: missing required 'identity_id'

	//  ISSUE 3: It seems we can't create keys because we can't create APIKeyAuthorization structs

	// Create API key
	// Since APIKeyAuthorization has unexported fields, we can't construct it directly
	// apiKey, apiKeyID, err := cloud.CreateKey(ctx, ORG_ID, []app.APIKeyAuthorization{{
	// 	Role: app.AuthRoleOwner,
	// 	ResourceType: app.AuthResourceTypeLocation,
	// 	ResourceID: LOCATION_ID,
	// }}, "mytestkey")
	// if err != nil {
	// 	logger.Fatal(err)
	// }
	// if apiKey == "" {
	// 	logger.Fatal("API key should not be empty")
	// }
	// if apiKeyID == "" {
	// 	logger.Fatal("API key ID should not be empty")
	// }

	//  ISSUE 4: RenameKey does not return the key ID
	apiKeyID2, apiKey2, err := cloud.CreateKeyFromExistingKeyAuthorizations(ctx, newAPIKeyID)
	if err != nil {
		logger.Fatal(err)
	}
	if apiKey2 == "" {
		logger.Fatal("API key 2 should not be empty")
	}
	if apiKeyID2 == "" {
		logger.Fatal("API key ID 2 should not be empty")
	}
	fmt.Printf("API key id 2: %+v\n", apiKeyID2)

	apiKeyID3, apiKeyName3, err := cloud.RenameKey(ctx, apiKeyID2, "mytestkey2newName")
	if err != nil {
		logger.Fatal(err)
	}
	if apiKeyName3 != "mytestkey2newName" {
		logger.Fatal("API key 3 should be renamed")
	}
	fmt.Printf("API key id 3: %+v\n", apiKeyID3)

}
