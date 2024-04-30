---
title: "Manage Your Fleet with Viam's Fleet Management API"
linkTitle: "Fleet Management"
weight: 20
type: "docs"
description: "Use the fleet management API with Viam's client SDKs to manage your machine fleet with code."
tags:
  [
    "cloud",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "cloud management",
    "fleet management",
  ]
aliases:
  - /program/apis/fleet/
  - /build/program/apis/fleet/
---

The fleet management API allows you to [manage your machine fleet](/fleet/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).
With it you can

- create and manage organizations, locations, and individual machines
- manage permissions and authorization
- create and manage fragments

{{% alert title="Support Notice" color="note" %}}

Fleet management API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam fleet management API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`AppClient`](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient).
See the following example for reference.

<!-- After sveltekit migration we should also be able to get a key from the UI-->

Use the Viam CLI [to generate an API key to authenticate](/fleet/cli/#authenticate).

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your API key
      # ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an AppClient called "fleet"
    # to run fleet management API methods on
    fleet = viam_client.app_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated an `AppClient`, you can run the following [API methods](#api) against the `AppClient` object (named `fleet` in the examples).

## API

The fleet management API supports the following methods (among [others](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient)):

{{< readfile "/static/include/services/apis/fleet.md" >}}

### ListOrganizations

List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user is an authorized user of.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List[viam.proto.app.Organization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Organization): A list of the organization or organizations of which the user is an authorized owner.

```python {class="line-numbers linkable-line-numbers"}
org_list = await fleet.list_organizations()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organizations).

{{% /tab %}}
{{< /tabs >}}

### ListOrganizationMembers

List the members and invites of the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- (Tuple[List[[viam.proto.app.OrganizationMember]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationMember)], List[[viam.proto.app.OrganizationInvite]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)): A tuple containing two lists:
  - The first (`[0]`) is a list of organization members.
  - The second (`[1]`) is a list of organization invites.

```python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await fleet.list_organization_members()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

{{% /tab %}}
{{< /tabs >}}

### GetOrganizationNamespaceAvailability

Check the availability of an {{< glossary_tooltip term_id="organization" text="organization" >}} namespace.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `public_namespace` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The organization namespace to check.
  Namespaces can only contain lowercase alphanumeric and dash characters.

**Raises:**

- `GRPCError`: This error is raised if an invalid namespace (for example, `""`) is provided.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): `True` if the provided namespace is available.

```python {class="line-numbers linkable-line-numbers"}
available = await fleet.get_organization_namespace_availability(
    public_namespace="my-cool-organization")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_namespace_availability).

{{% /tab %}}
{{< /tabs >}}

### UpdateOrganizationInviteAuthorizations

Update (add or remove) the authorizations attached to an organization invite that has already been created.
If an invitation has only one authorization and you want to remove it, delete the invitation instead of using this method.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `email` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Email of the user the invite was sent to.
- `add_authorizations` [(Optional[List[viam.proto.app.Authorization]])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional list of authorizations to add to the invite.
- `remove_authorizations` [(Optional[List[viam.proto.app.Authorization]])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional list of authorizations to remove from the invite.

**Raises:**

- `GRPCError`: This error is raised if no authorizations are passed or if an invalid combination of authorizations is passed (for example, an authorization to remove when the invite only contains one authorization).

**Returns:**

- [(OrganizationInvite)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite): The updated invitation.

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

update_invite = await fleet.update_organization_invite_authorizations(
    email="notarealemail@viam.com",
    add_authorizations=[authorization_to_add]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization_invite_authorizations).

{{% /tab %}}
{{< /tabs >}}

### CreateLocation

Create and name a {{< glossary_tooltip term_id="location" text="location" >}} under the organization you are currently authenticated to.
Optionally, put the new location under a specified parent location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the new location.
- `parent_location_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional parent location to put the location under.
  Defaults to creating a location in your organization at root level if you do not provide a location ID.

**Raises:**

- `GRPCError`: This error is raised if an invalid name (such as "") or invalid parent location ID is passed.

**Returns:**

- [(viam.proto.app.Location)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location): The newly created location.

```python {class="line-numbers linkable-line-numbers"}
my_new_location = await fleet.create_location(name="Robotville",
                                              parent_location_id="111ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location).

{{% /tab %}}
{{< /tabs >}}

### GetLocation

Get a {{< glossary_tooltip term_id="location" text="location" >}} by its location ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to get.
  Defaults to the location ID provided at `AppClient` instantiation.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(viam.proto.app.Location)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location): The location corresponding to the provided ID.

```python {class="line-numbers linkable-line-numbers"}
location = await fleet.get_location(location_id="123ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_location).

{{% /tab %}}
{{< /tabs >}}

### UpdateLocation

Change the name of a {{< glossary_tooltip term_id="location" text="parent location" >}} and/or assign it a new location.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to update.
- `name` [Optional(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional new name to update the location name to.
  If nothing is passed, the name is not changed.
- `parent_location_id` [Optional(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional ID of the new location to move the location to.
  If nothing is passed, the location does not move.
  If an empty string is passed, the location moves up to the top level.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(viam.proto.app.Location)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location): The newly updated location.

```python {class="line-numbers linkable-line-numbers"}
# The following line takes the location with ID "abc12abcde" and moves it
# to be a sub-location of the location with ID "xyz34xxxxx"
my_updated_location = await fleet.update_location(
    location_id="abc12abcde",
    name="",
    parent_location_id="xyz34xxxxx",
)

# The following line changes the name of the location without changing its
# parent location
my_updated_location = await fleet.update_location(
    location_id="abc12abcde",
    name="Land Before Robots"
)

# The following line moves the location back up to be a top level location
# without changing its name
my_updated_location = await fleet.update_location(
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

- `location_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to delete.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed.

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
await fleet.delete_location(location_id="abc12abcde")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location).

{{% /tab %}}
{{< /tabs >}}

### ListLocations

Get a list of all {{< glossary_tooltip term_id="location" text="locations" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- (List[[viam.proto.app.Location](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)]): The list of locations.

```python {class="line-numbers linkable-line-numbers"}
locations = await fleet.list_locations()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_locations).

{{% /tab %}}
{{< /tabs >}}

### LocationAuth

Get a location’s `LocationAuth` (location secret or secrets).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to retrieve `LocationAuth` from.
  Defaults to the location ID provided at `AppClient` instantiation.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(viam.proto.app.LocationAuth)](https://python.viam.dev/autoapi/viam/gen/app/v1/app_pb2/index.html#viam.gen.app.v1.app_pb2.LocationAuth): The `LocationAuth` containing location secrets and secret IDs.

```python {class="line-numbers linkable-line-numbers"}
loc_auth = await fleet.location_auth(location_id="123xy12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.location_auth).

{{% /tab %}}
{{< /tabs >}}

### CreateLocationSecret

Create a new location secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to generate a new secret for.
  Defaults to the location ID provided at `AppClient` instantiation.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(viam.proto.app.LocationAuth)](https://python.viam.dev/autoapi/viam/gen/app/v1/app_pb2/index.html#viam.gen.app.v1.app_pb2.LocationAuth): The specified location's `LocationAuth` containing the newly created secret.

```python {class="line-numbers linkable-line-numbers"}
new_loc_auth = await fleet.create_location_secret()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_location_secret).

{{% /tab %}}
{{< /tabs >}}

### DeleteLocationSecret

Delete a location secret.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `location_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to delete the secret from.
  Defaults to the location ID provided at `AppClient` instantiation.
- `secret_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The `id` of the secret to delete (not the secret string itself).

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

```python {class="line-numbers linkable-line-numbers"}
await fleet.delete_location_secret(
    secret_id="abcd123-456-7890ab-cxyz98-989898xyzxyz")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location_secret).

{{% /tab %}}
{{< /tabs >}}

### GetRobot

Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine to get.

**Raises:**

- `GRPCError`: This error is raised if an invalid robot ID is passed.

**Returns:**

- [(viam.proto.app.Robot)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot): The machine.

```python {class="line-numbers linkable-line-numbers"}
robot = await fleet.get_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot).

{{% /tab %}}
{{< /tabs >}}

### GetRobotParts

Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine to get parts from.

**Raises:**

- `GRPCError`: This error is raised if an invalid robot ID is passed.

**Returns:**

- (List[[viam.app.app_client.RobotPart]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart)): The list of machine parts.

```python {class="line-numbers linkable-line-numbers"}
list_of_parts = await fleet.get_robot_parts(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to get.
- `dest` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional filepath to write the machine part’s config in JSON format to.
- `indent` [(int)](https://docs.python.org/3/library/functions.html#int): Size (in number of spaces) of indent when writing the JSON config to `dest`.
  Defaults to `4`.

**Returns:**

- [(viam.app.app_client.RobotPart)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart): The machine {{< glossary_tooltip term_id="part" text="part" >}}.

```python {class="line-numbers linkable-line-numbers"}
my_robot_part = await fleet.get_robot_part(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to get logs from. See [Find part ID](#find-part-id) for instructions on retrieving this value.
- `filter` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Only include logs with messages that contain the string `filter`.
  Defaults to empty string `""`, meaning no filter.
- `dest` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Optional filepath to write the log entries to.
- `errors_only` [(bool)](https://docs.python.org/3/library/functions.html#bool): (Optional) Specifies whether to limit returned log messages to error logs only.
  Defaults to `True`, including only error-level messages by default.
- `num_log_entries` [(int)](https://docs.python.org/3/library/functions.html#int): Number of log entries to return.
  Passing `0` returns all logs.
  Defaults to `100`.
  All logs or the first `num_log_entries` logs will be returned, whichever comes first.

**Raises:**

- `GRPCError`: This error is raised if an invalid robot part ID is passed.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The list of log entries.

```python {class="line-numbers linkable-line-numbers"}
part_logs = await fleet.get_robot_part_logs(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to retrieve logs from.
- `errors_only` [(bool)](https://docs.python.org/3/library/functions.html#bool): (Optional) Specifies whether to limit returned log messages to error logs only.
  Defaults to `True`, including only error-level messages by default.
- `filter` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Only include logs with messages that contain the string `filter`.
  Defaults to empty string `""`, meaning no filter.

**Returns:**

- (\_LogsStream[[List[LogEntry]]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.LogEntry)): The asynchronous iterator receiving live machine part logs.

```python {class="line-numbers linkable-line-numbers"}
logs_stream = await fleet.tail_robot_part_logs(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to retrieve history from. See [Find part ID](#find-part-id) for instructions on retrieving this value.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine part ID is passed.

**Returns:**

- (List[[viam.app.app_client.RobotPartHistoryEntry](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPartHistoryEntry)]): The list of the machine part’s history.

```python {class="line-numbers linkable-line-numbers"}
part_history = await fleet.get_robot_part_history(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to update. See [Find part ID](#find-part-id) for instructions on retrieving this value.
- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): New name to be updated on the machine part.
- `robot_config` (Mapping[str, Any]): Optional new config represented as a dictionary to be updated on the machine part.
  The machine part's config remains unchanged if a new `robot_config` is not passed.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine part ID, name, or config is passed.

**Returns:**

- [(viam.app.app_client.RobotPart)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart): The newly updated machine part.

```python {class="line-numbers linkable-line-numbers"}
my_robot_part = await fleet.update_robot_part(
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

- `robot_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine to create a new part for.
- `part_name` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the new part.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine ID is passed.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The new machine part’s ID.

```python {class="line-numbers linkable-line-numbers"}
new_part_id = await fleet.new_robot_part(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to delete. See [Find part ID](#find-part-id) for instructions on retrieving this value.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine part ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.delete_robot_part(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to mark as main. See [Find part ID](#find-part-id) for instructions on retrieving this value.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine part ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.mark_part_as_main(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to mark for restart. See [Find part ID](#find-part-id) for instructions on retrieving this value.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine part ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.mark_part_for_restart(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to create a secret for. See [Find part ID](#find-part-id) for instructions on retrieving this value.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine part ID is passed.

**Returns:**

- [(viam.app.app_client.RobotPart)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.RobotPart): The machine part the new secret was generated for.

```python {class="line-numbers linkable-line-numbers"}
part_with_new_secret = await fleet.create_robot_part_secret(
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

- `robot_part_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine part to delete the secret from. See [Find part ID](#find-part-id) for instructions on retrieving this value.
- `secret_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the secret to delete.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine part ID or secret ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.delete_robot_part_secret(
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

- `location_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to retrieve the machines from.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed.

**Returns:**

- (List[[viam.proto.app.Robot](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot)]): The list of machines.

```python {class="line-numbers linkable-line-numbers"}
list_of_machines = await fleet.list_robots(location_id="123ab12345")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_robots).

{{% /tab %}}
{{< /tabs >}}

### NewRobot

Create a new {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the new machine.
- `location_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to create the new machine in.
  Defaults to the current authorized location.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The new machine's ID.

```python {class="line-numbers linkable-line-numbers"}
new_machine_id = await fleet.new_robot(name="beepboop")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot).

{{% /tab %}}
{{< /tabs >}}

### UpdateRobot

Change the name of an existing machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine to update.
- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): New name for the machine.
- `location_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location in which the machine exists.
  Defaults to the location ID provided at `AppClient` instantiation.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine ID, name, or location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.
  **Returns:**

- [(viam.proto.app.Robot)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Robot): The newly updated machine.

```python {class="line-numbers linkable-line-numbers"}
updated_robot = await fleet.update_robot(
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

- `robot_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the machine to delete.

**Raises:**

- `GRPCError`: This error is raised if an invalid machine ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.delete_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot).

{{% /tab %}}
{{< /tabs >}}

### ListFragments

Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}} in the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `show_public` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): (Optional) Specify whether to only show public fragments. If `True`, only public fragments will be returned.
  If `False`, only private fragments will be returned.
  Default: `True`.

**Returns:**

- (List[[viam.app.app_client.Fragment]](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment)): The list of fragments.

```python {class="line-numbers linkable-line-numbers"}
fragments_list = await fleet.list_fragments(show_public=False)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_fragments).

{{% /tab %}}
{{< /tabs >}}

### GetFragment

Get a {{< glossary_tooltip term_id="fragment" text="fragment" >}} by ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `fragment_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the fragment to get.

**Raises:**

- `GRPCError`: This error is raised if an invalid fragment ID is passed.

**Returns:**

- [(viam.app.app_client.Fragment)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment): The fragment.

```python {class="line-numbers linkable-line-numbers"}
# Get a fragment and print its name and when it was created.
the_fragment = await fleet.get_fragment(
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

- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the new fragment.
- `config` (Optional[Mapping[str, Any]]): Dictionary representation of the new config to assign to the fragment.
  Can be assigned by updating the fragment.

**Raises:**

- `GRPCError`: This error is raised if an invalid name is passed.

**Returns:**

- [(viam.app.app_client.Fragment)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment): The newly created fragment.

```python {class="line-numbers linkable-line-numbers"}
new_fragment = await fleet.create_fragment(
  name="cool_smart_machine_to_configure_several_of")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_fragment).

{{% /tab %}}
{{< /tabs >}}

### UpdateFragment

Update a {{< glossary_tooltip term_id="fragment" text="fragment" >}} name and its config and/or visibility.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `fragment_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the fragment to update.
- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): New name to associate with the fragment.
- `config` (Optional[Mapping[str, Any]]): Dictionary representation of the new config to assign to the fragment.
  Not passing this parameter will leave the fragment's config unchanged.
- `public` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): Specify whether the fragment is public.
  Default: `False` (private).

**Raises:**

- `GRPCError`: This error is raised if an invalid fragment ID, name, or config is passed.

**Returns:**

- [(viam.app.app_client.Fragment)](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.Fragment): The newly updated fragment.

```python {class="line-numbers linkable-line-numbers"}
updated_fragment = await fleet.update_fragment(
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

- `fragment_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the fragment to delete.

**Raises:**

- `GRPCError`: This error is raised if an invalid fragment ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.delete_fragment(
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

- `identity_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the entity the role belongs to (for example, a user ID).
- `role` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The role to add (either `"owner"` or `"operator"`).
- `resource_type` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The type of the resource to add the role to (either `"organization"`, `"location"`, or `"robot"`).
  Must match the type of the `resource_id`'s resource.
- `resource_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the resource the role applies to (the ID of either an {{< glossary_tooltip term_id="organization" text="organization" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="machine" text="machine" >}}.)

**Raises:**

- `GRPCError`: This error is raised if an invalid identity ID, role, resource type, or resource ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.add_role(
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

- `identity_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the entity the role belongs to (for example, a user ID).
- `role` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The role to remove (either `"owner"` or `"operator"`).
- `resource_type` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The type of the resource to remove the role from (either `"organization"`, `"location"`, or `"robot"`).
  Must match the type of the `resource_id`'s resource.
- `resource_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the resource the role applies to (the ID of either an {{< glossary_tooltip term_id="organization" text="organization" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="machine" text="machine" >}}.)

**Raises:**

- `GRPCError`: This error is raised if an invalid identity ID, role, resource type, or resource ID is passed.

```python {class="line-numbers linkable-line-numbers"}
await fleet.remove_role(
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

- `resource_ids` (Optional[List[(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): IDs of the resources to retrieve authorizations from. Defaults to none.

**Raises:**

- `GRPCError`: This error is raised if an invalid resource ID is passed.

**Returns:**

- (List[[Authorization](https://python.viam.dev/autoapi/viam/gen/app/v1/app_pb2/index.html#viam.gen.app.v1.app_pb2.Authorization)]): The list of authorizations.

```python {class="line-numbers linkable-line-numbers"}
list_of_auths = await fleet.list_authorizations(
  resource_ids=["1a123456-x1yz-0ab0-a12xyzabc"])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_authorizations).

{{% /tab %}}
{{< /tabs >}}

### CreateModule

Create a {{< glossary_tooltip term_id="module" text="module" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The name of the module. Must be unique within your organization.

**Raises:**

- `GRPCError`: This error is raised if an invalid name (for example, `""`) is passed.

**Returns:**

- (Tuple[[string, string](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing the ID [0] of the new module and its URL [1].

```python {class="line-numbers linkable-line-numbers"}
new_module = await fleet.create_module(name="cool_new_hoverboard_module")
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

- `module_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the module being updated, containing module name (for example, `"my-module"`) or namespace and module name (for example, `"my-org:my-module"`).
- `url` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The URL to reference for documentation and code (_not_ the URL of the module itself).
- `description` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): A short description of the module that explains its purpose.
- `models` (Optional[List[[viam.proto.app.Model](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Model)]]): List of models that are available in the module.
- `entrypoint` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The executable to run to start the module program.
- `public` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): Set the visibility of the module.
  Defaults to `False` (private).

**Raises:**

- `GRPCError`: This error is raised if an invalid module ID, URL, list of models, or organization ID is passed.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The URL of the newly updated module.

```python {class="line-numbers linkable-line-numbers"}
url_of_my_module = await fleet.update_module(
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

- `module_file_info` (Optional[[viam.proto.app.ModuleFileInfo](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.ModuleFileInfo)]): Relevant metadata.
- `file` [(bytes)](https://docs.python.org/3/library/stdtypes.html#bytes): Bytes of file to upload.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the uploaded file.

```python {class="line-numbers linkable-line-numbers"}
file_id = await fleet.upload_module_file(file=b"<file>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.upload_module_file).

{{% /tab %}}
{{< /tabs >}}

### GetModule

Get a {{< glossary_tooltip term_id="module" text="module" >}} by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `module_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the module being retrieved, containing module name (for example, `"my-module"`) or namespace and module name (for example, `"my-org:my-module"`).

**Raises:**

- `GRPCError`: This error is raised if an invalid module ID is passed.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The module.

```python {class="line-numbers linkable-line-numbers"}
the_module = await fleet.get_module(module_id="my-cool-modular-base")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_module).

{{% /tab %}}
{{< /tabs >}}

### ListModules

List the {{< glossary_tooltip term_id="module" text="modules" >}} under the organization you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Raises:**

- `GRPCError`: This error is raised if an invalid machine ID is passed.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The list of modules.

```python {class="line-numbers linkable-line-numbers"}
modules_list = await fleet.list_modules()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_modules).

{{% /tab %}}
{{< /tabs >}}

### CreateOrganizationInvite

{{< tabs >}}
{{% tab name="Python" %}}

Create an {{< glossary_tooltip term_id="organization" text="organization" >}} invite and send it by email.

**Parameters:**

- `email` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The email address to send the invite to.
- `authorizations` [(Optional[List[viam.proto.app.Authorization]])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Authorizations to include in the invite.
  If not provided, full owner permissions will be granted.

**Returns:**

- None.

**Raises:**

- `GRPCError`: This error is raised if an invalid email is provided, or if the user is already a member of the org.

```python {class="line-numbers linkable-line-numbers"}
await fleet.create_organization_invite("youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_organization_invite).

{{% /tab %}}
{{< /tabs >}}

### DeleteOrganizationMember

{{< tabs >}}
{{% tab name="Python" %}}

Remove a member from the {{< glossary_tooltip term_id="organization" text="organization" >}} you are currently authenticated to.

**Parameters:**

- `user_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the user to remove.

**Returns:**

- None.

```python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await fleet.list_organization_members()
first_user_id = member_list[0].user_id

await fleet.delete_organization_member(first_user_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_member).

{{% /tab %}}
{{< /tabs >}}

### DeleteOrganizationInvite

{{< tabs >}}
{{% tab name="Python" %}}

Delete a pending organization invite to the organization you are currently authenticated to.

**Parameters:**

- `email` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The email address the pending invite was sent to.

**Returns:**

- None.

**Raises:**

- `GRPCError`: This error is raised if no pending invite is associated with the provided email address.

```python {class="line-numbers linkable-line-numbers"}
await fleet.delete_organization_invite("youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_organization_invite).

{{% /tab %}}
{{< /tabs >}}

### ResendOrganizationInvite

{{< tabs >}}
{{% tab name="Python" %}}

Resend a pending organization invite email.

**Parameters:**

- `email` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The email address associated with the invite.

**Returns:**

- None.

**Raises:**

- `GRPCError`: This error is raised if no pending invite is associated with the provided email address.

```python {class="line-numbers linkable-line-numbers"}
await fleet.resend_organization_invite("youremail@email.com")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.resend_organization_invite).

{{% /tab %}}
{{< /tabs >}}

### GetRoverRentalRobots

{{< tabs >}}
{{% tab name="Python" %}}

Return a list of rover rental robots within an {{< glossary_tooltip term_id="organization" text="organization" >}}.

**Parameters:**

- None.

**Returns:**

- [(List[viam.proto.app.RoverRentalRobot])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.RoverRentalRobot): The list of rover rental robots.

```python {class="line-numbers linkable-line-numbers"}
rental_robots = await fleet.get_rover_rental_robots()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_rover_rental_robots).

{{% /tab %}}
{{< /tabs >}}

### CheckPermissions

{{< tabs >}}
{{% tab name="Python" %}}

Check if the organization, location, or robot your `ViamClient` is authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.

**Parameters:**

- `permissions` [(List[viam.proto.app.AuthorizedPermissions])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.AuthorizedPermissions): A list containing the resource type and ID, followed by the resource permissions to check.

**Returns:**

- [(List[viam.proto.app.AuthorizedPermissions])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.AuthorizedPermissions): The permissions argument, with invalid permissions filtered out.

**Raises:**

- `GRPCError`: This error is raised if the list of permissions to validate is empty.

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.app import AuthorizedPermissions

# Check whether the entity you're currently
# authenticated to has permission to control
# and/or read logs from robots
# in the "organization-identifier123" org
permissions = [AuthorizedPermissions(resource_type="organization",
                                     resource_id="organization-identifier123",
                                     permissions=["control_robot",
                                                  "read_robot_logs"])]

filtered_permissions = await fleet.check_permissions(permissions)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.check_permissions).

{{% /tab %}}
{{< /tabs >}}

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

For more information about managing permissions, see [Role-Based Access Control](/fleet/rbac/#permissions).

### CreateKey

{{< tabs >}}
{{% tab name="Python" %}}

Create a new [API key](/fleet/rbac/#api-keys).

**Parameters:**

- `authorizations` [(List[APIKeyAuthorization])](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.APIKeyAuthorization): A list of authorizations to associate with the key.
- `name` [(Optional[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): A name for the key. If None, defaults to the current timestamp.

**Returns:**

- [(Tuple[str, str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The api key and api key ID.

**Raises:**

- `GRPCError`: This error is raised if the authorizations list is empty.

```python {class="line-numbers linkable-line-numbers"}
from viam.app.app_client import APIKeyAuthorization

auth = APIKeyAuthorization(
  role="owner",
  resource_type="robot",
  resource_id="your-robot-id123"
)

api_key, api_key_id = fleet.create_key([auth], "my_key")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key).

{{% /tab %}}
{{< /tabs >}}

### CreateKeyFromExistingKeyAuthorizations

{{< tabs >}}
{{% tab name="Python" %}}

Create a new API key with an existing key’s authorizations.

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The ID of the API key to duplicate authorizations from.

**Returns:**

- [(Tuple[str, str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The new API key and API key ID.

```python {class="line-numbers linkable-line-numbers"}
api_key, api_key_id = fleet.create_key_from_existing_key_authorizations(
  id="INSERT YOUR API KEY ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_key_from_existing_key_authorizations).

{{% /tab %}}
{{< /tabs >}}

### ListKeys

{{< tabs >}}
{{% tab name="Python" %}}

List all keys for the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to.

**Parameters:**

- None.

**Returns:**

- [(List[viam.proto.app.APIKeyWithAuthorizations])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.APIKeyWithAuthorizations): The existing API keys and authorizations.

```python {class="line-numbers linkable-line-numbers"}
keys = fleet.list_keys()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_keys).

{{% /tab %}}
{{< /tabs >}}

## Find part ID

To copy the ID of your machine part, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**.

For example:

![Part ID displayed in the Viam app.](/build/program/data-client/grab-part-id.png)
