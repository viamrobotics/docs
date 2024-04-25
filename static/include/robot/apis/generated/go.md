### DiscoverComponents

DiscoverComponents returns discovered component configurations.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `resource` [(DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/resource#resource):

**Returns:**

- `resource` [(Discovery)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/resource#resource):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

### FrameSystemConfig

FrameSystemConfig returns the individual parts that make up a robot's [frame](/mobility/frame-system/) system

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `framesystem` [(Config)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/robot/framesystem#framesystem):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

### TransformPose

TransformPose will transform the pose of the requested poseInFrame to the desired [frame](/mobility/frame-system/) in the robot's [frame](/mobility/frame-system/) system.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `referenceframe` [(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `dst` [(string)](<INSERT PARAM TYPE LINK>)
- `referenceframe` [(LinkInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `` [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `referenceframe` [(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/referenceframe#referenceframe):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

### TransformPCD

TransformPointCloud will transform the pointcloud to the desired [frame](/mobility/frame-system/) in the robot's [frame](/mobility/frame-system/) system.Do not move the robot between the generation of the initial pointcloud and the receiptof the transformed pointcloud because that will make the transformations inaccurate.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `srcpc` [(PointCloud)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/pointcloud#srcpc):
- `` [(srcName)](<INSERT PARAM TYPE LINK>)
- `dstName` [(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- `pointcloud` [(PointCloud)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/pointcloud#pointcloud):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

### GetStatus

Status takes a list of resource names and returns their corresponding statuses. If no names are passed in, return all statuses.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `resource` [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/resource#resource):

**Returns:**

- `[]<a` [(Status)](<INSERT PARAM TYPE LINK>)
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

### GetCloudMetadata

CloudMetadata returns app-related information about the robot.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `cloud` [(Metadata)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/cloud#cloud):
- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

### Close

Close attempts to cleanly close down all constituent parts of the robot.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

### StopAll

StopAll cancels all current and outstanding operations for the robot and stops all actuators and movement

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#ctx):
- `resource` [(string)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/resource#resource):

**Returns:**

- `a` [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

