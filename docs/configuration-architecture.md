---
title: Viam Configuration Architecture
summary: High level overview of the configuration architecture for Viam's robotics platform
authors:
    - Matt Dannenberg
date: 2022-04-08
---
# app.viam and Robot Organizational Hierarchy

## Cloud App
Viam’s fleet management website, app.viam.com, is the place for users and organizations to store, manage, and control their robotic fleets.

## Organization
On [app.viam.com](https://app.viam.com/), robots belong to organizations. An organization is usually a company, a research group, or an individual (if an individual is building with Viam).

A user account on [app.viam.com](https://app.viam.com/) can be a member of many organizations and will always be a member of at least one organization. If the new user was invited to [app.viam.com](https://app.viam.com/) via an existing organization, their first organization will be that which invited them. If the new user signed up on their own (that is, without an invite from an existing organization), an organization will be created for them, containing only them and named for their user account (this name can be modified later if the user so desires).

Any member of an organization can invite new members to that organization. Users can create new organizations at any point with the click of a button. For example, if a user has personal robots at home but is also working on some robots at school with a team, they would likely belong to two separate organizations to keep those use cases apart.

## Locations
All robots belong to a location. The purpose of these locations is for an organization to sort and manage their fleet. Organizations can and often do have several locations. For example, Cool Robot Inc may have three warehouses (in NYC, LA, and Chicago), and create a location corresponding with each one containing the robots which reside in that physical warehouse. It is not necessary for locations on [app.viam.com](https://app.viam.com/) to align with physical locations in the real world; they are simply a way to subdivide your robot fleet for easier management. For example, some users use locations with the names "production" and "testing" to keep their robots clearly separated.

In some cases, locations alone may be insufficiently granular. For this, we’ve provided the concept of sublocations. Sub locations allow you to further divide your robotic fleet. Expanding on the example above, Cool Robot Inc has expanded their fleet and now has two warehouses in NYC. They are then able to add sublocations to NYC named “warehouse A” “warehouse B.” This allows them to keep their robots aligned with the locations they are in, while still allowing them to address all NYC robots once.

Currently (Note: subject to change), access permissions for robots are granted at the location level. If an organization wishes to invite external contributors or partner organizations to collaborate on robots, they share an entire location with that organization or user. This grants the external collaborators access to every robot at that location.

## Robots and Their Parts 
Robots in Viam are composed of parts. Parts typically correspond to individual compute units (ex, pi, jetson, arduino) running an instance of the viam-server. A simple robot may contain a single part. For example, a rover with four wheels and a camera all attached to a single Raspberry Pi. Meanwhile, a more sophisticated robot, like an autonomous forklift, could consist of multiple computers and therefore multiple parts. This forklift could be one main computer handling the decisions making, one with cameras for image processing, and a third for locomotion and actuating the forklift itself. 

Most often, a robot will be a single system in which all of its parts work together. So the autonomous forklift above is a single robot made up of three parts, but if there were multiple forklifts, each forklift would be a robot (ten forklifts, ten robots, each composed of three parts).

One part of the robot must be designated the main part and the other parts will be children of that main part or children of those children. These non-main parts are linked to the main part via the `remotes` section of the main part’s configuration JSON. Typically, the main part will be the one receiving connections from client applications and ferrying API requests to the other parts as needed. 

## Resources
Parts themselves are composed of resources. The most common types of resources in Viam are components, services, and remotes:

* Components are the physical pieces of the robot (ex, motors, arms, cameras).

* Services are libraries providing algorithms or higher level functionality (ex, navigation, SLAM, or object manipulation).

* Remotes are other parts of the robot. Adding a remote to a part allows the user to treat any resource of the remote part as though it were local to the part, thus connecting them.

Components have Types which indicate the API for that component (ex, arm, motor, etc). They also have Models, which indicate which implementation should be used to actuate with them. For example, an arm component could be a UR5 or an xArm and the appropriate implementation is indicated by selecting the corresponding Model. These component implementations can come from a few different sources. The most common models of a component will have implementations in RDK, which can be selected from the Model dropdown of the configuration UI. If the Model you are working with is not supported in RDK, you’ll have to write your own component driver in one of Viam’s SDKs. For example, a component you are using may have an existing Python library. In that case, you could use Viam’s Python SDK to wrap the existing component library in Viam’s API for that component Type using a few short lines of Python. If no library currently exists, you will have to write a full driver for that component’s API in the language of your choice using the Viam SDK for that language. 
