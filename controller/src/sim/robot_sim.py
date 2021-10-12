import queue
import threading
import time

import numpy as np
import pybullet as p
import pybullet_data as pd

from ..command import Command
from ..controller import Controller


class XArmSim(threading.Thread):
    """Simulated xArm class."""

    controller: Controller
    robot_sim: int

    def __init__(
        self,
        controller: Controller,
        time_step: float = 1.0 / 60.0
    ):
        super().__init__()

        p.connect(p.GUI)
        p.setAdditionalSearchPath(pd.getDataPath())

        self.controller = controller
        self.time_step = time_step

        # default load robot_sim model
        pybullet_flags = p.URDF_ENABLE_CACHED_GRAPHICS_SHAPES
        self.robot_sim = p.loadURDF(
            "xarm/xarm6_robot.urdf",
            [0, 0, 0],
            [0, 0, 0, 1],
            useFixedBase=True,
            flags=pybullet_flags,
        )

        # set robot_sim to base position
        for joint_num in range(1, self.controller.DOFs + 1):
            p.changeDynamics(
                self.robot_sim, joint_num, linearDamping=0, angularDamping=0
            )
            info = p.getJointInfo(self.robot_sim, joint_num)

            jointType = info[2]
            if jointType == p.JOINT_PRISMATIC:
                p.resetJointState(
                    self.robot_sim,
                    joint_num,
                    self.controller.joint_positions[joint_num - 1],
                )
            elif jointType == p.JOINT_REVOLUTE:
                p.resetJointState(
                    self.robot_sim,
                    joint_num,
                    self.controller.joint_positions[joint_num - 1],
                )

        # get cartesian position
        self.controller.cartesian_pos = self.get_cartesian_pos()
        self.controller.future_cartesian_pos = self.controller.cartesian_pos

        # self.move(self.controller.joint_positions)

    def run(self):
        while 1:
            self.step()
            p.stepSimulation()
            time.sleep(self.time_step)

    def get_cartesian_pos(self, compute=True):
        end_effector_state = p.getLinkState(
            self.robot_sim,
            self.controller.end_effector_index,
            computeForwardKinematics=compute,
        )
        end_effector_xyz = end_effector_state[4]
        end_effector_rpy = p.getEulerFromQuaternion(end_effector_state[5])
        cartesian_pos = end_effector_xyz + end_effector_rpy
        # print(cartesian_pos)
        return Command(*cartesian_pos, is_radian=True)

    def format_cartesian_pos(self, in_radians: bool = True) -> str:
        xyz = self.controller.cartesian_pos[:3]
        rpy = self.controller.cartesian_pos[3:]

        ret = ""
        ret += ", ".join([f"{coord * 1000:.2f}" for coord in xyz])
        ret += ", "
        ret += ", ".join(
            [
                f"{coord:.2f}" if in_radians else f"{np.rad2deg(coord):.2f}"
                for coord in rpy
            ]
        )

        return ret

    def run_ik(self, xyzrpy: list):
        xyz = xyzrpy[:3]
        rpy = xyzrpy[3:]

        rpy_quaternion = p.getQuaternionFromEuler(rpy)

        if self.controller.use_null_space:
            # target_joint_positions = p.calculateInverseKinematics(
            #     self.robot_sim,
            #     self.controller.end_effector_index,
            #     xyz,
            #     rpy_quaternion,
            #     lowerLimits=self.controller.ll,
            #     upperLimits=self.controller.ul,
            #     jointRanges=self.controller.jr,
            #     restPoses=self.controller.rp,
            #     # restPoses=np.array(self.controller.joint_positions).tolist(),
            #     residualThreshold=1e-5,
            #     maxNumIterations=50,
            # )
            pass
        else:
            target_joint_positions = p.calculateInverseKinematics(
                self.robot_sim,
                self.controller.end_effector_index,
                xyz,
                rpy_quaternion,
                maxNumIterations=50,
            )

        return target_joint_positions

    def move(self, target_joint_positions: list):
        if self.controller.use_dynamics:
            for i in range(self.controller.DOFs):
                p.setJointMotorControl2(
                    self.robot_sim,
                    i + 1,
                    p.POSITION_CONTROL,
                    target_joint_positions[i],
                    force=5 * 240.0,
                )
        else:
            for i in range(self.controller.DOFs):
                p.resetJointState(self.robot_sim, i + 1, target_joint_positions[i])

        if self.controller.move_real:
            self.controller.arm_real.set_servo_angle_j(  # type: ignore[union-attr]
                target_joint_positions, is_radian=True
            )

    def reset(self):
        pass

    def step(self):
        try:
            target_position = self.controller.decomposed_command_queue.get(block=False)
            # print(target_position)

            self.controller.decomposed_command_queue.task_done()
        except queue.Empty:
            return

        # xyzrpy = [
        #     0.2069,  # in meters
        #     0.0,  # in meters
        #     0.2587,  # in meters
        #     math.pi,  # in radians
        #     0.0,  # in radians
        #     0.0,  # in radians
        # ]
        # jointPoses = self.run_ik(xyzrpy)
        # print("jointPoses=",jointPoses)

        target_joint_positions = self.run_ik(target_position)

        self.move(target_joint_positions)

        self.controller.joint_positions = target_joint_positions
        self.controller.cartesian_pos = self.get_cartesian_pos(compute=True)

        p.addUserDebugLine(
            self.controller.cartesian_pos[:3],
            target_position[:3],
        )

        # print(old_cartesian_pos[:3], "\n", self.cartesian_pos[:3])
