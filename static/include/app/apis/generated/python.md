### ListOrganizations

List the organization(s) the user is an authorized owner of.

**Parameters:**


**Returns:**

- [(List[viam.proto.app.Organization])](INSERT RETURN TYPE LINK): The list of organizations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organizations).

```python
org_list = await cloud.list_organizations()
```

### GetOrganization

Return details about the requested organization.

**Parameters:**

- `org_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the organization to query. If None, defaults to the
currently-authed org.

**Returns:**

- [(viam.proto.app.Organization)](INSERT RETURN TYPE LINK): The requested organization.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization).

### GetOrganizationNamespaceAvailability

Check the availability of an organization namespace.

**Parameters:**

- `public_namespace` [(str)](<INSERT PARAM TYPE LINK>): Organization namespace to check. Namespaces can only contain lowercase lowercase alphanumeric and dash
characters.

**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): True if the provided namespace is available.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_namespace_availability).

```python
available = await cloud.get_organization_namespace_availability(
    public_namespace="my-cool-organization")
```

### UpdateOrganization

Updates organization details.

**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional. If provided, update’s the org’s CRM ID.
- `public_namespace` [(str)](<INSERT PARAM TYPE LINK>): Optional. If provided, update’s the org’s CRM ID.
- `region` [(str)](<INSERT PARAM TYPE LINK>): Optional. If provided, update’s the org’s CRM ID.
- `cid` [(str)](<INSERT PARAM TYPE LINK>): Optional. If provided, update’s the org’s CRM ID.

**Returns:**

- [(viam.proto.app.Organization)](INSERT RETURN TYPE LINK): The updated organization.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization).

### ListOrganizationMembers

List the members and invites of the currently authed-to organization.

**Parameters:**


**Returns:**

- [(Tuple[List[viam.proto.app.OrganizationMember], List[viam.proto.app.OrganizationInvite]])](INSERT RETURN TYPE LINK): A tuple containing two lists; the first
[0] of organization members, and the second [1] of organization invites.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

```python
member_list, invite_list = await cloud.list_organization_members()
```

### UpdateOrganizationInviteAuthorizations

Update the authorizations attached to an organization invite that has already been created.

**Parameters:**

- `email` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional. Optional list of authorizations to remove from the invite.
- `add_authorizations` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional. Optional list of authorizations to remove from the invite.
- `remove_authorizations` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional. Optional list of authorizations to remove from the invite.

**Returns:**

- [(viam.proto.app.OrganizationInvite)](INSERT RETURN TYPE LINK): The updated invite.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization_invite_authorizations).

```python
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
    email="notarealemail@viam.com",
    add_authorizations =[authorization_to_add]
)
```

### DeleteOrganizationMember

Remove a member from the organization.

**Parameters:**

- `user_id` [(str)](<INSERT PARAM TYPE LINK>): The ID of the user to remove.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_member).

```python
member_list, invite_list = await cloud.list_organization_members()
first_user_id = member_list[0].user_id

await cloud.delete_organization_member(first_user_id)
```

### DeleteOrganizationInvite

Deletes a pending organization invite.

**Parameters:**

- `email` [(str)](<INSERT PARAM TYPE LINK>): The email address the pending invite was sent to.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_invite).

```python
await cloud.delete_organization_invite("youremail@email.com")
```

### ResendOrganizationInvite

Re-sends a pending organization invite email.

**Parameters:**

- `email` [(str)](<INSERT PARAM TYPE LINK>): The email address associated with the invite.

**Returns:**

- [(viam.proto.app.OrganizationInvite)](INSERT RETURN TYPE LINK)

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.resend_organization_invite).

```python
await cloud.resend_organization_invite("youremail@email.com")
```

### CreateLocation

Create and name a location under the currently authed-to organization and the specified parent location.

**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional. Optional parent location to put the location under. Defaults to a root-level location if no
location ID is provided.
- `parent_location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. Optional parent location to put the location under. Defaults to a root-level location if no
location ID is provided.

**Returns:**

- [(viam.proto.app.Location)](INSERT RETURN TYPE LINK): The newly created location.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location).

```python
my_new_location = await cloud.create_location(name="Robotville",
                                              parent_location_id="111ab12345")
```

### GetLocation

Get a location.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location to get. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

- [(viam.proto.app.Location)](INSERT RETURN TYPE LINK): The location.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_location).

```python
location = await cloud.get_location(location_id="123ab12345")
```

### UpdateLocation

Change the name of a location and/or assign it a new parent location.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. Optional ID of new parent location to move the location under. Defaults to the empty string
“” (i.e., no new parent location is assigned).
- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional. Optional ID of new parent location to move the location under. Defaults to the empty string
“” (i.e., no new parent location is assigned).
- `parent_location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. Optional ID of new parent location to move the location under. Defaults to the empty string
“” (i.e., no new parent location is assigned).

**Returns:**

- [(viam.proto.app.Location)](INSERT RETURN TYPE LINK): The newly updated location.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_location).

```python
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

