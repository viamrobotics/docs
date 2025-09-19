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
)

func main() {
	ORG_ID = os.Getenv("TEST_ORG_ID")
	API_KEY = os.Getenv("VIAM_API_KEY")
	API_KEY_ID = os.Getenv("VIAM_API_KEY_ID")
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

	// Create registry item
	err = cloud.CreateRegistryItem(ctx, ORG_ID, "new-registry-item-12", app.PackageTypeMLModel)
	if err != nil {
		logger.Fatal(err)
	}

	// Get number of registry items
    registryItems, err := cloud.ListRegistryItems(
		ctx,
		&ORG_ID,
		[]app.PackageType{app.PackageTypeMLModel},
		[]app.Visibility{app.VisibilityPrivate, app.VisibilityPublic},
		[]string{"linux/any"},
		[]app.RegistryItemStatus{app.RegistryItemStatusPublished},
		&app.ListRegistryItemsOptions{})
	if err != nil {
		logger.Fatal(err)
	}
	numRegistryItems := len(registryItems)
	fmt.Println("Number of registry items:", numRegistryItems)
    if numRegistryItems <= 0 {
		logger.Fatal("Expected > 0 registry items")
	}

	// DOES NOT SEEM TO DELETE THE REGISTRY ITEM
	// Delete registry item
	err = cloud.DeleteRegistryItem(ctx, "docs-test:new-registry-item-12")
	if err != nil {
		logger.Fatal(err)
	}

	// Get number of registry items
    registryItems, err = cloud.ListRegistryItems(
		ctx,
		&ORG_ID,
		[]app.PackageType{app.PackageTypeMLModel},
		[]app.Visibility{app.VisibilityPrivate, app.VisibilityPublic},
		[]string{"linux/any"},
		[]app.RegistryItemStatus{app.RegistryItemStatusPublished},
		&app.ListRegistryItemsOptions{})
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Println("Number of registry items:", len(registryItems))
	if numRegistryItems - 1 != len(registryItems) {
		logger.Fatal("Expected 1 fewer registry item after deletion")
	}

}
