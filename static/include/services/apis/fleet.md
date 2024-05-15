<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ListOrganizations`](/program/apis/app/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user owns.
[`GetOrganizationNamespaceAvailability`](/program/apis/app/fleet/#getorganizationnamespaceavailability) | Check the availability of an organization namespace.
[`ListOrganizationMembers`](/program/apis/app/fleet/#listorganizationmembers) | List the members and invites of the current organization.
[`UpdateOrganizationInviteAuthorizations`](/program/apis/app/fleet/#updateorganizationinviteauthorizations) | Update the authorizations attached to an organization invite that has already been created.
[`CreateLocation`](/program/apis/app/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}}.
[`GetLocation`](/program/apis/app/fleet/#getlocation) | Get a location by its ID.
[`UpdateLocation`](/program/apis/app/fleet/#updatelocation ) | Change the name of and/or assign a parent location to a location.
[`DeleteLocation`](/program/apis/app/fleet/#deletelocation ) | Delete a location.
[`ListLocations`](/program/apis/app/fleet/#listlocations ) | List locations.
[`LocationAuth`](/program/apis/app/fleet/#locationauth ) | Get a location's authorization (location secrets).
[`CreateLocationSecret`](/program/apis/app/fleet/#createlocationsecret ) | Create a new location secret. *Deprecated*.
[`DeleteLocationSecret`](/program/apis/app/fleet/#deletelocationsecret ) | Delete a location secret. *Deprecated*.
[`GetRobot`](/program/apis/app/fleet/#getrobot ) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by machine ID.
[`GetRobotParts`](/program/apis/app/fleet/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific machine.
[`GetRobotPart`](/program/apis/app/fleet/#getrobotpart ) | Get a machine {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/program/apis/app/fleet/#getrobotpartlogs ) | Get the logs associated with a machine part.
[`TailRobotPartLogs`](/program/apis/app/fleet/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live machine part logs.
[`GetRobotPartHistory`](/program/apis/app/fleet/#getrobotparthistory ) | Get a list containing the history of a machine part.
[`UpdateRobotPart`](/program/apis/app/fleet/#updaterobotpart ) | Update the name or configuration of a machine part.
[`NewRobotPart`](/program/apis/app/fleet/#newrobotpart ) | Create a new machine part.
[`DeleteRobotPart`](/program/apis/app/fleet/#deleterobotpart ) | Delete a machine part.
[`MarkPartAsMain`](/program/apis/app/fleet/#markpartasmain ) | Mark a part as the [_main_ part](/machine/configure/parts/#machine-parts) of a machine.
[`MarkPartForRestart`](/program/apis/app/fleet/#markpartforrestart ) | Mark a machine part for restart.
[`CreateRobotPartSecret`](/program/apis/app/fleet/#createrobotpartsecret ) | Create a machine part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/program/apis/app/fleet/#deleterobotpartsecret ) | Delete a machine part secret. *Deprecated*.
[`ListRobots`](/program/apis/app/fleet/#listrobots ) | Get a list of all machines in a location.
[`NewRobot`](/program/apis/app/fleet/#newrobot ) | Create a new machine.
[`UpdateRobot`](/program/apis/app/fleet/#updaterobot ) | Change the name of an existing machine.
[`DeleteRobot`](/program/apis/app/fleet/#deleterobot ) | Delete a machine.
[`ListFragments`](/program/apis/app/fleet/#listfragments ) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}}.
[`GetFragment`](/program/apis/app/fleet/#getfragment ) | Get a fragment by its ID.
[`CreateFragment`](/program/apis/app/fleet/#createfragment ) | Create a new private fragment.
[`UpdateFragment`](/program/apis/app/fleet/#updatefragment ) | Update a fragment name, config or visibility.
[`DeleteFragment`](/program/apis/app/fleet/#deletefragment ) | Delete a fragment.
[`AddRole`](/program/apis/app/fleet/#addrole ) | Add a role (owner or operator).
[`RemoveRole`](/program/apis/app/fleet/#removerole ) | Remove a role (owner or operator).
[`ListAuthorizations`](/program/apis/app/fleet/#listauthorizations ) | List authorizations (owners and operators).
[`CreateModule`](/program/apis/app/fleet/#createmodule ) | Create a {{< glossary_tooltip term_id="module" text="module" >}}.
[`UpdateModule`](/program/apis/app/fleet/#updatemodule ) | Update module metadata.
[`UploadModuleFile`](/program/apis/app/fleet/#uploadmodulefile ) | Upload a module file.
[`GetModule`](/program/apis/app/fleet/#getmodule ) | Get a module by its ID.
[`ListModules`](/program/apis/app/fleet/#listmodules ) | List available modules.
[`CreateOrganizationInvite`](/program/apis/app/fleet/#createorganizationinvite) | Create an organization invite and send it by email.
[`DeleteOrganizationMember`](/program/apis/app/fleet/#deleteorganizationmember) | Remove a member from the organization.
[`DeleteOrganizationInvite`](/program/apis/app/fleet/#deleteorganizationinvite) | Delete a pending organization invite.
[`ResendOrganizationInvite`](/program/apis/app/fleet/#resendorganizationinvite) | Resend a pending organization invite email.
[`GetRoverRentalRobots`](/program/apis/app/fleet/#getroverrentalrobots) | Return a list of rover rental robots within an org.
[`CheckPermissions`](/program/apis/app/fleet/#checkpermissions) | Check if the entity you're currently authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.
[`CreateKey`](/program/apis/app/fleet/#createkey) | Create a new API key.
[`CreateKeyFromExistingKeyAuthorizations`](/program/apis/app/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations.
[`ListKeys`](/program/apis/app/fleet/#listkeys) | List all keys for an organization.
