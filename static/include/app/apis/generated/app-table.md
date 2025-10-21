<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetUserIDByEmail`](/dev/reference/apis/fleet/#getuseridbyemail) | Get the ID of a user by email. |
| [`CreateOrganization`](/dev/reference/apis/fleet/#createorganization) | Create an organization. |
| [`ListOrganizations`](/dev/reference/apis/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user is an authorized user of. |
| [`GetOrganizationsWithAccessToLocation`](/dev/reference/apis/fleet/#getorganizationswithaccesstolocation) | Get all organizations that have access to a location. |
| [`ListOrganizationsByUser`](/dev/reference/apis/fleet/#listorganizationsbyuser) | List the organizations a user belongs to. |
| [`GetOrganization`](/dev/reference/apis/fleet/#getorganization) | Retrieve the organization object for the requested organization containing the organization's ID, name, public namespace, and more. |
| [`GetOrganizationNamespaceAvailability`](/dev/reference/apis/fleet/#getorganizationnamespaceavailability) | Check the availability of an {{< glossary_tooltip term_id="organization" text="organization" >}} namespace. |
| [`UpdateOrganization`](/dev/reference/apis/fleet/#updateorganization) | Updates organization details. |
| [`DeleteOrganization`](/dev/reference/apis/fleet/#deleteorganization) | Delete an organization. |
| [`ListOrganizationMembers`](/dev/reference/apis/fleet/#listorganizationmembers) | List the members and invites of the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to. |
| [`CreateOrganizationInvite`](/dev/reference/apis/fleet/#createorganizationinvite) | Create an {{< glossary_tooltip term_id="organization" text="organization" >}} invite and send it by email. |
| [`UpdateOrganizationInviteAuthorizations`](/dev/reference/apis/fleet/#updateorganizationinviteauthorizations) | Update (add or remove) the authorizations attached to an organization invite that has already been created. |
| [`DeleteOrganizationMember`](/dev/reference/apis/fleet/#deleteorganizationmember) | Remove a member from the {{< glossary_tooltip term_id="organization" text="organization" >}} you are currently authenticated to. |
| [`DeleteOrganizationInvite`](/dev/reference/apis/fleet/#deleteorganizationinvite) | Delete a pending organization invite to the organization you are currently authenticated to. |
| [`ResendOrganizationInvite`](/dev/reference/apis/fleet/#resendorganizationinvite) | Resend a pending organization invite email. |
| [`GetOrganizationMetadata`](/dev/reference/apis/fleet/#getorganizationmetadata) | Gets the user-defined metadata for an organization. |
| [`UpdateOrganizationMetadata`](/dev/reference/apis/fleet/#updateorganizationmetadata) | Updates the user-defined metadata for an organization. |
| [`CreateLocation`](/dev/reference/apis/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}} under the organization you are currently authenticated to. |
| [`GetLocation`](/dev/reference/apis/fleet/#getlocation) | Get a {{< glossary_tooltip term_id="location" text="location" >}} by its location ID. |
| [`UpdateLocation`](/dev/reference/apis/fleet/#updatelocation) | Change the name of a {{< glossary_tooltip term_id="location" text="location" >}} and/or assign a parent location to a location. |
| [`DeleteLocation`](/dev/reference/apis/fleet/#deletelocation) | Delete a {{< glossary_tooltip term_id="location" text="location" >}}. |
| [`ListLocations`](/dev/reference/apis/fleet/#listlocations) | Get a list of all {{< glossary_tooltip term_id="location" text="locations" >}} under the organization you are currently authenticated to. |
| [`ShareLocation`](/dev/reference/apis/fleet/#sharelocation) | Share a location with an organization. |
| [`UnshareLocation`](/dev/reference/apis/fleet/#unsharelocation) | Stop sharing a location with an organization. |
| [`LocationAuth`](/dev/reference/apis/fleet/#locationauth) | Get a location’s `LocationAuth` (location secret or secrets). |
| [`CreateLocationSecret`](/dev/reference/apis/fleet/#createlocationsecret) | Create a new location secret. |
| [`DeleteLocationSecret`](/dev/reference/apis/fleet/#deletelocationsecret) | Delete a location secret. |
| [`GetLocationMetadata`](/dev/reference/apis/fleet/#getlocationmetadata) | Get the user-defined metadata for a location. |
| [`UpdateLocationMetadata`](/dev/reference/apis/fleet/#updatelocationmetadata) | Update the user-defined metadata for a location. |
| [`GetRobot`](/dev/reference/apis/fleet/#getrobot) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by its ID. |
| [`GetRobotAPIKeys`](/dev/reference/apis/fleet/#getrobotapikeys) | Gets the API keys for the machine. |
| [`GetRobotParts`](/dev/reference/apis/fleet/#getrobotparts) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific {{< glossary_tooltip term_id="machine" text="machine" >}}. |
| [`GetRobotPart`](/dev/reference/apis/fleet/#getrobotpart) | Get a specific machine {{< glossary_tooltip term_id="part" text="part" >}} including its part config, part address, and other information. |
| [`GetRobotPartLogs`](/dev/reference/apis/fleet/#getrobotpartlogs) | Get the logs associated with a specific machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`GetRobotPartByNameAndLocation`](/dev/reference/apis/fleet/#getrobotpartbynameandlocation) | Query a specific robot part by name and location id. |
| [`TailRobotPartLogs`](/dev/reference/apis/fleet/#tailrobotpartlogs) | Get an asynchronous iterator that receives live machine part logs. |
| [`GetRobotPartHistory`](/dev/reference/apis/fleet/#getrobotparthistory) | Get a list containing the history of a machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`UpdateRobotPart`](/dev/reference/apis/fleet/#updaterobotpart) | Change the name of and assign an optional new configuration to a machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`NewRobotPart`](/dev/reference/apis/fleet/#newrobotpart) | Create a new machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`DeleteRobotPart`](/dev/reference/apis/fleet/#deleterobotpart) | Delete the specified machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`MarkPartAsMain`](/dev/reference/apis/fleet/#markpartasmain) | Mark a machine part as the _main_ part of a machine. |
| [`MarkPartForRestart`](/dev/reference/apis/fleet/#markpartforrestart) | Mark a specified machine part for restart. |
| [`CreateRobotPartSecret`](/dev/reference/apis/fleet/#createrobotpartsecret) | Create a machine {{< glossary_tooltip term_id="part" text="part" >}} secret. |
| [`DeleteRobotPartSecret`](/dev/reference/apis/fleet/#deleterobotpartsecret) | Delete a machine part secret. |
| [`ListRobots`](/dev/reference/apis/fleet/#listrobots) | Get a list of all machines in a specified location. |
| [`NewRobot`](/dev/reference/apis/fleet/#newrobot) | Create a new {{< glossary_tooltip term_id="machine" text="machine" >}}. |
| [`UpdateRobot`](/dev/reference/apis/fleet/#updaterobot) | Update an existing machine's name and/or location. |
| [`DeleteRobot`](/dev/reference/apis/fleet/#deleterobot) | Delete a specified machine. |
| [`GetRobotMetadata`](/dev/reference/apis/fleet/#getrobotmetadata) | Gets the user-defined metadata for a machine. |
| [`GetRobotPartMetadata`](/dev/reference/apis/fleet/#getrobotpartmetadata) | Gets the user-defined metadata for a machine part. |
| [`UpdateRobotMetadata`](/dev/reference/apis/fleet/#updaterobotmetadata) | Updates the user-defined metadata for a machine. |
| [`UpdateRobotPartMetadata`](/dev/reference/apis/fleet/#updaterobotpartmetadata) | Updates the user-defined metadata for a machine part. |
| [`ListFragments`](/dev/reference/apis/fleet/#listfragments) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}} in the organization you are currently authenticated to. |
| [`ListMachineFragments`](/dev/reference/apis/fleet/#listmachinefragments) | Get a list of top level and nested {{< glossary_tooltip term_id="fragment" text="fragments" >}} for a machine, as well as additionally specified fragment IDs. |
| [`ListMachineSummaries`](/dev/reference/apis/fleet/#listmachinesummaries) | Lists machine summaries for an organization, optionally filtered by fragment IDs, location IDs, and limit. |
| [`GetFragment`](/dev/reference/apis/fleet/#getfragment) | Get a {{< glossary_tooltip term_id="fragment" text="fragment" >}} by ID. |
| [`CreateFragment`](/dev/reference/apis/fleet/#createfragment) | Create a new private {{< glossary_tooltip term_id="fragment" text="fragment" >}}. |
| [`UpdateFragment`](/dev/reference/apis/fleet/#updatefragment) | Update a {{< glossary_tooltip term_id="fragment" text="fragment" >}} name and its config and/or visibility. |
| [`DeleteFragment`](/dev/reference/apis/fleet/#deletefragment) | Delete a {{< glossary_tooltip term_id="fragment" text="fragment" >}}. |
| [`GetFragmentHistory`](/dev/reference/apis/fleet/#getfragmenthistory) | Get fragment history. |
| [`AddRole`](/dev/reference/apis/fleet/#addrole) | Add a role under the organization you are currently authenticated to. |
| [`RemoveRole`](/dev/reference/apis/fleet/#removerole) | Remove a role under the organization you are currently authenticated to. |
| [`ChangeRole`](/dev/reference/apis/fleet/#changerole) | Changes an existing role to a new role. |
| [`ListAuthorizations`](/dev/reference/apis/fleet/#listauthorizations) | List all authorizations (owners and operators) of a specific resource (or resources) within the organization you are currently authenticated to. |
| [`CheckPermissions`](/dev/reference/apis/fleet/#checkpermissions) | Check if the organization, location, or robot your `ViamClient` is authenticated to is permitted to perform some action or set of actions on the resource you pass to the method. |
| [`GetRegistryItem`](/dev/reference/apis/fleet/#getregistryitem) | Get metadata about a registry item (a module, training script, or ML model) by registry item ID. |
| [`CreateRegistryItem`](/dev/reference/apis/fleet/#createregistryitem) | Create a registry item. |
| [`UpdateRegistryItem`](/dev/reference/apis/fleet/#updateregistryitem) | Update a registry item. |
| [`ListRegistryItems`](/dev/reference/apis/fleet/#listregistryitems) | List the registry items in an organization. |
| [`DeleteRegistryItem`](/dev/reference/apis/fleet/#deleteregistryitem) | Delete a registry item. |
| [`CreateModule`](/dev/reference/apis/fleet/#createmodule) | Create a {{< glossary_tooltip term_id="module" text="module" >}} under the organization you are currently authenticated to. |
| [`UpdateModule`](/dev/reference/apis/fleet/#updatemodule) | Update the documentation URL, description, models, entrypoint, and/or the visibility of a {{< glossary_tooltip term_id="module" text="module" >}}. |
| [`UploadModuleFile`](/dev/reference/apis/fleet/#uploadmodulefile) | Upload a {{< glossary_tooltip term_id="module" text="module" >}} file. |
| [`GetModule`](/dev/reference/apis/fleet/#getmodule) | Get a {{< glossary_tooltip term_id="module" text="module" >}} by its ID. |
| [`ListModules`](/dev/reference/apis/fleet/#listmodules) | List the {{< glossary_tooltip term_id="module" text="modules" >}} under the organization you are currently authenticated to. |
| [`CreateKey`](/dev/reference/apis/fleet/#createkey) | Create a new API key. |
| [`DeleteKey`](/dev/reference/apis/fleet/#deletekey) | Delete an API key. |
| [`RotateKey`](/dev/reference/apis/fleet/#rotatekey) | Rotate an API key. |
| [`ListKeys`](/dev/reference/apis/fleet/#listkeys) | List all keys for the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to. |
| [`RenameKey`](/dev/reference/apis/fleet/#renamekey) | RenameKey renames an API key and returns its ID and name. |
| [`CreateKeyFromExistingKeyAuthorizations`](/dev/reference/apis/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations. |
| [`GetAppContent`](/dev/reference/apis/fleet/#getappcontent) | Retrieve the app content for an organization. |
| [`GetAppBranding`](/dev/reference/apis/fleet/#getappbranding) | Retrieves the app branding for an organization or app. |
