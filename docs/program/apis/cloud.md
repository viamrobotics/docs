---
title: "Manage Your Fleet with Viam's Cloud API"
linkTitle: "Cloud Management"
weight: 20
type: "docs"
description: "Use the cloud app API with Viam's client SDKs to manage your robot fleet with code."
tags: ["cloud", "sdk", "viam-server", "networking", "apis", "robot api", "cloud management"]
---

The cloud app API allows you to [manage your robot fleet](/manage/fleet/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).
With it you can

- create and manage organizations, locations, and individual robots
- manage permissions and authorization
- create and manage fragments

{{% alert title="Support Notice" color="note" %}}

Cloud app API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam cloud app API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`AppClient`](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient).
See the following example for reference.
To find the location secret, go to [Viam app](https://app.viam.com/), and go to the  [**Code sample**](https://docs.viam.com/manage/fleet/robots/#code-sample) tab of any of the robots in the location.
Toggle **Include secret** on and copy the `payload`.
For the URL, use the address of any of the robots in the location (also found on the **Code sample** tab).

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

async def connect() -> ViamClient:
    dial_options = DialOptions(
        auth_entity='mrroboto.this_is_just_an_example.viam.cloud',  # The URL of a robot in the location.
        credentials=Credentials(
            type='robot-location-secret',
            payload='YOUR LOCATION SECRET' # The location secret
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

  # Make a ViamClient
  viam_client = await connect()
  # Instantiate an AppClient called "cloud" to run the cloud app API methods on
  cloud = viam_client.app_client

  viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated an `AppClient`, you can run the following [API methods](#api) against the `AppClient` object (named `cloud` in the examples).

## API

The cloud API supports the following methods (among [others](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient)):

{{< readfile "/static/include/services/apis/cloud.md" >}}

### ListOrganizations

List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user is an authorized user of.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List[viam.proto.app.Organization])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Organization): A list of the organization or organizations of which the user is an authorized owner.

```python {class="line-numbers linkable-line-numbers"}
org_list = await cloud.list_organizations()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organizations).

{{% /tab %}}
{{< /tabs >}}

### ListOrganizationMembers

List the members and invites of the {{< glossary_tooltip term_id="organization" text="organizations" >}} that you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- (Tuple[List[[viam.proto.app.OrganizationMember]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationMember)], List[[viam.proto.app.OrganizationInvite]](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite)): A tuple containing two lists:
  - The first (`[0]`) is a list of organization members.
  - The second (`[1]`) is a list of organization invites.

```python {class="line-numbers linkable-line-numbers"}
member_list, invite_list = await cloud.list_organization_members()
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
available = await cloud.get_organization_namespace_availability(public_namespace="my-cool-organization")
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
authorization_to_add=Authorization(
    authorization_type="some type of auth",
    authorization_id="identifier",
    resource_type="abc",
    resource_id="resource-identifier123",
    identity_id="id12345",
    organization_id="org_id_123"
)

update_invite = await cloud.update_organization_invite_authorizations(
    email="notarealemail@viam.com",
    remove_authorizations=[authorization_to_add]
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
my_new_location = await cloud.create_location(name="Robotville", parent_location_id="111ab12345")
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

- `location_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to delete.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed.

**Returns:**

- None

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

- None

**Returns:**

- (List[[viam.proto.app.Location](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Location)]): The list of locations.

```python {class="line-numbers linkable-line-numbers"}
locations = await cloud.list_locations()
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
loc_auth = await cloud.location_auth(location_id="123xy12345")
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
new_loc_auth = await cloud.create_location_secret()
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

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str):

```python {class="line-numbers linkable-line-numbers"}
await cloud.delete_location_secret(secret_id="abcd123-456-7890ab-cxyz98-989898xyzxyz")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_location_secret).

{{% /tab %}}
{{< /tabs >}}

### GetRobot

Get a robot by its ID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot_id` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the robot to get.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The robot.

```python {class="line-numbers linkable-line-numbers"}
robot = await cloud.get_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot).

{{% /tab %}}
{{< /tabs >}}

### NewRobot

Create a new {{< glossary_tooltip term_id="robot" text="robot" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the new robot.
- `location_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location to create the new robot in.
  Defaults to the current authorized location.

**Raises:**

- `GRPCError`: This error is raised if an invalid location ID is passed, or if one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The new robot's ID.

```python {class="line-numbers linkable-line-numbers"}
new_robot_id = await cloud.new_robot(name="beepboop")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot).

{{% /tab %}}
{{< /tabs >}}