### DeleteLocation

Delete a location.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the location to delete. Must be specified.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location).

```python
await cloud.delete_location(location_id="abc12abcde")
```

### ListLocations

Get a list of all locations under the currently authed-to organization.

**Parameters:**


**Returns:**

- [(List[viam.proto.app.Location])](INSERT RETURN TYPE LINK): The list of locations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_locations).

```python
locations = await cloud.list_locations()
```

### LocationAuth

Get a location’s LocationAuth (location secret(s)).

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location to retrieve LocationAuth from. Defaults to the location ID provided at AppClient
instantiation.

**Returns:**

- [(viam.proto.app.LocationAuth)](INSERT RETURN TYPE LINK): The LocationAuth containing location secrets.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.location_auth).

```python
loc_auth = await cloud.location_auth(location_id="123xy12345")
```

### CreateLocationSecret

Create a new location secret.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location to generate a new secret for. Defaults to the location ID provided at
AppClient instantiation.

**Returns:**

- [(viam.proto.app.LocationAuth)](INSERT RETURN TYPE LINK): The specified location’s LocationAuth containing the newly created secret.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location_secret).

```python
new_loc_auth = await cloud.create_location_secret()
```

### DeleteLocationSecret

Delete a location secret.

**Parameters:**

- `secret_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location to delete secret from. Defaults to the location ID provided at AppClient instantiation.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location to delete secret from. Defaults to the location ID provided at AppClient instantiation.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location_secret).

```python
await cloud.delete_location_secret(
    secret_id="abcd123-456-7890ab-cxyz98-989898xyzxyz")
```

### GetRobot

Get a robot.

**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot to get.

**Returns:**

- [(viam.proto.app.Robot)](INSERT RETURN TYPE LINK): The robot.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot).

```python
robot = await cloud.get_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

### GetRobotParts

Get a list of all the parts under a specific robot.

**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot to get parts from.

**Returns:**

- [(List[RobotPart])](INSERT RETURN TYPE LINK): The list of robot parts.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_parts).

```python
list_of_parts = await cloud.get_robot_parts(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

### GetRobotPart

Get a robot part.

**Parameters:**

- `robot_part_id` [(int)](<INSERT PARAM TYPE LINK>): Size (in number of spaces) of indent when writing config to dest. Defaults to 4.
- `dest` [(int)](<INSERT PARAM TYPE LINK>): Size (in number of spaces) of indent when writing config to dest. Defaults to 4.
- `indent` [(int)](<INSERT PARAM TYPE LINK>): Size (in number of spaces) of indent when writing config to dest. Defaults to 4.

**Returns:**

- [(RobotPart)](INSERT RETURN TYPE LINK): The robot part.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part).

```python
my_robot_part = await cloud.get_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### GetRobotPartLogs

Get the logs associated with a robot part.

**Parameters:**

- `robot_part_id` [(int)](<INSERT PARAM TYPE LINK>): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first
num_log_entries logs will be returned, whichever comes first.
- `filter` [(int)](<INSERT PARAM TYPE LINK>): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first
num_log_entries logs will be returned, whichever comes first.
- `dest` [(int)](<INSERT PARAM TYPE LINK>): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first
num_log_entries logs will be returned, whichever comes first.
- `errors_only` [(int)](<INSERT PARAM TYPE LINK>): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first
num_log_entries logs will be returned, whichever comes first.
- `num_log_entries` [(int)](<INSERT PARAM TYPE LINK>): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first
num_log_entries logs will be returned, whichever comes first.

**Returns:**

- [(List[LogEntry])](INSERT RETURN TYPE LINK): The list of log entries.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_logs).

```python
part_logs = await cloud.get_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22", num_log_entries=20)
```

### TailRobotPartLogs

Get an asynchronous iterator that receives live robot part logs.

**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. Only include logs with messages that contain the string filter. Defaults to empty string “” (i.e., no
filter).
- `errors_only` [(str)](<INSERT PARAM TYPE LINK>): Optional. Only include logs with messages that contain the string filter. Defaults to empty string “” (i.e., no
filter).
- `filter` [(str)](<INSERT PARAM TYPE LINK>): Optional. Only include logs with messages that contain the string filter. Defaults to empty string “” (i.e., no
filter).

**Returns:**

- [(viam.app._logs._LogsStream[List[LogEntry]])](INSERT RETURN TYPE LINK): The asynchronous iterator receiving live robot part logs.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.tail_robot_part_logs).

