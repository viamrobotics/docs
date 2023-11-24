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
[`GetRobot`](/build/program/apis/cloud/#getrobot ) | Get a {{< glossary_tooltip term_id="robot" text="robot" >}} by robot ID.
[`GetRobotParts`](/build/program/apis/cloud/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific robot.
[`GetRobotPart`](/build/program/apis/cloud/#getrobotpart ) | Get a robot {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/build/program/apis/cloud/#getrobotpartlogs ) | Get the logs associated with a robot part.
[`TailRobotPartLogs`](/build/program/apis/cloud/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live robot part logs.
[`GetRobotPartHistory`](/build/program/apis/cloud/#getrobotparthistory ) | Get a list containing the history of a robot part.
[`UpdateRobotPart`](/build/program/apis/cloud/#updaterobotpart ) | Update the name or configuration of a robot part.
[`NewRobotPart`](/build/program/apis/cloud/#newrobotpart ) | Create a new robot part.
[`DeleteRobotPart`](/build/program/apis/cloud/#deleterobotpart ) | Delete a robot part.
[`MarkPartAsMain`](/build/program/apis/cloud/#markpartasmain ) | Mark a robot part as the [_main_ part](/build/configure/parts-and-remotes/#robot-parts) of a robot.
[`MarkPartForRestart`](/build/program/apis/cloud/#markpartforrestart ) | Mark a robot part for restart.
[`CreateRobotPartSecret`](/build/program/apis/cloud/#createrobotpartsecret ) | Create a robot part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/build/program/apis/cloud/#deleterobotpartsecret ) | Delete a robot part secret. *Deprecated*.
[`ListRobots`](/build/program/apis/cloud/#listrobots ) | Get a list of all robots in a location.
[`NewRobot`](/build/program/apis/cloud/#newrobot ) | Create a new robot.
[`UpdateRobot`](/build/program/apis/cloud/#updaterobot ) | Change the name of an existing robot.
[`DeleteRobot`](/build/program/apis/cloud/#deleterobot ) | Delete a robot.
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
