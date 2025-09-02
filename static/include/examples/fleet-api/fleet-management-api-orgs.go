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
  TEST_EMAIL := os.Getenv("TEST_EMAIL")
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

	// TODO: internal only
	// id, err := cloud.GetUserIDByEmail(ctx, EMAIL_ADDRESS)
	// if err != nil {
	//     logger.Fatal(err)
	// }
	// fmt.Printf("USER ID: %s\n", id)

	// TODO: internal only
	// organization, err := cloud.CreateOrganization(ctx, "example-org")
	// if err != nil {
	//     logger.Fatal(err)
	// }
	// fmt.Printf("Organization: %+v\n", organization)

	orgList, err := cloud.ListOrganizations(ctx)
	if err != nil {
		logger.Fatal(err)
	}
	if len(orgList) == 0 {
		logger.Fatal("No organizations found")
	}
	if orgList[0].ID != ORG_ID {
		logger.Fatal("Organization ID mismatch")
	}

	orgListWithAccess, err := cloud.GetOrganizationsWithAccessToLocation(ctx, LOCATION_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(orgListWithAccess) == 0 {
		logger.Fatal("No organizations with access to location found")
	}
	if orgListWithAccess[0].ID != ORG_ID {
		logger.Fatal("Organization ID mismatch")
	}

	memberList, invitesList, err := cloud.ListOrganizationMembers(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(memberList) == 0 {
		logger.Fatal("No organization members found")
	}
	if memberList[0].UserID != "4984b52e-6715-4a52-8321-a05bdd4bb4a4" {
		logger.Fatal("Member user ID mismatch")
	}

	// TODO: internal only
	// orgListByUser, err := cloud.ListOrganizationsByUser(ctx, firstUserID)
	// if err != nil {
	//     logger.Fatal(err)
	// }
	// fmt.Printf("Organizations by user: %+v\n", orgListByUser)

	org, err := cloud.GetOrganization(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if org.ID != ORG_ID {
		logger.Fatal("Organization ID mismatch")
	}

	orgNamespace := "test-org-namespace-unavailable"
	available, err := cloud.GetOrganizationNamespaceAvailability(ctx, orgNamespace)
	if err != nil {
		logger.Fatal(err)
	}
	if !available {
		logger.Fatal("Namespace should be available")
	}

	organization, err := cloud.UpdateOrganization(
    ctx, ORG_ID,
    &app.UpdateOrganizationOptions{
      Name: stringPtr("docs-scheduled-tests"),
    })
	if err != nil {
		logger.Fatal(err)
	}
	if organization.Name != "docs-scheduled-tests" {
		logger.Fatal("Organization name mismatch")
	}

	// CANT TEST
	// err = cloud.DeleteOrganization(ctx, "298d2032-7a63-4a7f-810c-0a841e219bd9")
	// if err != nil {
	//     logger.Fatal(err)
	// }

	// Create organization invite
	_, err = cloud.CreateOrganizationInvite(
    ctx, ORG_ID, testEmail, []*app.Authorization{},
    &app.CreateOrganizationInviteOptions{
		  SendEmailInvite: boolPtr(true),
	  })
	if err != nil {
		logger.Fatal(err)
	}

	memberList, invitesList, err = cloud.ListOrganizationMembers(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(invitesList) != 1 {
		logger.Fatal("Expected 1 invite")
	}
	if invitesList[0].Email != testEmail {
		logger.Fatal("Invite email mismatch")
	}

	// Update organization invite authorizations
	updateInvite, err := cloud.UpdateOrganizationInviteAuthorizations(
    ctx, ORG_ID, testEmail,
    []*app.Authorization{
      {
        AuthorizationType: "role",
        AuthorizationID:   "location_owner",
        ResourceType:      "location",
        ResourceID:        LOCATION_ID,
        OrganizationID:    ORG_ID,
        IdentityID:        "",
      },
    }, []*app.Authorization{})
	if err != nil {
		logger.Fatal(err)
	}
	if len(updateInvite.Authorizations) < 2 {
		logger.Fatal("Expected at least 2 authorizations")
	}
	if updateInvite.Authorizations[1].AuthorizationID != "location_owner" {
		logger.Fatal("Authorization ID mismatch")
	}

	orgInvite, err := cloud.ResendOrganizationInvite(ctx, ORG_ID, TEST_EMAIL)
	if err != nil {
		logger.Fatal(err)
	}
	if orgInvite.Email != TEST_EMAIL {
		logger.Fatal("Resend invite email mismatch")
	}

	err = cloud.DeleteOrganizationInvite(ctx, ORG_ID, TEST_EMAIL)
	if err != nil {
		logger.Fatal(err)
	}

	memberList, invitesList, err = cloud.ListOrganizationMembers(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(invitesList) != 0 {
		logger.Fatal("Expected 0 invites after deletion")
	}

	// CANT TEST
	// err = cloud.DeleteOrganizationMember(ctx, ORG_ID, firstUserID)
	// if err != nil {
	//     logger.Fatal(err)
	// }

	// Create location
	newLocation, err := cloud.CreateLocation(
    ctx, ORG_ID, "Robotville", &app.CreateLocationOptions{
  		ParentLocationID: stringPtr(LOCATION_ID),
	  })
	if err != nil {
		logger.Fatal(err)
	}
	if newLocation.Name != "Robotville" {
		logger.Fatal("Location name mismatch")
	}

	location, err := cloud.GetLocation(ctx, newLocation.ID)
	if err != nil {
		logger.Fatal(err)
	}
	if location.Name != "Robotville" {
		logger.Fatal("Retrieved location name mismatch")
	}

	// Update location
	updatedLocation, err := cloud.UpdateLocation(
    ctx, newLocation.ID, &app.UpdateLocationOptions{
      ParentLocationID: stringPtr(LOCATION_ID),
      Name: stringPtr("Robotville 2"),
    })
	if err != nil {
		logger.Fatal(err)
	}
	if updatedLocation.Name != "Robotville 2" {
		logger.Fatal("Updated location name mismatch")
	}

	// Share and unshare location
	orgID2 := "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1"
	err = cloud.ShareLocation(ctx, newLocation.ID, orgID2)
	if err != nil {
		logger.Fatal(err)
	}

	err = cloud.UnshareLocation(ctx, newLocation.ID, orgID2)
	if err != nil {
		logger.Fatal(err)
	}

	locAuth, err := cloud.LocationAuth(ctx, newLocation.ID)
	if err != nil {
		logger.Fatal(err)
	}
	if locAuth.LocationID != newLocation.ID {
		logger.Fatal("Location auth location ID mismatch")
	}

	newLocAuth, err := cloud.CreateLocationSecret(ctx, newLocation.ID)
	if err != nil {
		logger.Fatal(err)
	}
	if newLocAuth.LocationID != newLocation.ID {
		logger.Fatal("New location auth location ID mismatch")
	}
  fmt.Printf("New location auth: %+v\n", newLocAuth.Secrets[0].ID)

	err = cloud.DeleteLocationSecret(ctx, newLocAuth.LocationID, newLocAuth.Secrets[0].ID)
	if err != nil {
		logger.Fatal(err)
	}

	locAuth, err = cloud.LocationAuth(ctx, newLocation.ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(locAuth.Secrets) != 1 {
		logger.Fatal("Expected 1 secret after deletion")
	}

	err = cloud.DeleteLocation(ctx, newLocation.ID)
	if err != nil {
		logger.Fatal(err)
	}

	locations, err := cloud.ListLocations(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(locations) != 2 {
		logger.Fatal("Expected 2 locations after deletion")
	}

	// API Key management
	keys, err := cloud.ListKeys(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
  fmt.Printf("Keys: %+v\n", keys)
	numKeys := len(keys)
  if numKeys == 0 {
    logger.Fatal("Expected keys")
  }

	// Create API key
	// Since APIKeyAuthorization has unexported fields, we can't construct it directly
	// The SDK might provide a constructor or expect a different approach
	// apiKey, apiKeyID, err := cloud.CreateKey(ctx, ORG_ID, []app.APIKeyAuthorization{}, "mytestkey")
	// if err != nil {
	// 	logger.Fatal(err)
	// }
	// if apiKey == "" {
	// 	logger.Fatal("API key should not be empty")
	// }
	// if apiKeyID == "" {
	// 	logger.Fatal("API key ID should not be empty")
	// }

	// Rotate key
  apiKeyID := "0db45704-b5f7-4731-aff1-73c957f3c650"
	newAPIKeyID, newAPIKey, err := cloud.RotateKey(ctx, apiKeyID)
	if err != nil {
		logger.Fatal(err)
	}
	if newAPIKeyID == "" {
		logger.Fatal("New API key ID should not be empty")
	}
	if newAPIKey == "" {
		logger.Fatal("New API key should not be empty")
	}
	// if apiKey == newAPIKey {
	// 	logger.Fatal("API keys should be different after rotation")
	// }

	// keys, err = cloud.ListKeys(ctx, ORG_ID)
  // fmt.Printf("Keys: %d\n", keys)
  // for _, key := range keys {
  //   fmt.Printf("Key ID: %+v\n", key.APIKey)
  //   fmt.Printf("Key Authorizations: %+v\n", key.Authorizations)
  // }
	// if err != nil {
	// 	logger.Fatal(err)
	// }
	// newNumKeys := len(keys)
	// if newNumKeys != numKeys+1 {
	// 	logger.Fatal("Expected one more key after rotation")
	// }

	// Create key from existing authorizations
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

	keys, err = cloud.ListKeys(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	newNumKeys2 := len(keys)
	if newNumKeys2 != numKeys+1 {
		logger.Fatal("Expected one more key after creating from existing")
	}

	// Clean up keys
	err = cloud.DeleteKey(ctx, apiKeyID2)
	if err != nil {
		logger.Fatal(err)
	}

	keys, err = cloud.ListKeys(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}
	finalNumKeys := len(keys)
	if finalNumKeys != numKeys {
		logger.Fatal("Expected original number of keys after cleanup")
	}

	// Role management
	userID := memberList[1].UserID

	// err = cloud.AddRole(
  //   ctx,
  //   ORG_ID,
  //   userID,
  //   app.AuthRoleOwner,
  //   app.AuthResourceTypeLocation,
  //   LOCATION_ID,
  // )
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	memberList, invitesList, err = cloud.ListOrganizationMembers(ctx, ORG_ID)
	if err != nil {
		logger.Fatal(err)
	}

	listOfAuths, err := cloud.ListAuthorizations(ctx, ORG_ID, []string{LOCATION_ID})
  fmt.Printf("List of authorizations: %+v\n", listOfAuths)
	if err != nil {
		logger.Fatal(err)
	}
	// if len(listOfAuths) != 1 {
	// 	logger.Fatal("Expected 1 authorization")
	// }

	// Change role
  fmt.Printf(userID)
	// err = cloud.ChangeRole(ctx, &app.Authorization{}, ORG_ID, userID, app.AuthRoleOwner, app.AuthResourceTypeOrganization, ORG_ID)
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	listOfAuths, err = cloud.ListAuthorizations(ctx, ORG_ID, []string{LOCATION_ID})
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfAuths) != 0 {
		logger.Fatal("Expected 0 authorizations after role change")
	}

	listOfAuths, err = cloud.ListAuthorizations(ctx, ORG_ID, []string{ORG_ID})
	if err != nil {
		logger.Fatal(err)
	}
  fmt.Printf("List of authorizations: %+v\n", listOfAuths)
	// if len(listOfAuths) != 3 {
	// 	logger.Fatal("Expected 3 authorizations for organization")
	// }

	// Remove role
	// err = cloud.RemoveRole(ctx, &app.Authorization{
	// 	AuthorizationType: app.AuthRoleOwner,
	// 	AuthorizationID:   "organization_owner",
	// 	OrganizationID:    ORG_ID,
	// 	ResourceID:        ORG_ID,
	// 	ResourceType:      app.AuthResourceTypeOrganization,
	// 	IdentityID:        "",
  //   IdentityType:      "api-key",
	// })
	// if err != nil {
	// 	logger.Fatal(err)
	// }

	listOfAuths, err = cloud.ListAuthorizations(ctx, ORG_ID, []string{ORG_ID})
	if err != nil {
		logger.Fatal(err)
	}
	if len(listOfAuths) != 2 {
		logger.Fatal("Expected 2 authorizations after role removal")
	}

	// Check permissions
	filteredPermissions, err := cloud.CheckPermissions(ctx, []*app.AuthorizedPermissions{
		{
			ResourceType: app.AuthResourceTypeOrganization,
			ResourceID:   ORG_ID,
			Permissions:  []string{"control_robot", "read_robot_logs"},
		},
	})
	if err != nil {
		logger.Fatal(err)
	}
	if len(filteredPermissions) != 1 {
		logger.Fatal("Expected 1 filtered permission")
	}
	if filteredPermissions[0].ResourceType != "organization" {
		logger.Fatal("Permission resource type mismatch")
	}
	if filteredPermissions[0].ResourceID != ORG_ID {
		logger.Fatal("Permission resource ID mismatch")
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
