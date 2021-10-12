import os
import sys
import time

import pybullet as p
import pybullet_data as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import src.sim.robot_sim as xarm_sim
from src.controller import Controller

p.connect(p.GUI)
p.setAdditionalSearchPath(pd.getDataPath())

timeStep = 1.0 / 60.0
p.setTimeStep(timeStep)
p.setGravity(0, 0, -9.8)

controller = Controller()
xarm = xarm_sim.XArmSim(p, controller)
while 1:
    xarm.step()
    p.stepSimulation()
    time.sleep(timeStep)
