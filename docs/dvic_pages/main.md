# ALFRED : General Purpose Middleware for Personal Robotic Arm Assistants

# About

# Abstract

# Article

# Introduction

## Context

## Motivations

- Worker 2.0 & Industry 4.0

Industry 4.0 has recently become the standard for factory automation. Network-controlled, intelligent machines allow for faster production, at lower cost and risk. Robots have become controllable remotely, and as such, the worker in this new type of industry, a "Worker 2.0", needs to adapt to these new methods of production. With ALFRED, we aim to create a new system that makes working with robot arms remotely easier and adds more capabilities to these robot arms.

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

# ALFRED Overview

## Middleware architecture

<!-- TODO: architecture schematic -->

## 1.1 Environment Analysis

### Static Environment Discovery

The system uses VSLAM* to analyze the environment around the arm. From this algorithmn, a 3D occupancy map* is extracted. The robot does an initial scan at boot time, then updates the map in the background during execution.

Forbidden zones* cand be determined from the occupancy map. Forbidden zones are zones of space where an object was detected, which the arm cannot go through. A padding, for path planning, is added around the forbidden zones. This is necessary since the position of the arm is represented by the center of its end-effector*, and collision can occur in a radius around this position. The padding allows for a margin between the end-effector and the object in space.

### Static Object Recognition

Object recognition is run from the camera feed to detect objects present in the environment. The object detection model is trained on the COCO dataset*. Inference is done with YOLOv5* for its speed of execution and lightweight nature.

### Semantic Environment Mapping

We use VSLAM data associated with object data from object recognition, to construct a map that gives the position of objects in space and the space they occupy. This map makes interactions between the arm and objects easier: the system knows at all times where objects are and what they look like, so it can know how to manipulate them.

## Arm Robotic Control

### Trajectory Planning

## Human Robot Control Interfaces

### Interactive Modalities

#### Voice control

With voice recognition* and Natural Language Processing*, the system can be controlled by voice. The goal is to allow speaking to the system in a natural manner, like to a real human. It helps integration in the environment and allows for better efficiency: the user doesn't have to remember precise phrases, and they can achieve finer control with precise commands that can't always be predicted.

#### Control with gestures

The robot arm can be controlled with the user's hands. By running hand recognition\* on video feed from a computer or phone, we can extract commands to execute. For example

#### Web interface

A web interface allows the users to control the arm from a computer or a mobile phone.

### Decision Loop

- Robot to Human
- Human to Robot

## Applications

=> Autres pages (Cross reality, ) => tabs

## Future works
