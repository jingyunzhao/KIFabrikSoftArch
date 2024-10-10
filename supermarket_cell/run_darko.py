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

json_file_path = "/home/fandibi/Desktop/Jingyun/KIFabrikSoftArch/supermarket_cell/DarkoDB.json"
with open(json_file_path, 'r') as json_file:
    DarkoDB = json.load(json_file)

robot_address = "192.168.50.89"
robot = robot_address

M_PI_2 = math.pi/2
M_PI_4 = math.pi/4

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(robot_address, username="robot", password="R0b0tn1K")

def initialize_robot():
    initial_joint_pose = np.array([0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4])
    response = start_task(robot, "MoveToJointPose", parameters={"parameters": {"q_g": initial_joint_pose .tolist(),"pose":"NoneObject","speed":1.5,"acc": 1}})
    wait_for_task(robot, response["result"]["task_uuid"])
    time.sleep(0.5)

def get_current_joint_pose():
    robot_state = call_method(robot, 12000, "get_state")
    print(robot_state['result']['q'])
    return robot_state['result']['q']

def get_current_cartesian_pose():
    robot_state = call_method(robot, 12000, "get_state")
    print(robot_state['result']['O_T_EE'])
    DarkoDB["EndEffector"]["pos_Darko"] = robot_state['result']['O_T_EE']
    print(DarkoDB["EndEffector"]["pos_Darko"])
    return robot_state['result']['O_T_EE']
    

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
    DarkoDB["Darko"]["pos_globalCoSys"][1] = DarkoDB["Darko"]["pos_globalCoSys"][1] + step

def move_backward(step):
    command_backward = "bash /home/robot/ki_fabrik/call_service.sh " + str(step) + " 0.0"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_backward)
    time.sleep(3)

    DarkoDB["Darko"]["pos_globalCoSys"][1] -= step
    

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
    time.sleep(0.5)

def turn_0_degree():
    command_0degree = "bash /home/robot/ki_fabrik/gripper_0.sh"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_0degree)
    time.sleep(0.5)

def pick_place_cart_pose(stack, initial_pose, final_pose):
    if stack == "stack1":
        initialize_robot()
        # move to the top of object
        current_pose_inter = initial_pose.copy()
        current_pose_inter[14] += 0.5
        move_to_cartesian_pose(current_pose_inter)
        # move to initial pose and grasp object
        move_to_cartesian_pose(initial_pose)
        grasp()
        inter_pose1 = initial_pose.copy()
        # move up
        inter_pose1[14] += 0.5
        move_to_cartesian_pose(inter_pose1)
        # move to the intermediate pose
        initialize_robot()
        # move to the top of MiR
        inter_pose3 = final_pose.copy()
        inter_pose3[14] += 0.2
        move_to_cartesian_pose(inter_pose3)
        # move to the final pose and release object
        move_to_cartesian_pose(final_pose)
        release()
        # move to initial pose
        initialize_robot()
        
    elif stack == "stack2":
        move_backward(2.2)
        move_to_cartesian_pose(initial_pose)
        grasp()
        inter_pose1 = initial_pose.copy()
        # move relative z
        inter_pose1[14] += 0.5
        move_to_cartesian_pose(inter_pose1)
        # move relative x,y
        inter_pose2 = inter_pose1.copy()
        inter_pose2[12] += 0.2
        inter_pose2[13] -= 0.5
        move_to_cartesian_pose(inter_pose2)
        move_forward(2.2)
        move_to_cartesian_pose(final_pose)
        release()
        initialize_robot()


    


if __name__ == '__main__':
    #move_backward(1)
    #move_forward(1)
    get_current_cartesian_pose()
    initial_pose_BoltLarge = np.array(
        [0.9902428657423871, 0.1325419312182168, 0.04303142241723327, 0.0, 0.13271805028444744, -0.9911530447466347, -0.0012494071275994721, 0.0, 0.0424851265150495, 0.006948262978694707, -0.999072938111417, 0.0, -0.011126171265929945, 0.5759671442350419, 0.007212040424899813, 1.0]
    )
    final_pose_BoltLarge = np.array(
        [0.8190554874025577, -0.5732162667808365, 0.023900210325427985, 0.0, -0.572760914343335, -0.8193851955692595, -0.02351247078708345, 0.0, 0.033061209239012804, 0.00556891190156289, -0.9994378138052847, 0.0, 0.5321851108118002, 0.08072829748227492, 0.33030582256626995, 1.0]
    
    )

    initial_pose_BoltSmall = np.array(
        [0.9981532545215135, 0.05395392750475516, 0.02791154232432424, 0.0, 0.05252054439545814, -0.9973791678427912, 0.049763319519765, 0.0, 0.030523317390408842, -0.04820548993665706, -0.9983709520190637, 0.0, -0.11586759245703397, 0.5753492421623617, 0.026784858418667123, 1.0]

    )

    finally_pose_BoltSmall = np.array(
        [0.7486427209512829, -0.6618148695526198, 0.039181051615655216, 0.0, -0.6624459018396971, -0.7490969203093383, 0.004385329959711692, 0.0, 0.02644812852453665, -0.029238372425868173, -0.9992225047883159, 0.0, 0.41436092063618934, -0.028685068836993108, 0.33444100516400777, 1.0]
    )

    initial_pose_GearSmall = np.array(
        [0.9925286946145085, 0.0989738991449122, 0.07135094711965871, 0.0, 0.09999239241720918, -0.9949291733466405, -0.010837964866760266, 0.0, 0.06991646319360297, 0.017891543025211926, -0.9973923906179926, 0.0, 0.08884711341420029, 0.5789054267001537, -0.011781603958383624, 1.0]
    )

    final_pose_GearSmall = np.array(
        [0.0202856600554806, -0.9997824464066198, 0.004853025170720392, 0.0, -0.9992457683974307, -0.02043505130223294, -0.033019736796395235, 0.0, 0.03311172505233741, -0.0041795377099953695, -0.9994429173937793, 0.0, 0.4242902179946293, 0.10191520899873982, 0.34132227759775197, 1.0]

    )

    
    pick_place_cart_pose("stack1", initial_pose_BoltLarge, final_pose_BoltLarge)
    pick_place_cart_pose("stack1", initial_pose_BoltSmall, finally_pose_BoltSmall)
    pick_place_cart_pose("stack1", initial_pose_GearSmall, final_pose_GearSmall)
    move_backward(1)
    with open(json_file_path, 'w') as json_file:
        json.dump(DarkoDB, json_file, indent=4)


    # initial_pose_CompoundGear = np.array(
    #     [0.9168473819555785, -0.3974205508853576, 0.03804975604626876, 0.0, -0.3983261866273177, -0.9170269165478312, 0.01994701415542364, 0.0, 0.02696529710834051, -0.03344458193424104, -0.9990767401411679, 0.0, 0.1972393117864518, 0.5509806750582436, -0.02476130578160346, 1.0]
    #     )

    # final_pose_CompoundGear = np.array(
    #     [0.868384828188408, -0.4928111012458896, 0.055181597122616916, 0.0, -0.4923544608743575, -0.8701031059195818, -0.02253153182138038, 0.0, 0.059117468055643226, -0.007602865111960997, -0.9982220802069945, 0.0, 0.5325441187335227, -0.029319966002356694, 0.350057878391162, 1.0]
    # )
    # pick_place_cart_pose("stack2", initial_pose_CompoundGear, final_pose_CompoundGear)



    
    
