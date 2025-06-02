### GetUserIDByEmail

Get the ID of a user by email.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `email` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The email of the user.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The ID of the user.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
id = await cloud.get_user_id_by_email("youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_user_id_by_email).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `email` (string) (required): The email of the user.

**Returns:**

- (string): The ID of the user.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
userID, err := client.GetUserIDByEmail(ctx, "youremail@email.com")
if err != nil {
    log.Fatalf("Failed to get user ID: %v", err)
}
fmt.Printf("User ID: %s\n", userID)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.GetUserIDByEmail).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `email` (string) (required): The email address of the user.

**Returns:**

- (Promise<string>): The user's ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
// This method is used internally only. To obtain a user's ID, use the listOrganizationsByUser method.
const members = await appClient.listOrganizationMembers(
  '<YOUR-ORGANIZATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getuseridbyemail).

{{% /tab %}}
{{< /tabs >}}

### CreateOrganization

Create an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the organization.

**Returns:**

- ([viam.proto.app.Organization](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Organization)): The created organization.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
organization = await cloud.create_organization("name")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_organization).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` (string) (required): The name of the organization.

**Returns:**

- (*app.Organization): The created organization.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
organization, err := client.CreateOrganization(ctx, "name")
if err != nil {
    log.Fatalf("Failed to create organization: %v", err)
}
fmt.Printf("Created organization: %s\n", organization.Name)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.CreateOrganization).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `name` (string) (required): The name of the new organization.

**Returns:**

- (Promise<undefined | [Organization](https://ts.viam.dev/classes/appApi.Organization.html)>): The new organization.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createorganization).

{{% /tab %}}
{{< /tabs >}}

### ListOrganizations

List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user is an authorized user of.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- ([List[viam.proto.app.Organization]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Organization)): The list of organizations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
org_list = await cloud.list_organizations()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organizations).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- ([]*app.Organization): The list of organizations.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
orgList, err := client.ListOrganizations(ctx)
if err != nil {
    log.Fatalf("Failed to list organizations: %v", err)
}
for _, org := range orgList {
    fmt.Printf("Organization: %s (ID: %s)\n", org.Name, org.Id)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.ListOrganizations).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[Organization](https://ts.viam.dev/classes/appApi.Organization.html)[]>): The organization list.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const organizations = await appClient.listOrganizations();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listorganizations).

{{% /tab %}}
{{< /tabs >}}

### GetOrganizationsWithAccessToLocation

Get all organizations that have access to a location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the location.

**Returns:**

- ([List[viam.proto.app.OrganizationIdentity]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationIdentity)): The list of organizations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
org_list = await cloud.get_organizations_with_access_to_location("location-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organizations_with_access_to_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `locationID` (string) (required): The ID of the location.

**Returns:**

- ([]*app.OrganizationIdentity): The list of organizations.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
orgList, err := client.GetOrganizationsWithAccessToLocation(ctx, "location-id")
if err != nil {
    log.Fatalf("Failed to get organizations with access to location: %v", err)
}
for _, org := range orgList {
    fmt.Printf("Organization: %s\n", org.Name)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.GetOrganizationsWithAccessToLocation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locationId` (string) (required): The ID of the location to query.

**Returns:**

