<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ListOrganizations`](/reference/apis/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user owns.
[`GetOrganizationNamespaceAvailability`](/reference/apis/fleet/#getorganizationnamespaceavailability) | Check the availability of an organization namespace.
[`ListOrganizationMembers`](/reference/apis/fleet/#listorganizationmembers) | List the members and invites of the current organization.
[`UpdateOrganizationInviteAuthorizations`](/reference/apis/fleet/#updateorganizationinviteauthorizations) | Update the authorizations attached to an organization invite that has already been created.
[`CreateLocation`](/reference/apis/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}}.
[`GetLocation`](/reference/apis/fleet/#getlocation) | Get a location by its ID.
[`UpdateLocation`](/reference/apis/fleet/#updatelocation ) | Change the name of a location and/or assign a parent location to a location.
[`DeleteLocation`](/reference/apis/fleet/#deletelocation ) | Delete a location.
[`ListLocations`](/reference/apis/fleet/#listlocations ) | List locations.
[`LocationAuth`](/reference/apis/fleet/#locationauth ) | Get a location's authorization (location secrets).
[`CreateLocationSecret`](/reference/apis/fleet/#createlocationsecret ) | Create a new location secret. *Deprecated*.
[`DeleteLocationSecret`](/reference/apis/fleet/#deletelocationsecret ) | Delete a location secret. *Deprecated*.
[`GetRobot`](/reference/apis/fleet/#getrobot ) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by machine ID.
[`GetRobotParts`](/reference/apis/fleet/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific machine.
[`GetRobotPart`](/reference/apis/fleet/#getrobotpart ) | Get a machine {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/reference/apis/fleet/#getrobotpartlogs ) | Get the logs associated with a machine part.
[`TailRobotPartLogs`](/reference/apis/fleet/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live machine part logs.
[`GetRobotPartHistory`](/reference/apis/fleet/#getrobotparthistory ) | Get a list containing the history of a machine part.
[`UpdateRobotPart`](/reference/apis/fleet/#updaterobotpart ) | Update the name or configuration of a machine part.
[`NewRobotPart`](/reference/apis/fleet/#newrobotpart ) | Create a new machine part.
[`DeleteRobotPart`](/reference/apis/fleet/#deleterobotpart ) | Delete a machine part.
[`MarkPartAsMain`](/reference/apis/fleet/#markpartasmain ) | Mark a part as the [_main_ part](/hardware/multi-machine/overview/#machine-parts) of a machine.
[`MarkPartForRestart`](/reference/apis/fleet/#markpartforrestart ) | Mark a machine part for restart.
[`CreateRobotPartSecret`](/reference/apis/fleet/#createrobotpartsecret ) | Create a machine part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/reference/apis/fleet/#deleterobotpartsecret ) | Delete a machine part secret. *Deprecated*.
[`ListRobots`](/reference/apis/fleet/#listrobots ) | Get a list of all machines in a location.
[`NewRobot`](/reference/apis/fleet/#newrobot ) | Create a new machine.
[`UpdateRobot`](/reference/apis/fleet/#updaterobot ) | Change the name of an existing machine.
[`DeleteRobot`](/reference/apis/fleet/#deleterobot ) | Delete a machine.
[`ListFragments`](/reference/apis/fleet/#listfragments ) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}}.
[`GetFragment`](/reference/apis/fleet/#getfragment ) | Get a fragment by its ID.
[`CreateFragment`](/reference/apis/fleet/#createfragment ) | Create a new private fragment.
[`UpdateFragment`](/reference/apis/fleet/#updatefragment ) | Update a fragment name, config or visibility.
[`DeleteFragment`](/reference/apis/fleet/#deletefragment ) | Delete a fragment.
[`AddRole`](/reference/apis/fleet/#addrole ) | Add a role (owner or operator).
[`RemoveRole`](/reference/apis/fleet/#removerole ) | Remove a role (owner or operator).
[`ListAuthorizations`](/reference/apis/fleet/#listauthorizations ) | List authorizations (owners and operators).
[`CreateModule`](/reference/apis/fleet/#createmodule ) | Create a {{< glossary_tooltip term_id="module" text="module" >}}.
[`UpdateModule`](/reference/apis/fleet/#updatemodule ) | Update module metadata.
[`UploadModuleFile`](/reference/apis/fleet/#uploadmodulefile ) | Upload a module file.
[`GetModule`](/reference/apis/fleet/#getmodule ) | Get a module by its ID.
[`ListModules`](/reference/apis/fleet/#listmodules ) | List available modules.
[`CreateOrganizationInvite`](/reference/apis/fleet/#createorganizationinvite) | Create an organization invite and send it by email.
[`DeleteOrganizationMember`](/reference/apis/fleet/#deleteorganizationmember) | Remove a member from the organization.
[`DeleteOrganizationInvite`](/reference/apis/fleet/#deleteorganizationinvite) | Delete a pending organization invite.
[`ResendOrganizationInvite`](/reference/apis/fleet/#resendorganizationinvite) | Resend a pending organization invite email.
[`GetRoverRentalRobots`](/reference/apis/fleet/#getroverrentalrobots) | Return a list of rover rental robots within an org.
[`CheckPermissions`](/reference/apis/fleet/#checkpermissions) | Check if the entity you're currently authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.
[`CreateKey`](/reference/apis/fleet/#createkey) | Create a new API key.
[`CreateKeyFromExistingKeyAuthorizations`](/reference/apis/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations.
[`ListKeys`](/reference/apis/fleet/#listkeys) | List all keys for an organization.