```python
logs_stream = await cloud.tail_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### GetRobotPartHistory

Get a list containing the history of a robot part.

**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot part to retrieve history from.

**Returns:**

- [(List[RobotPartHistoryEntry])](INSERT RETURN TYPE LINK): The list of the robot part’s history.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_history).

```python
part_history = await cloud.get_robot_part_history(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### UpdateRobotPart

Change the name and assign an optional new configuration to a robot part.

**Parameters:**

- `robot_part_id` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional. Optional new config represented as a dictionary to be updated on the robot part. The robot
part’s config will remain as is (no change) if one isn’t passed.
- `name` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional. Optional new config represented as a dictionary to be updated on the robot part. The robot
part’s config will remain as is (no change) if one isn’t passed.
- `robot_config` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional. Optional new config represented as a dictionary to be updated on the robot part. The robot
part’s config will remain as is (no change) if one isn’t passed.

**Returns:**

- [(RobotPart)](INSERT RETURN TYPE LINK): The newly updated robot part.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot_part).

```python
my_robot_part = await cloud.update_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### NewRobotPart

Create a new robot part.

**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>): Name of the new part.
- `part_name` [(str)](<INSERT PARAM TYPE LINK>): Name of the new part.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The new robot part’s ID.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot_part).

```python
new_part_id = await cloud.new_robot_part(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc", part_name="myNewSubPart")
```

### DeleteRobotPart

Delete the specified robot part.

**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot part to delete. Must be specified.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part).

```python
await cloud.delete_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### MarkPartAsMain

Mark a robot part as the main part of a robot.

**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot part to mark as main.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_as_main).

```python
await cloud.mark_part_as_main(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### MarkPartForRestart

Mark the specified robot part for restart.

**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot part to mark for restart.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_for_restart).

```python
await cloud.mark_part_for_restart(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### CreateRobotPartSecret

Create a robot part secret.

**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot part to create a secret for.

**Returns:**

- [(RobotPart)](INSERT RETURN TYPE LINK): The robot part the new secret was generated for.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_robot_part_secret).

```python
part_with_new_secret = await cloud.create_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### DeleteRobotPartSecret

Delete a robot part secret.

**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the secret to delete.
- `secret_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the secret to delete.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part_secret).

```python
await cloud.delete_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22",
    secret_id="123xyz12-abcd-4321-12ab-12xy1xyz12xy")
```

### ListRobots

Get a list of all robots under the specified location.

**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location to retrieve the robots from. Defaults to the location ID provided at
AppClient instantiation.

**Returns:**

- [(List[viam.proto.app.Robot])](INSERT RETURN TYPE LINK): The list of robots.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_robots).

```python
list_of_machines = await cloud.list_robots(location_id="123ab12345")
```

### NewRobot

Create a new robot.

**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location under which to create the robot. Defaults to the current authorized location.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location under which to create the robot. Defaults to the current authorized location.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The new robot’s ID.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot).

```python
new_machine_id = await cloud.new_robot(name="beepboop")
```

### UpdateRobot

Change the name of an existing robot.

**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location under which the robot exists. Defaults to the location ID provided at
AppClient instantiation
- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location under which the robot exists. Defaults to the location ID provided at
AppClient instantiation
- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional. ID of the location under which the robot exists. Defaults to the location ID provided at
AppClient instantiation

**Returns:**

- [(viam.proto.app.Robot)](INSERT RETURN TYPE LINK): The newly updated robot.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot).

```python
updated_robot = await cloud.update_robot(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc",
    name="Orange-Robot")
```

### DeleteRobot

Delete the specified robot.

**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the robot to delete.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot).

```python
await cloud.delete_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

### ListFragments

Get a list of fragments under the currently authed-to organization.

**Parameters:**

- `show_public` [(bool)](<INSERT PARAM TYPE LINK>): Optional boolean specifying whether or not to only show public fragments. If True, only public fragments will
return. If False, only private fragments will return. Defaults to True.

**Returns:**

- [(List[Fragment])](INSERT RETURN TYPE LINK): The list of fragments.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_fragments).

```python
fragments_list = await cloud.list_fragments(show_public=False)
```

### GetFragment

Get a fragment.

**Parameters:**

- `fragment_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the fragment to get.

**Returns:**

- [(Fragment)](INSERT RETURN TYPE LINK): The fragment.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_fragment).

```python
# Get a fragment and print its name and when it was created.
the_fragment = await cloud.get_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567")
print("Name: ", the_fragment.name, "\nCreated on: ", the_fragment.created_on)
```

### CreateFragment

Create a new private fragment.

**Parameters:**

- `name` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional. Optional Dictionary representation of new config to assign to specified fragment. Can be
assigned by updating the fragment.
- `config` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional. Optional Dictionary representation of new config to assign to specified fragment. Can be
assigned by updating the fragment.

**Returns:**

- [(Fragment)](INSERT RETURN TYPE LINK): The newly created fragment.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_fragment).

```python
new_fragment = await cloud.create_fragment(
    name="cool_smart_machine_to_configure_several_of")
```

### UpdateFragment

Update a fragment name AND its config and/or visibility.

**Parameters:**

