### Infer



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `tensors` [(Tensors)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/ml#tensors):

**Returns:**

- `ml` [(Tensors)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/ml#ml):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

### Metadata



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `a` [(MLMetadata)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

### CurrentPosition



**Parameters:**

- `context` [(Context)](https://pkg.go.dev/context#context):

**Returns:**

- `referenceframe` [(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Localizer).

### Move



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `componentName` [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/resource#componentName):
- `referenceframe` [(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `referenceframe` [(WorldState)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `pb` [(Constraints)](https://pkg.go.dev/go.viam.com/api/service/motion/v1#pb):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(bool)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

### MoveOnMap



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `req` [(MoveOnMapReq)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(ExecutionID)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

### MoveOnGlobe



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `req` [(MoveOnGlobeReq)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(ExecutionID)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

### GetPose



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `componentName` [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/resource#componentName):
- `destinationFrame` [(string)](<INSERT PARAM TYPE LINK>)
- `referenceframe` [(LinkInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `referenceframe` [(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

### StopPlan



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `req` [(StopPlanReq)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

### ListPlanStatuses



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `req` [(ListPlanStatusesReq)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `[]<a` [(PlanStatusWithID)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

### GetPlan



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `req` [(PlanHistoryReq)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `[]<a` [(PlanWithStatus)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

### GetMode



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(Mode)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### SetMode



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `mode` [(Mode)](<INSERT PARAM TYPE LINK>)
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### GetLocation



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `spatialmath` [(GeoPose)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/spatialmath#spatialmath):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### GetWaypoints



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `[]<a` [(Waypoint)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### AddWaypoint



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `geo` [(Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#geo):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### RemoveWaypoint



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `id` [(ObjectID)](https://pkg.go.dev/go.mongodb.org/mongo-driver/bson/primitive#id):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### GetObstacles



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `spatialmath` [(GeoObstacle)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/spatialmath#spatialmath):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### GetPaths



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `[]*<a` [(Path)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### GetProperties



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `a` [(Properties)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

### GetPosition



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `spatialmath` [(Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/spatialmath#spatialmath):
- `a` [(string)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

### GetPointCloudMap



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `returnEditedMap` [(bool)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

### GetInternalState



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

### GetProperties



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `a` [(Properties)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

### GetDetectionsFromCamera



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `cameraName` [(string)](<INSERT PARAM TYPE LINK>)
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `objectdetection` [(Detection)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/vision/objectdetection#objectdetection):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

### GetDetections



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `img` [(Image)](https://pkg.go.dev/image#img):
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `objectdetection` [(Detection)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/vision/objectdetection#objectdetection):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

### GetClassificationsFromCamera

classifier methods

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `cameraName` [(string)](<INSERT PARAM TYPE LINK>)
- `n` [(int)](<INSERT PARAM TYPE LINK>)
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `classification` [(Classifications)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/vision/classification#classification):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

### GetClassifications



**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `img` [(Image)](https://pkg.go.dev/image#img):
- `n` [(int)](<INSERT PARAM TYPE LINK>)
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `classification` [(Classifications)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/vision/classification#classification):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

### GetObjectPointClouds

segmenter methods

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `cameraName` [(string)](<INSERT PARAM TYPE LINK>)
- `extra map[<a` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `viz` [(Object)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/vision#viz):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

