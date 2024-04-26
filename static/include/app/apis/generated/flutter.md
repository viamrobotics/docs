### AddRole

**Parameters:**

- `authorization` [(Authorization)](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/addRole.html).

### ChangeRole

**Parameters:**

- `newAuthorization` [(Authorization)](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html):
- `oldAuthorization` [(Authorization)](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/changeRole.html).

### CheckPermissions

**Parameters:**

- `permissions` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[AuthorizedPermissions](https://flutter.viam.dev/viam_protos.app.app/AuthorizedPermissions-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/checkPermissions.html).

### CreateFragment

**Parameters:**

- `config` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createFragment.html).

### CreateKey

**Parameters:**

- `authorizations` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createKey.html).

### CreateKeyFromExistingKeyAuthorizations

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createKeyFromExistingKeyAuthorizations.html).

### CreateLocation

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `parentLocationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createLocation.html).

### CreateLocationSecret

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createLocationSecret.html).

### CreateModule

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createModule.html).

### CreateOrganization

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createOrganization.html).

### CreateOrganizationInvite

**Parameters:**

- `authorizations` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:
- `email` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:
- `organizationId` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:
- `sendEmailInvite` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createOrganizationInvite.html).

### CreateRegistryItem

**Parameters:**

- `name` [(PackageType)](https://flutter.viam.dev/viam_protos.app.packages/PackageType-class.html):
- `organizationId` [(PackageType)](https://flutter.viam.dev/viam_protos.app.packages/PackageType-class.html):
- `type` [(PackageType)](https://flutter.viam.dev/viam_protos.app.packages/PackageType-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createRegistryItem.html).

### CreateRobotPartSecret

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createRobotPartSecret.html).

### DeleteFragment

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteFragment.html).

### DeleteKey

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteKey.html).

### DeleteLocation

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteLocation.html).

### DeleteLocationSecret

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `secretId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteLocationSecret.html).

### DeleteOrganization

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteOrganization.html).

### DeleteOrganizationInvite

**Parameters:**

- `email` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteOrganizationInvite.html).

### DeleteOrganizationMember

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `userId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteOrganizationMember.html).

### DeleteRegistryItem

**Parameters:**

- `itemId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteRegistryItem.html).

### DeleteRobot

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteRobot.html).

### DeleteRobotPart

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteRobotPart.html).

### DeleteRobotPartSecret

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `secretId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteRobotPartSecret.html).

### GetFragment

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getFragment.html).

### GetLocation

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getLocation.html).

### GetModule

**Parameters:**

- `moduleId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getModule.html).

### GetOrganization

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getOrganization.html).

### GetOrganizationNamespaceAvailability

**Parameters:**

- `publicNamespace` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getOrganizationNamespaceAvailability.html).

### GetOrganizationsWithAccessToLocation

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getOrganizationsWithAccessToLocation.html).

### GetRegistryItem

**Parameters:**

- `itemId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRegistryItem.html).

### GetRobot

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobot.html).

### GetRobotAPIKeys

**Parameters:**

- `robotId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotAPIKeys.html).

### GetRobotPart

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotPart.html).

### GetRobotPartHistory

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotPartHistory.html).

### GetRobotPartLogs

**Parameters:**

- `errorsOnly` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `filter` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `levels` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `pageToken` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotPartLogs.html).

### GetRobotParts

**Parameters:**

- `robotId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotParts.html).

### GetUserIDByEmail

**Parameters:**

- `email` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getUserIDByEmail.html).

### ListAuthorizations

**Parameters:**

- `organizationId` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `resourceIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listAuthorizations.html).

### ListFragments

**Parameters:**

- `organizationId` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `showPublic` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listFragments.html).

### ListKeys

**Parameters:**

- `orgId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listKeys.html).

### ListLocations

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listLocations.html).

### ListModules

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listModules.html).

### ListOrganizationMembers

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listOrganizationMembers.html).

### ListOrganizations

**Parameters:**


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listOrganizations.html).

### ListOrganizationsByUser

**Parameters:**

- `userId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listOrganizationsByUser.html).

### ListRegistryItems

**Parameters:**

- `organizationId` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Visibility](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)>:
- `pageToken` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Visibility](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)>:
- `platforms` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Visibility](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)>:
- `searchTerm` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Visibility](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)>:
- `statuses` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Visibility](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)>:
- `types` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Visibility](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)>:
- `visibilities` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Visibility](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listRegistryItems.html).

### ListRobots

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/listRobots.html).

### LocationAuth

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/locationAuth.html).

### MarkPartAsMain

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/markPartAsMain.html).

### MarkPartForRestart

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/markPartForRestart.html).

### NewRobot

**Parameters:**

- `location` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/newRobot.html).

### NewRobotPart

**Parameters:**

- `partName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `robotId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/newRobotPart.html).

### RemoveRole

**Parameters:**

- `authorization` [(Authorization)](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/removeRole.html).

### ResendOrganizationInvite

**Parameters:**

- `email` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/resendOrganizationInvite.html).

### RotateKey

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/rotateKey.html).

### ShareLocation

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/shareLocation.html).

### TailRobotPartLogs

**Parameters:**

- `errorsOnly` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `filter` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/tailRobotPartLogs.html).

### UnshareLocation

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/unshareLocation.html).

### UpdateFragment

**Parameters:**

- `config` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `id` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `name` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `public` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateFragment.html).

