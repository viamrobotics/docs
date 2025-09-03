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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `email` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetUserIDByEmail).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `name` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*Organization)](https://pkg.go.dev/go.viam.com/rdk/app#Organization)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateOrganization).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [([]*Organization)](https://pkg.go.dev/go.viam.com/rdk/app#Organization)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListOrganizations).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `userID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*OrgDetails)](https://pkg.go.dev/go.viam.com/rdk/app#OrgDetails)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListOrganizationsByUser).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*Organization)](https://pkg.go.dev/go.viam.com/rdk/app#Organization)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetOrganization).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `namespace` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetOrganizationNamespaceAvailability).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)
- `opts` [(*UpdateOrganizationOptions)](https://pkg.go.dev/go.viam.com/rdk/app#UpdateOrganizationOptions)

**Returns:**

- [(*Organization)](https://pkg.go.dev/go.viam.com/rdk/app#Organization)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateOrganization).

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

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization. You can obtain your organization ID from the organization settings page.

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteOrganization).

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

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list members of. You can obtain your organization ID from the organization settings page.

**Returns:**

- (Tuple[List[[app.OrganizationMember](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationMember)], List[[app.OrganizationInvite](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)]]): A tuple containing two lists; the first
\[0] of organization members, and the second \[1] of organization invites.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await cloud.list_organization_members("<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*OrganizationMember)](https://pkg.go.dev/go.viam.com/rdk/app#OrganizationMember)
- [([]*OrganizationInvite)](https://pkg.go.dev/go.viam.com/rdk/app#OrganizationInvite)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListOrganizationMembers).

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

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create an invite for. You can obtain your organization ID from the organization settings page.
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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `email` [(string)](https://pkg.go.dev/builtin#string)
- `authorizations` [([]*Authorization)](https://pkg.go.dev/go.viam.com/rdk/app#Authorization)
- `opts` [(*CreateOrganizationInviteOptions)](https://pkg.go.dev/go.viam.com/rdk/app#CreateOrganizationInviteOptions)

**Returns:**

- [(*OrganizationInvite)](https://pkg.go.dev/go.viam.com/rdk/app#OrganizationInvite)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateOrganizationInvite).

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

### UpdateOrganizationInviteAuthorizations

Update (add or remove) the authorizations attached to an organization invite that has already been created.
If an invitation has only one authorization and you want to remove it, delete the invitation instead of using this method.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that the invite is for. You can obtain your organization ID from the organization settings page.
- `email` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Email of the user the invite was sent to.
- `add_authorizations` ([List[viam.proto.app.Authorization]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization)) (optional): Optional list of authorizations to add to the invite.
- `remove_authorizations` ([List[viam.proto.app.Authorization]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization)) (optional): Optional list of authorizations to remove from the invite.

**Returns:**

- ([app.OrganizationInvite](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)): The updated invite.

**Raises:**

- (GRPCError): If no authorizations are passed or if an invalid combination of authorizations is passed (for example an authorization to remove when the invite only contains one authorization).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app import Authorization

auth = Authorization(
    authorization_type="role",
    authorization_id="location_owner",
    resource_type="location", # "robot", "location", or "organization"
    resource_id="012456lni0", # machine id, location id or org id
    identity_id="",
    organization_id="<YOUR-ORG-ID>",
    identity_type=""
)

update_invite = await cloud.update_organization_invite_authorizations(
    org_id="<YOUR-ORG-ID>",
    email="notarealemail@viam.com",
    add_authorizations=[auth]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization_invite_authorizations).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `email` [(string)](https://pkg.go.dev/builtin#string)
- `addAuthorizations`
- `removeAuthorizations` [([]*Authorization)](https://pkg.go.dev/go.viam.com/rdk/app#Authorization)

**Returns:**

- [(*OrganizationInvite)](https://pkg.go.dev/go.viam.com/rdk/app#OrganizationInvite)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateOrganizationInviteAuthorizations).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The id of the organization.
- `email` (string) (required): The email address associated with the invite.
- `addAuthsList` ([Authorization](https://ts.viam.dev/classes/appApi.Authorization.html)) (required): List of authorizations to add to the invite.
- `removeAuthsList` ([Authorization](https://ts.viam.dev/classes/appApi.Authorization.html)) (required): List of authorizations to remove from the invite.

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
const invite = await appClient.updateOrganizationInviteAuthorizations(
  '<YOUR-ORGANIZATION-ID>',
  'youremail@email.com',
  [auth],
  []
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updateorganizationinviteauthorizations).

{{% /tab %}}
{{< /tabs >}}

### DeleteOrganizationMember

Remove a member from the {{< glossary_tooltip term_id="organization" text="organization" >}} you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the org to remove the user from. You can obtain your organization ID from the organization settings page.
- `user_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the user to remove.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await cloud.list_organization_members(org_id="<YOUR-ORG-ID>")
first_user_id = member_list[0].user_id

await cloud.delete_organization_member(org_id="org_id", user_id=first_user_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_member).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `userID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteOrganizationMember).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.
- `userId` (string) (required): The ID of the user.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteOrganizationMember(
  '<YOUR-ORGANIZATION-ID>',
  '<YOUR-USER-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deleteorganizationmember).

{{% /tab %}}
{{< /tabs >}}

### DeleteOrganizationInvite

Delete a pending organization invite to the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that the invite to delete was for. You can obtain your organization ID from the organization settings page.
- `email` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The email address the pending invite was sent to.

**Returns:**

- None.

**Raises:**

- (GRPCError): If no pending invite is associated with the provided email address.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_organization_invite("<YOUR-ORG-ID>", "youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_invite).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `email` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteOrganizationInvite).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.
- `email` (string) (required): The email associated with the invite to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteOrganizationInvite(
  '<YOUR-ORGANIZATION-ID>',
  'youremail@email.com'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deleteorganizationinvite).

{{% /tab %}}
{{< /tabs >}}

### ResendOrganizationInvite

Resend a pending organization invite email.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that the invite to resend was for. You can obtain your organization ID from the organization settings page.
- `email` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The email address associated with the invite.

**Returns:**

- ([app.OrganizationInvite](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)): The organization invite sent.

**Raises:**

- (GRPCError): If no pending invite is associated with the provided email address.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
org_invite = await cloud.resend_organization_invite("<YOUR-ORG-ID>", "youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.resend_organization_invite).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `email` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*OrganizationInvite)](https://pkg.go.dev/go.viam.com/rdk/app#OrganizationInvite)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ResendOrganizationInvite).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.
- `email` (string) (required): The email associated with the invite to resend.

**Returns:**

- (Promise<undefined | [OrganizationInvite](https://ts.viam.dev/classes/appApi.OrganizationInvite.html)>): The invite.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const invite = await appClient.resendOrganizationInvite(
  '<YOUR-ORGANIZATION-ID>',
  'youremail@email.com'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#resendorganizationinvite).

{{% /tab %}}
{{< /tabs >}}

### GetOrganizationMetadata

Gets the user-defined metadata for an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization with which the user-defined metadata is associated. You can obtain your organization ID from the organization settings page.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]): The user\-defined metadata converted from JSON to a Python dictionary.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
metadata = await cloud.get_organization_metadata(org_id="<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetOrganizationMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the organization.

**Returns:**

- (Promise<Record<string, [JsonValue](https://ts.viam.dev/types/JsonValue.html)>>): The metadata associated with the organization.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const metadata = await appClient.getOrganizationMetadata(
  '<YOUR-ORGANIZATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getorganizationmetadata).

{{% /tab %}}
{{< /tabs >}}

### UpdateOrganizationMetadata

Updates the user-defined metadata for an organization.
User-defined metadata is billed as data.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required)
- `metadata` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (required): The user-defined metadata to upload as a Python dictionary.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.update_organization_metadata(org_id="<YOUR-ORG-ID>", metadata=)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `organizationID` [(string)](https://pkg.go.dev/builtin#string)
- `data` (interface{})

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateOrganizationMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the organization.
- `data` (Record) (required): The metadata to update.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.updateOrganizationMetadata('<YOUR-ORGANIZATION-ID>', {
  key: 'value',
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updateorganizationmetadata).

{{% /tab %}}
{{< /tabs >}}

### CreateLocation

Create and name a {{< glossary_tooltip term_id="location" text="location" >}} under the organization you are currently authenticated to.
Optionally, put the new location under a specified parent location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the location under. You can obtain your organization ID from the organization settings page.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the location.
- `parent_location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional parent location to put the location under. Defaults to a root-level location if no location ID is provided.

**Returns:**

- ([viam.proto.app.Location](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)): The newly created location.

**Raises:**

- (GRPCError): If either an invalid name (for example, “”), or parent location ID (for example, a nonexistent ID) is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_new_location = await cloud.create_location(org_id="<YOUR-ORG-ID>", name="Robotville", parent_location_id="111ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `name` [(string)](https://pkg.go.dev/builtin#string)
- `opts` [(*CreateLocationOptions)](https://pkg.go.dev/go.viam.com/rdk/app#CreateLocationOptions)

**Returns:**

- [(*Location)](https://pkg.go.dev/go.viam.com/rdk/app#Location)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateLocation).

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

### GetLocation

Get a {{< glossary_tooltip term_id="location" text="location" >}} by its location ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location to get. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- ([viam.proto.app.Location](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)): The location.

**Raises:**

- (GRPCError): If an invalid location ID is passed or if one isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
location = await cloud.get_location(location_id="123ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*Location)](https://pkg.go.dev/go.viam.com/rdk/app#Location)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetLocation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to query.

**Returns:**

- (Promise<undefined | [Location](https://ts.viam.dev/classes/appApi.Location.html)>): The location object.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const location = await appClient.getLocation('<YOUR-LOCATION-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getlocation).

{{% /tab %}}
{{< /tabs >}}

### UpdateLocation

Change the name of a {{< glossary_tooltip term_id="location" text="location" >}} and/or assign a parent location to a location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the location to update. Must be specified.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional new name to be updated on the location. Defaults to the empty string “” (that is, the name doesn’t change).
- `parent_location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional ID of new parent location to move the location under. Defaults to the empty string “” (that is, no new parent location is assigned).

**Returns:**

- ([viam.proto.app.Location](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)): The newly updated location.

**Raises:**

- (GRPCError): If either an invalid location ID, name, or parent location ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# The following line takes the location with ID "abc12abcde" and moves it to be a
# sub-location of the location with ID "xyz34xxxxx"
my_updated_location = await cloud.update_location(
    location_id="abc12abcde",
    name="",
    parent_location_id="xyz34xxxxx",
)

# The following line changes the name of the location without changing its parent location
my_updated_location = await cloud.update_location(
    location_id="abc12abcde",
    name="Land Before Robots"
)

# The following line moves the location back up to be a top level location without changing its name
my_updated_location = await cloud.update_location(
    location_id="abc12abcde",
    name="",
    parent_location_id=""
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)
- `opts` [(*UpdateLocationOptions)](https://pkg.go.dev/go.viam.com/rdk/app#UpdateLocationOptions)

**Returns:**

- [(*Location)](https://pkg.go.dev/go.viam.com/rdk/app#Location)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateLocation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to update.
- `name` (string) (optional): Optional string to update the location's name to.
- `parentLocId` (string) (optional): Optional string to update the location's parent location
  to.
- `region` (string) (optional): Optional string to update the location's region to.

**Returns:**

- (Promise<undefined | [Location](https://ts.viam.dev/classes/appApi.Location.html)>): The location object.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const location = await appClient.updateLocation(
  '<YOUR-LOCATION-ID>',
  'newName'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updatelocation).

{{% /tab %}}
{{< /tabs >}}

### DeleteLocation

Delete a {{< glossary_tooltip term_id="location" text="location" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the location to delete. Must be specified.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid location ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_location(location_id="abc12abcde")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteLocation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteLocation('<YOUR-LOCATION-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deletelocation).

{{% /tab %}}
{{< /tabs >}}

### ListLocations

Get a list of all {{< glossary_tooltip term_id="location" text="locations" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the org to list locations for. You can obtain your organization ID from the organization settings page.

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*Location)](https://pkg.go.dev/go.viam.com/rdk/app#Location)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListLocations).

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
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listlocations).

{{% /tab %}}
{{< /tabs >}}

### ShareLocation

Share a location with an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization.
- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the location.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.share_location("<YOUR-ORG-ID>", "<YOUR-LOCATION-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.share_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID`
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ShareLocation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to share with.
- `locId` (string) (required): The ID of the location to share.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.shareLocation(
  '<OTHER-ORGANIZATION-ID>',
  '<YOUR-LOCATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#sharelocation).

{{% /tab %}}
{{< /tabs >}}

### UnshareLocation

Stop sharing a location with an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization.
- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the location.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.unshare_location("<YOUR-ORG-ID>", "<YOUR-LOCATION-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.unshare_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID`
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UnshareLocation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to unshare with.
- `locId` (string) (required): The ID of the location to unshare.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.unshareLocation(
  '<OTHER-ORGANIZATION-ID>',
  '<YOUR-LOCATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#unsharelocation).

{{% /tab %}}
{{< /tabs >}}

### LocationAuth

Get a location’s `LocationAuth` (location secret or secrets).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location to retrieve LocationAuth from. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- ([viam.proto.app.LocationAuth](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.LocationAuth)): The LocationAuth containing location secrets.

**Raises:**

- (GRPCError): If an invalid location ID is passed or if one isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
loc_auth = await cloud.location_auth(location_id="123xy12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.location_auth).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*LocationAuth)](https://pkg.go.dev/go.viam.com/rdk/app#LocationAuth)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.LocationAuth).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to retrieve `LocationAuth` from.

**Returns:**

- (Promise<undefined | [LocationAuth](https://ts.viam.dev/classes/appApi.LocationAuth.html)>): The `LocationAuth` for the requested location.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const locationAuth = await appClient.locationAuth(
  '<YOUR-LOCATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#locationauth).

{{% /tab %}}
{{< /tabs >}}

### CreateLocationSecret

Create a new location secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location to generate a new secret for. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- ([viam.proto.app.LocationAuth](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.LocationAuth)): The specified location’s LocationAuth containing the newly created secret.

**Raises:**

- (GRPCError): If an invalid location ID is passed or one isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_loc_auth = await cloud.create_location_secret(location_id="123xy12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location_secret).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*LocationAuth)](https://pkg.go.dev/go.viam.com/rdk/app#LocationAuth)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateLocationSecret).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to create a `LocationAuth` for.

**Returns:**

- (Promise<undefined | [LocationAuth](https://ts.viam.dev/classes/appApi.LocationAuth.html)>): The newly created `LocationAuth`.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const locationAuth = await appClient.createLocationSecret(
  '<YOUR-LOCATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createlocationsecret).

{{% /tab %}}
{{< /tabs >}}

### DeleteLocationSecret

Delete a location secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `secret_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the secret to delete.
- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location to delete secret from. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- None.

**Raises:**

- (GRPCError): If either an invalid location ID or secret ID is passed or a location ID isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_location_secret(
    secret_id="abcd123-456-7890ab-cxyz98-989898xyzxyz",
    location_id="123xy12345"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location_secret).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID`
- `secretID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteLocationSecret).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `locId` (string) (required): The ID of the location to delete the `LocationAuth` from.
- `secretId` (string) (required): The ID of the location secret to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteLocationSecret(
  '<YOUR-LOCATION-ID>',
  '<YOUR-SECRET-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deletelocationsecret).

{{% /tab %}}
{{< /tabs >}}

### GetLocationMetadata

Get the user-defined metadata for a location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the location with which the user-defined metadata is associated. You can obtain your location ID from the location’s page.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]): The user\-defined metadata converted from JSON to a Python dictionary.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
metadata = await cloud.get_location_metadata(location_id="<YOUR-LOCATION-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_location_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetLocationMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the location.

**Returns:**

- (Promise<Record<string, [JsonValue](https://ts.viam.dev/types/JsonValue.html)>>): The metadata associated with the location.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const metadata = await appClient.getLocationMetadata(
  '<YOUR-LOCATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getlocationmetadata).

{{% /tab %}}
{{< /tabs >}}

### UpdateLocationMetadata

Update the user-defined metadata for a location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the location with which to associate the user-defined metadata. You can obtain your location ID from the location’s page.
- `metadata` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (required): The user-defined metadata converted from JSON to a Python dictionary.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.update_location_metadata(location_id="<YOUR-LOCATION-ID>", metadata=)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_location_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)
- `data` (interface{})

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateLocationMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the location.
- `data` (Record) (required): The metadata to update.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.updateLocationMetadata('<YOUR-LOCATION-ID>', {
  key: 'value',
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updatelocationmetadata).

{{% /tab %}}
{{< /tabs >}}

### GetRobot

Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine to get. You can copy this value from the URL of the machine’s page.

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*Robot)](https://pkg.go.dev/go.viam.com/rdk/app#Robot)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobot).

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

### GetRobotAPIKeys

Gets the [API keys](/operate/control/api-keys/) for the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the machine.

**Returns:**

- ([List[viam.proto.app.APIKeyWithAuthorizations]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.APIKeyWithAuthorizations)): The list of API keys.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
api_keys = await cloud.get_robot_api_keys(robot_id="robot-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_api_keys).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `robotID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*APIKeyWithAuthorizations)](https://pkg.go.dev/go.viam.com/rdk/app#APIKeyWithAuthorizations)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobotAPIKeys).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `robotId` (string) (required): The ID of the robot to get API keys for.

**Returns:**

- (Promise<[APIKeyWithAuthorizations](https://ts.viam.dev/classes/appApi.APIKeyWithAuthorizations.html)[]>): A list of the robot's API keys.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotAPIKeys =
  await appClient.getRobotAPIKeys('<YOUR-ROBOT-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotapikeys).

{{% /tab %}}
{{< /tabs >}}

### GetRobotParts

Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine to get parts from.

**Returns:**

- ([List[RobotPart]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The list of machine parts.

**Raises:**

- (GRPCError): If an invalid machine ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
list_of_parts = await cloud.get_robot_parts(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_parts).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `robotID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*RobotPart)](https://pkg.go.dev/go.viam.com/rdk/app#RobotPart)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobotParts).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `robotId` (string) (required): The ID of the robot to query.

**Returns:**

- (Promise<[RobotPart](https://ts.viam.dev/classes/appApi.RobotPart.html)[]>): The list of `RobotPart` objects associated with the robot.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotParts = await appClient.getRobotParts('<YOUR-ROBOT-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotparts).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPart

Get a specific machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to get. You can retrieve this value by navigating to the machine’s page, clicking on the part status dropdown, and clicking the copy icon next to Part ID.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath to write the machine part’s config file in JSON format to.
- `indent` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Size (in number of spaces) of indent when writing config to dest. Defaults to 4.

**Returns:**

- ([RobotPart](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The machine part.

**Raises:**

- (GRPCError): If an invalid machine part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_robot_part = await cloud.get_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22"
)
# Get the part's address
address = my_robot_part.fqdn
# Check if machine is live (last access time less than 10 sec ago)
if (time.time() - my_robot_part.last_access.timestamp()) <= 10000:
    print("Machine is live.")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*RobotPart)](https://pkg.go.dev/go.viam.com/rdk/app#RobotPart)
- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobotPart).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the requested robot part.

**Returns:**

- (Promise<[GetRobotPartResponse](https://ts.viam.dev/classes/appApi.GetRobotPartResponse.html)>): The robot part and a its json config.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPart = await appClient.getRobotPart('<YOUR-ROBOT-PART-ID>');
// Get the part's address
const address = robotPart.part.fqdn;
// Check if machine is live (last access time less than 10 sec ago)
if (
  Date.now() - Number(robotPart.part.lastAccess.seconds) * 1000 <=
  10000
) {
  console.log('Machine is live');
}
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotpart).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPartLogs

Get the logs associated with a specific machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to get logs from.
- `filter` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Only include logs with messages that contain the string filter. Defaults to empty string “” (that is, no filter).
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath to write the log entries to.
- `log_levels` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): List of log levels for which entries should be returned. Defaults to empty list, which returns all logs.
- `num_log_entries` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first num_log_entries logs will be returned, whichever comes first.

**Returns:**

- ([List[LogEntry]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.LogEntry)): The list of log entries.

**Raises:**

- (GRPCError): If an invalid robot part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
part_logs = await cloud.get_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22",
    num_log_entries=20
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_logs).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)
- `opts` [(*GetRobotPartLogsOptions)](https://pkg.go.dev/go.viam.com/rdk/app#GetRobotPartLogsOptions)

**Returns:**

- [([]*LogEntry)](https://pkg.go.dev/go.viam.com/rdk/app#LogEntry)
- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobotPartLogs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the requested robot part.
- `filter` (string) (optional): Optional string to filter logs on.
- `levels` (string) (optional): Optional array of log levels to return. Defaults to returning
  all log levels.
- `pageToken` (string) (optional): Optional string indicating which page of logs to query.
  Defaults to the most recent.

**Returns:**

- (Promise<[GetRobotPartLogsResponse](https://ts.viam.dev/classes/appApi.GetRobotPartLogsResponse.html)>): The robot requested logs and the page token for the next page of
logs.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPartLogs = await appClient.getRobotPartLogs(
  '<YOUR-ROBOT-PART-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotpartlogs).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPartByNameAndLocation

Query a specific robot part by name and location id.

{{< tabs >}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `name` (string) (required): The name of the requested robot part.
- `locationId` (string) (required): The ID of the location of the requested robot part.

**Returns:**

- (Promise<[GetRobotPartByNameAndLocationResponse](https://ts.viam.dev/classes/appApi.GetRobotPartByNameAndLocationResponse.html)>): The robot part.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPart = await appClient.getRobotPartByNameAndLocation(
  '<YOUR-ROBOT-PART-NAME>',
  '<YOUR-LOCATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotpartbynameandlocation).

{{% /tab %}}
{{< /tabs >}}

### TailRobotPartLogs

Get an asynchronous iterator that receives live machine part logs.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to retrieve logs from.
- `errors_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Boolean specifying whether or not to only include error logs. Defaults to True.
- `filter` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Only include logs with messages that contain the string filter. Defaults to empty string “” (that is, no filter).

**Returns:**

- ([viam.app._logs._LogsStream[List[LogEntry]]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.LogEntry)): The asynchronous iterator receiving live machine part logs.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
logs_stream = await cloud.tail_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.tail_robot_part_logs).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)
- `errorsOnly` [(bool)](https://pkg.go.dev/builtin#bool)
- `opts` [(*TailRobotPartLogsOptions)](https://pkg.go.dev/go.viam.com/rdk/app#TailRobotPartLogsOptions)

**Returns:**

- [(*RobotPartLogStream)](https://pkg.go.dev/go.viam.com/rdk/app#RobotPartLogStream)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.TailRobotPartLogs).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the requested robot part.
- `queue` ([LogEntry](https://ts.viam.dev/classes/commonApi.LogEntry.html)) (required): A queue to put the log entries into.
- `filter` (string) (optional): Optional string to filter logs on.
- `errorsOnly` (boolean) (optional): Optional bool to indicate whether or not only error\-level
  logs should be returned. Defaults to true.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPartLogs = await appClient.tailRobotPartLogs(
  '<YOUR-ROBOT-PART-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#tailrobotpartlogs).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPartHistory

Get a list containing the history of a machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to retrieve history from.

**Returns:**

- ([List[RobotPartHistoryEntry]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPartHistoryEntry)): The list of the machine part’s history.

**Raises:**

- (GRPCError): If an invalid machine part ID is provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
part_history = await cloud.get_robot_part_history(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_history).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*RobotPartHistoryEntry)](https://pkg.go.dev/go.viam.com/rdk/app#RobotPartHistoryEntry)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobotPartHistory).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the requested robot part.

**Returns:**

- (Promise<[RobotPartHistoryEntry](https://ts.viam.dev/classes/appApi.RobotPartHistoryEntry.html)[]>): The list of the robot part's history.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPartHistory = await appClient.getRobotPartHistory(
  '<YOUR-ROBOT-PART-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotparthistory).

{{% /tab %}}
{{< /tabs >}}

### UpdateRobotPart

Change the name of and assign an optional new configuration to a machine {{< glossary_tooltip term_id="part" text="part" >}}.
You can only change the name and configuration of the machine part, not the location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to update.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New name to be updated on the robot part.
- `robot_config` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional new config represented as a dictionary to be updated on the machine part. The machine part’s config will remain as is (no change) if one isn’t passed.
- `last_known_update` ([datetime.datetime](https://docs.python.org/3/library/datetime.html)) (optional): Optional time of the last known update to this part’s config. If provided, this will result in a GRPCError if the upstream config has changed since this time, indicating that the local config is out of date. Omitting this parameter will result in an overwrite of the upstream config.

**Returns:**

- ([RobotPart](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The newly updated robot part.

**Raises:**

- (GRPCError): If either an invalid machine part ID, name, or config is passed, or if the upstream config has changed since last_known_update.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_machine_part = await cloud.update_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot_part).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id`
- `name` [(string)](https://pkg.go.dev/builtin#string)
- `robotConfig` (interface{})

**Returns:**

- [(*RobotPart)](https://pkg.go.dev/go.viam.com/rdk/app#RobotPart)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateRobotPart).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the requested robot part.
- `name` (string) (required): The new name of the robot part.
- `robotConfig` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The new config for the robot part.

**Returns:**

- (Promise<undefined | [RobotPart](https://ts.viam.dev/classes/appApi.RobotPart.html)>): The updated robot part.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPart = await appClient.updateRobotPart(
  '<YOUR-ROBOT-PART-ID>',
  'newName'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updaterobotpart).

{{% /tab %}}
{{< /tabs >}}

### NewRobotPart

Create a new machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine to create a new part for. See [Find machine ID](#find-machine-id) for instructions on retrieving this value.
- `part_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the new part.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The new machine part’s ID.

**Raises:**

- (GRPCError): If either an invalid machine ID or name is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_part_id = await cloud.new_robot_part(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc", part_name="myNewSubPart"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot_part).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `robotID`
- `partName` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.NewRobotPart).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `robotId` (string) (required): The ID of the robot to create a part for.
- `partName` (string) (required): The name for the new robot part.

**Returns:**

- (Promise<string>): The ID of the newly\-created robot part.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPartId = await appClient.newRobotPart(
  '<YOUR-ROBOT-ID>',
  'newPart'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#newrobotpart).

{{% /tab %}}
{{< /tabs >}}

### DeleteRobotPart

Delete the specified machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to delete. See [Find part ID](#find-part-id) for instructions on retrieving this value.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid machine part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `partID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteRobotPart).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `partId` (string) (required): The ID of the part to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteRobotPart('<YOUR-ROBOT-PART-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deleterobotpart).

{{% /tab %}}
{{< /tabs >}}

### MarkPartAsMain

Mark a machine part as the [_main_ part](/operate/reference/architecture/parts/#machine-parts) of a machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to mark as main.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid machine part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.mark_part_as_main(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_as_main).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `partID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.MarkPartAsMain).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `partId` (string) (required): The ID of the part to mark as main.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.markPartAsMain('<YOUR-ROBOT-PART-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#markpartasmain).

{{% /tab %}}
{{< /tabs >}}

### MarkPartForRestart

Mark a specified machine part for restart.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to mark for restart.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid machine part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.mark_part_for_restart(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_for_restart).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `partID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.MarkPartForRestart).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `partId` (string) (required): The ID of the part to mark for restart.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.markPartForRestart('<YOUR-ROBOT-PART-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#markpartforrestart).

{{% /tab %}}
{{< /tabs >}}

### CreateRobotPartSecret

Create a machine {{< glossary_tooltip term_id="part" text="part" >}} secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to create a secret for.

**Returns:**

- ([RobotPart](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The machine part the new secret was generated for.

**Raises:**

- (GRPCError): If an invalid machine part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
part_with_new_secret = await cloud.create_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_robot_part_secret).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `partID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*RobotPart)](https://pkg.go.dev/go.viam.com/rdk/app#RobotPart)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateRobotPartSecret).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `partId` (string) (required): The ID of the part to create a secret for.

**Returns:**

- (Promise<undefined | [RobotPart](https://ts.viam.dev/classes/appApi.RobotPart.html)>): The robot part object.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robotPart = await appClient.createRobotPartSecret(
  '<YOUR-ROBOT-PART-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createrobotpartsecret).

{{% /tab %}}
{{< /tabs >}}

### DeleteRobotPartSecret

Delete a machine part secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine part to delete the secret from.
- `secret_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the secret to delete.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid machine part ID or secret ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22",
    secret_id="123xyz12-abcd-4321-12ab-12xy1xyz12xy")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part_secret).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `partID`
- `secretID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteRobotPartSecret).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `partId` (string) (required): The ID of the part to delete a secret from.
- `secretId` (string) (required): The ID of the secret to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteRobotPartSecret(
  '<YOUR-ROBOT-PART-ID>',
  '<YOUR-SECRET-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deleterobotpartsecret).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `locationID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*Robot)](https://pkg.go.dev/go.viam.com/rdk/app#Robot)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListRobots).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `name`
- `location` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.NewRobot).

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

### UpdateRobot

Update an existing machine's name and/or location.

You can change:

- The machine's name (within the same location)
- The machine's location (within the same organization)
- Both name and location simultaneously

**Requirements for location changes:**

- You must be an organization owner, or have owner permissions for both the current and destination locations
- The destination location must be within the same organization
- No other machine in the destination location can have the same name

{{< alert title="Important" color="note" >}}
Moving a machine has several important implications:

- **Machine address changes**: The machine's network address will change to `<machine-main-part-name>.<new-location-id>.viam.cloud`. You'll need to update any code that references the old address.
- **Permission changes**: Access permissions will be updated. Users with access to the current location lose access, and users with access to the new location gain access to the machine.
- **Data access**: Users in the new location cannot access historical data from when the machine was in the previous location.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine to update. See [Find machine ID](#find-machine-id) for instructions on retrieving this value.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New name to be updated on the machine.
- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location under which the machine exists. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- ([viam.proto.app.Robot](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot)): The newly updated machine.

**Raises:**

- (GRPCError): If either an invalid machine ID, name, or location ID is passed or a location ID isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
updated_robot = await cloud.update_robot(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc",
    name="Orange-Robot",
    location_id="23ab12345"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id`
- `name`
- `location` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*Robot)](https://pkg.go.dev/go.viam.com/rdk/app#Robot)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateRobot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `robotId` (string) (required): The ID of the robot to update.
- `locId` (string) (required): The ID of the location where the robot is.
- `name` (string) (required): The name to update the robot to.

**Returns:**

- (Promise<undefined | [appApi](https://ts.viam.dev/modules/appApi.html).[Robot](https://ts.viam.dev/classes/appApi.Robot.html)>): The newly\-modified robot object.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const robot = await appClient.updateRobot(
  '<YOUR-ROBOT-ID>',
  '<YOUR-LOCATION-ID>',
  'newName'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updaterobot).

{{% /tab %}}
{{< /tabs >}}

### DeleteRobot

Delete a specified machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine to delete. See [Find machine ID](#find-machine-id) for instructions on retrieving this value.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid machine ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteRobot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the robot to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteRobot('<YOUR-ROBOT-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deleterobot).

{{% /tab %}}
{{< /tabs >}}

### GetRobotMetadata

Gets the user-defined metadata for a machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the robot with which the user-defined metadata is associated. You can obtain your robot ID from the machine page.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]): The user\-defined metadata converted from JSON to a Python dictionary.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
metadata = await cloud.get_robot_metadata(robot_id="<YOUR-ROBOT-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `robotID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobotMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the robot.

**Returns:**

- (Promise<Record<string, [JsonValue](https://ts.viam.dev/types/JsonValue.html)>>): The metadata associated with the robot.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const metadata = await appClient.getRobotMetadata('<YOUR-ROBOT-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotmetadata).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPartMetadata

Gets the user-defined metadata for a machine part.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the robot part with which the user-defined metadata is associated. You can obtain your robot part ID from the machine page.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]): The user\-defined metadata converted from JSON to a Python dictionary.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
metadata = await cloud.get_robot_part_metadata(robot_part_id="<YOUR-ROBOT-PART-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `robotID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRobotPartMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the robot part.

**Returns:**

- (Promise<Record<string, [JsonValue](https://ts.viam.dev/types/JsonValue.html)>>): The metadata associated with the robot part.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const metadata = await appClient.getRobotPartMetadata(
  '<YOUR-ROBOT-PART-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getrobotpartmetadata).

{{% /tab %}}
{{< /tabs >}}

### UpdateRobotMetadata

Updates the user-defined metadata for a machine.
User-defined metadata is billed as data.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the robot with which to associate the user-defined metadata. You can obtain your robot ID from the machine page.
- `metadata` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (required): The user-defined metadata converted from JSON to a Python dictionary.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.update_robot_metadata(robot_id="<YOUR-ROBOT-ID>", metadata=)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `robotID` [(string)](https://pkg.go.dev/builtin#string)
- `data` (interface{})

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateRobotMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the robot.
- `data` (Record) (required): The metadata to update.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.updateRobotMetadata('<YOUR-ROBOT-ID>', {
  key: 'value',
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updaterobotmetadata).

{{% /tab %}}
{{< /tabs >}}

### UpdateRobotPartMetadata

Updates the user-defined metadata for a machine part.
User-defined metadata is billed as data.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required)
- `metadata` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (required): The user-defined metadata converted from JSON to a Python dictionary.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.update_robot_part_metadata(robot_part_id="<YOUR-ROBOT-PART-ID>", metadata=)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot_part_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `robotID` [(string)](https://pkg.go.dev/builtin#string)
- `data` (interface{})

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateRobotPartMetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the robot part.
- `data` (Record) (required): The metadata to update.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.updateRobotPartMetadata('<YOUR-ROBOT-PART-ID>', {
  key: 'value',
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updaterobotpartmetadata).

{{% /tab %}}
{{< /tabs >}}

### ListFragments

Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}} in the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list fragments for. You can obtain your organization ID from the organization settings page.
- `show_public` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Optional boolean specifying whether or not to only show public fragments. If True, only public fragments will return. If False, only private fragments will return. Defaults to True.  Deprecated since version 0.25.0: Use visibilities instead.
- `visibilities` ([List[Fragment]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment.Visibility)) (optional): List of FragmentVisibilities specifying which types of fragments to include in the results. If empty, by default only public fragments will be returned.

**Returns:**

- ([List[Fragment]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment)): The list of fragments.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
fragments_list = await cloud.list_fragments(org_id="org-id", visibilities=[])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_fragments).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)
- `showPublic` [(bool)](https://pkg.go.dev/builtin#bool)
- `fragmentVisibility` [([]FragmentVisibility)](https://pkg.go.dev/go.viam.com/rdk/app#FragmentVisibility)

**Returns:**

- [([]*Fragment)](https://pkg.go.dev/go.viam.com/rdk/app#Fragment)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListFragments).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to list fragments for.
- `publicOnly` (boolean) (optional): Optional, deprecated boolean. Use fragmentVisibilities
  instead. If true then only public fragments will be listed. Defaults to
  true.
- `fragmentVisibility` ([FragmentVisibility](https://ts.viam.dev/enums/appApi.FragmentVisibility.html)) (optional)

**Returns:**

- (Promise<[Fragment](https://ts.viam.dev/classes/appApi.Fragment.html)[]>): The list of fragment objects.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const fragments = await appClient.listFragments(
  '<YOUR-ORGANIZATION-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listfragments).

{{% /tab %}}
{{< /tabs >}}

### ListMachineFragments

Get a list of top level and nested {{< glossary_tooltip term_id="fragment" text="fragments" >}} for a machine, as well as additionally specified fragment IDs.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `machineID` [(string)](https://pkg.go.dev/builtin#string)
- `additionalIDs` [([]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*Fragment)](https://pkg.go.dev/go.viam.com/rdk/app#Fragment)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListMachineFragments).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `machineId` (string) (required): The machine ID used to filter fragments defined in a
  machine's parts. Also returns any fragments nested within the fragments
  defined in parts.
- `additionalFragmentIds` (string) (optional): Additional fragment IDs to append to the
  response. Useful when needing to view fragments that will be
  provisionally added to the machine alongside existing fragments.

**Returns:**

- (Promise<[Fragment](https://ts.viam.dev/classes/appApi.Fragment.html)[]>): The list of top level and nested fragments for a machine, as well
as additionally specified fragment IDs.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const fragments = await appClient.listMachineFragments(
  '<YOUR-MACHINE-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listmachinefragments).

{{% /tab %}}
{{< /tabs >}}

### ListMachineSummaries

Lists machine summaries for an organization, optionally filtered by fragment IDs, location IDs, and limit.

{{< tabs >}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization.
- `fragmentIds` (string) (optional): Optional list of fragment IDs to filter machines.
- `locationIds` (string) (optional): Optional list of location IDs to filter machines.
- `limit` (number) (optional): Optional max number of machines to return.

**Returns:**

- (Promise<[LocationSummary](https://ts.viam.dev/classes/appApi.LocationSummary.html)[]>): The list of location summaries.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const summaries = await appClient.listMachineSummaries(
  'orgId',
  ['frag1'],
  ['loc1'],
  10
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listmachinesummaries).

{{% /tab %}}
{{< /tabs >}}

### GetFragment

Get a {{< glossary_tooltip term_id="fragment" text="fragment" >}} by ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `fragment_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the fragment to get.
- `version` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional specification of the fragment version to get (revision or tag).

**Returns:**

- ([Fragment](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment)): The fragment.

**Raises:**

- (GRPCError): If an invalid fragment ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Get a fragment and print its name and when it was created.
the_fragment = await cloud.get_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567")
print("Name: ", the_fragment.name, "\nCreated on: ", the_fragment.created_on)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_fragment).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id`
- `version` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*Fragment)](https://pkg.go.dev/go.viam.com/rdk/app#Fragment)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetFragment).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the fragment to look up.

**Returns:**

- (Promise<undefined | [Fragment](https://ts.viam.dev/classes/appApi.Fragment.html)>): The requested fragment.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const fragment = await appClient.getFragment(
  '12a12ab1-1234-5678-abcd-abcd01234567'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getfragment).

{{% /tab %}}
{{< /tabs >}}

### CreateFragment

Create a new private {{< glossary_tooltip term_id="fragment" text="fragment" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the fragment within. You can obtain your organization ID from the organization settings page.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the fragment.
- `config` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional Dictionary representation of new config to assign to specified fragment. Can be assigned by updating the fragment.

**Returns:**

- ([Fragment](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment)): The newly created fragment.

**Raises:**

- (GRPCError): If an invalid name is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_fragment = await cloud.create_fragment(org_id="org-id", name="cool_smart_machine_to_configure_several_of")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_fragment).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `name` [(string)](https://pkg.go.dev/builtin#string)
- `config` [(map[string]interface{})](https://pkg.go.dev/builtin#string)
- `opts` [(*CreateFragmentOptions)](https://pkg.go.dev/go.viam.com/rdk/app#CreateFragmentOptions)

**Returns:**

- [(*Fragment)](https://pkg.go.dev/go.viam.com/rdk/app#Fragment)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateFragment).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to create the fragment
  under.
- `name` (string) (required): The name of the new fragment.
- `config` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The new fragment's config.

**Returns:**

- (Promise<undefined | [Fragment](https://ts.viam.dev/classes/appApi.Fragment.html)>): The newly created fragment.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const fragment = await appClient.createFragment(
  '<YOUR-ORGANIZATION-ID>',
  'newFragment'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createfragment).

{{% /tab %}}
{{< /tabs >}}

### UpdateFragment

Update a {{< glossary_tooltip term_id="fragment" text="fragment" >}} name and its config and/or visibility.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `fragment_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the fragment to update.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New name to associate with the fragment.
- `config` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional Dictionary representation of new config to assign to specified fragment. Not passing this parameter will leave the fragment’s config unchanged.
- `public` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (optional): Boolean specifying whether the fragment is public. Not passing this parameter will leave the fragment’s visibility unchanged. A fragment is private by default when created.  Deprecated since version 0.25.0: Use visibility instead.
- `visibility` ([Fragment](https://python.viam.dev/autoapi/viam/gen/app/v1/app_pb2/index.html#viam.gen.app.v1.app_pb2.FragmentVisibility)) (optional): Optional FragmentVisibility list specifying who should be allowed to view the fragment. Not passing this parameter will leave the fragment’s visibility unchanged. A fragment is private by default when created.
- `last_known_update` ([datetime.datetime](https://docs.python.org/3/library/datetime.html)) (optional): Optional time of the last known update to this fragment’s config. If provided, this will result in a GRPCError if the upstream config has changed since this time, indicating that the local config is out of date. Omitting this parameter will result in an overwrite of the upstream config.

**Returns:**

- ([Fragment](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment)): The newly updated fragment.

**Raises:**

- (GRPCError): if an invalid ID, name, or config is passed, or if the upstream fragment config has changed since last_known_update.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
updated_fragment = await cloud.update_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567",
    name="better_name")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_fragment).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id`
- `name` [(string)](https://pkg.go.dev/builtin#string)
- `config` [(map[string]interface{})](https://pkg.go.dev/builtin#string)
- `opts` [(*UpdateFragmentOptions)](https://pkg.go.dev/go.viam.com/rdk/app#UpdateFragmentOptions)

**Returns:**

- [(*Fragment)](https://pkg.go.dev/go.viam.com/rdk/app#Fragment)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateFragment).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the fragment to update.
- `name` (string) (required): The name to update the fragment to.
- `config` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The config to update the fragment to.
- `makePublic` (boolean) (optional): Optional, deprecated boolean specifying whether the
  fragment should be public or not. If not passed, the visibility will be
  unchanged. Fragments are private by default when created.
- `visibility` ([FragmentVisibility](https://ts.viam.dev/enums/appApi.FragmentVisibility.html)) (optional): Optional FragmentVisibility specifying the updated
  fragment visibility. If not passed, the visibility will be unchanged. If
  visibility is not set and makePublic is set, makePublic takes effect. If
  makePublic and visibility are set, they must not be conflicting. If
  neither is set, the fragment visibility will remain unchanged.

**Returns:**

- (Promise<undefined | [Fragment](https://ts.viam.dev/classes/appApi.Fragment.html)>): The updated fragment.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const fragment = await appClient.updateFragment(
  '12a12ab1-1234-5678-abcd-abcd01234567',
  'better_name'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updatefragment).

{{% /tab %}}
{{< /tabs >}}

### DeleteFragment

Delete a {{< glossary_tooltip term_id="fragment" text="fragment" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `fragment_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the fragment to delete.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid fragment ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_fragment).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteFragment).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the fragment to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteFragment('12a12ab1-1234-5678-abcd-abcd01234567');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deletefragment).

{{% /tab %}}
{{< /tabs >}}

### GetFragmentHistory

Get fragment history.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the fragment to fetch history for.
- `page_token` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) | None) (optional): the page token for the fragment history collection.
- `page_limit` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): the number of fragment history documents to return in the result. The default page limit is 10.

**Returns:**

- ([List[FragmentHistoryEntry]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.FragmentHistoryEntry)): A list of documents with the fragment history.

**Raises:**

- (GRPCError): if an invalid fragment id, page token or page limit is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
fragment_history = await cloud.get_fragment_history(
    id = "12a12ab1-1234-5678-abcd-abcd01234567",
    page_token = "pg-token",
    page_limit = 10
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_fragment_history).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)
- `opts` [(*GetFragmentHistoryOptions)](https://pkg.go.dev/go.viam.com/rdk/app#GetFragmentHistoryOptions)

**Returns:**

- [([]*FragmentHistoryEntry)](https://pkg.go.dev/go.viam.com/rdk/app#FragmentHistoryEntry)
- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetFragmentHistory).

{{% /tab %}}
{{< /tabs >}}

### AddRole

Add a role under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the role in. You can obtain your organization ID from the organization settings page.
- `identity_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the entity the role belongs to (for example, a user ID).
- `role` (Literal['owner'] | Literal['operator']) (required): The role to add (either `"owner"` or `"operator"`).
- `resource_type` (Literal['organization'] | Literal['location'] | Literal['robot']) (required): The type of the resource to add the role to (either `"organization"`, `"location"`, or `"robot"`). Must match the type of the `resource_id`'s resource.
- `resource_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the resource the role applies to (the ID of either an {{< glossary_tooltip term_id="organization" text="organization" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="machine" text="machine" >}}.).

**Returns:**

- None.

**Raises:**

- (GRPCError): If either an invalid identity ID, role ID, resource type, or resource ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.add_role(
    org_id="<YOUR-ORG-ID>",
    identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    role="owner",
    resource_type="location",
    resource_id="111ab12345"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.add_role).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `identityID` [(string)](https://pkg.go.dev/builtin#string)
- `role` [(AuthRole)](https://pkg.go.dev/go.viam.com/rdk/app#AuthRole)
- `resourceType` [(AuthResourceType)](https://pkg.go.dev/go.viam.com/rdk/app#AuthResourceType)
- `resourceID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.AddRole).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to create the role under.
- `entityId` (string) (required): The ID of the entity the role belongs to (for example a
  user ID).
- `role` (string) (required): The role to add ("owner" or "operator").
- `resourceType` (string) (required): The type of resource to create the role for ("robot",
  "location", or "organization").
- `resourceId` (string) (required): The ID of the resource the role is being created for.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.addRole(
  '<YOUR-ORGANIZATION-ID>',
  '<YOUR-USER-ID>',
  'owner',
  'robot',
  '<YOUR-ROBOT-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#addrole).

{{% /tab %}}
{{< /tabs >}}

### RemoveRole

Remove a role under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization the role exists in. You can obtain your organization ID from the organization settings page.
- `identity_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the entity the role belongs to (for example, a user ID).
- `role` (Literal['owner'] | Literal['operator']) (required): The role to remove.
- `resource_type` (Literal['organization'] | Literal['location'] | Literal['robot']) (required): Type of the resource the role is being removed from. Must match resource_id.
- `resource_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the resource the role applies to (that is, either an organization, location, or robot ID).

**Returns:**

- None.

**Raises:**

- (GRPCError): If either an invalid identity ID, role ID, resource type, or resource ID or is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.remove_role(
    org_id="<YOUR-ORG-ID>",
    identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    role="owner",
    resource_type="location",
    resource_id="111ab12345"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.remove_role).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `authorization` [(*Authorization)](https://pkg.go.dev/go.viam.com/rdk/app#Authorization)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.RemoveRole).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to remove the role from.
- `entityId` (string) (required): The ID of the entity the role belongs to (for example a
  user ID).
- `role` (string) (required): The role to remove ("owner" or "operator").
- `resourceType` (string) (required): The type of resource to remove the role from ("robot",
  "location", or "organization").
- `resourceId` (string) (required): The ID of the resource the role is being removes from.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.removeRole(
  '<YOUR-ORGANIZATION-ID>',
  '<YOUR-USER-ID>',
  'owner',
  'robot',
  '<YOUR-ROBOT-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#removerole).

{{% /tab %}}
{{< /tabs >}}

### ChangeRole

Changes an existing role to a new role.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the organization.
- `old_identity_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the entity the role belongs to (for example, a user ID).
- `old_role` (Literal['owner'] | Literal['operator']) (required): The role to be changed.
- `old_resource_type` (Literal['organization'] | Literal['location'] | Literal['robot']) (required): Type of the resource the role is added to. Must match old_resource_id.
- `old_resource_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the resource the role applies to (that is, either an organization, location, or robot ID).
- `new_identity_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New ID of the entity the role belongs to (for example, a user ID).
- `new_role` (Literal['owner'] | Literal['operator']) (required): The new role.
- `new_resource_type` (Literal['organization'] | Literal['location'] | Literal['robot']) (required): Type of the resource to add role to. Must match new_resource_id.
- `new_resource_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New ID of the resource the role applies to (that is, either an organization, location, or robot ID).

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.change_role(
    organization_id="<YOUR-ORG-ID>",
    old_identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    old_role="operator",
    old_resource_type="location",
    old_resource_id="111ab12345",
    new_identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    new_role="owner",
    new_resource_type="organization",
    new_resource_id="abc12345"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.change_role).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `oldAuthorization` [(*Authorization)](https://pkg.go.dev/go.viam.com/rdk/app#Authorization)
- `newOrgID`
- `newIdentityID` [(string)](https://pkg.go.dev/builtin#string)
- `newRole` [(AuthRole)](https://pkg.go.dev/go.viam.com/rdk/app#AuthRole)
- `newResourceType` [(AuthResourceType)](https://pkg.go.dev/go.viam.com/rdk/app#AuthResourceType)
- `newResourceID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ChangeRole).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `oldAuthorization` ([Authorization](https://ts.viam.dev/classes/appApi.Authorization.html)) (required): The existing authorization.
- `newAuthorization` ([Authorization](https://ts.viam.dev/classes/appApi.Authorization.html)) (required): The new authorization to change to.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const oldAuth = new VIAM.appApi.Authorization({
  authorizationType: 'role',
  authorizationId: 'organization_owner',
  organizationId: '<YOUR-ORGANIZATION-ID>',
  resourceId: '<YOUR-RESOURCE-ID>', // The resource to grant access to
  resourceType: 'organization', // The type of resource to grant access to
  identityId: '<USER-ID>', // The user id of the user to grant access to (optional)
  roleId: 'owner', // The role to grant access to
  identityType: 'user',
});
const newAuth = new VIAM.appApi.Authorization({
  authorizationType: 'role',
  authorizationId: 'organization_operator',
  organizationId: '<YOUR-ORGANIZATION-ID>',
  resourceId: '<YOUR-RESOURCE-ID>', // The resource to grant access to
  resourceType: 'organization', // The type of resource to grant access To
  identityId: '<USER-ID>', // The user id of the user to grant access to (optional)
  roleId: 'operator', // The role to grant access to
  identityType: 'user',
});
await appClient.changeRole(oldAuth, newAuth);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#changerole).

{{% /tab %}}
{{< /tabs >}}

### ListAuthorizations

List all authorizations (owners and operators) of a specific resource (or resources) within the organization you are currently authenticated to.
If no resource IDs are provided, all resource authorizations within the organizations are returned.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list authorizations for.
- `resource_ids` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): IDs of the resources to retrieve authorizations from. If None, defaults to all resources.

**Returns:**

- ([List[viam.proto.app.Authorization]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization)): The list of authorizations.

**Raises:**

- (GRPCError): If an invalid resource ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
list_of_auths = await cloud.list_authorizations(
    org_id="<YOUR-ORG-ID>",
    resource_ids=["1a123456-x1yz-0ab0-a12xyzabc"])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_authorizations).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)
- `resourceIDs` [([]string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*Authorization)](https://pkg.go.dev/go.viam.com/rdk/app#Authorization)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListAuthorizations).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to list authorizations for.
- `resourceIds` (string) (optional): Optional list of IDs of resources to list authorizations
  for. If not provided, all resources will be included.

**Returns:**

- (Promise<[Authorization](https://ts.viam.dev/classes/appApi.Authorization.html)[]>): The list of authorizations.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listauthorizations).

{{% /tab %}}
{{< /tabs >}}

### CheckPermissions

Check if the organization, location, or robot your `ViamClient` is authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `permissions` ([List[viam.proto.app.AuthorizedPermissions]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.AuthorizedPermissions)) (required): the permissions to validate (for example, “read_organization”, “control_robot”).

**Returns:**

- ([List[viam.proto.app.AuthorizedPermissions]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.AuthorizedPermissions)): The permissions argument, with invalid permissions filtered out.

**Raises:**

- (GRPCError): If the list of permissions to validate is empty.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app import AuthorizedPermissions

# Check whether the entity you're currently authenticated to has permission to control and/or
# read logs from robots in the "organization-identifier123" org
permissions = [AuthorizedPermissions(resource_type="organization",
                                     resource_id="<YOUR-ORG-ID>",
                                     permissions=["control_robot",
                                                  "read_robot_logs"])]

filtered_permissions = await cloud.check_permissions(permissions)
```

Valid arguments for permissions are as follows:

{{% expand "Click to see permissions strings available" %}}

```python
"read_organization"
"write_organization"

"read_fragment"
"write_fragment"

"read_location"
"write_location"

"read_location_secret"
"read_robot_secret"

"read_robot"
"read_robot_config"
"read_robot_logs"
"write_robot"
"control_robot"

"read_organization_data_management"
"read_location_data_management"
"read_robot_data_management"
"write_organization_data_management"
"write_location_data_management"
"write_robot_data_management"

"read_robot_history"

"read_mapping_sessions"
"create_maps"

"write_private_registry_item"
"write_public_registry_item"
"read_private_registry_item"

"train_models"

"read_packages"
"write_packages"
"delete_packages"

"configure_database_user"
"get_database_connection"

"create_dataset"
"list_dataset"
"rename_dataset"
"delete_dataset"
```

{{% /expand %}}

For more information about managing permissions, see [Role-Based Access Control](/manage/manage/rbac/).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.check_permissions).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `permissions` [([]*AuthorizedPermissions)](https://pkg.go.dev/go.viam.com/rdk/app#AuthorizedPermissions)

**Returns:**

- [([]*AuthorizedPermissions)](https://pkg.go.dev/go.viam.com/rdk/app#AuthorizedPermissions)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CheckPermissions).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `permissions` ([AuthorizedPermissions](https://ts.viam.dev/classes/appApi.AuthorizedPermissions.html)) (required): A list of permissions to check.

**Returns:**

- (Promise<[AuthorizedPermissions](https://ts.viam.dev/classes/appApi.AuthorizedPermissions.html)[]>): A filtered list of the authorized permissions.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#checkpermissions).

{{% /tab %}}
{{< /tabs >}}

### GetRegistryItem

Get metadata about a registry item (a module, training script, or ML model) by registry item ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `item_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the registry item. This is the namespace and name of the item in the form namespace:name. For example, Viam’s csi-cam-pi module’s item ID would be viam:csi-cam-pi. You can also use org-id:name. For example, abc01234-0123-4567-ab12-a11a00a2aa22:training-script.
- `include_markdown_documentation` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required)

**Returns:**

- ([viam.proto.app.RegistryItem](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.RegistryItem)): The registry item.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
item = await cloud.get_registry_item("item-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_registry_item).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `itemID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*RegistryItem)](https://pkg.go.dev/go.viam.com/rdk/app#RegistryItem)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetRegistryItem).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `itemId` (string) (required): The ID of the item to get.

**Returns:**

- (Promise<undefined | [RegistryItem](https://ts.viam.dev/classes/appApi.RegistryItem.html)>): The requested item.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const registryItem = await appClient.getRegistryItem(
  '<YOUR-REGISTRY-ITEM-ID>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getregistryitem).

{{% /tab %}}
{{< /tabs >}}

### CreateRegistryItem

Create a registry item.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The organization to create the registry item under.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the registry item, which must be unique within your org.
- `type` (viam.proto.app.packages.PackageType.ValueType) (required): The type of the item in the registry.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.packages import PackageType

await cloud.create_registry_item("<YOUR-ORG-ID>", "name", PackageType.PACKAGE_TYPE_ML_MODEL)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_registry_item).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `name` [(string)](https://pkg.go.dev/builtin#string)
- `packageType` [(PackageType)](https://pkg.go.dev/go.viam.com/rdk/app#PackageType)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateRegistryItem).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to create the registry
  item under.
- `name` (string) (required): The name of the registry item.
- `type` (PackageType) (required): The type of the item in the registry.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.createRegistryItem(
  '<YOUR-ORGANIZATION-ID>',
  'newRegistryItemName',
  5
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createregistryitem).

{{% /tab %}}
{{< /tabs >}}

### UpdateRegistryItem

Update a registry item.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `item_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the registry item, containing either the namespace and module name (for example, my-org:my-module) or organization ID and module name (org-id:my-module).
- `type` (viam.proto.app.packages.PackageType.ValueType) (required): The type of the item in the registry.
- `description` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The description of the registry item.
- `visibility` (viam.proto.app.Visibility.ValueType) (required): The visibility of the registry item.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.packages import PackageType
from viam.proto.app import Visibility

await cloud.update_registry_item(
    "your-namespace:your-name",
    PackageType.PACKAGE_TYPE_ML_TRAINING,
    "description",
    Visibility.VISIBILITY_PUBLIC
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_registry_item).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `itemID` [(string)](https://pkg.go.dev/builtin#string)
- `packageType` [(PackageType)](https://pkg.go.dev/go.viam.com/rdk/app#PackageType)
- `description` [(string)](https://pkg.go.dev/builtin#string)
- `visibility` [(Visibility)](https://pkg.go.dev/go.viam.com/rdk/app#Visibility)
- `opts` [(*UpdateRegistryItemOptions)](https://pkg.go.dev/go.viam.com/rdk/app#UpdateRegistryItemOptions)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateRegistryItem).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `itemId` (string) (required): The ID of the registry item to update.
- `type` (PackageType) (required): The PackageType to update the item to.
- `description` (string) (required): A description of the item.
- `visibility` ([Visibility](https://ts.viam.dev/enums/appApi.Visibility.html)) (required): A visibility value to update to.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.updateRegistryItem(
  '<YOUR-REGISTRY-ITEM-ID>',
  5, // Package: ML Model
  'new description',
  1 // Private
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updateregistryitem).

{{% /tab %}}
{{< /tabs >}}

### ListRegistryItems

List the registry items in an organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `organization_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to return registry items for.
- `types` (List[viam.proto.app.packages.PackageType.ValueType]) (required): The types of registry items.
- `visibilities` (List[viam.proto.app.Visibility.ValueType]) (required): The visibilities of registry items.
- `platforms` (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (required): The platforms of registry items.
- `statuses` (List[viam.proto.app.RegistryItemStatus.ValueType]) (required): The types of the items in the registry.
- `search_term` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): The search term of the registry items.
- `page_token` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): The page token of the registry items.

**Returns:**

- ([List[viam.proto.app.RegistryItem]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.RegistryItem)): The list of registry items.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app.packages import PackageType
from viam.proto.app import Visibility, RegistryItemStatus

# List private, published ml training scripts in your organization
registry_items = await cloud.list_registry_items(
    organization_id="<YOUR-ORG-ID>",
    types=[PackageType.PACKAGE_TYPE_ML_TRAINING],
    visibilities=[Visibility.VISIBILITY_PRIVATE],
    platforms=[""],
    statuses=[RegistryItemStatus.REGISTRY_ITEM_STATUS_PUBLISHED]
)

# List public, published linux modules in all organizations
registry_items = await cloud.list_registry_items(
    organization_id="",
    types=[PackageType.PACKAGE_TYPE_MODULE],
    visibilities=[Visibility.VISIBILITY_PUBLIC],
    platforms=["linux/any"],
    statuses=[RegistryItemStatus.REGISTRY_ITEM_STATUS_PUBLISHED]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_registry_items).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(*string)](https://pkg.go.dev/builtin#string)
- `types` [([]PackageType)](https://pkg.go.dev/go.viam.com/rdk/app#PackageType)
- `visibilities` [([]Visibility)](https://pkg.go.dev/go.viam.com/rdk/app#Visibility)
- `platforms` [([]string)](https://pkg.go.dev/builtin#string)
- `statuses` [([]RegistryItemStatus)](https://pkg.go.dev/go.viam.com/rdk/app#RegistryItemStatus)
- `opts` [(*ListRegistryItemsOptions)](https://pkg.go.dev/go.viam.com/rdk/app#ListRegistryItemsOptions)

**Returns:**

- [([]*RegistryItem)](https://pkg.go.dev/go.viam.com/rdk/app#RegistryItem)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListRegistryItems).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to query registry items
  for.
- `types` (PackageType) (required): A list of types to query. If empty, will not filter on type.
- `visibilities` ([Visibility](https://ts.viam.dev/enums/appApi.Visibility.html)) (required): A list of visibilities to query for. If empty, will not
  filter on visibility.
- `platforms` (string) (required): A list of platforms to query for. If empty, will not
  filter on platform.
- `statuses` ([RegistryItemStatus](https://ts.viam.dev/enums/appApi.RegistryItemStatus.html)) (required): A list of statuses to query for. If empty, will not filter
  on status.
- `searchTerm` (string) (optional): Optional search term to filter on.
- `pageToken` (string) (optional): Optional page token for results. If not provided, will
  return all results.

**Returns:**

- (Promise<[RegistryItem](https://ts.viam.dev/classes/appApi.RegistryItem.html)[]>): The list of registry items.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const registryItems = await appClient.listRegistryItems(
  '<YOUR-ORGANIZATION-ID>',
  [], // All package types
  [1], // Private packages
  [],
  [1] // Active packages
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listregistryitems).

{{% /tab %}}
{{< /tabs >}}

### DeleteRegistryItem

Delete a registry item.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `item_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the deleted registry item, containing either the namespace and module name (for example, my-org:my-module) or organization ID and module name (org-id:my-module).

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_registry_item("your-namespace:your-name")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_registry_item).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `itemID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteRegistryItem).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `itemId` (string) (required): The ID of the item to delete.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await appClient.deleteRegistryItem('<YOUR-REGISTRY-ITEM-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#deleteregistryitem).

{{% /tab %}}
{{< /tabs >}}

### CreateModule

Create a {{< glossary_tooltip term_id="module" text="module" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the module under. You can obtain your organization ID from the organization settings page.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the module. Must be unique within your organization.

**Returns:**

- (Tuple[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing the ID \[0] of the new module and its URL \[1].

**Raises:**

- (GRPCError): If an invalid name (for example, “”) is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_module = await cloud.create_module(org_id="org-id", name="cool_new_hoverboard_module")
print("Module ID:", new_module[0])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_module).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID`
- `name` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateModule).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to create the module under.
- `name` (string) (required): The name of the module.

**Returns:**

- (Promise<[CreateModuleResponse](https://ts.viam.dev/classes/appApi.CreateModuleResponse.html)>): The module ID and a URL to its detail page.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const module = await appClient.createModule(
  '<YOUR-ORGANIZATION-ID>',
  'newModule'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createmodule).

{{% /tab %}}
{{< /tabs >}}

### UpdateModule

Update the documentation URL, description, models, entrypoint, and/or the visibility of a {{< glossary_tooltip term_id="module" text="module" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `module_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the module being updated, containing either the namespace and module name (for example, my-org:my-module) or organization ID and module name (org-id:my-module).
- `url` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The url to reference for documentation and code (NOT the url of the module itself).
- `description` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): A short description of the module that explains its purpose.
- `models` ([List[viam.proto.app.Model]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model)) (optional): list of models that are available in the module.
- `entrypoint` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The executable to run to start the module program.
- `public` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): The visibility that should be set for the module. Defaults to False (private).

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The URL of the newly updated module.

**Raises:**

- (GRPCError): If either an invalid module ID, URL, list of models, or organization ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app import Model

model = Model(
    api="rdk:component:base",
    model="my-group:cool_new_hoverboard_module:wheeled"
)

url_of_my_module = await cloud.update_module(
    module_id="my-group:cool_new_hoverboard_module",
    url="https://docsformymodule.viam.com",
    models=[model],
    description="A base to support hoverboards.",
    entrypoint="exec"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_module).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `moduleID` [(string)](https://pkg.go.dev/builtin#string)
- `visibility` [(Visibility)](https://pkg.go.dev/go.viam.com/rdk/app#Visibility)
- `url`
- `description` [(string)](https://pkg.go.dev/builtin#string)
- `models` [([]*Model)](https://pkg.go.dev/go.viam.com/rdk/app#Model)
- `apps` [([]*App)](https://pkg.go.dev/go.viam.com/rdk/app#App)
- `entrypoint` [(string)](https://pkg.go.dev/builtin#string)
- `opts` [(*UpdateModuleOptions)](https://pkg.go.dev/go.viam.com/rdk/app#UpdateModuleOptions)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UpdateModule).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `moduleId` (string) (required): The ID of the module to update.
- `visibility` ([Visibility](https://ts.viam.dev/enums/appApi.Visibility.html)) (required): The visibility to set for the module.
- `url` (string) (required): The url to reference for documentation, code, etc.
- `description` (string) (required): A short description of the module.
- `models` ([Model](https://ts.viam.dev/classes/appApi.Model.html)) (required): A list of models available in the module.
- `entrypoint` (string) (required): The executable to run to start the module program.

**Returns:**

- (Promise<string>): The module URL.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const module = await appClient.updateModule(
  '<YOUR-MODULE-ID>',
  1,
  'https://example.com',
  'new description',
  [{ model: 'namespace:group:model1', api: 'rdk:component:generic' }],
  'entrypoint'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#updatemodule).

{{% /tab %}}
{{< /tabs >}}

### UploadModuleFile

Upload a {{< glossary_tooltip term_id="module" text="module" >}} file.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `module_file_info` ([viam.proto.app.ModuleFileInfo](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.ModuleFileInfo)) (optional): Relevant metadata.
- `file` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): Bytes of file to upload.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): URL of uploaded file.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app import ModuleFileInfo

module_file_info = ModuleFileInfo(
    module_id = "sierra:cool_new_hoverboard_module",
    version = "1.0.0",
    platform = "darwin/arm64"
)

file_id = await cloud.upload_module_file(
    module_file_info=module_file_info,
    file=b"<file>"
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.upload_module_file).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `fileInfo` [(ModuleFileInfo)](https://pkg.go.dev/go.viam.com/rdk/app#ModuleFileInfo)
- `file` [([]byte)](https://pkg.go.dev/builtin#byte)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.UploadModuleFile).

{{% /tab %}}
{{< /tabs >}}

### GetModule

Get a {{< glossary_tooltip term_id="module" text="module" >}} by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `module_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the module being retrieved, containing either the namespace and module name (for example, my-org:my-module) or organization ID and module name (org-id:my-module).

**Returns:**

- ([viam.proto.app.Module](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Module)): The module.

**Raises:**

- (GRPCError): If an invalid module ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
the_module = await cloud.get_module(module_id="my-group:my-cool-modular-base")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_module).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `moduleID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*Module)](https://pkg.go.dev/go.viam.com/rdk/app#Module)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.GetModule).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `moduleId` (string) (required): The ID of the module.

**Returns:**

- (Promise<undefined | [Module](https://ts.viam.dev/classes/appApi.Module.html)>): The requested module.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const module = await appClient.getModule('<YOUR-MODULE-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getmodule).

{{% /tab %}}
{{< /tabs >}}

### ListModules

List the {{< glossary_tooltip term_id="module" text="modules" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list modules for. You can obtain your organization ID from the organization settings page.

**Returns:**

- ([List[viam.proto.app.Module]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Module)): The list of modules.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
modules_list = await cloud.list_modules("<YOUR-ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_modules).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `opts` [(*ListModulesOptions)](https://pkg.go.dev/go.viam.com/rdk/app#ListModulesOptions)

**Returns:**

- [([]*Module)](https://pkg.go.dev/go.viam.com/rdk/app#Module)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListModules).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `organizationId` (string) (required): The ID of the organization to query.

**Returns:**

- (Promise<[Module](https://ts.viam.dev/classes/appApi.Module.html)[]>): The organization's modules.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const modules = await appClient.listModules('<YOUR-ORGANIZATION-ID>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#listmodules).

{{% /tab %}}
{{< /tabs >}}

### CreateKey

Create a new [API key](/operate/control/api-keys/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the key for. You can obtain your organization ID from the organization settings page.
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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)
- `keyAuthorizations` [([]APIKeyAuthorization)](https://pkg.go.dev/go.viam.com/rdk/app#APIKeyAuthorization)
- `name` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.CreateKey).

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.DeleteKey).

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
key, id = await cloud.rotate_key("key-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.rotate_key).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string)
- [(string)](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.RotateKey).

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

### ListKeys

List all keys for the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list API keys for. You can obtain your organization ID from the organization settings page.

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

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]*APIKeyWithAuthorizations)](https://pkg.go.dev/go.viam.com/rdk/app#APIKeyWithAuthorizations)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#AppClient.ListKeys).

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

### CreateKeyFromExistingKeyAuthorizations

Create a new API key with an existing key’s authorizations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the API key to duplication authorizations from.

**Returns:**

- (Tuple[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The API key and API key id.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
api_key, api_key_id = await cloud.create_key_from_existing_key_authorizations(
    id="INSERT YOUR API KEY ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key_from_existing_key_authorizations).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The ID of the key to duplicate.

**Returns:**

- (Promise<[CreateKeyFromExistingKeyAuthorizationsResponse](https://ts.viam.dev/classes/appApi.CreateKeyFromExistingKeyAuthorizationsResponse.html)>): The new key and ID.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const key =
  await appClient.createKeyFromExistingKeyAuthorizations(
    '<YOUR-KEY-ID>'
  );
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#createkeyfromexistingkeyauthorizations).

{{% /tab %}}
{{< /tabs >}}

### GetAppContent

Retrieve the app content for an organization.

{{< tabs >}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `publicNamespace` (string) (required): The public namespace of the organization.
- `name` (string) (required): The name of the app.

**Returns:**

- (Promise<[GetAppContentResponse](https://ts.viam.dev/classes/appApi.GetAppContentResponse.html)>): The blob path and entrypoint of the app content.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const appContent = await appClient.getAppContent(
  '<YOUR-PUBLIC-NAMESPACE>',
  '<YOUR-APP-NAME>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getappcontent).

{{% /tab %}}
{{< /tabs >}}

### GetAppBranding

Retrieves the app branding for an organization or app.

{{< tabs >}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `publicNamespace` (string) (required): The public namespace of the organization.
- `name` (string) (required): The name of the app.

**Returns:**

- (Promise<[GetAppBrandingResponse](https://ts.viam.dev/classes/appApi.GetAppBrandingResponse.html)>): The branding information for the app.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const branding = await appClient.getAppBranding(
  '<YOUR-PUBLIC-NAMESPACE>',
  '<YOUR-APP-NAME>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AppClient.html#getappbranding).

{{% /tab %}}
{{< /tabs >}}
