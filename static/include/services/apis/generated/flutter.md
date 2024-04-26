### DoCommand

**Parameters:**

- `command` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.generic/GenericServiceClient/doCommand.html).

### Infer

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `inputTensors` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.mlmodel/MLModelServiceClient/infer.html).

### Metadata

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.mlmodel/MLModelServiceClient/metadata.html).

### DoCommand

**Parameters:**

- `command` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/doCommand.html).

### GetPlan

**Parameters:**

- `componentName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `executionId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `lastPlanOnly` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/getPlan.html).

### GetPose

**Parameters:**

- `componentName` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)>:
- `destinationFrame` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)>:
- `extra` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)>:
- `name` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)>:
- `supplementalTransforms` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/getPose.html).

### ListPlanStatuses

**Parameters:**

- `extra` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `name` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `onlyActivePlans` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/listPlanStatuses.html).

### Move

**Parameters:**

- `componentName` [(WorldState)](https://flutter.viam.dev/viam_protos.common.common/WorldState-class.html):
- `constraints` [(WorldState)](https://flutter.viam.dev/viam_protos.common.common/WorldState-class.html):
- `destination` [(WorldState)](https://flutter.viam.dev/viam_protos.common.common/WorldState-class.html):
- `extra` [(WorldState)](https://flutter.viam.dev/viam_protos.common.common/WorldState-class.html):
- `name` [(WorldState)](https://flutter.viam.dev/viam_protos.common.common/WorldState-class.html):
- `worldState` [(WorldState)](https://flutter.viam.dev/viam_protos.common.common/WorldState-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/move.html).

### MoveOnGlobe

**Parameters:**

- `componentName` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:
- `destination` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:
- `extra` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:
- `heading` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:
- `motionConfiguration` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:
- `movementSensorName` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:
- `name` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:
- `obstacles` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/moveOnGlobe.html).

### MoveOnMap

**Parameters:**

- `componentName` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)>:
- `destination` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)>:
- `extra` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)>:
- `motionConfiguration` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)>:
- `name` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)>:
- `obstacles` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)>:
- `slamServiceName` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/moveOnMap.html).

### StopPlan

**Parameters:**

- `componentName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/stopPlan.html).

### AddWaypoint

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `location` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/addWaypoint.html).

### DoCommand

**Parameters:**

- `command` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/doCommand.html).

### GetLocation

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getLocation.html).

### GetMode

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getMode.html).

### GetObstacles

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getObstacles.html).

### GetPaths

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getPaths.html).

### GetProperties

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getProperties.html).

### GetWaypoints

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getWaypoints.html).

### RemoveWaypoint

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/removeWaypoint.html).

### SetMode

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `mode` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/setMode.html).

### DoCommand

**Parameters:**

- `command` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/doCommand.html).

### GetInternalState

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getInternalState.html).

### GetPointCloudMap

**Parameters:**

- `name` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):
- `returnEditedMap` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getPointCloudMap.html).

### GetPosition

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getPosition.html).

### GetProperties

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getProperties.html).

### DoCommand

**Parameters:**

- `command` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/doCommand.html).

### GetClassifications

**Parameters:**

- `extra` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `height` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `image` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `mimeType` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `n` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `name` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `width` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getClassifications.html).

### GetClassificationsFromCamera

**Parameters:**

- `cameraName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `n` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getClassificationsFromCamera.html).

### GetDetections

**Parameters:**

- `extra` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `height` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `image` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `mimeType` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `name` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:
- `width` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>:

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getDetections.html).

### GetDetectionsFromCamera

**Parameters:**

- `cameraName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getDetectionsFromCamera.html).

### GetObjectPointClouds

**Parameters:**

- `cameraName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `mimeType` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html):

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getObjectPointClouds.html).