- `fragment_id` [(bool)](<INSERT PARAM TYPE LINK>): Optional. Boolean specifying whether the fragment is public. Not passing this parameter will leave the fragment’s
visibility unchanged. A fragment is private by default when created.
- `name` [(bool)](<INSERT PARAM TYPE LINK>): Optional. Boolean specifying whether the fragment is public. Not passing this parameter will leave the fragment’s
visibility unchanged. A fragment is private by default when created.
- `config` [(bool)](<INSERT PARAM TYPE LINK>): Optional. Boolean specifying whether the fragment is public. Not passing this parameter will leave the fragment’s
visibility unchanged. A fragment is private by default when created.
- `public` [(bool)](<INSERT PARAM TYPE LINK>): Optional. Boolean specifying whether the fragment is public. Not passing this parameter will leave the fragment’s
visibility unchanged. A fragment is private by default when created.

**Returns:**

- [(Fragment)](INSERT RETURN TYPE LINK): The newly updated fragment.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_fragment).

```python
updated_fragment = await cloud.update_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567",
    name="better_name")
```

### DeleteFragment

Delete a fragment.

**Parameters:**

- `fragment_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the fragment to delete.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_fragment).

```python
await cloud.delete_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567")
```

### AddRole

Add a role under the currently authed-to organization.

**Parameters:**

- `identity_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).
- `role` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).
- `resource_type` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).
- `resource_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.add_role).

```python
await cloud.add_role(
    identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    role="owner",
    resource_type="location",
    resource_id="111ab12345")
```

### RemoveRole

Remove a role under the currently authed-to organization.

**Parameters:**

- `identity_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).
- `role` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).
- `resource_type` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).
- `resource_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the resource the role applies to (i.e., either an organization, location, or robot ID).

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.remove_role).

```python
await cloud.remove_role(
    identity_id="abc01234-0123-4567-ab12-a11a00a2aa22",
    role="owner",
    resource_type="location",
    resource_id="111ab12345")
```

### ListAuthorizations

List all authorizations under a specific resource (or resources) within the currently authed-to organization. If no resource IDs are provided, all resource authorizations within the organizations are returned.

**Parameters:**

- `resource_ids` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. IDs of the resources to retrieve authorizations from.
If None, defaults to all resources.

**Returns:**

- [(List[viam.proto.app.Authorization])](INSERT RETURN TYPE LINK): The list of authorizations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_authorizations).

```python
list_of_auths = await cloud.list_authorizations(
    resource_ids=["1a123456-x1yz-0ab0-a12xyzabc"])
```

### CheckPermissions

Checks validity of a list of permissions.

**Parameters:**

- `permissions` [(List[viam.proto.app.AuthorizedPermissions])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.AuthorizedPermissions): the permissions to validate
(e.g., “read_organization”, “control_robot”)

**Returns:**

- [(List[viam.proto.app.AuthorizedPermissions])](INSERT RETURN TYPE LINK): The permissions argument, with invalid permissions filtered out.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.check_permissions).

```python
from viam.proto.app import AuthorizedPermissions

# Check whether the entity you're currently authenticated to has permission to control and/or
# read logs from robots in the "organization-identifier123" org
permissions = [AuthorizedPermissions(resource_type="organization",
                                     resource_id="organization-identifier123",
                                     permissions=["control_robot",
                                                  "read_robot_logs"])]

filtered_permissions = await cloud.check_permissions(permissions)
```

### CreateModule

Create a module under the currently authed-to organization.

**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): The name of the module. Must be unique within your organization.

**Returns:**

- [(Tuple[str, str])](INSERT RETURN TYPE LINK): A tuple containing the ID [0] of the new module and its URL [1].

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_module).

```python
new_module = await cloud.create_module(name="cool_new_hoverboard_module")
print("Module ID:", new_module[0])
```

### UpdateModule

Update the documentation URL, description, models, entrypoint, and/or the visibility of a module.

**Parameters:**

- `module_id` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model): The visibility that should be set for the module. Defaults to False (private).
- `url` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model): The visibility that should be set for the module. Defaults to False (private).
- `description` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model): The visibility that should be set for the module. Defaults to False (private).
- `models` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model): The visibility that should be set for the module. Defaults to False (private).
- `entrypoint` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model): The visibility that should be set for the module. Defaults to False (private).
- `organization_id` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model): The visibility that should be set for the module. Defaults to False (private).
- `public` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model): The visibility that should be set for the module. Defaults to False (private).

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The URL of the newly updated module.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_module).

```python
url_of_my_module = await cloud.update_module(
    module_id="my-group:cool_new_hoverboard_module",
    url="https://docsformymodule.viam.com",
    description="A base to support hoverboards.",
    entrypoint="exec")
