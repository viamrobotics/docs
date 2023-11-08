<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ListOrganizations`](/program/apis/cloud/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user owns.
[`GetOrganizationNamespaceAvailability`](/program/apis/cloud/#getorganizationnamespaceavailability) | Check the availability of an organization namespace.
[`ListOrganizationMembers`](/program/apis/cloud/#listorganizationmembers) | List the members and invites of the current organization.
[`UpdateOrganizationInviteAuthorizations`](/program/apis/cloud/#updateorganizationinviteauthorizations) | Update the authorizations attached to an organization invite that has already been created.
[`CreateLocation`](/program/apis/cloud/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}}.
[`GetLocation`](/program/apis/cloud/#getlocation) | Get a location by its ID.
[`UpdateLocation`](/program/apis/cloud/#updatelocation ) | Change the name of and/or assign a parent location to a location.
[`DeleteLocation`](/program/apis/cloud/#deletelocation ) | Delete a location.
[`ListLocations`](/program/apis/cloud/#listlocations ) | List locations.
[`LocationAuth`](/program/apis/cloud/#locationauth ) | Get a location's authorization (location secrets).
[`CreateLocationSecret`](/program/apis/cloud/#createlocationsecret ) | Create a new location secret. *Deprecated*.
[`DeleteLocationSecret`](/program/apis/cloud/#deletelocationsecret ) | Delete a location secret. *Deprecated*.
[`GetRobot`](/program/apis/cloud/#getrobot ) | Get a {{< glossary_tooltip term_id="robot" text="robot" >}} by robot ID.
[`GetRobotParts`](/program/apis/cloud/#getrobotparts ) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific robot.
[`GetRobotPart`](/program/apis/cloud/#getrobotpart ) | Get a robot {{< glossary_tooltip term_id="part" text="part" >}}.
[`GetRobotPartLogs`](/program/apis/cloud/#getrobotpartlogs ) | Get the logs associated with a robot part.
[`TailRobotPartLogs`](/program/apis/cloud/#tailrobotpartlogs ) | Get an asynchronous iterator that receives live robot part logs.
[`GetRobotPartHistory`](/program/apis/cloud/#getrobotparthistory ) | Get a list containing the history of a robot part.
[`UpdateRobotPart`](/program/apis/cloud/#updaterobotpart ) | Update the name or configuration of a robot part.
[`NewRobotPart`](/program/apis/cloud/#newrobotpart ) | Create a new robot part.
[`DeleteRobotPart`](/program/apis/cloud/#deleterobotpart ) | Delete a robot part.
[`MarkPartAsMain`](/program/apis/cloud/#markpartasmain ) | Mark a robot part as the [_main_ part](/manage/parts-and-remotes/#robot-parts) of a robot.
[`MarkPartForRestart`](/program/apis/cloud/#markpartforrestart ) | Mark a robot part for restart.
[`CreateRobotPartSecret`](/program/apis/cloud/#createrobotpartsecret ) | Create a robot part secret. *Deprecated*.
[`DeleteRobotPartSecret`](/program/apis/cloud/#deleterobotpartsecret ) | Delete a robot part secret. *Deprecated*.
[`ListRobots`](/program/apis/cloud/#listrobots ) | Get a list of all robots in a location.
[`NewRobot`](/program/apis/cloud/#newrobot ) | Create a new robot.
[`UpdateRobot`](/program/apis/cloud/#updaterobot ) | Change the name of an existing robot.
[`DeleteRobot`](/program/apis/cloud/#deleterobot ) | Delete a robot.
[`ListFragments`](/program/apis/cloud/#listfragments ) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}}.
[`GetFragment`](/program/apis/cloud/#getfragment ) | Get a fragment by its ID.
[`CreateFragment`](/program/apis/cloud/#createfragment ) | Create a new private fragment.
[`UpdateFragment`](/program/apis/cloud/#updatefragment ) | Update a fragment name, config or visibility.
[`DeleteFragment`](/program/apis/cloud/#deletefragment ) | Delete a fragment.
[`AddRole`](/program/apis/cloud/#addrole ) | Add a role (owner or operator).
[`RemoveRole`](/program/apis/cloud/#removerole ) | Remove a role (owner or operator).
[`ListAuthorizations`](/program/apis/cloud/#listauthorizations ) | List authorizations (owners and operators).
[`CreateModule`](/program/apis/cloud/#createmodule ) | Create a {{< glossary_tooltip term_id="module" text="module" >}}.
[`UpdateModule`](/program/apis/cloud/#updatemodule ) | Update module metadata.
[`UploadModuleFile`](/program/apis/cloud/#uploadmodulefile ) | Upload a module file.
[`GetModule`](/program/apis/cloud/#getmodule ) | Get a module by its ID.
[`ListModules`](/program/apis/cloud/#listmodules ) | List available modules.
