---
title: Viam High Level Overview
summary: High level overview of Viam's robotics platform
authors:
    - Matt Dannenberg
date: 2022-05-19
---
# Coming soon!
This page has a fairly verbose outline, just gotta make it into proper paragraphs with some guiding examples:
- A robot is a computer which:
  - Takes in information about its environment to make decisions
  - Acts on its environment 
  - Or both
- In viam robots are made up of parts
  - Each part is a discrete compute unit
  - Each part runs a viam server process
  - Each process takes in a config which describes its:
    - Components: the hardware attached to it
    - Services: viam-built algorithms (nav, computer vision, etc)
    - Remotes: the other parts of the robot for this one to connect to
- Parts communicate with one another over webrtc using grpc/protobuf APIs, which enables:
  - Consistent APIs across all hardware
  - SDK libraries in any language you desire
  - Direct secure connections to and between parts
  - Access to the whole robot via just one of its parts
- To get started, install the viam-server service on an SBC (ex, rPi) and connect it to app.viam.com, which will provide you with:
  - A nice UI for writing the robot configs
  - Logs
  - Boilerplate connection code for your robot using an SDKs
  - Web control interface which lets you actuate your hardware using a graphical UI on top of our standard APIs 
  - Doesnt exist yet but: package updates, data retention, block coding interface
  - Using app.viam also automatically supplies your robot with certs for secure connection
- This control interface is neat, but how do I make my robot autonomous?
  - SDK-based applications
  - These can be run locally on one part of the robot or on an entirely separate computer (like your laptop)
  - Same APIs as the webUI you’ve been playing with
  - <diagram of comms flow>
- I have some fancy new piece of hardware yall dont support.
  - Use the SDK to subclass a component type and write your own implementation
  - If there is an existing library this can be done in dozens of lines of code
  - In addition to the component implementation, you’ll want to write a small SDK application which spins up a server containing that component
    - Your part can manage this process and will expose the api same as all your other components
- Managing your fleet (more on app.viam’s organizational structure)
  - Users are members of orgs
  - Orgs have locations
  - Robots reside in locations
    - May be physical, may be separate by development environment (ex, testing, prod)