```

### UploadModuleFile

Upload a module file

**Parameters:**

- `module_file_info` [(bytes)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.ModuleFileInfo): Bytes of file to upload.
- `file` [(bytes)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.ModuleFileInfo): Bytes of file to upload.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ID of uploaded file.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.upload_module_file).

```python
file_id = await cloud.upload_module_file(file=b"<file>")
```

### GetModule

Get a module.

**Parameters:**

- `module_id` [(str)](<INSERT PARAM TYPE LINK>): ID of the module being retrieved, containing module name or namespace and module name.

**Returns:**

- [(viam.proto.app.Module)](INSERT RETURN TYPE LINK): The module.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_module).

```python
the_module = await cloud.get_module(module_id="my-cool-modular-base")
```

### ListModules

List the modules under the currently authed-to organization.

**Parameters:**


**Returns:**

- [(List[viam.proto.app.Module])](INSERT RETURN TYPE LINK): The list of modules.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_modules).

```python
modules_list = await cloud.list_modules()
```

### CreateKey

Creates a new [API key](/fleet/cli/#authenticate).

**Parameters:**

- `authorizations` [(str)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.APIKeyAuthorization): Optional. A name for the key. If None, defaults to the current timestamp.
- `name` [(str)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.APIKeyAuthorization): Optional. A name for the key. If None, defaults to the current timestamp.

**Returns:**

- [(Tuple[str, str])](INSERT RETURN TYPE LINK): The api key and api key ID.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key).

```python
from viam.app.app_client import APIKeyAuthorization

auth = APIKeyAuthorization(
role="owner",
resource_type="robot",
resource_id="your-robot-id123"
)

api_key, api_key_id = cloud.create_key([auth], "my_key")
```

### CreateKeyFromExistingKeyAuthorizations

Creates a new [API key](/fleet/cli/#authenticate) with an existing key’s authorizations

**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>): the ID of the API key to duplication authorizations from

**Returns:**

- [(Tuple[str, str])](INSERT RETURN TYPE LINK): The API key and API key id

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key_from_existing_key_authorizations).

```python
api_key, api_key_id = cloud.create_key_from_existing_key_authorizations(
    id="INSERT YOUR API KEY ID")
```

### ListKeys

Lists all keys for the currently-authed-to org.

**Parameters:**


**Returns:**

- [(List[viam.proto.app.APIKeyWithAuthorizations])](INSERT RETURN TYPE LINK): The existing API keys and authorizations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_keys).

```python
keys = cloud.list_keys()
```

### TabularDataByFilter

Filter and download tabular data.

**Parameters:**

- `filter` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Optional filepath for writing retrieved data.
- `dest` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Optional filepath for writing retrieved data.

**Returns:**

- [(List[TabularData])](INSERT RETURN TYPE LINK): The tabular data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
tabular_data = await data_client.tabular_data_by_filter(my_filter)
```

### BinaryDataByFilter

Filter and download binary data.

**Parameters:**

- `filter` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Number of binary data to return. Passing 0 returns all binary data matching the filter no matter.
Defaults to 100 if no binary data is requested, otherwise 10. All binary data or the first num_files will be returned,
whichever comes first.
- `dest` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Number of binary data to return. Passing 0 returns all binary data matching the filter no matter.
Defaults to 100 if no binary data is requested, otherwise 10. All binary data or the first num_files will be returned,
whichever comes first.
- `include_file_data` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Number of binary data to return. Passing 0 returns all binary data matching the filter no matter.
Defaults to 100 if no binary data is requested, otherwise 10. All binary data or the first num_files will be returned,
whichever comes first.
- `num_files` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Number of binary data to return. Passing 0 returns all binary data matching the filter no matter.
Defaults to 100 if no binary data is requested, otherwise 10. All binary data or the first num_files will be returned,
whichever comes first.

**Returns:**

- [(List[BinaryData])](INSERT RETURN TYPE LINK): The binary data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_type="camera")
binary_data = await data_client.binary_data_by_filter(my_filter)
```

### BinaryDataByIDs

Filter and download binary data.

**Parameters:**

- `binary_ids` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Optional. Optional filepath for writing retrieved data.
- `dest` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Optional. Optional filepath for writing retrieved data.

**Returns:**

- [(List[BinaryData])](INSERT RETURN TYPE LINK): The binary data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_ids).

```python
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
)

my_ids = []

for obj in binary_metadata:
    my_ids.append(
        BinaryID(
            file_id=obj.metadata.id,
            organization_id=obj.metadata.capture_metadata.organization_id,
            location_id=obj.metadata.capture_metadata.location_id
        )
    )

binary_data = await data_client.binary_data_by_ids(my_ids)
```

### DeleteTabularData

Delete tabular data older than a specified number of days.

**Parameters:**

- `organization_id` [(int)](<INSERT PARAM TYPE LINK>): Delete data that was captured up to this many days ago. For example if delete_older_than_days
is 10, this deletes any data that was captured up to 10 days ago. If it is 0, all existing data is deleted.
- `delete_older_than_days` [(int)](<INSERT PARAM TYPE LINK>): Delete data that was captured up to this many days ago. For example if delete_older_than_days
is 10, this deletes any data that was captured up to 10 days ago. If it is 0, all existing data is deleted.

**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of items deleted.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_tabular_data).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
days_of_data_to_delete = 10
tabular_data = await data_client.delete_tabular_data(
    org_id="a12b3c4e-1234-1abc-ab1c-ab1c2d345abc", days_of_data_to_delete)
```

