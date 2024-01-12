<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ListOrganizations`](/build/program/apis/cloud/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user owns.
[`GetOrganizationNamespaceAvailability`](/build/program/apis/cloud/#getorganizationnamespaceavailability) | Check the availability of an organization namespace.
[`ListOrganizationMembers`](/build/program/apis/cloud/#listorganizationmembers) | List the members and invites of the current organization.
[`UpdateOrganizationInviteAuthorizations`](/build/program/apis/cloud/#updateorganizationinviteauthorizations) | Update the authorizations attached to an organization invite that has already been created.
[`CreateLocation`](/build/program/apis/cloud/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}}.
[`GetLocation`](/build/program/apis/cloud/#getlocation) | Get a location by its ID.
[`UpdateLocation`](/build/program/apis/cloud/#updatelocation ) | Change the name of and/or assign a parent location to a location.
[`DeleteLocation`](/build/program/apis/cloud/#deletelocation ) | Delete a location.
[`ListLocations`](/build/program/apis/cloud/#listlocations ) | List locations.
[`LocationAuth`](/build/program/apis/cloud/#locationauth ) | Get a location's authorization (location secrets).
[`CreateLocationSecret`](/build/program/apis/cloud/#createlocationsecret ) | Create a new location secret. *Deprecated*.
[`DeleteLocationSecret`](/build/program/apis/cloud/#deletelocationsecret ) | Delete a location secret. *Deprecated*.
[`GetRobot`](/build/program/apis/cloud/#getrobot ) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by machine ID.
[`GetRobotParts`](/build/program/apis/cloud/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific machine.
[`GetRobotPart`](/build/program/apis/cloud/#getrobotpart ) | Get a machine {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/build/program/apis/cloud/#getrobotpartlogs ) | Get the logs associated with a machine part.
[`TailRobotPartLogs`](/build/program/apis/cloud/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live machine part logs.
[`GetRobotPartHistory`](/build/program/apis/cloud/#getrobotparthistory ) | Get a list containing the history of a machine part.
[`UpdateRobotPart`](/build/program/apis/cloud/#updaterobotpart ) | Update the name or configuration of a machine part.
[`NewRobotPart`](/build/program/apis/cloud/#newrobotpart ) | Create a new machine part.
[`DeleteRobotPart`](/build/program/apis/cloud/#deleterobotpart ) | Delete a machine part.
[`MarkPartAsMain`](/build/program/apis/cloud/#markpartasmain ) | Mark a part as the [_main_ part](/build/configure/parts-and-remotes/#machine-parts) of a machine.
[`MarkPartForRestart`](/build/program/apis/cloud/#markpartforrestart ) | Mark a machine part for restart.
[`CreateRobotPartSecret`](/build/program/apis/cloud/#createrobotpartsecret ) | Create a machine part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/build/program/apis/cloud/#deleterobotpartsecret ) | Delete a machine part secret. *Deprecated*.
[`ListRobots`](/build/program/apis/cloud/#listrobots ) | Get a list of all machines in a location.
[`NewRobot`](/build/program/apis/cloud/#newrobot ) | Create a new machine.
[`UpdateRobot`](/build/program/apis/cloud/#updaterobot ) | Change the name of an existing machine.
[`DeleteRobot`](/build/program/apis/cloud/#deleterobot ) | Delete a machine.
[`ListFragments`](/build/program/apis/cloud/#listfragments ) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}}.
[`GetFragment`](/build/program/apis/cloud/#getfragment ) | Get a fragment by its ID.
[`CreateFragment`](/build/program/apis/cloud/#createfragment ) | Create a new private fragment.
[`UpdateFragment`](/build/program/apis/cloud/#updatefragment ) | Update a fragment name, config or visibility.
[`DeleteFragment`](/build/program/apis/cloud/#deletefragment ) | Delete a fragment.
[`AddRole`](/build/program/apis/cloud/#addrole ) | Add a role (owner or operator).
[`RemoveRole`](/build/program/apis/cloud/#removerole ) | Remove a role (owner or operator).
[`ListAuthorizations`](/build/program/apis/cloud/#listauthorizations ) | List authorizations (owners and operators).
[`CreateModule`](/build/program/apis/cloud/#createmodule ) | Create a {{< glossary_tooltip term_id="module" text="module" >}}.
[`UpdateModule`](/build/program/apis/cloud/#updatemodule ) | Update module metadata.
[`UploadModuleFile`](/build/program/apis/cloud/#uploadmodulefile ) | Upload a module file.
[`GetModule`](/build/program/apis/cloud/#getmodule ) | Get a module by its ID.
[`ListModules`](/build/program/apis/cloud/#listmodules ) | List available modules.
[`CreateOrganizationInvite`](/build/program/apis/cloud/#createorganizationinvite) | Create an organization invite and send it by email.
[`DeleteOrganizationMember`](/build/program/apis/cloud/#deleteorganizationmember) | Remove a member from the organization.
[`DeleteOrganizationInvite`](/build/program/apis/cloud/#deleteorganizationinvite) | Delete a pending organization invite.
[`ResendOrganizationInvite`](/build/program/apis/cloud/#resendorganizationinvite) | Resend a pending organization invite email.
[`GetRoverRentalRobots`](/build/program/apis/cloud/#getroverrentalrobots) | Return a list of rover rental robots within an org.
[`CheckPermissions`](/build/program/apis/cloud/#checkpermissions) | Check if the entity you're currently authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.
[`CreateKey`](/build/program/apis/cloud/#createkey) | Create a new API key.
[`CreateKeyFromExistingKeyAuthorizations`](/build/program/apis/cloud/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations.
[`ListKeys`](/build/program/apis/cloud/#listkeys) | List all keys for an organization.
