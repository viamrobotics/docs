---
title: "Viam API keys"
linkTitle: "API keys"
weight: 50
layout: "docs"
type: "docs"
description: "Run control logic on a machine."
images: ["/general/code.png"]
date: "2025-01-15"
---

API keys grant access to organizations, locations, and machines.

To view all API keys in use for your organization and the locations and machines inside it, click on the organization dropdown in the top navigation bar and click on **Settings**.

{{<imgproc src="/fleet/api-keys.png" resize="700x" declaredimensions=true alt="API Keys table" class="shadow" >}}

## Add an API key

On your organization's page, click **Generate key** to generate a new key.
Optionally, give the key a name.
Click on the **Resource** menu and choose what organization, location, or machine you want the key to grant access to.
If you select organization, your key grants access to all locations and machines contained within that organization.
If you select location, your key grants access to all of the machines contained within that location.

For **Role**, assign either an **Owner** or **Operator** role.
See [Permissions](/manage/manage/rbac/) for information about the privilege each role entails at each resource level.

## Change an API key's access

To edit an API key, click on **Show details** in the key's row of the key table's **Resources** column.

{{<imgproc src="/fleet/additional-details.png" resize="700x" declaredimensions=true alt="Additional details for a key" class="shadow" >}}

To edit the role, click on the dropdown menu next to the role and select **Owner** or **Operator**.
See [Permissions](/manage/manage/rbac/) for information about the privilege each role entails at each resource level.

To change the entities it is able to access, click **+ Grant additional access**.
Select which organization, location, or machine you want the key to grant access to.
Click **Choose** to confirm your selection.

## Rotate an API key

If you ever need to rotate an API key, click on the **Generate Key** button on the organization setting page to generate a new key.

Viam supports flexible key rotation with up to two keys in use at one time. After generating a new secret key, update all references to the key in your code as soon as possible and then remove the old key.
