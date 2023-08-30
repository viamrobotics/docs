---
title: "Managing Your Fleet with Viam's Cloud API"
linkTitle: "Cloud Management"
weight: 20
type: "docs"
description: "How to use the cloud API with Viam's client SDKs."
tags: ["cloud", "sdk", "viam-server", "networking", "apis", "robot api", "cloud management"]
---

The cloud app API allows you to [manage your robot fleet](/manage/fleet/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).
Functionality includes:

- create and manage organizations, locations, and individual robots
- manage permissions and authorization
- create and manage fragments

{{% alert title="Support Notice" color="note" %}}

Cloud app API methods are only available in the Python SDK.

{{% /alert %}}

## API

{{% alert title="Tip" color="tip" %}}

To use the Viam cloud app API, you need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`AppClient`](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient):

```python {class="line-numbers linkable-line-numbers"}
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

async def connect() -> ViamClient:
    dial_options = DialOptions(
        auth_entity='mrroboto.this_is_just_an_example.viam.cloud',  # The URL of your robot.
        credentials=Credentials(
            type='robot-location-secret',
            payload='YOUR ROBOT LOCATION SECRET' # The location secret of your robot
        )
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

  # Make a ViamClient
  viam_client = await connect()
  # Instantiate an AppClient called "cloud" to run the cloud app API methods on
  cloud = await viam_client.app_client()
```

Then, run methods on the `AppClient` according to the code examples for each method below.

{{% /alert %}}

The cloud API supports the following methods:

{{< readfile "/static/include/services/apis/cloud.md" >}}

### ListOrganizations

List the organizations the user is an authorized user of.

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

List the members and invites of the organization that you are currently authenticated to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Tuple[List[viam.proto.app.OrganizationMember]])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationMember): A tuple containing to lists:
  - The first (`[0]`) is a list of organization members.
  - The second (`[1]`) is a list of organization invites.

```python {class="line-numbers linkable-line-numbers"}
member_list = await cloud.list_organization_members()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.list_organization_members).

{{% /tab %}}
{{< /tabs >}}

### GetOrganizationNamespaceAvailability

Check the availability of an organization namespace.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `public_namespace` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The organization namespace to check.
Namespaces can only contain lowercase alphanumeric and dash characters.

**Raises:**

- GRPCError: An error is raised if an invalid namespace (for example, `""`) is provided.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): `True` if the provided namespace is available.

```python {class="line-numbers linkable-line-numbers"}
available = await cloud.get_organization_namespace_availability(public_namespace="my-cool-organization")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_namespace_availability).

{{% /tab %}}
{{< /tabs >}}

### UpdateOrganizationInviteAuthorizations

Update the authorizations attached to an organization invite that has already been created.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `email` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Email of the user the invite was sent to.
- `add_authorization` [(Optional[List[viam.proto.app.Authorization]])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional list of authorizations to add to the invite.
- `remove_authorization` [(Optional[List[viam.proto.app.Authorization]])](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.Authorization): Optional list of authorizations to remove from the invite.

**Raises:**

- GRPCError: An error is raised if no authorizations are passed or if an invalid combination of authorizations is passed (for example, an authorization to remove when the invite only contains one authorization).

**Returns:**

- [(OrganizationInvite)](https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite): The updated invitation.

```python {class="line-numbers linkable-line-numbers"}
update_invite = await cloud.update_organization_invite_authorizations(
    email="notarealemail@viam.com",
    remove_authorization=[
        authorization_type="some type of auth",
        authorization_id="identifier",
        resource_type="abc",
        resource_id="resource-identifier123",
        identity_id="id12345",
        organization_id="org_id_123"
    ]
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_organization_invite_authorizations).

{{% /tab %}}
{{< /tabs >}}

### NewRobot

Create a new robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the new robot.
- `location_id` [(Optional[string])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ID of the location under which to create the new robot.
  Defaults to the current authorized location.

**Raises:**

- GRPCError: An error is raised if an invalid location ID is passed or one isn't passed and no location ID was provided at `AppClient` instantiation.

**Returns:**

- [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The new robot's ID.

```python {class="line-numbers linkable-line-numbers"}
new_robot_id = await cloud.new_robot(name="beepboop")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_organization_namespace_availability).

{{% /tab %}}
{{< /tabs >}}
