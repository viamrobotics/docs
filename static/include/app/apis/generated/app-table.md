<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`ListOrganizations`](/appendix/apis/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user is an authorized user of. |
| [`GetOrganization`](/appendix/apis/fleet/#getorganization) | Return details about the requested organization. |
| [`GetOrganizationNamespaceAvailability`](/appendix/apis/fleet/#getorganizationnamespaceavailability) | Check the availability of an {{< glossary_tooltip term_id="organization" text="organization" >}} namespace. |
| [`UpdateOrganization`](/appendix/apis/fleet/#updateorganization) | Updates organization details. |
| [`ListOrganizationMembers`](/appendix/apis/fleet/#listorganizationmembers) | List the members and invites of the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to. |
| [`CreateOrganizationInvite`](/appendix/apis/fleet/#createorganizationinvite) | Create an {{< glossary_tooltip term_id="organization" text="organization" >}} invite and send it by email. |
| [`UpdateOrganizationInviteAuthorizations`](/appendix/apis/fleet/#updateorganizationinviteauthorizations) | Update (add or remove) the authorizations attached to an organization invite that has already been created. |
| [`DeleteOrganizationMember`](/appendix/apis/fleet/#deleteorganizationmember) | Remove a member from the {{< glossary_tooltip term_id="organization" text="organization" >}} you are currently authenticated to. |
| [`DeleteOrganizationInvite`](/appendix/apis/fleet/#deleteorganizationinvite) | Delete a pending organization invite to the organization you are currently authenticated to. |
| [`ResendOrganizationInvite`](/appendix/apis/fleet/#resendorganizationinvite) | Resend a pending organization invite email. |
| [`CreateLocation`](/appendix/apis/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}} under the organization you are currently authenticated to. |
| [`GetLocation`](/appendix/apis/fleet/#getlocation) | Get a {{< glossary_tooltip term_id="location" text="location" >}} by its location ID. |
| [`UpdateLocation`](/appendix/apis/fleet/#updatelocation) | Change the name of a {{< glossary_tooltip term_id="location" text="parent location" >}} and/or assign it a new location. |
| [`DeleteLocation`](/appendix/apis/fleet/#deletelocation) | Delete a {{< glossary_tooltip term_id="location" text="location" >}}. |
| [`ListLocations`](/appendix/apis/fleet/#listlocations) | Get a list of all {{< glossary_tooltip term_id="location" text="locations" >}} under the organization you are currently authenticated to. |
| [`LocationAuth`](/appendix/apis/fleet/#locationauth) | Get a location’s `LocationAuth` (location secret or secrets). |
| [`GetRobot`](/appendix/apis/fleet/#getrobot) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by its ID. |
| [`GetRobotParts`](/appendix/apis/fleet/#getrobotparts) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific {{< glossary_tooltip term_id="machine" text="machine" >}}. |
| [`GetRobotPart`](/appendix/apis/fleet/#getrobotpart) | Get a specific machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`GetRobotPartLogs`](/appendix/apis/fleet/#getrobotpartlogs) | Get the logs associated with a specific machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`TailRobotPartLogs`](/appendix/apis/fleet/#tailrobotpartlogs) | Get an asynchronous iterator that receives live machine part logs. |
| [`GetRobotPartHistory`](/appendix/apis/fleet/#getrobotparthistory) | Get a list containing the history of a machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`UpdateRobotPart`](/appendix/apis/fleet/#updaterobotpart) | Change the name of and assign an optional new configuration to a machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`NewRobotPart`](/appendix/apis/fleet/#newrobotpart) | Create a new machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`DeleteRobotPart`](/appendix/apis/fleet/#deleterobotpart) | Delete the specified machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`MarkPartAsMain`](/appendix/apis/fleet/#markpartasmain) | Mark a machine part as the _main_ part of a machine. |
| [`MarkPartForRestart`](/appendix/apis/fleet/#markpartforrestart) | Mark a specified machine part for restart. |
| [`CreateRobotPartSecret`](/appendix/apis/fleet/#createrobotpartsecret) | Create a machine {{< glossary_tooltip term_id="part" text="part" >}} secret. |
| [`DeleteRobotPartSecret`](/appendix/apis/fleet/#deleterobotpartsecret) | Delete a machine part secret. |
| [`ListRobots`](/appendix/apis/fleet/#listrobots) | Get a list of all machines in a specified location. |
| [`NewRobot`](/appendix/apis/fleet/#newrobot) | Create a new {{< glossary_tooltip term_id="machine" text="machine" >}}. |
| [`UpdateRobot`](/appendix/apis/fleet/#updaterobot) | Change the name of an existing machine. |
| [`DeleteRobot`](/appendix/apis/fleet/#deleterobot) | Delete a specified machine. |
| [`ListFragments`](/appendix/apis/fleet/#listfragments) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}} in the organization you are currently authenticated to. |
| [`GetFragment`](/appendix/apis/fleet/#getfragment) | Get a {{< glossary_tooltip term_id="fragment" text="fragment" >}} by ID. |
| [`CreateFragment`](/appendix/apis/fleet/#createfragment) | Create a new private {{< glossary_tooltip term_id="fragment" text="fragment" >}}. |
| [`UpdateFragment`](/appendix/apis/fleet/#updatefragment) | Update a {{< glossary_tooltip term_id="fragment" text="fragment" >}} name and its config and/or visibility. |
| [`DeleteFragment`](/appendix/apis/fleet/#deletefragment) | Delete a {{< glossary_tooltip term_id="fragment" text="fragment" >}}. |
| [`AddRole`](/appendix/apis/fleet/#addrole) | Add a role under the organization you are currently authenticated to. |
| [`RemoveRole`](/appendix/apis/fleet/#removerole) | Remove a role under the organization you are currently authenticated to. |
| [`ListAuthorizations`](/appendix/apis/fleet/#listauthorizations) | List all authorizations (owners and operators) of a specific resource (or resources) within the organization you are currently authenticated to. |
| [`CheckPermissions`](/appendix/apis/fleet/#checkpermissions) | Check if the organization, location, or robot your `ViamClient` is authenticated to is permitted to perform some action or set of actions on the resource you pass to the method. |
| [`CreateModule`](/appendix/apis/fleet/#createmodule) | Create a {{< glossary_tooltip term_id="module" text="module" >}} under the organization you are currently authenticated to. |
| [`UpdateModule`](/appendix/apis/fleet/#updatemodule) | Update the documentation URL, description, models, entrypoint, and/or the visibility of a {{< glossary_tooltip term_id="module" text="module" >}}. |
| [`UploadModuleFile`](/appendix/apis/fleet/#uploadmodulefile) | Upload a {{< glossary_tooltip term_id="module" text="module" >}} file. |
| [`GetModule`](/appendix/apis/fleet/#getmodule) | Get a {{< glossary_tooltip term_id="module" text="module" >}} by its ID. |
| [`ListModules`](/appendix/apis/fleet/#listmodules) | List the {{< glossary_tooltip term_id="module" text="modules" >}} under the organization you are currently authenticated to. |
| [`CreateKey`](/appendix/apis/fleet/#createkey) | Create a new API key. |
| [`ListKeys`](/appendix/apis/fleet/#listkeys) | List all keys for the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to. |
| [`CreateKeyFromExistingKeyAuthorizations`](/appendix/apis/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations. |
