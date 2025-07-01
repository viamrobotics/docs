---
title: "Choose data region"
linkTitle: "Choose data region"
description: "Configure where in the world Viam stores your cloud data."
weight: 30
type: "docs"
tags: ["data region", "region", "data continent", "compliance", "performance"]
---

When you specify a data region, Viam stores all of your data, including tabular data, binary data, and even the [hot data store](/data-ai/capture-data/advanced/advanced-data-capture-sync/#capture-to-the-hot-data-store), in that region.
By default, new organizations store data in North America.
Locations shared across multiple organizations store data in the primary organization region.

## Supported regions

Viam supports the following data regions:

- **North America** (`us-central`):

  - GCS: `us-central1`
  - Azure: `eastus2`
  - MongoDB Atlas: `US_EAST_2`

- **Europe** (`eu-west`):
  - GCS: `europe-west4`
  - Azure: `westeurope`
  - MongoDB Atlas: `EUROPE_WEST`

## Set organization data region

{{< alert title="Caution: You cannot change region if you have already synced data" color="caution" >}}

You must set the region before syncing data.
Once you sync data in an organization, you cannot change the data region.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Open the organization dropdown in the top right of Viam, next to your initials.
1. Click **Settings and invites** to open the organization settings menu.
1. From the **Data region** dropdown, choose the geographic location where you would like to store data.
1. A dialog will appear at the bottom of the screen containing the text **Region updated**.

{{% /tab %}}
{{% tab name="Python" %}}

You can check your organization's data region using [`get_organization`](/dev/reference/apis/fleet/#getorganization), and set your organization's data region using [`update_organization`](/dev/reference/apis/fleet/#updateorganization):

```python
viam_client = ViamClient.create_from_dial_options(
    dial_options=DialOptions.with_api_key(
        api_key="your-api-key",
        api_key_id="your-api-key-id"
    )
)

# Check organization region
org = await viam_client.app_client.get_organization(org_id="your-org-id")
print(f"Current region: {org.default_region}")

# Update organization region
updated_org = await viam_client.app_client.update_organization(
    org_id="your-org-id",
    region="eu-west"  # or "us-central"
)

print(f"Organization region updated to: {updated_org.region}")

viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

You can check your organization's data region using [`GetOrganization`](/dev/reference/apis/fleet/#getorganization), and set your organization's data region using [`UpdateOrganization`](/dev/reference/apis/fleet/#updateorganization):

```go
ctx := context.Background()

appClient, err := app.NewAppClient(ctx, app.Config{
    Auth: app.Credentials{
        Type:    "api-key",
        Payload: "your-api-key",
    },
}, logging.NewLogger("client"))
if err != nil {
    log.Fatal(err)
}
defer appClient.Close()

organizationId := "your-org-id"

// Check organization region
org, err := appClient.GetOrganization(ctx, organizationId)
if err != nil {
    log.Fatal(err)
}
fmt.Printf("Current region: %s\n", org.DefaultRegion)

// Configure UpdateOrganizationOptions for European region
updateOptions := &app.UpdateOrganizationOptions{
    Name:   nil,
    Region: stringPtr("eu-west"),  # or "us-central"
}

// Update organization region
updatedOrg, err := appClient.UpdateOrganization(ctx, organizationId, updateOptions)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Organization region updated to: %s\n", updatedOrg.DefaultRegion)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

You can check your organization's data region using [`getOrganization`](/dev/reference/apis/fleet/#getorganization), and set your organization's data region using [`UpdateOrganization`](/dev/reference/apis/fleet/#updateorganization):

```typescript
const client = await createViamClient({
  credential: {
    type: "api-key",
    authEntity: "your-api-key-id",
    payload: "your-api-key",
  },
});

// Check organization region
const org = await client.appClient.getOrganization({
  organizationId: "your-org-id",
});
console.log(`Current region: ${org.defaultRegion}`);

// Update organization region
const updatedOrg = await client.appClient.updateOrganization({
  organizationId: "your-org-id",
  region: "eu-west", // or "us-central"
});

console.log(`Organization region updated to: ${updatedOrg.region}`);

client.disconnect();
```

{{% /tab %}}
{{< /tabs >}}