### DeleteBinaryDataByFilter

Filter and delete binary data.

**Parameters:**

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Optional Filter specifying binary data to delete. Passing an empty Filter will lead to
all data being deleted. Exercise caution when using this option.

**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of items deleted.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
res = await data_client.delete_binary_data_by_filter(my_filter)
```

### DeleteBinaryDataByIDs

Filter and delete binary data.

**Parameters:**

- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): BinaryID objects specifying the data to be deleted. Must be non-empty.

**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of items deleted.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_ids).

```python
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
)

my_ids = []

for obj in binary_metadata:
    my_ids.append(
        BinaryID(
            file_id=obj.metadata.id,
            organization_id=obj.metadata.capture_metadata.organization_id,
            location_id=obj.metadata.capture_metadata.location_id
        )
    )

binary_data = await data_client.delete_binary_data_by_ids(my_ids)
```

### AddTagsToBinaryDataByIDs

Add tags to binary data.

**Parameters:**

- `tags` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): List of BinaryID objects specifying binary data to tag. Must be non-empty.
- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): List of BinaryID objects specifying binary data to tag. Must be non-empty.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_ids).

```python
from viam.proto.app.data import BinaryID

tags = ["tag1", "tag2"]

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
)

my_ids = []

for obj in binary_metadata:
    my_ids.append(
        BinaryID(
            file_id=obj.metadata.id,
            organization_id=obj.metadata.capture_metadata.organization_id,
            location_id=obj.metadata.capture_metadata.location_id
        )
    )

binary_data = await data_client.add_tags_to_binary_data_by_ids(tags, my_ids)
```

### AddTagsToBinaryDataByFilter

Add tags to binary data.

**Parameters:**

- `tags` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Filter specifying binary data to tag. If no Filter is provided, all data will be
tagged.
- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Filter specifying binary data to tag. If no Filter is provided, all data will be
tagged.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_tags_to_binary_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = ["tag1", "tag2"]
res = await data_client.add_tags_to_binary_data_by_filter(tags, my_filter)
```

### RemoveTagsFromBinaryDataByIDs

Remove tags from binary.

**Parameters:**

- `tags` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): List of BinaryID objects specifying binary data to untag. Must be non-empty.
- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): List of BinaryID objects specifying binary data to untag. Must be non-empty.

**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of tags removed.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_tags_from_binary_data_by_ids).

```python
from viam.proto.app.data import BinaryID

tags = ["tag1", "tag2"]

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
)

my_ids = []

for obj in binary_metadata:
    my_ids.append(
        BinaryID(
            file_id=obj.metadata.id,
            organization_id=obj.metadata.capture_metadata.organization_id,
            location_id=obj.metadata.capture_metadata.location_id
        )
    )

binary_data = await data_client.remove_tags_from_binary_data_by_ids(
    tags, my_ids)
```

### RemoveTagsFromBinaryDataByFilter

Remove tags from binary data.

**Parameters:**

- `tags` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Filter specifying binary data to untag. If no Filter is provided, all data will be
untagged.
- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Filter specifying binary data to untag. If no Filter is provided, all data will be
untagged.

**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The number of tags removed.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_tags_from_binary_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = ["tag1", "tag2"]
res = await data_client.remove_tags_from_binary_data_by_filter(tags, my_filter)
```

### TagsByFilter

Get a list of tags using a filter.

**Parameters:**

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Filter specifying data to retrieve from. If no Filter is provided, all data tags will
return.

**Returns:**

- [(List[str])](INSERT RETURN TYPE LINK): The list of tags.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tags_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = await data_client.tags_by_filter(my_filter)
```

### AddBoundingBoxToImageByID

Add a bounding box to an image.

**Parameters:**

- `binary_id` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Max Y value of the bounding box normalized from 0 to 1.
- `label` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Max Y value of the bounding box normalized from 0 to 1.
- `x_min_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Max Y value of the bounding box normalized from 0 to 1.
- `y_min_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Max Y value of the bounding box normalized from 0 to 1.
- `x_max_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Max Y value of the bounding box normalized from 0 to 1.
- `y_max_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Max Y value of the bounding box normalized from 0 to 1.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The bounding box ID

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_bounding_box_to_image_by_id).

```python
from viam.proto.app.data import BinaryID

MY_BINARY_ID = BinaryID(
    file_id=your-file_id,
    organization_id=your-org-id,
    location_id=your-location-id
)

bbox_label = await data_client.add_bounding_box_to_image_by_id(
    binary_id=MY_BINARY_ID,
    label="label",
    x_min_normalized=0,
    y_min_normalized=.1,
    x_max_normalized=.2,
    y_max_normalized=.3
)

print(bbox_label)
```

