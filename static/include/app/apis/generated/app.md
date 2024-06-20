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
{{< /tabs >}}

### GetOrganization

Return details about the requested organization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to query.

**Returns:**

- ([viam.proto.app.Organization](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Organization)): The requested organization.

**Raises:**

- (GRPCError): If the provided org_id is invalid, or not currently authed to.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization).

{{% /tab %}}
{{< /tabs >}}

### GetOrganizationNamespaceAvailability

Check the availability of an {{< glossary_tooltip term_id="organization" text="organization" >}} namespace.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `public_namespace` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Organization namespace to check. Namespaces can only contain lowercase lowercase alphanumeric and dash characters.

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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization).

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
member_list, invite_list = await cloud.list_organization_members("org-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

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
await cloud.create_organization_invite("org-id", "youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_organization_invite).

{{% /tab %}}
{{< /tabs >}}

### UpdateOrganizationInviteAuthorizations

Update (add or remove) the authorizations attached to an organization invite that has already been created.
If an invitation has only one authorization and you want to remove it, delete the invitation instead of using this method.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that the invite is for. You can obtain your organization ID from the Viam app’s organization settings page.
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

authorization_to_add = Authorization(
    authorization_type="some type of auth",
    authorization_id="identifier",
    resource_type="abc",
    resource_id="resource-identifier123",
    identity_id="id12345",
    organization_id="org_id_123"
)

update_invite = await cloud.update_organization_invite_authorizations(
    org_id="org_id_123",
    email="notarealemail@viam.com",
    add_authorizations =[authorization_to_add]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization_invite_authorizations).

{{% /tab %}}
{{< /tabs >}}

### DeleteOrganizationMember

Remove a member from the {{< glossary_tooltip term_id="organization" text="organization" >}} you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the org to remove the user from. You can obtain your organization ID from the Viam app’s organization settings page.
- `user_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the user to remove.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await cloud.list_organization_members()
first_user_id = member_list[0].user_id

await cloud.delete_organization_member(org_id="org_id", user_id=first_user_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_member).

{{% /tab %}}
{{< /tabs >}}

### DeleteOrganizationInvite

Delete a pending organization invite to the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that the invite to delete was for. You can obtain your organization ID from the Viam app’s organization settings page.
- `email` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The email address the pending invite was sent to.

**Returns:**

- None.

**Raises:**

- (GRPCError): If no pending invite is associated with the provided email address.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_organization_invite("org-id", "youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_invite).

{{% /tab %}}
{{< /tabs >}}

### ResendOrganizationInvite

Resend a pending organization invite email.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization that the invite to resend was for. You can obtain your organization ID from the Viam app’s organization settings page.
- `email` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The email address associated with the invite.

**Returns:**

- ([app.OrganizationInvite](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)): The organization invite sent.

**Raises:**

- (GRPCError): If no pending invite is associated with the provided email address.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
org_invite = await cloud.resend_organization_invite("org-id", "youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.resend_organization_invite).

{{% /tab %}}
{{< /tabs >}}

### CreateLocation

Create and name a {{< glossary_tooltip term_id="location" text="location" >}} under the organization you are currently authenticated to.
Optionally, put the new location under a specified parent location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the location under. You can obtain your organization ID from the Viam app’s organization settings page.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the location.
- `parent_location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional parent location to put the location under. Defaults to a root-level location if no location ID is provided.

**Returns:**

- ([viam.proto.app.Location](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)): The newly created location.

**Raises:**

- (GRPCError): If either an invalid name (for example, “”), or parent location ID (for example, a nonexistent ID) is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_new_location = await cloud.create_location(org_id="org-id", name="Robotville", parent_location_id="111ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location).

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
{{< /tabs >}}

### UpdateLocation

Change the name of a {{< glossary_tooltip term_id="location" text="parent location" >}} and/or assign it a new location.

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
{{< /tabs >}}

### ListLocations

Get a list of all {{< glossary_tooltip term_id="location" text="locations" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the org to list locations for. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- ([List[viam.proto.app.Location]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)): The list of locations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
locations = await cloud.list_locations("org-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_locations).

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
{{< /tabs >}}

### GetRobot

Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot to get.

**Returns:**

- ([viam.proto.app.Robot](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot)): The robot.

**Raises:**

- (GRPCError): If an invalid robot ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
robot = await cloud.get_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot).

{{% /tab %}}
{{< /tabs >}}

### GetRobotParts

Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot to get parts from.

**Returns:**

- ([List[RobotPart]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The list of robot parts.

**Raises:**

- (GRPCError): If an invalid robot ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
list_of_parts = await cloud.get_robot_parts(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_parts).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPart

Get a specific machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to get.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath to write the robot part’s config file in JSON format to.
- `indent` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Size (in number of spaces) of indent when writing config to dest. Defaults to 4.

**Returns:**

- ([RobotPart](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The robot part.

**Raises:**

- (GRPCError): If an invalid robot part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_robot_part = await cloud.get_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPartLogs

Get the logs associated with a specific machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to get logs from.
- `filter` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Only include logs with messages that contain the string filter. Defaults to empty string “” (that is, no filter).
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Optional filepath to write the log entries to.
- `errors_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Boolean specifying whether or not to only include error logs. Defaults to True.
- `num_log_entries` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first num_log_entries logs will be returned, whichever comes first.

**Returns:**

- ([List[LogEntry]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.LogEntry)): The list of log entries.

**Raises:**

- (GRPCError): If an invalid robot part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
part_logs = await cloud.get_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22", num_log_entries=20)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_logs).

{{% /tab %}}
{{< /tabs >}}

### TailRobotPartLogs

Get an asynchronous iterator that receives live machine part logs.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to retrieve logs from.
- `errors_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Boolean specifying whether or not to only include error logs. Defaults to True.
- `filter` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): Only include logs with messages that contain the string filter. Defaults to empty string “” (that is, no filter).

**Returns:**

- ([viam.app._logs._LogsStream[List[LogEntry]]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.LogEntry)): The asynchronous iterator receiving live robot part logs.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
logs_stream = await cloud.tail_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.tail_robot_part_logs).

{{% /tab %}}
{{< /tabs >}}

### GetRobotPartHistory

Get a list containing the history of a machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to retrieve history from.

**Returns:**

- ([List[RobotPartHistoryEntry]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPartHistoryEntry)): The list of the robot part’s history.

**Raises:**

- (GRPCError): If an invalid robot part ID is provided.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
part_history = await cloud.get_robot_part_history(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_history).

{{% /tab %}}
{{< /tabs >}}

### UpdateRobotPart

Change the name of and assign an optional new configuration to a machine {{< glossary_tooltip term_id="part" text="part" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to update.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New name to be updated on the robot part.
- `robot_config` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional new config represented as a dictionary to be updated on the robot part. The robot part’s config will remain as is (no change) if one isn’t passed.

**Returns:**

- ([RobotPart](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The newly updated robot part.

**Raises:**

- (GRPCError): If either an invalid robot part ID, name, or config is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_robot_part = await cloud.update_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot_part).

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

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The new robot part’s ID.

**Raises:**

- (GRPCError): If either an invalid robot ID or name is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_part_id = await cloud.new_robot_part(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc", part_name="myNewSubPart")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot_part).

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

- (GRPCError): If an invalid robot part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part).

{{% /tab %}}
{{< /tabs >}}

### MarkPartAsMain

Mark a machine part as the [_main_ part](/build/configure/parts/#machine-parts) of a machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to mark as main.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid robot part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.mark_part_as_main(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_as_main).

{{% /tab %}}
{{< /tabs >}}

### MarkPartForRestart

Mark a specified machine part for restart.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to mark for restart.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid robot part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.mark_part_for_restart(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_for_restart).

{{% /tab %}}
{{< /tabs >}}

### CreateRobotPartSecret

Create a machine {{< glossary_tooltip term_id="part" text="part" >}} secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to create a secret for.

**Returns:**

- ([RobotPart](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The robot part the new secret was generated for.

**Raises:**

- (GRPCError): If an invalid robot part ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
part_with_new_secret = await cloud.create_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_robot_part_secret).

{{% /tab %}}
{{< /tabs >}}

### DeleteRobotPartSecret

Delete a machine part secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_part_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the robot part to delete the secret from.
- `secret_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the secret to delete.

**Returns:**

- None.

**Raises:**

- (GRPCError): If an invalid robot part ID or secret ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22",
    secret_id="123xyz12-abcd-4321-12ab-12xy1xyz12xy")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part_secret).

{{% /tab %}}
{{< /tabs >}}

### ListRobots

Get a list of all machines in a specified location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location to retrieve the robots from. Defaults to the location ID provided at AppClient instantiation.

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
{{< /tabs >}}

### NewRobot

Create a new {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the new robot.
- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location under which to create the robot. Defaults to the current authorized location.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): The new robot’s ID.

**Raises:**

- (GRPCError): If an invalid location ID is passed or one isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_machine_id = await cloud.new_robot(name="beepboop")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot).

{{% /tab %}}
{{< /tabs >}}

### UpdateRobot

Change the name of an existing machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the machine to update. See [Find machine ID](#find-machine-id) for instructions on retrieving this value.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New name to be updated on the robot.
- `location_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): ID of the location under which the robot exists. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- ([viam.proto.app.Robot](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot)): The newly updated robot.

**Raises:**

- (GRPCError): If either an invalid robot ID, name, or location ID is passed or a location ID isn’t passed and there was no location ID provided at AppClient instantiation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
updated_robot = await cloud.update_robot(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc",
    name="Orange-Robot")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot).

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

- (GRPCError): If an invalid robot ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot).

{{% /tab %}}
{{< /tabs >}}

### ListFragments

Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}} in the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list fragments for. You can obtain your organization ID from the Viam app’s organization settings page.
- `show_public` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Optional boolean specifying whether or not to only show public fragments. If True, only public fragments will return. If False, only private fragments will return. Defaults to True.

**Returns:**

- ([List[Fragment]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment)): The list of fragments.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
fragments_list = await cloud.list_fragments(org_id="org-id", show_public=False)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_fragments).

{{% /tab %}}
{{< /tabs >}}

### GetFragment

Get a {{< glossary_tooltip term_id="fragment" text="fragment" >}} by ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `fragment_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the fragment to get.

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
{{< /tabs >}}

### CreateFragment

Create a new private {{< glossary_tooltip term_id="fragment" text="fragment" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the fragment within. You can obtain your organization ID from the Viam app’s organization settings page.
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
{{< /tabs >}}

### UpdateFragment

Update a {{< glossary_tooltip term_id="fragment" text="fragment" >}} name and its config and/or visibility.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `fragment_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the fragment to update.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): New name to associate with the fragment.
- `config` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Optional Dictionary representation of new config to assign to specified fragment. Not passing this parameter will leave the fragment’s config unchanged.
- `public` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (optional): Boolean specifying whether the fragment is public. Not passing this parameter will leave the fragment’s visibility unchanged. A fragment is private by default when created.

**Returns:**

- ([Fragment](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment)): The newly updated fragment.

**Raises:**

- (GRPCError): if an invalid ID, name, or config is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
updated_fragment = await cloud.update_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567",
    name="better_name")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_fragment).

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
{{< /tabs >}}

### AddRole

Add a role under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the role in. You can obtain your organization ID from the Viam app’s organization settings page.
- `identity_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the entity the role belongs to (for example, a user ID).
- `role` (Literal[owner] | Literal[operator]) (required): The role to add (either `"owner"` or `"operator"`).
- `resource_type` (Literal[organization] | Literal[location] | Literal[robot]) (required): The type of the resource to add the role to (either `"organization"`, `"location"`, or `"robot"`). Must match the type of the `resource_id`'s resource.
- `resource_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the resource the role applies to (the ID of either an {{< glossary_tooltip term_id="organization" text="organization" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="machine" text="machine" >}}.).

**Returns:**

- None.

**Raises:**

- (GRPCError): If either an invalid identity ID, role ID, resource type, or resource ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.add_role(
    org_id="org-id",
    identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    role="owner",
    resource_type="location",
    resource_id="111ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.add_role).

{{% /tab %}}
{{< /tabs >}}

### RemoveRole

Remove a role under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization the role exists in. You can obtain your organization ID from the Viam app’s organization settings page.
- `identity_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the entity the role belongs to (for example, a user ID).
- `role` (Literal[owner] | Literal[operator]) (required): The role to remove.
- `resource_type` (Literal[organization] | Literal[location] | Literal[robot]) (required): Type of the resource the role is being removed from. Must match resource_id.
- `resource_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the resource the role applies to (that is, either an organization, location, or robot ID).

**Returns:**

- None.

**Raises:**

- (GRPCError): If either an invalid identity ID, role ID, resource type, or resource ID or is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await cloud.remove_role(
    org_id="org-id",
    identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    role="owner",
    resource_type="location",
    resource_id="111ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.remove_role).

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
    org_id="org-id",
    resource_ids=["1a123456-x1yz-0ab0-a12xyzabc"])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_authorizations).

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
                                     resource_id="organization-identifier123",
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

For more information about managing permissions, see [Role-Based Access Control](/cloud/rbac/#permissions).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.check_permissions).

{{% /tab %}}
{{< /tabs >}}

### CreateModule

Create a {{< glossary_tooltip term_id="module" text="module" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to create the module under. You can obtain your organization ID from the Viam app’s organization settings page.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the module. Must be unique within your organization.

**Returns:**

- (Tuple[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing the ID [0] of the new module and its URL [1].

**Raises:**

- (GRPCError): If an invalid name (for example, “”) is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
new_module = await cloud.create_module(org_id="org-id", name="cool_new_hoverboard_module")
print("Module ID:", new_module[0])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_module).

{{% /tab %}}
{{< /tabs >}}

### UpdateModule

Update the documentation URL, description, models, entrypoint, and/or the visibility of a {{< glossary_tooltip term_id="module" text="module" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `module_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the module being updated, containing module name (for example, “my-module”) or namespace and module name (for example, “my-org:my-module”).
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
url_of_my_module = await cloud.update_module(
    module_id="my-group:cool_new_hoverboard_module",
    url="https://docsformymodule.viam.com",
    description="A base to support hoverboards.",
    entrypoint="exec")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_module).

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

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ID of uploaded file.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
file_id = await cloud.upload_module_file(file=b"<file>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.upload_module_file).

{{% /tab %}}
{{< /tabs >}}

### GetModule

Get a {{< glossary_tooltip term_id="module" text="module" >}} by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `module_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of the module being retrieved, containing module name or namespace and module name.

**Returns:**

- ([viam.proto.app.Module](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Module)): The module.

**Raises:**

- (GRPCError): If an invalid module ID is passed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
the_module = await cloud.get_module(module_id="my-cool-modular-base")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_module).

{{% /tab %}}
{{< /tabs >}}

### ListModules

List the {{< glossary_tooltip term_id="module" text="modules" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list modules for. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- ([List[viam.proto.app.Module]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Module)): The list of modules.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
modules_list = await cloud.list_modules("org-id")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_modules).

{{% /tab %}}
{{< /tabs >}}

### CreateKey

Create a new [API key](/cloud/rbac/#api-keys).

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
resource_id="your-robot-id123"
)

api_key, api_key_id = cloud.create_key([auth], "my_key")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key).

{{% /tab %}}
{{< /tabs >}}

### ListKeys

List all keys for the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The ID of the organization to list API keys for. You can obtain your organization ID from the Viam app’s organization settings page.

**Returns:**

- ([List[viam.proto.app.APIKeyWithAuthorizations]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.APIKeyWithAuthorizations)): The existing API keys and authorizations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
keys = await cloud.list_keys()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_keys).

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
{{< /tabs >}}
