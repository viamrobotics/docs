---
title: Robot Configuartion File
summary: An explanation of viam's JSON configuration file format; the top level fields, their meanings, and example entries.
authors:
    - Matt Dannenberg
date: 2022-04-18, 2022-05-19
---
# Robot Configuration

## Resources
Parts themselves are composed of resources. The most common types of resources in Viam are components, services, and remotes:

* Components are the physical pieces of the robot (ex, motors, arms, cameras).

* Services are libraries providing algorithms or higher level functionality (ex, navigation, SLAM, or object manipulation).

* Remotes are other parts of the robot. Adding a remote to a part allows the user to treat any resource of the remote part as though it were local to the part, thus connecting them.

Components have Types which indicate the API for that component (ex, arm, motor, etc). They also have Models, which indicate which implementation should be used to actuate with them. For example, an arm component could be a UR5 or an xArm and the appropriate implementation is indicated by selecting the corresponding Model. These component implementations can come from a few different sources. The most common models of a component will have implementations in RDK, which can be selected from the Model dropdown of the configuration UI. If the Model you are working with is not supported in RDK, you’ll have to write your own component driver in one of Viam’s SDKs. For example, a component you are using may have an existing Python library. In that case, you could use Viam’s Python SDK to wrap the existing component library in Viam’s API for that component Type using a few short lines of Python. If no library currently exists, you will have to write a full driver for that component’s API in the language of your choice using the Viam SDK for that language. 

## Running a robot on the RDK
When the RDK starts, it uses the secret in its cloud configuration file to ask app.viam.com for its robot configuration (see Runtime architecture).

Next, the configuration is parsed and processed section by section specified in the JSON config fields, notably remotes, components, services, and processes.

#### Remotes
Remotes represent a connection to another robot part comprising the whole robot.

Initializing a remote involves establishing a network connection to that robot either over direct gRPC or gRPC via WebRTC.

Once established, the part making the connection will request information from the remote part about what components and services it offers (resource discovery) and from there on out will treat those resources as it treats its own local resources. That is, a user connecting to this part will see the components and services as if they were a resource of this part.

This allows for creating a single part that can handle or direct all operations/commands sent to it, even those components which belong to another part, providing for various network and compute topologies.

#### Processes
Processes are simply binaries or scripts that the RDK will run either once or indefinitely and maintain for the lifetime of the RDK. Two typical examples are: one, running an SDK server like the Python SDK where the implementation of a component is easier to create than the RDK; and two, a camera server that has the appropriate system driver to talk to the camera and communicate results over the wire.

#### Components and Services
Both components and services are part of the resource hierarchy and the RDK is packaged with a supported set of implementations (similar to drivers) for each component and service.

###### Components
The components are by default initialized in the order they are specified in the JSON config file fetched from the cloud. Changing the initialization order involves use of the depends_on field to create dependency relationships between components.

Initializing a component consults the component subtype (e.g. arm) and the model of the component (e.g. ur5e) in the packaged registry on how to construct and configure it.

Each component will have access to the other components that it depends on when it gets constructed. As components get reconfigured, the handle that one component has on another is kept intact for uninterrupted use.

###### Services
Once components are initialized, service initialization begins and strictly follows the order that the services were listed in.

