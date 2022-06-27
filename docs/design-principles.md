---
title: Viam Design Principles
summary: High level overview of the design princples that drive Viam's development
authors:
    - Matt Dannenberg
date: 2022-04-08
---
# Viam Design Principles

## Simplicity  
#### Getting Started
* With a robot in hand, you can configure and control it in the UI in a matter of minutes.

* Writing your first code using the robot only takes a few minutes more.

#### Fleet Management 
* Managing a fleet of robots is easy, and you never have to worry about security.

* You control when updates roll out to your robots. 

#### Debugging
* Debugging hardware and software together is frustrating. Viam is designed to make this easier

    * Logs can be viewed remotely in app.viam.com 

    * At every step of a chain you can debug or try commands manually.

    * You have access to to standard linux services and tools

    * Every viam-server exposes it’s own UI for debugging

* As your robot moves into production, understanding what, why, and when things happen and go wrong is easy and intuitive.

#### Extensibility
* It is easy and logical to add more features to your robot

* It is easy to test different versions of the same type of hardware without having to change your code

## Flexibility 
* Our tools are designed to be intuitive for developers with no prior experience in hardware or robotics, while being battle hardened for production environments

    * Our services are designed to abstract away the hard problems in robotics (SLAM, Vision, Motion Planning) and support most use cases

* Multiple entry points so that users can choose how to engage

    * Users can configure and control their robot via either our UI or by writing code. For users writing code, they have the option to leverage our services and existing drivers of our APIs or use their own custom algorithms and hardware implementations. These options mean that our users can be high school students just learning about software or trained roboticists with decades of experience.

## Over the wire protocols & standards
* At the heart of the Viam platform is a standard api specification. 

    * We provide an API for every category of hardware (eg: arm, motor, gantry),  that outlines methods that make it easy to program against that hardware

        * For example, the `arm` api has methods like “GetPosition” and “MovetoPosition” that allows the user to understand and manipulate the position of the end of a robotic arm

    * These APIs are opinionated, but have enough hooks and escape valves so that you’ll never get stuck.

        * In the example above, if a user would like to move their robotic arm without using Viam’s motion planning service, they would be able to via the “MovetoJointPositions” method which allows them to set joint positions explicitly

    * Doing this over a standard API using a well known protocol (GRPC) means that you’ll be able to use the language you want, and use components that may or may not be from Viam.

    * It also means that hardware can come pre-installed with these APIs even if they don’t use any Viam software.

* The APIs are all RPC, and some specific ones have streaming options.

    * RPC is the most flexible and easy to debug way of working with various pieces of systems.

    * Streaming interfaces are useful for status methods

        * For example, streaming ArmStatus would surface an arm’s joint positions and location of its end. This is analogous to subscribing to a topic in a typical ROS-based pub/sub architecture 

    * If there are areas where performance of complex algorithms is a concern, we make it easy to cache complex structures to avoid any extra latency.

* We provide idiomatic SDKs in every language. These allow easy access to your robot, and the ability to easily implement any new piece of hardware.

    * Unlike traditional robotics software tools, users are not beholden to python or C++

    * Let’s imagine that you are developing your robot in Go, but have a camera that has an existing python driver. You can program your business logic in Go, but then wrap the python driver in our python SDK, exposing it to the rest of the ecosystem easily.

## Security
* Security is paramount for us, as it should be for all robotics projects. 

* Everything in Viam is secure by default, including storing authentication requirements and end-to-end encryption. 

* App.viam.com allows users to set who can access each robot, ensuring that all camera or sensor data remains secure and private.

