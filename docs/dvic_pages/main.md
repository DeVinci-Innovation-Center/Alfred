# ALFRED : General Purpose Middleware for Personal Robotic Arm Assistants

# TODOS:

Bannière
Vidéo
Pas de is to =>
Pas de chiffres
Compiler les titres en phrases
SotA cobotics/robotics
compresser verticalement le schéma
commencer par for example pour les exemples
raccourcir les phrases

revoir syntaxe: pas de that, it enables, the goal is, ...


# About

## Content



# Article

# Introduction

## Context

Industry 4.0 has become the standard for factory automation. Network-controlled, intelligent machines allow for faster production, at lower cost and risk. Robots have become controllable remotely, and as such, the worker in this new type of industry, a "Worker 2.0", needs to adapt to these new methods of production.

## Motivations

ALFRED is an Artificial Intelligence-based middleware for robotic arms. The system uses a modular architecture, with a high degree of abstraction inspired by modern Operating Systems. ALFRED can be deployed on robotic arms with minimal adjustments. It is built for pushing Human-Robot interaction to its maximum, with multiple modalities of interaction and high performance, in business or research applications.

## What the project is

ALFRED uses docker-compose to deploy a complete middleware in the form of a group of containers, from complex robot control to high level user applications.

## State of the Art

### Artificial Intelligence

#### Computer vision

##### Context analysis

Context analysis comprises of scanning the environment to extract a map of the robot's surroundings. Visual SLAM is used to create a map representing the environment from a camera feed. The medium in a point cloud, which is a series of coordinates representing matter in space. OBR_SLAM3 [^5] is an example of VSLAM algorithm, and is powerful, robust and accurate even compared to the best systems.

From the point cloud, the system create an occupancy map, which tells the robot areas it can or cannot access.

Semantic mapping describes the concept of associating metadata to points in a point cloud. Traditional point clouds are only composed of coordinates where matter is present. With semantic mapping, it becomes possible to assign data to a group of points in space, e.g., saying a specific part of the map represents a bottle, or a couch.

##### Object detection

Object detection on on ALFRED uses YOLOv5 [^1]. YOLOv5 is a fast and easy to train model. The model can be finetuned in less than an hour of training for small specialized datasets (< 3000 images), which is what has been used on ALFRED. The YOLO family does what is called boxing: it determines a box around the objects it detects on the image.

YOLOv5 is pre-trained on the COCO dataset [^2], a state-of-the-art dataset specialized in common objects animals, and people. It has more than 200K captioned images, and 171 different classes of objects.

##### Pose estimation

Pose estimation is done with Mediapipe [^3]. Mediapipe is a Google project that offers multiple solutions for pose estimation, including body pose, face, hand, even hair detection, and holistic (all in one) models. It uses the latest technologies from Google to build performant models with easy integration with various programming languages.

ALFRED uses Mediapipe's hand detection model. Applications can extract landmarks, which represent key points on the hand. Gestures are detected from the landmarks using a classifier.

#### Language processing

Language processing consists of two parts: the first is Speech To Text (STT). STT uses Azure Speech, a Microsoft service, to translate voice data into text.

The second part is processing with RASA. RASA uses Natural Language Processing (NLP) to interpret text data into intents and variables. Intents represent the global meaning of the sentence and are hard-coded in the training data. Variables are pieces of information that can change even for the same intent.

## Middleware architecture

