<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetUserIDByEmail`](/reference/apis/fleet/#getuseridbyemail) | Get the ID of a user by email. |
| [`CreateOrganization`](/reference/apis/fleet/#createorganization) | Create an organization. |
| [`ListOrganizations`](/reference/apis/fleet/#listorganizations) | List the {{< glossary_tooltip term_id="organization" text="organizations" >}} the user is an authorized user of. |
| [`GetOrganizationsWithAccessToLocation`](/reference/apis/fleet/#getorganizationswithaccesstolocation) | Get all organizations that have access to a location. |
| [`ListOrganizationsByUser`](/reference/apis/fleet/#listorganizationsbyuser) | List the organizations a user belongs to. |
| [`GetOrganization`](/reference/apis/fleet/#getorganization) | Retrieve the organization object for the requested organization containing the organization's ID, name, public namespace, and more. |
| [`GetOrganizationNamespaceAvailability`](/reference/apis/fleet/#getorganizationnamespaceavailability) | Check the availability of an {{< glossary_tooltip term_id="organization" text="organization" >}} namespace. |
| [`UpdateOrganization`](/reference/apis/fleet/#updateorganization) | Updates organization details. |
| [`DeleteOrganization`](/reference/apis/fleet/#deleteorganization) | Delete an organization. |
| [`ListOrganizationMembers`](/reference/apis/fleet/#listorganizationmembers) | List the members and invites of the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to. |
| [`CreateOrganizationInvite`](/reference/apis/fleet/#createorganizationinvite) | Create an {{< glossary_tooltip term_id="organization" text="organization" >}} invite and send it by email. |
| [`UpdateOrganizationInviteAuthorizations`](/reference/apis/fleet/#updateorganizationinviteauthorizations) | Update (add or remove) the authorizations attached to an organization invite that has already been created. |
| [`DeleteOrganizationMember`](/reference/apis/fleet/#deleteorganizationmember) | Remove a member from the {{< glossary_tooltip term_id="organization" text="organization" >}} you are currently authenticated to. |
| [`DeleteOrganizationInvite`](/reference/apis/fleet/#deleteorganizationinvite) | Delete a pending organization invite to the organization you are currently authenticated to. |
| [`ResendOrganizationInvite`](/reference/apis/fleet/#resendorganizationinvite) | Resend a pending organization invite email. |
| [`GetOrganizationMetadata`](/reference/apis/fleet/#getorganizationmetadata) | Gets the user-defined metadata for an organization. |
| [`UpdateOrganizationMetadata`](/reference/apis/fleet/#updateorganizationmetadata) | Updates the user-defined metadata for an organization. |
| [`CreateLocation`](/reference/apis/fleet/#createlocation) | Create and name a {{< glossary_tooltip term_id="location" text="location" >}} under the organization you are currently authenticated to. |
| [`GetLocation`](/reference/apis/fleet/#getlocation) | Get a {{< glossary_tooltip term_id="location" text="location" >}} by its location ID. |
| [`UpdateLocation`](/reference/apis/fleet/#updatelocation) | Change the name of a {{< glossary_tooltip term_id="location" text="location" >}} and/or assign a parent location to a location. |
| [`DeleteLocation`](/reference/apis/fleet/#deletelocation) | Delete a {{< glossary_tooltip term_id="location" text="location" >}}. |
| [`ListLocations`](/reference/apis/fleet/#listlocations) | Get a list of all {{< glossary_tooltip term_id="location" text="locations" >}} under the organization you are currently authenticated to. |
| [`ShareLocation`](/reference/apis/fleet/#sharelocation) | Share a location with an organization. |
| [`UnshareLocation`](/reference/apis/fleet/#unsharelocation) | Stop sharing a location with an organization. |
| [`LocationAuth`](/reference/apis/fleet/#locationauth) | Get a location’s `LocationAuth` (location secret or secrets). |
| [`CreateLocationSecret`](/reference/apis/fleet/#createlocationsecret) | Create a new location secret. |
| [`DeleteLocationSecret`](/reference/apis/fleet/#deletelocationsecret) | Delete a location secret. |
| [`GetLocationMetadata`](/reference/apis/fleet/#getlocationmetadata) | Get the user-defined metadata for a location. |
| [`UpdateLocationMetadata`](/reference/apis/fleet/#updatelocationmetadata) | Update the user-defined metadata for a location. |
| [`GetRobot`](/reference/apis/fleet/#getrobot) | Get a {{< glossary_tooltip term_id="machine" text="machine" >}} by its ID. |
| [`GetRobotAPIKeys`](/reference/apis/fleet/#getrobotapikeys) | Gets the API keys for the machine. |
| [`GetRobotParts`](/reference/apis/fleet/#getrobotparts) | Get a list of all the {{< glossary_tooltip term_id="part" text="parts" >}} under a specific {{< glossary_tooltip term_id="machine" text="machine" >}}. |
| [`GetRobotPart`](/reference/apis/fleet/#getrobotpart) | Get a specific machine {{< glossary_tooltip term_id="part" text="part" >}} including its part config, part address, and other information. |
| [`GetRobotPartLogs`](/reference/apis/fleet/#getrobotpartlogs) | Get the logs associated with a specific machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`GetRobotPartByNameAndLocation`](/reference/apis/fleet/#getrobotpartbynameandlocation) | Query a specific robot part by name and location id. |
| [`TailRobotPartLogs`](/reference/apis/fleet/#tailrobotpartlogs) | Get an asynchronous iterator that receives live machine part logs. |
| [`GetRobotPartHistory`](/reference/apis/fleet/#getrobotparthistory) | Get a list containing the history of a machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`UpdateRobotPart`](/reference/apis/fleet/#updaterobotpart) | Change the name of and assign an optional new configuration to a machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`NewRobotPart`](/reference/apis/fleet/#newrobotpart) | Create a new machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`DeleteRobotPart`](/reference/apis/fleet/#deleterobotpart) | Delete the specified machine {{< glossary_tooltip term_id="part" text="part" >}}. |
| [`MarkPartAsMain`](/reference/apis/fleet/#markpartasmain) | Mark a machine part as the _main_ part of a machine. |
| [`MarkPartForRestart`](/reference/apis/fleet/#markpartforrestart) | Mark a specified machine part for restart. |
| [`CreateRobotPartSecret`](/reference/apis/fleet/#createrobotpartsecret) | Create a machine {{< glossary_tooltip term_id="part" text="part" >}} secret. |
| [`DeleteRobotPartSecret`](/reference/apis/fleet/#deleterobotpartsecret) | Delete a machine part secret. |
| [`ListRobots`](/reference/apis/fleet/#listrobots) | Get a list of all machines in a specified location. |
| [`NewRobot`](/reference/apis/fleet/#newrobot) | Create a new {{< glossary_tooltip term_id="machine" text="machine" >}}. |
| [`UpdateRobot`](/reference/apis/fleet/#updaterobot) | Update an existing machine's name and/or location. |
| [`DeleteRobot`](/reference/apis/fleet/#deleterobot) | Delete a specified machine. |
| [`GetRobotMetadata`](/reference/apis/fleet/#getrobotmetadata) | Gets the user-defined metadata for a machine. |
| [`GetRobotPartMetadata`](/reference/apis/fleet/#getrobotpartmetadata) | Gets the user-defined metadata for a machine part. |
| [`UpdateRobotMetadata`](/reference/apis/fleet/#updaterobotmetadata) | Updates the user-defined metadata for a machine. |
| [`UpdateRobotPartMetadata`](/reference/apis/fleet/#updaterobotpartmetadata) | Updates the user-defined metadata for a machine part. |
| [`ListFragments`](/reference/apis/fleet/#listfragments) | Get a list of {{< glossary_tooltip term_id="fragment" text="fragments" >}} in the organization you are currently authenticated to. |
| [`ListMachineFragments`](/reference/apis/fleet/#listmachinefragments) | Get a list of top level and nested {{< glossary_tooltip term_id="fragment" text="fragments" >}} for a machine, as well as additionally specified fragment IDs. |
| [`ListMachineSummaries`](/reference/apis/fleet/#listmachinesummaries) | Lists machine summaries for an organization, optionally filtered by fragment IDs, location IDs, and limit. |
| [`GetFragment`](/reference/apis/fleet/#getfragment) | Get a {{< glossary_tooltip term_id="fragment" text="fragment" >}} by ID. |
| [`CreateFragment`](/reference/apis/fleet/#createfragment) | Create a new private {{< glossary_tooltip term_id="fragment" text="fragment" >}}. |
| [`UpdateFragment`](/reference/apis/fleet/#updatefragment) | Update a {{< glossary_tooltip term_id="fragment" text="fragment" >}} name and its config and/or visibility. |
| [`DeleteFragment`](/reference/apis/fleet/#deletefragment) | Delete a {{< glossary_tooltip term_id="fragment" text="fragment" >}}. |
| [`GetFragmentHistory`](/reference/apis/fleet/#getfragmenthistory) | Get fragment history. |
| [`AddRole`](/reference/apis/fleet/#addrole) | Add a role under the organization you are currently authenticated to. |
| [`RemoveRole`](/reference/apis/fleet/#removerole) | Remove a role under the organization you are currently authenticated to. |
| [`ChangeRole`](/reference/apis/fleet/#changerole) | Changes an existing role to a new role. |
| [`ListAuthorizations`](/reference/apis/fleet/#listauthorizations) | List all authorizations (owners and operators) of a specific resource (or resources) within the organization you are currently authenticated to. |
| [`CheckPermissions`](/reference/apis/fleet/#checkpermissions) | Check if the organization, location, or robot your `ViamClient` is authenticated to is permitted to perform some action or set of actions on the resource you pass to the method. |
| [`GetRegistryItem`](/reference/apis/fleet/#getregistryitem) | Get metadata about a registry item (a module, training script, or ML model) by registry item ID. |
| [`CreateRegistryItem`](/reference/apis/fleet/#createregistryitem) | Create a registry item. |
| [`UpdateRegistryItem`](/reference/apis/fleet/#updateregistryitem) | Update a registry item. |
| [`ListRegistryItems`](/reference/apis/fleet/#listregistryitems) | List the registry items in an organization. |
| [`DeleteRegistryItem`](/reference/apis/fleet/#deleteregistryitem) | Delete a registry item. |
| [`CreateModule`](/reference/apis/fleet/#createmodule) | Create a {{< glossary_tooltip term_id="module" text="module" >}} under the organization you are currently authenticated to. |
| [`UpdateModule`](/reference/apis/fleet/#updatemodule) | Update the documentation URL, description, models, entrypoint, and/or the visibility of a {{< glossary_tooltip term_id="module" text="module" >}}. |
| [`UploadModuleFile`](/reference/apis/fleet/#uploadmodulefile) | Upload a {{< glossary_tooltip term_id="module" text="module" >}} file. |
| [`GetModule`](/reference/apis/fleet/#getmodule) | Get a {{< glossary_tooltip term_id="module" text="module" >}} by its ID. |
| [`ListModules`](/reference/apis/fleet/#listmodules) | List the {{< glossary_tooltip term_id="module" text="modules" >}} under the organization you are currently authenticated to. |
| [`CreateKey`](/reference/apis/fleet/#createkey) | Create a new API key. |
| [`DeleteKey`](/reference/apis/fleet/#deletekey) | Delete an API key. |
| [`RotateKey`](/reference/apis/fleet/#rotatekey) | Rotate an API key. |
| [`ListKeys`](/reference/apis/fleet/#listkeys) | List all keys for the {{< glossary_tooltip term_id="organization" text="organization" >}} that you are currently authenticated to. |
| [`RenameKey`](/reference/apis/fleet/#renamekey) | RenameKey renames an API key and returns its ID and name. |
| [`CreateKeyFromExistingKeyAuthorizations`](/reference/apis/fleet/#createkeyfromexistingkeyauthorizations) | Create a new API key with an existing key’s authorizations. |
| [`GetAppContent`](/reference/apis/fleet/#getappcontent) | Retrieve the app content for an organization. |
| [`GetAppBranding`](/reference/apis/fleet/#getappbranding) | Retrieves the app branding for an organization or app. |