### RemoveBoundingBoxFromImageByID

Removes a bounding box from an image.

**Parameters:**

- `bbox_id` [(viam.proto.app.data.BinaryID)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): The ID of the bounding box to remove.
- `binary_id` [(viam.proto.app.data.BinaryID)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): The ID of the bounding box to remove.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_bounding_box_from_image_by_id).

```python
from viam.proto.app.data import BinaryID

MY_BINARY_ID = BinaryID(
    file_id=your-file_id,
    organization_id=your-org-id,
    location_id=your-location-id
)

await data_client.remove_bounding_box_from_image_by_id(
binary_id=MY_BINARY_ID,
bbox_id="your-bounding-box-id-to-delete"
)
```

### BoundingBoxLabelsByFilter

Get a list of bounding box labels using a Filter.

**Parameters:**

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional. Filter specifying data to retrieve from. If no Filter is provided, all labels will
return.

**Returns:**

- [(List[str])](INSERT RETURN TYPE LINK): The list of bounding box labels.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.bounding_box_labels_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
bounding_box_labels = await data_client.bounding_box_labels_by_filter(
    my_filter)
```

### GetDatabaseConnection

Get a connection to access a MongoDB Atlas Data federation instance.

**Parameters:**

- `organization_id` [(str)](<INSERT PARAM TYPE LINK>): Organization to retrieve the connection for.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The hostname of the federated database.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_database_connection).

```python
data_client.get_database_connection(org_id="a12b3c4e-1234-1abc-ab1c-ab1c2d345abc")
```

### CreateDataset

Create a new dataset.

**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): The ID of the organization where the dataset is being created.
- `organization_id` [(str)](<INSERT PARAM TYPE LINK>): The ID of the organization where the dataset is being created.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The dataset ID of the created dataset.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.create_dataset).

```python
name = await data_client.create_dataset(
    name="<dataset-name>",
    organization_id="<your-org-id>"
)
print(name)
```

### ListDatasetsByIDs

Get a list of datasets using their IDs.

**Parameters:**

- `ids` [(List[str])](<INSERT PARAM TYPE LINK>): The IDs of the datasets being called for.

**Returns:**

- [(Sequence[viam.proto.app.dataset.Dataset])](INSERT RETURN TYPE LINK): The list of datasets.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_dataset_by_ids).

```python
datasets = await data_client.list_dataset_by_ids(
    ids=["abcd-1234xyz-8765z-123abc"]
)
print(datasets)
```

### ListDatasetsByOrganizationID

Get the datasets in an organization.

**Parameters:**

- `organization_id` [(str)](<INSERT PARAM TYPE LINK>): The ID of the organization.

**Returns:**

- [(Sequence[viam.proto.app.dataset.Dataset])](INSERT RETURN TYPE LINK): The list of datasets in the organization.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.list_datasets_by_organization_id).

```python
datasets = await data_client.list_dataset_by_ids(
    ids=["abcd-1234xyz-8765z-123abc"]
)
print(datasets)
```

### RenameDataset

Rename a dataset specified by the dataset ID.

**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>): The new name of the dataset.
- `name` [(str)](<INSERT PARAM TYPE LINK>): The new name of the dataset.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.rename_dataset).

```python
await data_client.rename_dataset(
    id="abcd-1234xyz-8765z-123abc",
    name="<dataset-name>"
)
```

### DeleteDataset

Delete a dataset.

**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>): The ID of the dataset.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_dataset).

```python
await data_client.delete_dataset(
    id="abcd-1234xyz-8765z-123abc"
)
```

### AddBinaryDataToDatasetByIDs

Add the BinaryData to the provided dataset.

**Parameters:**

- `binary_ids` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): The ID of the dataset to be added to.
- `dataset_id` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): The ID of the dataset to be added to.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.add_binary_data_to_dataset_by_ids).

```python
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
)

my_binary_ids = []

for obj in binary_metadata:
    my_binary_ids.append(
        BinaryID(
            file_id=obj.metadata.id,
            organization_id=obj.metadata.capture_metadata.organization_id,
            location_id=obj.metadata.capture_metadata.location_id
            )
        )

await data_client.add_binary_data_to_dataset_by_ids(
    binary_ids=my_binary_ids,
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

### RemoveBinaryDataFromDatasetByIDs

Remove the BinaryData from the provided dataset.

**Parameters:**

- `binary_ids` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): The ID of the dataset to be removed from.
- `dataset_id` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): The ID of the dataset to be removed from.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.remove_binary_data_from_dataset_by_ids).

