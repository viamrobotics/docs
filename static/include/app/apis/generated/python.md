### ListOrganizations

List the organization(s) the user is an authorized owner of.


**Parameters:**


**Returns:**

([List[viam.proto.app.Organization]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organizations).

```python
org_list = await cloud.list_organizations()
```

### GetOrganization

Return details about the requested organization.


**Parameters:**

- `org_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.Organization](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization).

### GetOrganizationNamespaceAvailability

Check the availability of an organization namespace.


**Parameters:**

- `public_namespace` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_namespace_availability).

```python
available = await cloud.get_organization_namespace_availability(
    public_namespace="my-cool-organization")
```

### UpdateOrganization

Updates organization details.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `public_namespace` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `region` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `cid` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.Organization](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization).

### ListOrganizationMembers

List the members and invites of the currently authed-to organization.


**Parameters:**


**Returns:**

([Tuple[List[viam.proto.app.OrganizationMember], List[viam.proto.app.OrganizationInvite]]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

```python
member_list, invite_list = await cloud.list_organization_members()
```

### UpdateOrganizationInviteAuthorizations

Update the authorizations attached to an organization invite that has already been created.


**Parameters:**

- `email` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional.
- `add_authorizations` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional.
- `remove_authorizations` [(List[viam.proto.app.Authorization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional.

**Returns:**

([viam.proto.app.OrganizationInvite](<INSERT RETURN TYPE LINK>)))
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

- `user_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_member).

```python
member_list, invite_list = await cloud.list_organization_members()
first_user_id = member_list[0].user_id

await cloud.delete_organization_member(first_user_id)
```

### DeleteOrganizationInvite

Deletes a pending organization invite.


**Parameters:**

- `email` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_invite).

```python
await cloud.delete_organization_invite("youremail@email.com")
```

### ResendOrganizationInvite

Re-sends a pending organization invite email.


**Parameters:**

- `email` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([viam.proto.app.OrganizationInvite](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.resend_organization_invite).

```python
await cloud.resend_organization_invite("youremail@email.com")
```

### CreateLocation

Create and name a location under the currently authed-to organization and the specified parent location.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `parent_location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.Location](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location).

```python
my_new_location = await cloud.create_location(name="Robotville",
                                              parent_location_id="111ab12345")
```

### GetLocation

Get a location.


**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.Location](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_location).

```python
location = await cloud.get_location(location_id="123ab12345")
```

### UpdateLocation

Change the name of a location and/or assign it a new parent location.


**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `parent_location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.Location](<INSERT RETURN TYPE LINK>)))
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

- `location_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location).

```python
await cloud.delete_location(location_id="abc12abcde")
```

### ListLocations

Get a list of all locations under the currently authed-to organization.


**Parameters:**


**Returns:**

([List[viam.proto.app.Location]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_locations).

```python
locations = await cloud.list_locations()
```

### LocationAuth

Get a location’s LocationAuth (location secret(s)).


**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.LocationAuth](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.location_auth).

```python
loc_auth = await cloud.location_auth(location_id="123xy12345")
```

### CreateLocationSecret

Create a new location secret.


**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.LocationAuth](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location_secret).

```python
new_loc_auth = await cloud.create_location_secret()
```

### DeleteLocationSecret

Delete a location secret.


**Parameters:**

- `secret_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location_secret).

```python
await cloud.delete_location_secret(
    secret_id="abcd123-456-7890ab-cxyz98-989898xyzxyz")
```

### GetRobot

Get a robot.


