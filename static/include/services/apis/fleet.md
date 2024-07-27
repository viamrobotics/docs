<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ListOrganizations`](/appendix/apis/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user owns.
[`GetOrganizationNamespaceAvailability`](/appendix/apis/fleet/#getorganizationnamespaceavailability) | Check the availability of an organization namespace.
[`ListOrganizationMembers`](/appendix/apis/fleet/#listorganizationmembers) | List the members and invites of the current organization.
[`UpdateOrganizationInviteAuthorizations`](/appendix/apis/fleet/#updateorganizationinviteauthorizations) | Update the authorizations attached to an organization invite that has already been created.
[`CreateLocation`](/appendix/apis/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}}.
[`GetLocation`](/appendix/apis/fleet/#getlocation) | Get a location by its ID.
[`UpdateLocation`](/appendix/apis/fleet/#updatelocation ) | Change the name of and/or assign a parent location to a location.
[`DeleteLocation`](/appendix/apis/fleet/#deletelocation ) | Delete a location.
[`ListLocations`](/appendix/apis/fleet/#listlocations ) | List locations.
[`LocationAuth`](/appendix/apis/fleet/#locationauth ) | Get a location's authorization (location secrets).
[`CreateLocationSecret`](/appendix/apis/fleet/#createlocationsecret ) | Create a new location secret. *Deprecated*.
[`DeleteLocationSecret`](/appendix/apis/fleet/#deletelocationsecret ) | Delete a location secret. *Deprecated*.
[`GetRobot`](/appendix/apis/fleet/#getrobot ) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by machine ID.
[`GetRobotParts`](/appendix/apis/fleet/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific machine.
[`GetRobotPart`](/appendix/apis/fleet/#getrobotpart ) | Get a machine {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/appendix/apis/fleet/#getrobotpartlogs ) | Get the logs associated with a machine part.
[`TailRobotPartLogs`](/appendix/apis/fleet/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live machine part logs.
[`GetRobotPartHistory`](/appendix/apis/fleet/#getrobotparthistory ) | Get a list containing the history of a machine part.
[`UpdateRobotPart`](/appendix/apis/fleet/#updaterobotpart ) | Update the name or configuration of a machine part.
[`NewRobotPart`](/appendix/apis/fleet/#newrobotpart ) | Create a new machine part.
[`DeleteRobotPart`](/appendix/apis/fleet/#deleterobotpart ) | Delete a machine part.
[`MarkPartAsMain`](/appendix/apis/fleet/#markpartasmain ) | Mark a part as the [_main_ part](/configure/parts/#machine-parts) of a machine.
[`MarkPartForRestart`](/appendix/apis/fleet/#markpartforrestart ) | Mark a machine part for restart.
[`CreateRobotPartSecret`](/appendix/apis/fleet/#createrobotpartsecret ) | Create a machine part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/appendix/apis/fleet/#deleterobotpartsecret ) | Delete a machine part secret. *Deprecated*.
[`ListRobots`](/appendix/apis/fleet/#listrobots ) | Get a list of all machines in a location.
[`NewRobot`](/appendix/apis/fleet/#newrobot ) | Create a new machine.
[`UpdateRobot`](/appendix/apis/fleet/#updaterobot ) | Change the name of an existing machine.
[`DeleteRobot`](/appendix/apis/fleet/#deleterobot ) | Delete a machine.
[`ListFragments`](/appendix/apis/fleet/#listfragments ) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}}.
[`GetFragment`](/appendix/apis/fleet/#getfragment ) | Get a fragment by its ID.
[`CreateFragment`](/appendix/apis/fleet/#createfragment ) | Create a new private fragment.
[`UpdateFragment`](/appendix/apis/fleet/#updatefragment ) | Update a fragment name, config or visibility.
[`DeleteFragment`](/appendix/apis/fleet/#deletefragment ) | Delete a fragment.
[`AddRole`](/appendix/apis/fleet/#addrole ) | Add a role (owner or operator).
[`RemoveRole`](/appendix/apis/fleet/#removerole ) | Remove a role (owner or operator).
[`ListAuthorizations`](/appendix/apis/fleet/#listauthorizations ) | List authorizations (owners and operators).
[`CreateModule`](/appendix/apis/fleet/#createmodule ) | Create a {{< glossary_tooltip term_id="module" text="module" >}}.
[`UpdateModule`](/appendix/apis/fleet/#updatemodule ) | Update module metadata.
[`UploadModuleFile`](/appendix/apis/fleet/#uploadmodulefile ) | Upload a module file.
[`GetModule`](/appendix/apis/fleet/#getmodule ) | Get a module by its ID.
[`ListModules`](/appendix/apis/fleet/#listmodules ) | List available modules.
[`CreateOrganizationInvite`](/appendix/apis/fleet/#createorganizationinvite) | Create an organization invite and send it by email.
[`DeleteOrganizationMember`](/appendix/apis/fleet/#deleteorganizationmember) | Remove a member from the organization.
[`DeleteOrganizationInvite`](/appendix/apis/fleet/#deleteorganizationinvite) | Delete a pending organization invite.
[`ResendOrganizationInvite`](/appendix/apis/fleet/#resendorganizationinvite) | Resend a pending organization invite email.
[`GetRoverRentalRobots`](/appendix/apis/fleet/#getroverrentalrobots) | Return a list of rover rental robots within an org.
[`CheckPermissions`](/appendix/apis/fleet/#checkpermissions) | Check if the entity you're currently authenticated to is permitted to perform some action or set of actions on the resource you pass to the method.
[`CreateKey`](/appendix/apis/fleet/#createkey) | Create a new API key.
[`CreateKeyFromExistingKeyAuthorizations`](/appendix/apis/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations.
[`ListKeys`](/appendix/apis/fleet/#listkeys) | List all keys for an organization.