```python
from viam.proto.app.data import BinaryID

binary_metadata = await data_client.binary_data_by_filter(
    include_file_data=False
)

my_binary_ids = []

for obj in binary_metadata:
    my_binary_ids.append(
        BinaryID(
            file_id=obj.metadata.id,
            organization_id=obj.metadata.capture_metadata.organization_id,
            location_id=obj.metadata.capture_metadata.location_id
        )
    )

await data_client.remove_binary_data_from_dataset_by_ids(
    binary_ids=my_binary_ids,
    dataset_id="abcd-1234xyz-8765z-123abc"
)
```

### BinaryDataCaptureUpload

Upload binary sensor data.

**Parameters:**

- `binary_data` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `part_id` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `component_type` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `component_name` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `method_name` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `file_extension` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `method_parameters` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `tags` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
- `data_request_times` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional. Optional tuple containing `datetime`s objects
denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): the file_id of the uploaded data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_capture_upload).

```python
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.binary_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='camera',
    component_name='my_camera',
    method_name='GetImages',
    method_parameters=None,
    tags=["tag_1", "tag_2"],
    data_request_times=[time_requested, time_received],
    file_extension=".jpg",
    binary_data=b"Encoded image bytes"
)
```

### TabularDataCaptureUpload

Upload tabular sensor data.

**Parameters:**

- `tabular_data` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.
- `part_id` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.
- `component_type` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.
- `component_name` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.
- `method_name` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.
- `method_parameters` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.
- `tags` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.
- `data_request_times` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tuples, each containing
datetime objects denoting the times this data was requested[0] by the robot and received[1] from the appropriate sensor.
Passing a list of tabular data and Timestamps with length n > 1 will result in n datapoints being uploaded, all tied to the
same metadata.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): the file_id of the uploaded data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_capture_upload).

```python
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.tabular_data_capture_upload(
    part_id="INSERT YOUR PART ID",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    tags=["tag_1", "tag_2"],
    data_request_times=[(time_requested, time_received)],
    tabular_data=[{'PowerPCT': 0, 'IsPowered': False}]
)
```

### StreamingDataCaptureUpload

Uploads the metadata and contents of streaming binary data.

**Parameters:**

- `data` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `part_id` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `file_ext` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `component_type` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `component_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `method_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `method_parameters` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `data_request_times` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): the file_id of the uploaded data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.streaming_data_capture_upload).

```python
time_requested = datetime(2023, 6, 5, 11)
time_received = datetime(2023, 6, 5, 11, 0, 3)

file_id = await data_client.streaming_data_capture_upload(
    data="byte-data-to-upload",
    part_id="INSERT YOUR PART ID",
    file_ext="png",
    component_type='motor',
    component_name='left_motor',
    method_name='IsPowered',
    data_request_times=[(time_requested, time_received)],
    tags=["tag_1", "tag_2"]
)
```

### FileUpload

Upload arbitrary file data.

**Parameters:**

- `part_id` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `data` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `component_type` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `component_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `method_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `file_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `method_parameters` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `file_extension` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ID of the new file.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload).

```python
file_id = await data_client.file_upload(
    data=b"Encoded image bytes",
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    file_name="your-file",
    file_extension=".txt"
)
```

### FileUploadFromPath

Upload arbitrary file data.

**Parameters:**

- `filepath` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `part_id` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `component_type` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `component_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `method_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `method_parameters` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>): Optional. Optional list of tags to allow for tag-based filtering when retrieving data.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ID of the new file.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.file_upload_from_path).

```python
file_id = await data_client.file_upload_from_path(
    part_id="INSERT YOUR PART ID",
    tags=["tag_1", "tag_2"],
    filepath="/Users/<your-username>/<your-directory>/<your-file.txt>"
)
```

### GetTrainingJob

Gets training job data.

**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>): id of the requested training job.

**Returns:**

- [(viam.proto.app.mltraining.TrainingJobMetadata)](INSERT RETURN TYPE LINK): training job data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.get_training_job).

```python
job_metadata = await ml_training_client.get_training_job(
    id="INSERT YOUR JOB ID")
```

### ListTrainingJobs

Returns training job data for all jobs within an org.

**Parameters:**

- `org_id` [(viam.proto.app.mltraining.TrainingStatus.ValueType)](<INSERT PARAM TYPE LINK>): Optional. status of training jobs to filter the list by.
If unspecified, all training jobs will be returned.
- `training_status` [(viam.proto.app.mltraining.TrainingStatus.ValueType)](<INSERT PARAM TYPE LINK>): Optional. status of training jobs to filter the list by.
If unspecified, all training jobs will be returned.

**Returns:**

- [(List[viam.proto.app.mltraining.TrainingJobMetadata])](INSERT RETURN TYPE LINK): a list of training job data.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.list_training_jobs).

```python
jobs_metadata = await ml_training_client.list_training_jobs(
    org_id="INSERT YOUR ORG ID")

first_job_id = jobs_metadata[1].id
```

### CancelTrainingJob

Cancels the specified training job.

**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>): the id of the job to be canceled.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.cancel_training_job).

```python
await ml_training_client.cancel_training_job(
    id="INSERT YOUR JOB ID")
```

