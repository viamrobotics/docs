---
title: Viam Configuration Architecture
summary: High level overview of the configuration architecture for Viam's robotics platform
authors:
    - Matt Dannenberg
date: 2022-04-08
---
# Configuration Architecture

The top-level organization unit in Viam is called an organization. An organization is usually a company, or a person (if an individual is building with Viam). An organization will have one method for billing, users, etc…

Within an organization, you can have multiple locations. Locations let you organize your robots. A location generally is based on a physical location, but that is not a requirement. 

You’ll be able to set permissions / configure your robot(s) at the location-level.

Robots all live inside of a location.

A robot is a collection of 1 to any number of computers or pieces.

Usually a robot would be a single system that works together.

E.g. an autonomous forklift that has multiple computers would be 1 robot. If you have 10 of these forklifts in a warehouse, you would have 10 robots.

Every different computer, or processor running a viam-server is called a part.

In our autonomous forklift example, you might have one main computer handling decision-making, another for image processing, and another controlling locomotion. In this case, the main computer would be the main part, and the other parts would automatically become children. A user or client would only ever interact with the main part, and the main part would ferry information as needed.

You can have only 1 part, or any number of parts, with any amount of nesting depth as your application requires, though we think most robots will have 1 to a handful of parts, and we think 3 layers of nesting will be rare.

A part consists of components and services.

Components are all the physical pieces of the robots. These include  motors, gantries, arms, cameras, sensors, etc… For any type of component, you can use:

one of our built-in models

Example: Your robot has a universal robotics arm, and so all you need to do it specify `UR5` as the model of arm in your config

Use an off-the-shelf one as a remote

This would mean that.... 

Write your own in any language using the SDK in the language of your choice

Example: You want to use a specific IMU and its firmware is written in C. You can write a driver against Viam’s IMU API using the C SDK.

Services are algorithms or higher level functionality, such as navigation, SLAM, or object manipulation.

Every component and part in the system can be included in the frame system.

The main part’s world frame is considered the world frame of the robot. 

Every other component in the main frame can be positioned relative to the main world frame, or relative to another component in the main part.

Every other part of the robot by default has its world state set to the world state of the main part. Each part’s components are configured relative to the part's world state.
