---
title: Orientation Vector
summary: Orientation Vector
authors:
    - Eliot Horowitz
date: 2022-6-09
---


# Summar
Viam's orientation vector is a method for describing the position and orientation of an object in 3d space.

# Basics
Orientation vectors are composted of 7 attributed
- X, Y, Z are linear offsets from the 0,0,0 measure in millimeters
- RX, RY, RZ - define a vector from the center of the object to an arbitrary point that is easy to measure. This defines the direction something is pointing in
- Theta - describes the rotation around that vector

# Example
Imagine a room with a camera in it.
One needs to know where in the room the camera is, and where it's pointing.
X, Y, Z are simple the measurements from the corner of the room.
To figure out RX, RY, and RZ you take a picture with the camera, determine the point in the very center of the image, and measure the x, y, z of that point from the corner, and that becomes RX, RY, and RZ. 
Theta is measured by looking at the picture and changing until down is correct, likely 0, 90 or 180.

# Why we like it
- Easy to measure 
- No protractor needed
- Rotation is pulled out (As theta) which is often used independatly (think wrist)