- (Promise<[OrganizationIdentity](https://ts.viam.dev/classes/appApi.OrganizationIdentity.html)[]>): The list of locations with access to the requested location.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const organizations =
  await appClient.getOrganizationsWithAccessToLocation(
    '<YOUR-LOCATION-ID>'
  );
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getorganizationswithaccesstolocation).

{{% /tab %}}
{{< /tabs >}}

### ListOrganizationsByUser

List the organizations a user belongs to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `user_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the user. You can retrieve this with the get_user_id_by_email() method.

**Returns:**

- ([List[viam.proto.app.OrgDetails]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrgDetails)): The list of organizations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
org_list = await cloud.list_organizations_by_user("<YOUR-USER-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organizations_by_user).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `userID` (string) (required): The ID of the user. You can retrieve this with the GetUserIDByEmail() method.

**Returns:**

- ([]*app.OrgDetails): The list of organizations.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
orgList, err := client.ListOrganizationsByUser(ctx, "<YOUR-USER-ID>")
if err != nil {
    log.Fatalf("Failed to list organizations by user: %v", err)
}
for _, org := range orgList {
    fmt.Printf("Organization: %s\n", org.OrgName)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.ListOrganizationsByUser).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `userId` (string) (required): The ID of the user to query.

**Returns:**

- (Promise<[OrgDetails](https://ts.viam.dev/classes/appApi.OrgDetails.html)[]>): The list of locations the requested user has access to.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listorganizationsbyuser).

{{% /tab %}}
{{< /tabs >}}

### GetOrganization

Retrieve the organization object for the requested organization containing the organization's ID, name, public namespace, and more.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to query. You can retrieve this from the organization settings page.

**Returns:**

- ([viam.proto.app.Organization](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Organization)): The requested organization.

**Raises:**

- (GRPCError): If the provided org_id is invalid, or not currently authed to.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
org = await cloud.get_organization("<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization to query. You can retrieve this from the organization settings page.

**Returns:**

- (*app.Organization): The requested organization.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
org, err := client.GetOrganization(ctx, "<YOUR-ORG-ID>")
if err != nil {
    log.Fatalf("Failed to get organization: %v", err)
}
fmt.Printf("Organization: %s\n", org.Name)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.GetOrganization).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.

**Returns:**

- (Promise<undefined | [Organization](https://ts.viam.dev/classes/appApi.Organization.html)>): Details about the organization, if it exists.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const organization = await appClient.getOrganization(
  '<YOUR-ORGANIZATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getorganization).

{{% /tab %}}
{{< /tabs >}}

### GetOrganizationNamespaceAvailability

Check the availability of an {{< glossary_tooltip term_id="organization" text="organization" >}} namespace.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `public_namespace` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Organization namespace to check. Namespaces can only contain lowercase alphanumeric and dash characters.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): True if the provided namespace is available.

**Raises:**

- (GRPCError): If an invalid namespace (for example, “”) is provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
available = await cloud.get_organization_namespace_availability(
    public_namespace="my-cool-organization")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_namespace_availability).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `publicNamespace` (string) (required): Organization namespace to check. Namespaces can only contain lowercase alphanumeric and dash characters.

**Returns:**

- (bool): True if the provided namespace is available.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
available, err := client.GetOrganizationNamespaceAvailability(ctx, "my-cool-organization")
if err != nil {
    log.Fatalf("Failed to check namespace availability: %v", err)
}
fmt.Printf("Namespace available: %t\n", available)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.GetOrganizationNamespaceAvailability).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `namespace` (string) (required): The namespace to query for availability.

**Returns:**

- (Promise<boolean>): A boolean indicating whether or not the namespace is available.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const isAvailable =
  await appClient.getOrganizationNamespaceAvailability('name');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getorganizationnamespaceavailability).

{{% /tab %}}
{{< /tabs >}}

### UpdateOrganization

Updates organization details.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to update.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): If provided, updates the org’s name.
- `public_namespace` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): If provided, sets the org’s namespace if it hasn’t already been set.
- `region` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): If provided, updates the org’s region.
- `cid` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): If provided, update’s the org’s CRM ID.

**Returns:**

- ([viam.proto.app.Organization](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Organization)): The updated organization.

**Raises:**

- (GRPCError): If the org’s namespace has already been set, or if the provided namespace is already taken.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
organization = await cloud.update_organization(
    org_id="<YOUR-ORG-ID>",
    name="Artoo's Org",
    public_namespace="artoo"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization to update.
- `name` (*string) (optional): If provided, updates the org's name.
- `publicNamespace` (*string) (optional): If provided, sets the org's namespace if it hasn't already been set.
- `region` (*string) (optional): If provided, updates the org's region.
- `cid` (*string) (optional): If provided, updates the org's CRM ID.

**Returns:**

- (*app.Organization): The updated organization.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
name := "Artoo's Org"
publicNamespace := "artoo"
organization, err := client.UpdateOrganization(ctx, "<YOUR-ORG-ID>", &name, &publicNamespace, nil, nil)
if err != nil {
    log.Fatalf("Failed to update organization: %v", err)
}
fmt.Printf("Updated organization: %s\n", organization.Name)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.UpdateOrganization).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The id of the organization to update.
- `name` (string) (optional): Optional name to update the organization with.
- `publicNamespace` (string) (optional): Optional namespace to update the organization with.
- `region` (string) (optional): Optional region to update the organization with.
- `cid` (string) (optional): Optional CRM ID to update the organization with.

**Returns:**

- (Promise<undefined | [Organization](https://ts.viam.dev/classes/appApi.Organization.html)>): The updated organization details.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const organization = await appClient.updateOrganization(
  '<YOUR-ORGANIZATION-ID>',
  'newName'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updateorganization).

{{% /tab %}}
{{< /tabs >}}

### DeleteOrganization

Delete an organization.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_organization("<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization. You can obtain your organization ID from the Viam app's organization settings page.

**Returns:**

- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
err := client.DeleteOrganization(ctx, "<YOUR-ORG-ID>")
if err != nil {
    log.Fatalf("Failed to delete organization: %v", err)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.DeleteOrganization).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The id of the organization to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteOrganization('<YOUR-ORGANIZATION-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deleteorganization).

{{% /tab %}}
{{< /tabs >}}

### ListOrganizationMembers

List the members and invites of the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list members of. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- (Tuple[List[[app.OrganizationMember](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationMember)], List[[app.OrganizationInvite](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)]]): A tuple containing two lists; the first [0] of organization members, and the second [1] of organization invites.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await cloud.list_organization_members("<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization to list members of. You can obtain your organization ID from the Viam app's organization settings page.

**Returns:**

- ([]*app.OrganizationMember): The list of organization members.
- ([]*app.OrganizationInvite): The list of organization invites.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
memberList, inviteList, err := client.ListOrganizationMembers(ctx, "<YOUR-ORG-ID>")
if err != nil {
    log.Fatalf("Failed to list organization members: %v", err)
}
fmt.Printf("Found %d members and %d invites\n", len(memberList), len(inviteList))
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.ListOrganizationMembers).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The id of the organization to query.

**Returns:**

- (Promise<[ListOrganizationMembersResponse](https://ts.viam.dev/classes/appApi.ListOrganizationMembersResponse.html)>): An object containing organization members, pending invites, and
org ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const members = await appClient.listOrganizationMembers(
  '<YOUR-ORGANIZATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listorganizationmembers).

{{% /tab %}}
{{< /tabs >}}

### CreateOrganizationInvite

Create an {{< glossary_tooltip term_id="organization" text="organization" >}} invite and send it by email.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create an invite for. You can obtain your organization ID from the Viam app’s organization settings page.
- `email` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The email address to send the invite to.
- `authorizations` ([List[viam.proto.app.Authorization]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization)) (optional): Specifications of the authorizations to include in the invite. If not provided, full owner permissions will be granted.
- `send_email_invite` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Whether or not an email should be sent to the recipient of an invite. The user must accept the email to be added to the associated authorizations. When set to false, the user automatically receives the associated authorization on the next login of the user with the associated email address.

**Returns:**

- ([app.OrganizationInvite](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)): The organization invite.

**Raises:**

- (GRPCError): if an invalid email is provided, or if the user is already a member of the org.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.create_organization_invite("<YOUR-ORG-ID>", "youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_organization_invite).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization to create an invite for. You can obtain your organization ID from the Viam app's organization settings page.
- `email` (string) (required): The email address to send the invite to.
- `authorizations` ([]*app.Authorization) (optional): Specifications of the authorizations to include in the invite. If not provided, full owner permissions will be granted.
- `sendEmailInvite` (*bool) (optional): Whether or not an email should be sent to the recipient of an invite. Defaults to true.

**Returns:**

- (*app.OrganizationInvite): The organization invite.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
invite, err := client.CreateOrganizationInvite(ctx, "<YOUR-ORG-ID>", "youremail@email.com", nil, nil)
if err != nil {
    log.Fatalf("Failed to create organization invite: %v", err)
}
fmt.Printf("Created invite for: %s\n", invite.Email)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.CreateOrganizationInvite).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The id of the organization to create the invite for.
- `email` (string) (required): The email address of the user to generate an invite for.
- `authorizations` ([Authorization](https://ts.viam.dev/classes/appApi.Authorization.html)) (required): The authorizations to associate with the new invite.
- `sendEmailInvite` (boolean) (optional): Bool of whether to send an email invite (true) or
  automatically add a user. Defaults to true.

**Returns:**

- (Promise<undefined | [OrganizationInvite](https://ts.viam.dev/classes/appApi.OrganizationInvite.html)>): The organization invite.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const auth = new VIAM.appApi.Authorization({
  authorizationType: 'role',
  authorizationId: 'organization_operator',
  organizationId: '<YOUR-ORGANIZATION-ID>',
  resourceId: '<YOUR-RESOURCE-ID>', // The resource to grant access to
  resourceType: 'organization', // The type of resource to grant access to
  identityId: '<YOUR-USER-ID>', // The user id of the user to grant access to (optional)
  roleId: 'owner', // The role to grant access to
  identityType: 'user',
});

const invite = await appClient.createOrganizationInvite(
  '<YOUR-ORGANIZATION-ID>',
  'youremail@email.com',
  [auth]
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createorganizationinvite).

{{% /tab %}}
{{< /tabs >}}

### ListRobots

Get a list of all machines in a specified location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location to retrieve the machines from. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- ([List[viam.proto.app.Robot]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot)): The list of robots.

**Raises:**

- (GRPCError): If an invalid location ID is passed or one isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
list_of_machines = await cloud.list_robots(location_id="123ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_robots).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `locationID` (string) (required): ID of the location to retrieve the machines from.

**Returns:**

- ([]*app.Robot): The list of robots.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
listOfMachines, err := client.ListRobots(ctx, "123ab12345")
if err != nil {
    log.Fatalf("Failed to list robots: %v", err)
}
for _, robot := range listOfMachines {
    fmt.Printf("Robot: %s (ID: %s)\n", robot.Name, robot.Id)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.ListRobots).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to list robots for.

**Returns:**

- (Promise<[appApi](https://ts.viam.dev/modules/appApi.html).[Robot](https://ts.viam.dev/classes/appApi.Robot.html)[]>): The list of robot objects.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robots = await appClient.listRobots('<YOUR-LOCATION-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listrobots).

{{% /tab %}}
{{< /tabs >}}

### NewRobot

Create a new {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the new machine.
- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location under which to create the machine. Defaults to the current authorized location.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The new robot’s ID.

**Raises:**

- (GRPCError): If an invalid location ID is passed or one isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_machine_id = await cloud.new_robot(name="beepboop", location_id="my-location-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` (string) (required): Name of the new machine.
- `locationID` (string) (required): ID of the location under which to create the machine.

**Returns:**

- (string): The new robot's ID.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
newMachineID, err := client.NewRobot(ctx, "beepboop", "my-location-id")
if err != nil {
    log.Fatalf("Failed to create new robot: %v", err)
}
fmt.Printf("Created new robot with ID: %s\n", newMachineID)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.NewRobot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to create the robot in.
- `name` (string) (required): The name of the new robot.

**Returns:**

- (Promise<string>): The new robot's ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotId = await appClient.newRobot(
  '<YOUR-LOCATION-ID>',
  'newRobot'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#newrobot).

{{% /tab %}}
{{< /tabs >}}

### GetRobot

Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine to get. You can copy this value from the URL of the machine's page.

**Returns:**

- ([viam.proto.app.Robot](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot)): The machine.

**Raises:**

- (GRPCError): If an invalid machine ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
machine = await cloud.get_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `robotID` (string) (required): ID of the machine to get. You can copy this value from the URL of the machine's page.

**Returns:**

- (*app.Robot): The machine.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
machine, err := client.GetRobot(ctx, "1a123456-x1yz-0ab0-a12xyzabc")
if err != nil {
    log.Fatalf("Failed to get robot: %v", err)
}
fmt.Printf("Robot: %s\n", machine.Name)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.GetRobot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the robot.

**Returns:**

- (Promise<undefined | [appApi](https://ts.viam.dev/modules/appApi.html).[Robot](https://ts.viam.dev/classes/appApi.Robot.html)>): The `Robot` object.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robot = await appClient.getRobot('<YOUR-ROBOT-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobot).

{{% /tab %}}
{{< /tabs >}}

### CreateLocation

Create and name a {{< glossary_tooltip term_id="location" text="location" >}} under the organization you are currently authenticated to.
Optionally, put the new location under a specified parent location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the location under. You can obtain your organization ID from the Viam app's organization settings page.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the location.
- `parent_location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional parent location to put the location under. Defaults to a root-level location if no location ID is provided.

**Returns:**

- ([viam.proto.app.Location](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)): The newly created location.

**Raises:**

- (GRPCError): If either an invalid name (for example, ""), or parent location ID (for example, a nonexistent ID) is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_new_location = await cloud.create_location(org_id="<YOUR-ORG-ID>", name="Robotville", parent_location_id="111ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization to create the location under. You can obtain your organization ID from the Viam app's organization settings page.
- `name` (string) (required): Name of the location.
- `parentLocationID` (*string) (optional): Optional parent location to put the location under. Defaults to a root-level location if no location ID is provided.

**Returns:**

- (*app.Location): The newly created location.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
parentLocationID := "111ab12345"
myNewLocation, err := client.CreateLocation(ctx, "<YOUR-ORG-ID>", "Robotville", &parentLocationID)
if err != nil {
    log.Fatalf("Failed to create location: %v", err)
}
fmt.Printf("Created location: %s\n", myNewLocation.Name)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.CreateLocation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to create the location
  under.
- `name` (string) (required): The name of the location to create.
- `parentLocationId` (string) (optional): Optional name of a parent location to create the
  new location under.

**Returns:**

- (Promise<undefined | [Location](https://ts.viam.dev/classes/appApi.Location.html)>): The location object.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const location = await appClient.createLocation(
  '<YOUR-ORGANIZATION-ID>',
  'name'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createlocation).

{{% /tab %}}
{{< /tabs >}}

### ListLocations

Get a list of all {{< glossary_tooltip term_id="location" text="locations" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the org to list locations for. You can obtain your organization ID from the Viam app's organization settings page.

**Returns:**

- ([List[viam.proto.app.Location]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)): The list of locations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
locations = await cloud.list_locations("<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_locations).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the org to list locations for. You can obtain your organization ID from the Viam app's organization settings page.

**Returns:**

- ([]*app.Location): The list of locations.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
locations, err := client.ListLocations(ctx, "<YOUR-ORG-ID>")
if err != nil {
    log.Fatalf("Failed to list locations: %v", err)
}
for _, location := range locations {
    fmt.Printf("Location: %s (ID: %s)\n", location.Name, location.Id)
});
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.ListLocations).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to query.

**Returns:**

- (Promise<[Location](https://ts.viam.dev/classes/appApi.Location.html)[]>): A list of locations under the organization.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const locations = await appClient.listLocations(
  '<YOUR-ORGANIZATION-ID>'
```


For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listlocations).

{{% /tab %}}
{{< /tabs >}}

### CreateKey

Create a new [API key](/operate/control/api-keys/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the key for. You can obtain your organization ID from the Viam app’s organization settings page.
- `authorizations` ([List[APIKeyAuthorization]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization)) (required): A list of authorizations to associate with the key.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): A name for the key. If None, defaults to the current timestamp.

**Returns:**

- (Tuple[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The api key and api key ID.

**Raises:**

- (GRPCError): If the authorizations list is empty.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.app.app_client import APIKeyAuthorization

auth = APIKeyAuthorization(
    role="owner",
    resource_type="robot",
    resource_id="your-machine-id123"
)

api_key, api_key_id = cloud.create_key(
    org_id="<YOUR-ORG-ID>",
    authorizations=[auth],
    name="my_key"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization to create the key for. You can obtain your organization ID from the Viam app's organization settings page.
- `authorizations` ([]*app.Authorization) (required): A list of authorizations to associate with the key.
- `name` (string) (optional): A name for the key. If empty, defaults to the current timestamp.

**Returns:**

- (string): The API key.
- (string): The API key ID.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
auth := &app.Authorization{
    AuthorizationType: "role",
    AuthorizationId:   "owner",
    ResourceType:      "robot",
    ResourceId:        "your-machine-id123",
}

apiKey, apiKeyID, err := client.CreateKey(ctx, "<YOUR-ORG-ID>", []*app.Authorization{auth}, "my_key")
if err != nil {
    log.Fatalf("Failed to create key: %v", err)
}
fmt.Printf("Created API key: %s (ID: %s)\n", apiKey, apiKeyID)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.CreateKey).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `authorizations` ([Authorization](https://ts.viam.dev/classes/appApi.Authorization.html)) (required): The list of authorizations to provide for the API key.
- `name` (string) (optional): An optional name for the key. If none is passed, defaults to
  present timestamp.

**Returns:**

- (Promise<[CreateKeyResponse](https://ts.viam.dev/classes/appApi.CreateKeyResponse.html)>): The new key and ID.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createkey).

{{% /tab %}}
{{< /tabs >}}

### ListKeys

List all keys for the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list API keys for. You can obtain your organization ID from the Viam app's organization settings page.

**Returns:**

- ([List[viam.proto.app.APIKeyWithAuthorizations]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.APIKeyWithAuthorizations)): The existing API keys and authorizations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
keys = await cloud.list_keys(org_id="<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_keys).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `orgID` (string) (required): The ID of the organization to list API keys for. You can obtain your organization ID from the Viam app's organization settings page.

**Returns:**

- ([]*app.APIKeyWithAuthorizations): The existing API keys and authorizations.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
keys, err := client.ListKeys(ctx, "<YOUR-ORG-ID>")
if err != nil {
    log.Fatalf("Failed to list keys: %v", err)
}
for _, key := range keys {
    fmt.Printf("API Key: %s\n", key.ApiKey.Name)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.ListKeys).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `orgId` (string) (required): The ID of the organization to query.

**Returns:**

- (Promise<[APIKeyWithAuthorizations](https://ts.viam.dev/classes/appApi.APIKeyWithAuthorizations.html)[]>): The list of API keys.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const keys = await appClient.listKeys('<YOUR-ORGANIZATION-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listkeys).

{{% /tab %}}
{{< /tabs >}}

### DeleteKey

Delete an [API key](/operate/control/api-keys/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the API key.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_key("key-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_key).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `id` (string) (required): The ID of the API key.

**Returns:**

- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
err := client.DeleteKey(ctx, "key-id")
if err != nil {
    log.Fatalf("Failed to delete key: %v", err)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.DeleteKey).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the key to delete.

**Returns:**

- (Promise<[DeleteKeyResponse](https://ts.viam.dev/classes/appApi.DeleteKeyResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteKey('<YOUR-KEY-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deletekey).

{{% /tab %}}
{{< /tabs >}}

### RotateKey

Rotate an [API key](/operate/control/api-keys/#rotate-an-api-key).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the key to be rotated.

**Returns:**

- (Tuple[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The API key and API key id.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
id, key = await cloud.rotate_key("key-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.rotate_key).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `id` (string) (required): The ID of the key to be rotated.

**Returns:**

- (string): The API key ID.
- (string): The API key.
- (error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
keyID, key, err := client.RotateKey(ctx, "key-id")
if err != nil {
    log.Fatalf("Failed to rotate key: %v", err)
}
fmt.Printf("Rotated key: %s (ID: %s)\n", key, keyID)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.77.0/app#AppClient.RotateKey).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the key to rotate.

**Returns:**

- (Promise<[RotateKeyResponse](https://ts.viam.dev/classes/appApi.RotateKeyResponse.html)>): The updated key and ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const key = await appClient.rotateKey('<YOUR-KEY-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#rotatekey).

{{% /tab %}}
{{< /tabs >}}
