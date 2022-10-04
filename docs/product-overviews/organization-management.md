---
title: "The Viam Platform"
linkTitle: "Viam Platform"
weight: 20
type: "docs"
description: "A guide to Viam's organizational hierarchy and permissioning."
---

## Cloud App
<<<<<<< HEAD
Users and organizations store, manage, and control their robotic fleets on the website ([https://app.viam.com](https://app.viam.com)).

## Organization
On Viam ([https://app.viam.com](https://app.viam.com)), robots belong to organizations.
An organization can be an individual, a research group, or a company.

A user can be a member of multiple organizations, but will always be a member of at least one organization.
If a member of an existing organization invites a new user to their organization, that new user's first organization will be the one to which they were invited.
=======
Users and organizations store, manage, and control their robotic fleets on the app's Website ([https://app.viam.com](https://app.viam.com)).

## Organization
On the Viam App ([https://app.viam.com](https://app.viam.com)), robots belong to organizations.
An organization can be an individual, a research group, or a company.

A user can be a member of multiple organizations, but will always be a member of at least one organization.
If a member of an existing organization invites a new user to that organization, then that new user's first organization will be the one to which they were invited.
>>>>>>> 4e407ac5f01641b10208e8482941a8785dac4e8c
If a user creates an account on their own (that is, without being invited to an existing organization), an organization will be created for them with membership of one and a name that matches that of their user account (which can be modified later).

Any member of an organization can invite new users to that organization.
Additionally, users can create additional organizations at any point in time.
<<<<<<< HEAD
For example, if a user has robots at home, and also has robots at school, that user would likely belong to two organizations to keep those use cases separate (a home organization and also a school organization).
=======
For example, if a user has robots at home, and also has robots at school, that user would likely belong to two organizations to keep those use cases separate (a home organization and a school organization).
>>>>>>> 4e407ac5f01641b10208e8482941a8785dac4e8c

## Locations
Locations live within organizations. All robots belong to a location.
Locations allow organizations to sort and manage their robot fleets.
Organizations often contain several locations.
For example, Cool Robot Inc, which is one organization, may have three warehouses (in NYC, LA, and Chicago). Cool Robot Inc could organize its robots into three locations based on their physical presence in a given warehouse. 
<<<<<<< HEAD
With that said, locations do not need to align with physical locations in the real world. Locations are simply a way to subdivide and manage robot fleets.
For example, some users may choose to use locations with names such as "production" and "testing" to separate their robots by development stage (rather than by physical location).
=======
With that said, locations do not need to align with physical locations in the real world. Locations are simply a way to subdivide and mange robot fleets.
For example, some users may choose to use locations with names like "production" and "testing" to separate their robots by development stage (rather than by physical location).
>>>>>>> 4e407ac5f01641b10208e8482941a8785dac4e8c

In some cases, locations alone may be insufficiently granular.
When locations are insufficiently granular, users can create sublocations.
Sublocations allow users to further segment their robot fleet.
<<<<<<< HEAD
Revisiting the Cool Robot Inc example above, the company has expanded its fleet and now has two warehouses in NYC, “warehouse A” and “warehouse B.” The two warehouses can each be a sublocation under the NYC location, allowing the company to organize and control robots based on their specific warehouse sublocation as well as more broadly based on their city location. 
=======
Revisiting the Cool Robot Inc example above, the company has expanded its fleet and now has two warehouses in NYC, “warehouse A” and “warehouse B.” The tw warehouses can each be a sublocation under the NYC location, allowing the company to organize and control robots based on their specific warehouse sublocation as well as more broadly based on their city location. 
>>>>>>> 4e407ac5f01641b10208e8482941a8785dac4e8c

Currently (subject to change), robots' access permissions are granted at the location level.
If an organization invites external contributors or partner organizations to collaborate on robots, then they will share an entire location and its sublocations with those users or organizations.
This grants the external collaborators access to every robot at that location.

## Robots and Their Parts 
Viam robots are composed of parts.
<<<<<<< HEAD
Each part typically corresponds to an individual computer (e.g., Raspberry Pi, Jetson, Arduino) running an instance of the viam-server.
A robot may be comprised of only one part. Take, for example, a simple wheeled rover with a camera, controlled by a Raspberry Pi. 
This is considered a single-part robot because it only contains one computer running viam-server, regardless of how many components it has.
Meanwhile, a more sophisticated robot, like an autonomous forklift, may consist of multiple computers (or multiple parts).
This forklift could have one main computer for decision making, a second for image processing, and a third for locomotion and actuation.
In this example, the autonomous forklift is a single robot composed of three parts.
If there were multiple forklifts, then each forklift would be a robot (each composed of three parts).

When a robot has multiple parts, one part must be designated the main part and the other parts are sub-parts. The main part and sub-parts are linked via the `remotes` section of the main part’s configuration JSON. Typically, the main part will receive connections from client applications and ferry API requests to the sub-parts as needed.
=======
Parts typically correspond to an individual computer (e.g., Raspberry Pi, Jetson, Arduino) running an instance of the viam-server.
A simple robot, like a rover with four wheels and a camera, may consist of one computer (or one part).
Meanwhile, a more sophisticated robot, like an autonomous forklift, may consist of multiple computers (or multiple parts).
This forklift could have one main computer for decision-making, a second for image-processing, and a third for locomotion and actuation.
In this example, the autonomous forklift is a single robot composed of three parts.
If there were multiple forklifts, then each forklift would be a robot (each composed of three parts).

When a robot has multiple parts, one part must be designated the main part and the other parts would be sub-parts. The main part and sub-parts are linked via the `remotes` section of the main part’s configuration JSON. Typically, the main part will receive connections from client applications and ferry API requests to the sub-parts as needed.
>>>>>>> 4e407ac5f01641b10208e8482941a8785dac4e8c

For more on configuring robots and their parts see [Viam's Robot Configuration](../../getting-started/robot-config/).
