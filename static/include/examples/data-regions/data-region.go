// :snippet-start: data-region
package main

import (
	"context"
	"fmt"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	orgID := ""
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY_DATA_REGIONS")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID_DATA_REGIONS")
	orgID = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1"
	// :remove-end:

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()
	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	// Get the app client from the viam client
	appClient := viamClient.AppClient()

	// Check organization region
	org, err := appClient.GetOrganization(ctx, orgID)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Printf("Current region: %s\n", org.DefaultRegion)

	// Configure UpdateOrganizationOptions for European region
	newRegion := "eu-west"  // or "us-central"
	updateOptions := &app.UpdateOrganizationOptions{
		Name:   nil,
		Region: &newRegion,
	}

	// Update organization region
	updatedOrg, err := appClient.UpdateOrganization(ctx, orgID, updateOptions)
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Organization region updated to: %s\n", updatedOrg.DefaultRegion)

}
// :snippet-end: