<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ListOrganizations`](/dev/reference/apis/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user owns.
[`GetOrganizationNamespaceAvailability`](/dev/reference/apis/fleet/#getorganizationnamespaceavailability) | Check the availability of an organization namespace.
[`ListOrganizationMembers`](/dev/reference/apis/fleet/#listorganizationmembers) | List the members and invites of the current organization.
[`UpdateOrganizationInviteAuthorizations`](/dev/reference/apis/fleet/#updateorganizationinviteauthorizations) | Update the authorizations attached to an organization invite that has already been created.
[`CreateLocation`](/dev/reference/apis/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}}.
[`GetLocation`](/dev/reference/apis/fleet/#getlocation) | Get a location by its ID.
[`UpdateLocation`](/dev/reference/apis/fleet/#updatelocation ) | Change the name of and/or assign a parent location to a location.
[`DeleteLocation`](/dev/reference/apis/fleet/#deletelocation ) | Delete a location.
[`ListLocations`](/dev/reference/apis/fleet/#listlocations ) | List locations.
[`LocationAuth`](/dev/reference/apis/fleet/#locationauth ) | Get a location's authorization (location secrets).
[`CreateLocationSecret`](/dev/reference/apis/fleet/#createlocationsecret ) | Create a new location secret. *Deprecated*.
[`DeleteLocationSecret`](/dev/reference/apis/fleet/#deletelocationsecret ) | Delete a location secret. *Deprecated*.
[`GetRobot`](/dev/reference/apis/fleet/#getrobot ) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by machine ID.
[`GetRobotParts`](/dev/reference/apis/fleet/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific machine.
[`GetRobotPart`](/dev/reference/apis/fleet/#getrobotpart ) | Get a machine {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/dev/reference/apis/fleet/#getrobotpartlogs ) | Get the logs associated with a machine part.
[`TailRobotPartLogs`](/dev/reference/apis/fleet/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live machine part logs.
[`GetRobotPartHistory`](/dev/reference/apis/fleet/#getrobotparthistory ) | Get a list containing the history of a machine part.
[`UpdateRobotPart`](/dev/reference/apis/fleet/#updaterobotpart ) | Update the name or configuration of a machine part.
[`NewRobotPart`](/dev/reference/apis/fleet/#newrobotpart ) | Create a new machine part.
[`DeleteRobotPart`](/dev/reference/apis/fleet/#deleterobotpart ) | Delete a machine part.
[`MarkPartAsMain`](/dev/reference/apis/fleet/#markpartasmain ) | Mark a part as the [_main_ part](/operate/reference/architecture/parts/#machine-parts) of a machine.
[`MarkPartForRestart`](/dev/reference/apis/fleet/#markpartforrestart ) | Mark a machine part for restart.
[`CreateRobotPartSecret`](/dev/reference/apis/fleet/#createrobotpartsecret ) | Create a machine part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/dev/reference/apis/fleet/#deleterobotpartsecret ) | Delete a machine part secret. *Deprecated*.
[`ListRobots`](/dev/reference/apis/fleet/#listrobots ) | Get a list of all machines in a location.
[`NewRobot`](/dev/reference/apis/fleet/#newrobot ) | Create a new machine.
[`UpdateRobot`](/dev/reference/apis/fleet/#updaterobot ) | Change the name of an existing machine.
[`DeleteRobot`](/dev/reference/apis/fleet/#deleterobot ) | Delete a machine.
[`ListFragments`](/dev/reference/apis/fleet/#listfragments ) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}}.
[`GetFragment`](/dev/reference/apis/fleet/#getfragment ) | Get a fragment by its ID.
[`CreateFragment`](/dev/reference/apis/fleet/#createfragment ) | Create a new private fragment.
[`UpdateFragment`](/dev/reference/apis/fleet/#updatefragment ) | Update a fragment name, config or visibility.
[`DeleteFragment`](/dev/reference/apis/fleet/#deletefragment ) | Delete a fragment.
[`AddRole`](/dev/reference/apis/fleet/#addrole ) | Add a role (owner or operator).
[`RemoveRole`](/dev/reference/apis/fleet/#removerole ) | Remove a role (owner or operator).
[`ListAuthorizations`](/dev/reference/apis/fleet/#listauthorizations ) | List authorizations (owners and operators).
[`CreateModule`](/dev/reference/apis/fleet/#createmodule ) | Create a {{< glossary_tooltip term_id="module" text="module" >}}.
[`UpdateModule`](/dev/reference/apis/fleet/#updatemodule ) | Update module metadata.
[`UploadModuleFile`](/dev/reference/apis/fleet/#uploadmodulefile ) | Upload a module file.
[`GetModule`](/dev/reference/apis/fleet/#getmodule ) | Get a module by its ID.
[`ListModules`](/dev/reference/apis/fleet/#listmodules ) | List available modules.
[`CreateOrganizationInvite`](/dev/reference/apis/fleet/#createorganizationinvite) | Create an organization invite and send it by email.
[`DeleteOrganizationMember`](/dev/reference/apis/fleet/#deleteorganizationmember) | Remove a member from the organization.
[`DeleteOrganizationInvite`](/dev/reference/apis/fleet/#deleteorganizationinvite) | Delete a pending organization invite.
[`ResendOrganizationInvite`](/dev/reference/apis/fleet/#resendorganizationinvite) | Resend a pending organization invite email.
[`GetRoverRentalRobots`](/dev/reference/apis/fleet/#getroverrentalrobots) | Return a list of rover rental robots within an org.
[`CheckPermissions`](/dev/reference/apis/fleet/#checkpermissions) | Check if the entity you're currently authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.
[`CreateKey`](/dev/reference/apis/fleet/#createkey) | Create a new API key.
[`CreateKeyFromExistingKeyAuthorizations`](/dev/reference/apis/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations.
[`ListKeys`](/dev/reference/apis/fleet/#listkeys) | List all keys for an organization.