![](https://dvic.devinci.fr/api/v3/img/full/uztu02mfhffc7spsyjzhsz4hss1yex.png)

## Environment Analysis

### Static Environment Discovery

The system uses VSLAM to analyze the environment around the arm. From this algorithmn, a 3D occupancy map is extracted. The robot does an initial scan at boot time, then updates the map in the background during execution.

Forbidden zones can be determined from the occupancy map. Forbidden zones are zones of space where an object was detected, which the arm cannot go through.

### Static Object Recognition

Object recognition is run from the camera feed to detect objects present in the environment. Inference is done with YOLOv5 for its speed of execution and lightweight nature. The model is trained on the COCO dataset.

### Semantic Environment Mapping

VSLAM data, associated with object data from object recognition, is used to construct a map that gives the position of objects in space and the space they occupy. This map makes interactions between the arm and objects easier: the system knows at all times where objects are and what they look like, so it can know how to manipulate them.

## Arm Robotic Control

### Trajectory Planning

ALFRED uses PyBullet and Robotics Toolbox for trajectory planning. PyBullet serves as a simulation for physics, calculating inverse kinematics** and visualizing the robot in the virtual space. Robotics Toolbox is used to calculate the trajectories in cartesian space*.

\*Cartesian/joint space: different representations for a given position in space. Cartesian space takes a point as its origin and descirbe a coordinate with x, y and z values for the 3 dimensions of space. Joint space represents a position in angles of the robot's joints.

**Inverse kinematics: mathematical equations to go from cartesian space to joint space, e.g. get joint angle values for a given position in space.


### Collision detection

The system uses the environment data obtained in [Environment Analysis](#environment-analysis) and the tools in [Trajectory Planning](#trajectory-planning) to prevent the robotic arm from colliding with objects in its environment.

## Human Robot Control Interfaces

### Interactive Modalities

ALFRED's interface relies on multiple modalities for interaction with the user:

- Gesture recognition
- Speech recognition
- Mouse and keyboard

The different modalities offer specialization on certain tasks. For example, grasping an object is only possible with speech and gestures.

#### Voice control

The system can be controlled by voice using STT and RASA. The user can talk to ALFRED in a natural manner, just like a real human. It helps integration in the environment and allows for better efficiency. The user doesn't have to remember precise phrases, and they can achieve finer control with precise commands that weren't predicted in training but were interpreted correctly during inference.

#### Control with gestures

Control with gestures is achieved by running hand recognition on a camera feed with Mediapipe. Mediapipe outputs landmarks, representing the different points on the hand (ex: index tip, wrist, ...). A landmarks classifier determines user gestures, e.g a thumb-up, a fist or a raised index. Gestures trigger events, which allow user to control the arm with their hands.

An example application is Hand Control, where the user can move the arm depending on the position of their hand in the camera frame, but also stop or start the arm and grasp items.

#### Web interface

The web interface allows the users to control the arm from a computer or a mobile phone. The web interface brings together voice control and hand control, and adds other control features.

For voice control, a button allows to start recording voice and "talk" to the assistant, and you can see its response as well.

For hand control, the interface uses the user's webcam to get the video feed for hand recognition.

Other features include visualization of the robot arm in 3D, graphs for joint positions, launching [applications](#applications), debugging with a console...

### Decision Loop

#### Human to Robot

The robot receives commands via a database with publish and subscribe capabilities (Redis), with its Controller interface. The commands are created in userspace: the robot has no concept of userspace applications, only where and how it should move.

Commands include cartesian movement, simultaneous joint movement, and single joint movement, with parameters for speed, acceleration, ...

For every command received, the robot analyzes the desired movement. It plans the path it will take, using path plannign algorithm, and taking into account environment data.

#### Robot to Human

In return, the robot gives feedback to the system: is the command possible ? did it have to modify it to prevent a collision ? or did everything go as planned ?

If the destination is impossible to reach (ex: out of bounds), the controller logs the error and doesn't execute the movement.

If the destination cannot be reached because of an obstacle, it logs the error, and moves to the closest point to the planned destination.

If nothing is wrong with the movement, the controller executes the command.

## Applications

=> Autres pages (Cross reality, ) => tabs

## Future works

- AR: virtual environment mimicking the real world
- Automatic tool changing station

# Bibliography

[^1]: YOLOv5: https://github.com/ultralytics/yolov5

[^2]: COCO dataset: https://cocodataset.org/

[^3]: Mediapipe: https://google.github.io/mediapipe/

[^4]: RASA: https://rasa.com/

[^5]: ORB_SLAM3: https://github.com/UZ-SLAMLab/ORB_SLAM3
