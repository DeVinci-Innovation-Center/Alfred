# ALFRED : General Purpose Middleware for Personal Robotic Arm Assistants

> TODOS:
>
> > Bannière\
> > Vidéo\
> > SotA cobotics/robotics\
>
> > intro = abstract en plus détaillé\
> > marquer un peu plus\

# About

## Content

Industry 4.0 has become the standard for factory automation. Network-controlled, intelligent machines allow for faster production, at lower cost and risk. Robots have become controllable remotely, and as such, the worker in this new type of industry, a "Worker 2.0", needs to adapt to these new methods of production.

ALFRED is an Artificial Intelligence-based middleware for robotic arms. The system uses a modular architecture, with a high degree of abstraction inspired by modern Operating Systems. ALFRED can be deployed on robotic arms with minimal adjustments. It is built for pushing Human-Robot interaction forward, with multiple modalities of interaction and high performance, in business or research applications.

ALFRED uses containers to deploy a complete middleware, from complex robot control to high level user applications.

# Article

## Content

@[space](3)

@[split](2,begin)

![](https://dvic.devinci.fr/api/v3/img/full/ysvpsl7k18npur8u15ptmvz2nyfmzd.jpg)

@[split](2,break)

Basic automation requires a robot to only repeat a set of movements indefinitely, but with the needs of Industry 4.0, robotic systems need to be more and more complex. Safety, adaptability and connectivity are now required for automation in the industry. Safety comes in the form of smart collision detection, with sensitive robots that know their environments and react to unseen obstacles or operators. Adaptability requires robots to have intelligent decision making systems and powerful sensing abilities. Robots need to communicate with each other to share information, and to be able to be controlled remotely for easier access.

ALFRED brings safety, adaptability and connectivity to any commercial robotic arm. ALFRED is a middleware, enhanced by Artificial Intelligence, focused on modularity, extensibility and abstraction. Inspired by modern Operating Systems, it brings together devices, interfaces and the robotic arm to create a system ready to be deployed in real situations. ALFRED is a way for manufacturers and researchers to develop applications for a robotic arm with minimal knowledge about robotic control. It integrates in its environment with its multiple interaction modalities, such as manual control with hands, voice control, and a web interface.

@[split](2,end)

To achieve its capabilities, ALFRED makes use of two fields of Artificial Intelligence: **Computer vision** and **Language processing**.

**Computer vision** is the analysis of the environment using image data, such as a video feed from a camera. The environment around a system can be analyzed with different context analysis techiques, object detection and pose estimation for people and animals. The **Context analysis** comprises of scanning the environment to extract a map of the robot's surroundings. Visual SLAM is used to create a map representing the environment from a camera feed. The medium in a point cloud, which is a series of coordinates representing matter in space. OBR_SLAM3 [^5] is an example of VSLAM algorithm, and is powerful, robust and accurate even compared to the best systems.
**Semantic mapping** is a subset of context analysis which describes the concept of associating metadata to points in a point cloud. Traditional point clouds are only composed of coordinates where matter is present. With semantic mapping, it becomes possible to assign data to a group of points in space, e.g., saying a specific part of the map represents a bottle, or a couch. One of the main **object detection** algorithm is the YOLO family, the most recent member being YOLOv5 [^1]. YOLOv5 is a fast and easy to train model. The YOLO family does what is called boxing: it determines a box around the objects it detects on the image.
YOLOv5 is pre-trained on the COCO dataset [^2], a state-of-the-art dataset specialized in common objects animals, and people. It has more than 200K captioned images, and 171 different classes of objects. **Pose estimation** is the detection of limbs of humans or animals. A Google project, Mediapipe [^3], offers solutions for state-of-the-art pose detection including body, face features and hand detection.

**Language processing** is the analysis and understanding of human speech, be it in text or vocal form. Understanding someone's voice generally needs two steps: translating speech into text and interpreting the text. Translating speech into text, or **Speech To Text (STT)**, is important since many language processing systems do not treat audio streams. STT models are hard to train, because everyone has a different voice, but Azure Speech, a Microsoft service, does STT with high precision.
Interpreting text is done with **Natural Language Processing (NLP)**, a field of Deep Learning focused on interpreting text data into intents and variables. Intents represent the global meaning of the sentence and are hard-coded in the training data. Variables are pieces of information that can change even for the same intent. Frameworks for easier usage of NLP exist, one example being RASA [^4].

## Architecture Overview

ALFRED is designed with modularity in mind, and follows design principles of modern operating systems. The system is separated into two parts:

-**Userspace**, which is made of **applications**, **interfaces** and a **Network Connector**. **Applications** are blocks which are added by the user, and use the system's API to control the arm. Applications are where robot commands are sent, environment data read, and information generated. **Interfaces** are the way to interact with the arm by launching applications, showing data, and getting user input. The **Network Connector** allows remote applications or other systems to interact with ALFRED.

-The **Kernel**: the kernel is the core of the system. It contains components necessary for the system to function. The components in the kernel are not accessible to the user. There are four parts in the kernel: the database, the drivers, robotic arm control and environment analysis. The **database** is used to persist data, and make it accessible to outside of the system, e.g. with robot position or logs. The **drivers** are the interface between the devices linked to ALFRED and the software. **Robotic arm control** controls the robot itself, does physics calculations and collision detection. **Environment analysis** is the eyes of the system, where the system learns about its environment.

![](https://dvic.devinci.fr/api/v3/img/full/0rzdd3pvcymy2e1o9fluj93mj7d14a.png)

## Environment Analysis

The system uses **VSLAM** to analyze the environment around the arm. From this algorithmn, a 3D occupancy map is extracted. The robot does an initial scan at boot time, then updates the map in the background during execution.

**Forbidden zones** can be determined from the occupancy map. Forbidden zones are zones of space where an object was detected, which the arm cannot go through.

**Object recognition** is run from the camera feed to detect objects present in the environment. Inference is done with YOLOv5 for its speed of execution and lightweight nature. The model is trained on the COCO dataset.

VSLAM data, associated with object data from object recognition, is used to construct a map that gives the position of objects in space and the space they occupy. This map makes interactions between the arm and objects easier: the system knows at all times where objects are and what they look like, so it can know how to manipulate them.

## Robotic Arm Control

ALFRED uses **PyBullet** [^6] and **Robotics Toolbox** [^7] for trajectory planning. PyBullet serves as a simulation for physics, calculating inverse kinematics[^**] and visualizing the robot in the virtual space. Robotics Toolbox is used to calculate the trajectories in cartesian space[^*].

The system uses the environment data obtained in [Environment Analysis](#environment-analysis) and the tools in [Trajectory Planning](#trajectory-planning) to prevent the robotic arm from colliding with objects in its environment.

![](https://dvic.devinci.fr/api/v3/img/full/gg4e7zhvto1r61uh3qaz3w0mm0k7zm.png)

The robot receives commands via (Redis). The commands are created in userspace: the robot has no concept of userspace applications, only where and how it should move. Commands include cartesian movement, simultaneous joint movement, and single joint movement, with parameters for speed, acceleration, ...

For every command received, the robot analyzes the desired movement. It plans the path it will take, using path plannign algorithm, and taking into account environment data.
In return, the robot gives feedback to the system: is the command possible ? did it have to modify it to prevent a collision ? or did everything go as planned ? If the destination is impossible to reach (ex: out of bounds), the controller logs the error and doesn't execute the movement. If the destination cannot be reached because of an obstacle, it logs the error, and moves to the closest point to the planned destination. If nothing is wrong with the movement, the controller executes the command.

[^*]: Cartesian/joint space: different representations for a given position in space. Cartesian space takes a point as its origin and descirbe a coordinate with x, y and z values for the 3 dimensions of space. Joint space represents a position in angles of the robot's joints.

[^**]: Inverse kinematics: mathematical equations to go from cartesian space to joint space, e.g. get joint angle values for a given position in space.
## Human Robot Control Interfaces

ALFRED's interface relies on multiple modalities for interaction with the user:

- Gesture recognition
- Speech recognition
- Mouse, keyboard, touchscreen

The different modalities offer specialization on certain tasks. For example, grasping an object is only possible with speech and gestures.

The system can be controlled by voice using **STT** and **RASA**. The user can talk to ALFRED in a natural manner, just like a real human. It helps integration in the environment and allows for better efficiency. The user doesn't have to remember precise phrases, and they can achieve finer control with precise commands that weren't predicted in training but were interpreted correctly during inference.

Control with gestures is achieved by running **hand recognition** on a camera feed with Mediapipe. Mediapipe outputs landmarks, representing the different points on the hand (ex: index tip, wrist, ...). A landmarks classifier determines user gestures, e.g a thumb-up, a fist or a raised index. Gestures trigger events, which allow user to control the arm with their hands.\
An example application is Hand Control, where the user can move the arm depending on the position of their hand in the camera frame, but also stop or start the arm and grasp items.

The **web interface** allows the users to control the arm from a computer or a mobile phone. The web interface brings together voice control and hand control, and adds other control features.

![](https://dvic.devinci.fr/api/v3/img/full/3tc4noooed3zcily3kmgx746kjwdue.png)

For **voice control**, a button allows to start recording voice and "talk" to the assistant, and you can see its response as well.

For **hand control**, the interface uses the user's webcam to get the video feed for hand recognition.

Other features include visualization of the robot arm in 3D, graphs for joint positions, launching [applications](#applications), debugging with a console...

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

[^6]: PyBullet: https://pybullet.org/wordpress/

[^7]: Robotics Toolbox: https://github.com/petercorke/robotics-toolbox-python
