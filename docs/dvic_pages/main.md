# ALFRED : General Purpose Middleware for Personal Robotic Arm Assistants

# About

# Abstract

# Article

# Introduction

## Context

## Motivations

- Worker 2.0 & Industry 4.0

Industry 4.0 has recently become the standard for factory automation. Network-controlled, intelligent machines allow for faster production, at lower cost and risk. Robots have become controllable remotely, and as such, the worker in this new type of industry, a "Worker 2.0", needs to adapt to these new methods of production. With ALFRED, the aim is to create a new system that makes working with robot arms remotely easier and adds more capabilities to these robot arms.

## State of the Art

- Arm Robotic

  - Mechanics
  - Trajectory planning
    - RRT
    - Trajectory computation
  -

- Cobotic & HCI

  - Multi modalities interactionEnvironment
  -

- Artificial Intelligence
  - computer vision (boxing, image segmentation, 3d pose estimation)
  - Language Processing
  - Context analysis
    - VSLAM
    - Semantic mapping
  - Decision Making

# Overview

## Middleware architecture

<!-- TODO: architecture schematic -->

## Environment Analysis

### Static Environment Discovery

The system uses VSLAM* to analyze the environment around the arm. From this algorithmn, a 3D occupancy map* is extracted. The robot does an initial scan at boot time, then updates the map in the background during execution.

Forbidden zones* can be determined from the occupancy map. Forbidden zones are zones of space where an object was detected, which the arm cannot go through. A padding is added around the forbidden zones, for path planning. This is necessary since the position of the arm is represented by the center of its end-effector*, and collision can occur in a radius around this position. The padding allows for a margin between the end-effector and the object in space.

### Static Object Recognition

Object recognition is run from the camera feed to detect objects present in the environment. The object detection model is trained on the COCO dataset*. Inference is done with YOLOv5* for its speed of execution and lightweight nature.

### Semantic Environment Mapping

VSLAM data, associated with object data from object recognition, is used to construct a map that gives the position of objects in space and the space they occupy. This map makes interactions between the arm and objects easier: the system knows at all times where objects are and what they look like, so it can know how to manipulate them.

## Arm Robotic Control

### Trajectory Planning

ALFRED uses PyBullet* and Robotics Toolbox* for trajectory planning. PyBullet serves as a simulation for physics, calculating inverse kinematics* and visualizing the robot in the virtual space. Robotics Toolbox is used to calculate the trajectories in cartesian space*.

### Collision detection

The system uses the environment data obtained in [Environment Analysis](#environment-analysis) and the tools in [Trajectory Planning](#trajectory-planning) to prevent the robotic arm from colliding with objects in its environment.

## Human Robot Control Interfaces

### Interactive Modalities

#### Voice control

With voice recognition* and Natural Language Processing*, the system can be controlled by voice. The goal is to allow speaking to the system in a natural manner, like to a real human. It helps integration in the environment and allows for better efficiency: the user doesn't have to remember precise phrases, and they can achieve finer control with precise commands that can't always be predicted.

#### Control with gestures

The robot arm can be controlled with the user's hands. The application runs hand recognition on a camera feed with Mediapipe*. It extracts landmarks* representing the different points on the hand (ex: index tip, wrist, ...). These landmarks are then fed to an classifier* to determine the current gesture the user is making. These gestures can be, for example, a thumb-up, a fist or a raised index. They can be mapped to commands, allowing the user to control the arm with their hands.

An example application is Hand Control, where the user can move the arm depending on the position of their hand in the camera frame, but also stop or start the arm and grasp items.

#### Web interface

The web interface allows the users to control the arm from a computer or a mobile phone. The web interface brings together voice control and hand control, and adds other control features.

For voice control, a button allows to start recording voice and "talk" to the assistant, and you can see its response as well.

For hand control, the interface uses the user's webcam to get the video feed for hand recognition.

Other features include visualization of the robot arm in 3D, graphs for joint positions, launching [applications](#applications), debugging with a console...

### Decision Loop

- Robot to Human
- Human to Robot

## Applications

=> Autres pages (Cross reality, ) => tabs

## Future works
