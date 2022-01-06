import pybullet as p
import pybullet_data as pd
from libalfred.utils.position import Position

from src.config import cfg


class RobotSim:
    """Simulated xArm class."""

    sim_id: int

    def __init__(self, time_step: float = 1.0 / 60.0):
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pd.getDataPath())

        self.time_step = time_step

        # default load robot_sim model
        pybullet_flags = p.URDF_ENABLE_CACHED_GRAPHICS_SHAPES
        self.sim_id = p.loadURDF(
            "xarm/xarm6_robot.urdf",
            [0, 0, 0],
            [0, 0, 0, 1],
            useFixedBase=True,
            flags=pybullet_flags,
        )

    def set_base_pose(self, joint_positions):
        """set robot_sim to base position"""

        for joint_num in range(1, cfg.ROBOT_DOFS + 1):
            p.changeDynamics(
                self.sim_id, joint_num, linearDamping=0, angularDamping=0,
            )
            info = p.getJointInfo(self.sim_id, joint_num)

            jointType = info[2]
            if jointType == p.JOINT_PRISMATIC:
                p.resetJointState(
                    self.sim_id, joint_num, joint_positions[joint_num - 1],
                )
            elif jointType == p.JOINT_REVOLUTE:
                p.resetJointState(
                    self.sim_id, joint_num, joint_positions[joint_num - 1],
                )

            return self.get_cartesian_pos()

    def step_simulation(self):
        p.stepSimulation()

    def calculate_inverse_kinematics(self, xyz: list, rpy_quaternion: list):
        target_joint_positions = p.calculateInverseKinematics(
            self.sim_id,
            cfg.END_EFFECTOR_INDEX,
            xyz,
            rpy_quaternion,
            maxNumIterations=50,
        )

        return target_joint_positions

    def get_quaternion_from_euler(self, rpy: list):
        return p.getQuaternionFromEuler(rpy)

    def get_cartesian_pos(self, compute=True):
        end_effector_state = p.getLinkState(
            self.sim_id,
            cfg.END_EFFECTOR_INDEX,
            computeForwardKinematics=compute,  # noqa: E501
        )
        end_effector_xyz = end_effector_state[4]
        end_effector_rpy = p.getEulerFromQuaternion(end_effector_state[5])
        cartesian_pos = end_effector_xyz + end_effector_rpy

        return Position(*cartesian_pos, is_radian=True)

    def move(self, target_joint_positions: list, use_dynamics: bool):
        if use_dynamics:
            for i in range(cfg.ROBOT_DOFS):
                p.setJointMotorControl2(
                    self.sim_id,
                    i + 1,
                    p.POSITION_CONTROL,
                    target_joint_positions[i],
                    force=5 * 240.0,
                )
        else:
            for i in range(cfg.ROBOT_DOFS):
                p.resetJointState(
                    self.sim_id, i + 1, target_joint_positions[i],
                )

    @classmethod
    def add_user_debug_line(cls, start_xyz: list, goal_xyz: list):
        p.addUserDebugLine(start_xyz, goal_xyz)