### UpdateLocation

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `parentLocationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `region` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateLocation.html).

### UpdateModule

**Parameters:**

- `description` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)<[Model](https://flutter.viam.dev/viam_protos.app.app/Model-class.html)>:
- `entrypoint` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)<[Model](https://flutter.viam.dev/viam_protos.app.app/Model-class.html)>:
- `models` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)<[Model](https://flutter.viam.dev/viam_protos.app.app/Model-class.html)>:
- `moduleId` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)<[Model](https://flutter.viam.dev/viam_protos.app.app/Model-class.html)>:
- `url` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)<[Model](https://flutter.viam.dev/viam_protos.app.app/Model-class.html)>:
- `visibility` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html)<[Model](https://flutter.viam.dev/viam_protos.app.app/Model-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateModule.html).

### UpdateOrganization

**Parameters:**

- `cid` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `publicNamespace` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `region` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateOrganization.html).

### UpdateOrganizationInviteAuthorizations

**Parameters:**

- `addAuthorizations` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:
- `email` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:
- `organizationId` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:
- `removeAuthorizations` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Authorization](https://flutter.viam.dev/viam_protos.app.app/Authorization-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateOrganizationInviteAuthorizations.html).

### UpdateRegistryItem

**Parameters:**

- `description` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html):
- `itemId` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html):
- `type` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html):
- `visibility` [(Visibility)](https://flutter.viam.dev/viam_protos.app.app/Visibility-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateRegistryItem.html).

### UpdateRobot

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `location` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateRobot.html).

### UpdateRobotPart

**Parameters:**

- `id` [(Struct)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(Struct)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `robotConfig` [(Struct)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateRobotPart.html).

### UploadModuleFile

**Parameters:**

- `first` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)>:
- `isBroadcast` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)>:
- `isEmpty` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)>:
- `last` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)>:
- `length` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)>:
- `single` [(Future)](dart-async/Future-class.html)<[int](dart-core/int-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/uploadModuleFile.html).

### AddBinaryDataToDatasetByIDs

**Parameters:**

- `binaryIds` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)>:
- `datasetId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/addBinaryDataToDatasetByIDs.html).

### AddBoundingBoxToImageByID

**Parameters:**

- `binaryId` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html):
- `label` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html):
- `xMaxNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html):
- `xMinNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html):
- `yMaxNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html):
- `yMinNormalized` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/addBoundingBoxToImageByID.html).

### AddTagsToBinaryDataByFilter

**Parameters:**

- `filter` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/addTagsToBinaryDataByFilter.html).

### AddTagsToBinaryDataByIDs

**Parameters:**

- `binaryIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/addTagsToBinaryDataByIDs.html).

### BinaryDataByFilter

**Parameters:**

- `countOnly` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `dataRequest` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `includeBinary` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `includeInternalData` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/binaryDataByFilter.html).

### BinaryDataByIDs

**Parameters:**

- `binaryIds` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)>:
- `includeBinary` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/binaryDataByIDs.html).

### BoundingBoxLabelsByFilter

**Parameters:**

- `filter` [(Filter)](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/boundingBoxLabelsByFilter.html).

### ConfigureDatabaseUser

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `password` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/configureDatabaseUser.html).

### DeleteBinaryDataByFilter

**Parameters:**

- `filter` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `includeInternalData` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/deleteBinaryDataByFilter.html).

### DeleteBinaryDataByIDs

**Parameters:**

- `binaryIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/deleteBinaryDataByIDs.html).

### DeleteTabularData

**Parameters:**

- `deleteOlderThanDays` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/deleteTabularData.html).

### GetDatabaseConnection

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/getDatabaseConnection.html).

### RemoveBinaryDataFromDatasetByIDs

**Parameters:**

- `binaryIds` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)>:
- `datasetId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html)<[BinaryID](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/removeBinaryDataFromDatasetByIDs.html).

### RemoveBoundingBoxFromImageByID

**Parameters:**

- `bboxId` [(BinaryID)](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html):
- `binaryId` [(BinaryID)](https://flutter.viam.dev/viam_protos.app.data/BinaryID-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/removeBoundingBoxFromImageByID.html).

### RemoveTagsFromBinaryDataByFilter

**Parameters:**

- `filter` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/removeTagsFromBinaryDataByFilter.html).

### RemoveTagsFromBinaryDataByIDs

**Parameters:**

- `binaryIds` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/removeTagsFromBinaryDataByIDs.html).

### TabularDataByFilter

**Parameters:**

- `countOnly` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `dataRequest` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `includeInternalData` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/tabularDataByFilter.html).

### TabularDataByMQL

**Parameters:**

- `mqlBinary` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/tabularDataByMQL.html).

### TabularDataBySQL

**Parameters:**

- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `sqlQuery` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/tabularDataBySQL.html).

### TagsByFilter

**Parameters:**

- `filter` [(Filter)](https://flutter.viam.dev/viam_protos.app.data/Filter-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.data/DataServiceClient/tagsByFilter.html).

### CancelTrainingJob

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/cancelTrainingJob.html).

### DeleteCompletedTrainingJob

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/deleteCompletedTrainingJob.html).

### GetTrainingJob

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/getTrainingJob.html).

### ListTrainingJobs

**Parameters:**

- `organizationId` [(TrainingStatus)](https://flutter.viam.dev/viam_protos.app.ml_training/TrainingStatus-class.html):
- `status` [(TrainingStatus)](https://flutter.viam.dev/viam_protos.app.ml_training/TrainingStatus-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/listTrainingJobs.html).

### <NO PROTO FOUND, USING METHOD NAME> submitCustomTrainingJob

**Parameters:**

- `datasetId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `modelName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `modelVersion` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `organizationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `registryItemId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/submitCustomTrainingJob.html).

### SubmitTrainingJob

**Parameters:**

- `datasetId` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `modelName` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `modelType` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `modelVersion` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `organizationId` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:
- `tags` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.ml_training/MLTrainingServiceClient/submitTrainingJob.html).