**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([viam.proto.app.Robot](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot).

```python
robot = await cloud.get_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

### GetRobotParts

Get a list of all the parts under a specific robot.


**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([List[RobotPart]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_parts).

```python
list_of_parts = await cloud.get_robot_parts(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

### GetRobotPart

Get a robot part.


**Parameters:**

- `robot_part_id` [(int)](<INSERT PARAM TYPE LINK>):
- `dest` [(int)](<INSERT PARAM TYPE LINK>):
- `indent` [(int)](<INSERT PARAM TYPE LINK>):

**Returns:**

([RobotPart](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part).

```python
my_robot_part = await cloud.get_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### GetRobotPartLogs

Get the logs associated with a robot part.


**Parameters:**

- `robot_part_id` [(int)](<INSERT PARAM TYPE LINK>):
- `filter` [(int)](<INSERT PARAM TYPE LINK>):
- `dest` [(int)](<INSERT PARAM TYPE LINK>):
- `errors_only` [(int)](<INSERT PARAM TYPE LINK>):
- `num_log_entries` [(int)](<INSERT PARAM TYPE LINK>):

**Returns:**

([List[LogEntry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_logs).

```python
part_logs = await cloud.get_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22", num_log_entries=20)
```

### TailRobotPartLogs

Get an asynchronous iterator that receives live robot part logs.


**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `errors_only` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `filter` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.app._logs._LogsStream[List[LogEntry]]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.tail_robot_part_logs).

```python
logs_stream = await cloud.tail_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### GetRobotPartHistory

Get a list containing the history of a robot part.


**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([List[RobotPartHistoryEntry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_history).

```python
part_history = await cloud.get_robot_part_history(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### UpdateRobotPart

Change the name and assign an optional new configuration to a robot part.


**Parameters:**

- `robot_part_id` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional.
- `name` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional.
- `robot_config` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([RobotPart](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot_part).

```python
my_robot_part = await cloud.update_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### NewRobotPart

Create a new robot part.


**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>):
- `part_name` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot_part).

```python
new_part_id = await cloud.new_robot_part(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc", part_name="myNewSubPart")
```

### DeleteRobotPart

Delete the specified robot part.


**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part).

```python
await cloud.delete_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### MarkPartAsMain

Mark a robot part as the main part of a robot.


**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_as_main).

```python
await cloud.mark_part_as_main(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### MarkPartForRestart

Mark the specified robot part for restart.


**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_for_restart).

```python
await cloud.mark_part_for_restart(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### CreateRobotPartSecret

Create a robot part secret.


**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([RobotPart](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_robot_part_secret).

```python
part_with_new_secret = await cloud.create_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

### DeleteRobotPartSecret

Delete a robot part secret.


**Parameters:**

- `robot_part_id` [(str)](<INSERT PARAM TYPE LINK>):
- `secret_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part_secret).

```python
await cloud.delete_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22",
    secret_id="123xyz12-abcd-4321-12ab-12xy1xyz12xy")
```

### ListRobots

Get a list of all robots under the specified location.


**Parameters:**

- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.app.Robot]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_robots).

```python
list_of_machines = await cloud.list_robots(location_id="123ab12345")
```

### NewRobot

Create a new robot.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot).

```python
new_machine_id = await cloud.new_robot(name="beepboop")
```

### UpdateRobot

Change the name of an existing robot.


**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `name` [(str)](<INSERT PARAM TYPE LINK>): Optional.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.app.Robot](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot).

```python
updated_robot = await cloud.update_robot(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc",
    name="Orange-Robot")
```

### DeleteRobot

Delete the specified robot.


**Parameters:**

- `robot_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot).

```python
await cloud.delete_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

### ListFragments

Get a list of fragments under the currently authed-to organization.


**Parameters:**

- `show_public` [(bool)](<INSERT PARAM TYPE LINK>):

**Returns:**

([List[Fragment]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_fragments).

```python
fragments_list = await cloud.list_fragments(show_public=False)
```

### GetFragment

Get a fragment.


**Parameters:**

- `fragment_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([Fragment](<INSERT RETURN TYPE LINK>)))
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

- `name` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional.
- `config` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Fragment](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_fragment).

```python
new_fragment = await cloud.create_fragment(
    name="cool_smart_machine_to_configure_several_of")
```

### UpdateFragment

Update a fragment name AND its config and/or visibility.


**Parameters:**

- `fragment_id` [(bool)](<INSERT PARAM TYPE LINK>): Optional.
- `name` [(bool)](<INSERT PARAM TYPE LINK>): Optional.
- `config` [(bool)](<INSERT PARAM TYPE LINK>): Optional.
- `public` [(bool)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Fragment](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_fragment).

```python
updated_fragment = await cloud.update_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567",
    name="better_name")
```

### DeleteFragment

Delete a fragment.


**Parameters:**

