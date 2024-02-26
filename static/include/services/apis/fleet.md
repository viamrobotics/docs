<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ListOrganizations`](/build/program/apis/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user owns.
[`GetOrganizationNamespaceAvailability`](/build/program/apis/fleet/#getorganizationnamespaceavailability) | Check the availability of an organization namespace.
[`ListOrganizationMembers`](/build/program/apis/fleet/#listorganizationmembers) | List the members and invites of the current organization.
[`UpdateOrganizationInviteAuthorizations`](/build/program/apis/fleet/#updateorganizationinviteauthorizations) | Update the authorizations attached to an organization invite that has already been created.
[`CreateLocation`](/build/program/apis/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}}.
[`GetLocation`](/build/program/apis/fleet/#getlocation) | Get a location by its ID.
[`UpdateLocation`](/build/program/apis/fleet/#updatelocation ) | Change the name of and/or assign a parent location to a location.
[`DeleteLocation`](/build/program/apis/fleet/#deletelocation ) | Delete a location.
[`ListLocations`](/build/program/apis/fleet/#listlocations ) | List locations.
[`LocationAuth`](/build/program/apis/fleet/#locationauth ) | Get a location's authorization (location secrets).
[`CreateLocationSecret`](/build/program/apis/fleet/#createlocationsecret ) | Create a new location secret. *Deprecated*.
[`DeleteLocationSecret`](/build/program/apis/fleet/#deletelocationsecret ) | Delete a location secret. *Deprecated*.
[`GetRobot`](/build/program/apis/fleet/#getrobot ) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by machine ID.
[`GetRobotParts`](/build/program/apis/fleet/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific machine.
[`GetRobotPart`](/build/program/apis/fleet/#getrobotpart ) | Get a machine {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/build/program/apis/fleet/#getrobotpartlogs ) | Get the logs associated with a machine part.
[`TailRobotPartLogs`](/build/program/apis/fleet/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live machine part logs.
[`GetRobotPartHistory`](/build/program/apis/fleet/#getrobotparthistory ) | Get a list containing the history of a machine part.
[`UpdateRobotPart`](/build/program/apis/fleet/#updaterobotpart ) | Update the name or configuration of a machine part.
[`NewRobotPart`](/build/program/apis/fleet/#newrobotpart ) | Create a new machine part.
[`DeleteRobotPart`](/build/program/apis/fleet/#deleterobotpart ) | Delete a machine part.
[`MarkPartAsMain`](/build/program/apis/fleet/#markpartasmain ) | Mark a part as the [_main_ part](/build/configure/parts-and-remotes/#machine-parts) of a machine.
[`MarkPartForRestart`](/build/program/apis/fleet/#markpartforrestart ) | Mark a machine part for restart.
[`CreateRobotPartSecret`](/build/program/apis/fleet/#createrobotpartsecret ) | Create a machine part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/build/program/apis/fleet/#deleterobotpartsecret ) | Delete a machine part secret. *Deprecated*.
[`ListRobots`](/build/program/apis/fleet/#listrobots ) | Get a list of all machines in a location.
[`NewRobot`](/build/program/apis/fleet/#newrobot ) | Create a new machine.
[`UpdateRobot`](/build/program/apis/fleet/#updaterobot ) | Change the name of an existing machine.
[`DeleteRobot`](/build/program/apis/fleet/#deleterobot ) | Delete a machine.
[`ListFragments`](/build/program/apis/fleet/#listfragments ) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}}.
[`GetFragment`](/build/program/apis/fleet/#getfragment ) | Get a fragment by its ID.
[`CreateFragment`](/build/program/apis/fleet/#createfragment ) | Create a new private fragment.
[`UpdateFragment`](/build/program/apis/fleet/#updatefragment ) | Update a fragment name, config or visibility.
[`DeleteFragment`](/build/program/apis/fleet/#deletefragment ) | Delete a fragment.
[`AddRole`](/build/program/apis/fleet/#addrole ) | Add a role (owner or operator).
[`RemoveRole`](/build/program/apis/fleet/#removerole ) | Remove a role (owner or operator).
[`ListAuthorizations`](/build/program/apis/fleet/#listauthorizations ) | List authorizations (owners and operators).
[`CreateModule`](/build/program/apis/fleet/#createmodule ) | Create a {{< glossary_tooltip term_id="module" text="module" >}}.
[`UpdateModule`](/build/program/apis/fleet/#updatemodule ) | Update module metadata.
[`UploadModuleFile`](/build/program/apis/fleet/#uploadmodulefile ) | Upload a module file.
[`GetModule`](/build/program/apis/fleet/#getmodule ) | Get a module by its ID.
[`ListModules`](/build/program/apis/fleet/#listmodules ) | List available modules.
[`CreateOrganizationInvite`](/build/program/apis/fleet/#createorganizationinvite) | Create an organization invite and send it by email.
[`DeleteOrganizationMember`](/build/program/apis/fleet/#deleteorganizationmember) | Remove a member from the organization.
[`DeleteOrganizationInvite`](/build/program/apis/fleet/#deleteorganizationinvite) | Delete a pending organization invite.
[`ResendOrganizationInvite`](/build/program/apis/fleet/#resendorganizationinvite) | Resend a pending organization invite email.
[`GetRoverRentalRobots`](/build/program/apis/fleet/#getroverrentalrobots) | Return a list of rover rental robots within an org.
[`CheckPermissions`](/build/program/apis/fleet/#checkpermissions) | Check if the entity you're currently authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.
[`CreateKey`](/build/program/apis/fleet/#createkey) | Create a new API key.
[`CreateKeyFromExistingKeyAuthorizations`](/build/program/apis/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations.
[`ListKeys`](/build/program/apis/fleet/#listkeys) | List all keys for an organization.
