# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import sys
import time
import numpy as np
import math
from utils.ws_client import *
import time
import paramiko

def start_skill(address: str, skill: str, parameters: dict, control: dict):
    response = start_task(address, "GenericTask", parameters={"parameters": {
        "skill_names": ["skill"],
        "skill_types": [skill]
    },
        "skills": {
            "skill": {
                "skill": parameters,
                "control": control
            }
        }})

robot_address = "192.168.50.89"
robot = robot_address

M_PI_2 = math.pi/2
M_PI_4 = math.pi/4

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(robot_address, username="robot", password="R0b0tn1K")

def initialize_robot():
    initial_joint_pose = np.array([0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4])
    response = start_task(robot, "MoveToJointPose", parameters={"parameters": {"q_g": initial_joint_pose .tolist(),"pose":"NoneObject","speed":1.5,"acc": 2}})
    wait_for_task(robot, response["result"]["task_uuid"])
    time.sleep(0.5)

def get_current_joint_pose():
    robot_state = call_method(robot, 12000, "get_state")
    print(robot_state['result']['q'])

def get_current_cartesian_pose():
    robot_state = call_method(robot, 12000, "get_state")
    print(robot_state['result']['O_T_EE'])

def move_to_cartesian_pose(cartesian_pose):
    response = start_task(robot, "MoveToCartPose", parameters={"parameters": {"T_EE_g": cartesian_pose.tolist(), "pose": "NoneObject"}})
    wait_for_task(robot, response["result"]["task_uuid"])
    time.sleep(0.5)

def move_to_joint_pose(joint_pose):
    response = start_task(robot, "MoveToJointPose", parameters={"parameters": {"q_g": joint_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
    wait_for_task(robot, response["result"]["task_uuid"])
    time.sleep(0.5)

def move_forward(step):
    command_forward = "bash /home/robot/ki_fabrik/call_service.sh " + str(-step) + " 0.0"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_forward)
    time.sleep(3)

def move_backward(step):
    command_backward = "bash /home/robot/ki_fabrik/call_service.sh " + str(step) + " 0.0"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_backward)
    time.sleep(3)

def move_left(step):
    command_left = "bash /home/robot/ki_fabrik/call_service_left.sh 0.0 " + str(step) + " 0.0"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_left)
    time.sleep(3)

def move_right(step):
    command_right = "bash /home/robot/ki_fabrik/call_service_right.sh 0.0 " + str(step) + " 0.0"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_right)
    time.sleep(3)

def grasp():
    command_grasp = "bash /home/robot/ki_fabrik/grasp.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_grasp)
    time.sleep(3.5)

def release():
    command_release = "bash /home/robot/ki_fabrik/release.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_release)
    time.sleep(3.5)

def turn_60_degree():
    command_60degree = "bash /home/robot/ki_fabrik/gripper_60.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_60degree)

def turn_0_degree():
    command_0degree = "bash /home/robot/ki_fabrik/gripper_0.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_0degree)

if __name__ == '__main__':
    # get_current_cartesian_pose()
    # #initialize_robot()
    # get_current_joint_pose()
    # move_forward(0.6)
     move_backward(0.2)
    #move_right(6.0)
    
    # move_to_cartesian_pose(np.array([0.7072690608193363, -0.706944460281559, 7.539860286166068e-05, 0.0, -0.7069444523180124, -0.7072690644453181, -0.00010869880324885561, 0.0, 0.0001301711161025116, 2.357667648042389e-05, -0.9999999912498103, 0.0, 0.30688001125769293, -2.6843747553594216e-05, 0.5903128317867639, 1.0]))
    
    #release()
    # turn_60_degree()
    # grasp()
    
    