- `fragment_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_fragment).

```python
await cloud.delete_fragment(
    fragment_id="12a12ab1-1234-5678-abcd-abcd01234567")
```

### AddRole

Add a role under the currently authed-to organization.


**Parameters:**

- `identity_id` [(str)](<INSERT PARAM TYPE LINK>):
- `role` [(str)](<INSERT PARAM TYPE LINK>):
- `resource_type` [(str)](<INSERT PARAM TYPE LINK>):
- `resource_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


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

- `identity_id` [(str)](<INSERT PARAM TYPE LINK>):
- `role` [(str)](<INSERT PARAM TYPE LINK>):
- `resource_type` [(str)](<INSERT PARAM TYPE LINK>):
- `resource_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


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

- `resource_ids` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.app.Authorization]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_authorizations).

```python
list_of_auths = await cloud.list_authorizations(
    resource_ids=["1a123456-x1yz-0ab0-a12xyzabc"])
```

### CheckPermissions

Checks validity of a list of permissions.


**Parameters:**

- `permissions` [(List[viam.proto.app.AuthorizedPermissions])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.AuthorizedPermissions):

**Returns:**

([List[viam.proto.app.AuthorizedPermissions]](<INSERT RETURN TYPE LINK>)))
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

- `name` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([Tuple[str, str]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_module).

```python
new_module = await cloud.create_module(name="cool_new_hoverboard_module")
print("Module ID:", new_module[0])
```

### UpdateModule

Update the documentation URL, description, models, entrypoint, and/or the visibility of a module.


**Parameters:**

- `module_id` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model):
- `url` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model):
- `description` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model):
- `models` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model):
- `entrypoint` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model):
- `organization_id` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model):
- `public` [(bool)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model):

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `module_file_info` [(bytes)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.ModuleFileInfo):
- `file` [(bytes)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.ModuleFileInfo):

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.upload_module_file).

```python
file_id = await cloud.upload_module_file(file=b"<file>")
```

### GetModule

Get a module.


**Parameters:**

- `module_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([viam.proto.app.Module](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_module).

```python
the_module = await cloud.get_module(module_id="my-cool-modular-base")
```

### ListModules

List the modules under the currently authed-to organization.


**Parameters:**


**Returns:**

([List[viam.proto.app.Module]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_modules).

```python
modules_list = await cloud.list_modules()
```

### CreateKey

Creates a new [API key](/fleet/cli/#authenticate).


**Parameters:**

- `authorizations` [(str)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.APIKeyAuthorization): Optional.
- `name` [(str)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.APIKeyAuthorization): Optional.

**Returns:**

([Tuple[str, str]](<INSERT RETURN TYPE LINK>)))
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

- `id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([Tuple[str, str]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key_from_existing_key_authorizations).

```python
api_key, api_key_id = cloud.create_key_from_existing_key_authorizations(
    id="INSERT YOUR API KEY ID")
```

### ListKeys

Lists all keys for the currently-authed-to org.


**Parameters:**


**Returns:**

([List[viam.proto.app.APIKeyWithAuthorizations]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_keys).

```python
keys = cloud.list_keys()
```

### TabularDataByFilter

Filter and download tabular data.


**Parameters:**

- `filter` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.
- `dest` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.

**Returns:**

([List[TabularData]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tabular_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
tabular_data = await data_client.tabular_data_by_filter(my_filter)
```

### BinaryDataByFilter

Filter and download binary data.


**Parameters:**

- `filter` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.
- `dest` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.
- `include_file_data` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.
- `num_files` [(int)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.

**Returns:**

([List[BinaryData]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.binary_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_type="camera")
binary_data = await data_client.binary_data_by_filter(my_filter)
```

### BinaryDataByIDs

Filter and download binary data.


**Parameters:**

- `binary_ids` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Optional.
- `dest` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID): Optional.

**Returns:**

([List[BinaryData]](<INSERT RETURN TYPE LINK>)))
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

- `organization_id` [(int)](<INSERT PARAM TYPE LINK>):
- `delete_older_than_days` [(int)](<INSERT PARAM TYPE LINK>):

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
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

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_binary_data_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="left_motor")
res = await data_client.delete_binary_data_by_filter(my_filter)
```

### DeleteBinaryDataByIDs

Filter and delete binary data.


**Parameters:**

- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
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

- `tags` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):

**Returns:**


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

- `tags` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.
- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.

**Returns:**


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

- `tags` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `binary_ids` [(List[viam.proto.app.data.BinaryID])](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
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

- `tags` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.
- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
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

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.

**Returns:**

([List[str]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.tags_by_filter).

```python
from viam.proto.app.data import Filter

my_filter = Filter(component_name="my_camera")
tags = await data_client.tags_by_filter(my_filter)
```

### AddBoundingBoxToImageByID

Add a bounding box to an image.


**Parameters:**

- `binary_id` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `label` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `x_min_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `y_min_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `x_max_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `y_max_normalized` [(float)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `bbox_id` [(viam.proto.app.data.BinaryID)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `binary_id` [(viam.proto.app.data.BinaryID)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):

**Returns:**


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

- `filter` [(viam.proto.app.data.Filter)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.Filter): Optional.

**Returns:**

([List[str]](<INSERT RETURN TYPE LINK>)))
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

- `organization_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.get_database_connection).

```python
data_client.get_database_connection(org_id="a12b3c4e-1234-1abc-ab1c-ab1c2d345abc")
```

### CreateDataset

Create a new dataset.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>):
- `organization_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `ids` [(List[str])](<INSERT PARAM TYPE LINK>):

**Returns:**

([Sequence[viam.proto.app.dataset.Dataset]](<INSERT RETURN TYPE LINK>)))
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

- `organization_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([Sequence[viam.proto.app.dataset.Dataset]](<INSERT RETURN TYPE LINK>)))
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

- `id` [(str)](<INSERT PARAM TYPE LINK>):
- `name` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


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

- `id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient.delete_dataset).

```python
await data_client.delete_dataset(
    id="abcd-1234xyz-8765z-123abc"
)
```

### AddBinaryDataToDatasetByIDs

Add the BinaryData to the provided dataset.


**Parameters:**

- `binary_ids` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `dataset_id` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):

**Returns:**


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

- `binary_ids` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):
- `dataset_id` [(str)](https://python.viam.dev/autoapi/viam/proto/app/data/index.html#viam.proto.app.data.BinaryID):

**Returns:**


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

- `binary_data` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `part_id` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `component_type` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `component_name` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `method_name` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `file_extension` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `method_parameters` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `tags` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.
- `data_request_times` [(Tuple[datetime.datetime, datetime.datetime])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `tabular_data` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.
- `part_id` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.
- `component_type` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.
- `component_name` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.
- `method_name` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.
- `method_parameters` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.
- `tags` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.
- `data_request_times` [(List[Tuple[datetime.datetime, datetime.datetime]])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `data` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `part_id` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `file_ext` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `component_type` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `component_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `method_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `method_parameters` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `data_request_times` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `part_id` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `data` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `component_type` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `component_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `method_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `file_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `method_parameters` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `file_extension` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `filepath` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `part_id` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `component_type` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `component_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `method_name` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `method_parameters` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.
- `tags` [(List[str])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([str](<INSERT RETURN TYPE LINK>)))
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

- `id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([viam.proto.app.mltraining.TrainingJobMetadata](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.get_training_job).

```python
job_metadata = await ml_training_client.get_training_job(
    id="INSERT YOUR JOB ID")
```

### ListTrainingJobs

Returns training job data for all jobs within an org.


**Parameters:**

- `org_id` [(viam.proto.app.mltraining.TrainingStatus.ValueType)](<INSERT PARAM TYPE LINK>): Optional.
- `training_status` [(viam.proto.app.mltraining.TrainingStatus.ValueType)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.app.mltraining.TrainingJobMetadata]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.list_training_jobs).

```python
jobs_metadata = await ml_training_client.list_training_jobs(
    org_id="INSERT YOUR ORG ID")

first_job_id = jobs_metadata[1].id
```

### CancelTrainingJob

Cancels the specified training job.


**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/ml_training_client/index.html#viam.app.ml_training_client.MLTrainingClient.cancel_training_job).

```python
await ml_training_client.cancel_training_job(
    id="INSERT YOUR JOB ID")
```

