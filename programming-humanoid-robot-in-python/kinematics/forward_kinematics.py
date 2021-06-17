'''In this exercise you need to implement forward kinematics for NAO robot

* Tasks:
    1. complete the kinematics chain definition (self.chains in class ForwardKinematicsAgent)
       The documentation from Aldebaran is here:
       http://doc.aldebaran.com/2-1/family/robots/bodyparts.html#effector-chain
    2. implement the calculation of local transformation for one joint in function
       ForwardKinematicsAgent.local_trans. The necessary documentation are:
       http://doc.aldebaran.com/2-1/family/nao_h21/joints_h21.html
       http://doc.aldebaran.com/2-1/family/nao_h21/links_h21.html
    3. complete function ForwardKinematicsAgent.forward_kinematics, save the transforms of all body parts in torso
       coordinate into self.transforms of class ForwardKinematicsAgent

* Hints:
    the local_trans has to consider different joint axes and link parameters for different joints
'''

# add PYTHONPATH
import os
import sys
import numpy as np
from joint_control.angle_interpolation import AngleInterpolationAgent
from joint_control.recognize_posture import PostureRecognitionAgent

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))


class ForwardKinematicsAgent(PostureRecognitionAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(ForwardKinematicsAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.transforms = {n: np.eye(4) for n in self.joint_names}

        # chains defines the name of chain and joints of the chain
        #self.chains_with = {'Head': ['HeadYaw', 'HeadPitch'],
        #                    # YOUR CODE HERE
        #                    'LArm': ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw',
        #                             'LHand'],
        #                    'RArm': ['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw',
        #                             'RHand'],
        #                    'LLeg': ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch',
        #                             'LAnkleRoll'],
        #                    'RLeg': ['RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll']
        #                    }

        self.chains = {'Head': ['HeadYaw', 'HeadPitch'],
                       # YOUR CODE HERE
                       'LArm': ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'],
                       'RArm': ['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'],
                       'LLeg': ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch',
                                'LAnkleRoll'],
                       'RLeg': ['RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch',
                                'RAnkleRoll']
                       }

        self.joint_lengths = {'HeadYaw': (0., 0., .1265), 'HeadPitch': (0., 0., 0.),
                              'LShoulderPitch': (0., .98, .100), 'LShoulderRoll': (0., 0., 0.),
                              'LElbowYaw': (.105, .015, 0.), 'LElbowRoll': (0., 0., 0.),
                              'RShoulderPitch': (0., -.098, .100), 'RShoulderRoll': (0., 0., 0.),
                              'RElbowYaw': (.105, -.015, 0.), 'RElbowRoll': (0., 0., 0.),
                              'LHipYawPitch': (0., .050, -.085), 'RHipYawPitch': (0., -.050, -.085),
                              'LHipRoll': (0., 0., 0.), 'LHipPitch': (0., 0., 0.), 'LKneePitch': (0., 0., -.100),
                              'LAnklePitch': (0., 0., -.1029), 'LAnkleRoll': (0., 0., 0.),
                              'RHipRoll': (0., 0., 0.), 'RHipPitch': (0., 0., 0.), 'RKneePitch': (0., 0., -.100),
                              'RAnklePitch': (0., 0., -.1029), 'RAnkleRoll': (0., 0., 0.),
                              'LHand': (.05775, 0., .01231), 'RHand': (.05775, 0., .01231),
                              'LWristYaw': (.05595, 0., 0.), 'RWristYaw': (.05595, 0., 0.)
                              }

        self.end_effectors = ['LHand', 'RHand', 'LWristYaw', 'RWristYaw']

    def think(self, perception):
        self.forward_kinematics(perception.joint)
        # print(self.transforms)
        return super(ForwardKinematicsAgent, self).think(perception)

    def local_trans(self, joint_name, joint_angle):
        '''calculate local transformation of one joint

        :param str joint_name: the name of joint
        :param float joint_angle: the angle of joint in radians
        :return: transformation
        :rtype: 4x4 matrix
        '''
        T = np.eye(4)
        # YOUR CODE HERE
        s = np.sin(joint_angle)
        c = np.cos(joint_angle)
        trans = self.joint_lengths[joint_name]

        rot_x = np.array([[1, 0, 0, 0],
                          [0, c, -s, 0],
                          [0, s, c, 0],
                          [0, 0, 0, 1]])
        rot_y = np.array([[c, 0, s, 0],
                          [0, 1, 0, 0],
                          [-s, 0, c, 0],
                          [0, 0, 0, 1]])
        rot_z = np.array([[c, s, 0, 0],
                          [-s, c, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        roll_45 = np.array([[np.cos(np.pi / 4), np.sin(np.pi / 4), 0, 0],
                            [-np.sin(np.pi / 4), np.cos(np.pi / 4), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        #if 'Hip' in joint_name:
        #    T = T @ roll_45 @ rot_y
        if 'Roll' in joint_name:
            T = T @ rot_x
        elif 'Pitch' in joint_name:
            T = T @ rot_y
        elif 'Yaw' in joint_name:
            T = T @ rot_z

        T[0, -1] = trans[0]
        T[1, -1] = trans[1]
        T[2, -1] = trans[2]

        return T.copy()

    def forward_kinematics(self, joints):
        '''forward kinematics

        :param joints: {joint_name: joint_angle}
        '''
        # for chain_joints in self.chains_with.values():
        for chain_joints in self.chains.values():
            T = np.eye(4)
            for joint in chain_joints:
                angle = joints[joint]
                # angle = joints[joint] if joint not in self.end_effectors else 0
                Tl = self.local_trans(joint, angle)
                T = T @ Tl
                self.transforms[joint] = T.copy()
        # print(self.transforms)

if __name__ == '__main__':
    agent = ForwardKinematicsAgent()
    agent.run()
