# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import socket
import sys
import time
import numpy as np
import math
from utils.ws_client import *
# from utils.ws_server import *
import time
import socket
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


import time

# import mongodb_client

if __name__ == '__main__':
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = ('192.168.50.99', 6666)
    client_address = ('192.168.50.198', 6666)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    robot_address = "192.168.50.89"
    robot = robot_address

    M_PI_2 = math.pi / 2
    M_PI_4 = math.pi / 4
    initial_joint_pose = np.array([0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4])

    test_qg = initial_joint_pose
    # test_qg = np.array([-1.1477964347996021, -1.3880052630009574, -0.9794327660107208, -2.4222280607667446, 2.298190836064857, 0.9830451754554606, 1.1098089323587337])
    # print(test_qg.tolist()
    initial_joint_pose = np.array(
        [-2.268885480857732, 0.4744216123505642, 2.6617370438120287, -2.062852881212679, -0.19150864213296553,
         1.63361104432943, 1.107074219133291])
    object_1_close_pose = np.array(
        [-1.0377019503158433, -0.4489570542896507, 2.8741077458900315, -1.3312100165702179, 0.07900342184893878,
         1.760030247138759, 1.8925708468846147])
    object_1_grasp_pose = np.array(
        [-1.03485671050925, -0.6809272759755451, 2.8813040543271784, -1.6100640451698967, 0.14916997120777767,
         2.25590418153339, 1.8891711855025755])

    object_2_close_pose = np.array(
        [-0.9272598373027588, -0.6411302692764682, 2.8621905297396477, -0.9926459863810485, 0.14434351238081358,
         1.6346448577774895, 1.9739544741403725])
    object_2_grasp_pose = np.array(
        [-0.933083209466051, -0.9224595624438502, 2.8768413398809596, -1.1606237204032865, 0.17352179712057114,
         1.991640931500329, 1.9770847749980596])

    clip_1_close_pose = np.array(
        [-1.005922393957774, -0.2182378066770603, 2.706780825564736, -1.6379148206766703, 0.05506252198778876,
         1.8570618579122753, 1.7012551053456133])
    clip_1_grasp_pose = np.array(
        [-1.0223227153297552, -0.5017795692553942, 2.7518800473464164, -1.8985448426533893, 0.18476918443578305,
         2.363389016765944, 1.6103409783136513])

    clip_2_close_pose = np.array(
        [-1.1639658706146372, -0.8739003850200718, 2.677226972312258, -0.9357609403800438, 0.2905798906683922,
         1.7508346380127802, 1.4267260106495685])
    clip_2_grasp_pose = np.array(
        [-1.1369058975336916, -0.9256658871884931, 2.7333433099909445, -1.1710651942303303, 0.293888136672726,
         2.0220558674372326, 1.4179525391351846])

    on_top_of_shelf_pose = np.array(
        [-2.622488614174592, -0.37543804799464703, 2.86243587768287, -2.3509098590047737, -0.028267208419220084,
         2.710033222569359, 0.16349286358472373])
    on_top_of_shelf_pose_2 = np.array(
        [-2.795723049172184, -0.4374196746391162, 2.8008170841426083, -2.3425375659436365, 0.10045927123228708,
         2.775411907566918, -0.05565405010266437])

    drop_pose_1 = np.array(
        [-2.892550315733541, -1.5309489314263325, 2.542056708800685, -0.6452538620556476, 0.5944558501376046,
         2.062135200623292, 0.4399882428761731])
    drop_pose_2 = np.array(
        [-2.8629356735832987, -1.391049015195746, 2.577345009219527, -0.8303657457786693, 0.6527464072042041,
         2.003277264699543, -0.15063784227189086])

    transition_pose = np.array(
        [-1.526560262286872, 0.23213233465942273, 2.6525232539929844, -1.5605149462348535, -0.08279935989777278,
         1.2832932142656215, 1.1896703052197561])

    robot_state = call_method(robot, 12000, "get_state")
    print(robot_state)

    response = start_task(robot, "MoveToJointPose", parameters={
        "parameters": {"q_g": initial_joint_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
    wait_for_task(robot, response["result"]["task_uuid"])
    # print(response)

    ssh = paramiko.SSHClient()
    a = ssh.load_system_host_keys()
    ssh.connect(robot_address, username="robot", password="R0b0tn1K")
    # time.sleep(5)

    # command = "rosservice call /robot/robot_local_control/NavigationComponent/MoveComponent/add \"{procedure: {goal: {x: -0.2, y: 0}, maximum_velocity: {linear: {x: 0.05, y: 0.05, z: 0.05}, angular: {x: 0.05, y: 0.05, z: 0.05}}}}\""
    # source_command = "source /home/robot/.bashrc"

    command_forward = "bash /home/robot/ki_fabrik/call_service_forward.sh -0.6 0.0"
    command_backward = "bash /home/robot/ki_fabrik/call_service_backward.sh 0.6 0.0"

    command_grasp = "bash /home/robot/ki_fabrik/grasp.sh"
    command_release = "bash /home/robot/ki_fabrik/release.sh"

    command_60degree = "bash /home/robot/ki_fabrik/gripper_60.sh"
    command_0degree = "bash /home/robot/ki_fabrik/gripper_0.sh"

    command_pan_target_obj = "bash /home/robot/ki_fabrik/pan_target_obj.sh"
    command_pan_target = "bash /home/robot/ki_fabrik/pan_target.sh"
    command_tilt_target = "bash /home/robot/ki_fabrik/tilt_target.sh"
    command_tilt_target_obj = "bash /home/robot/ki_fabrik/tilt_target_obj.sh"
    # command = "uname -a"

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_forward)
    time.sleep(3)
    # # print(ssh_stderr)
    # # print(ssh_stdout)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_60degree)
    time.sleep(3)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_release)
    time.sleep(3)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_pan_target_obj)
    time.sleep(3)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_tilt_target_obj)
    time.sleep(3)

    lines = ssh_stderr.readline()
    for line in lines:
        print(line)
    sum = 0

    while True:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(4096)

        target_string = data.decode("utf-8")

        print('received {} bytes from {}'.format(len(data), address))

        print(data)
        print(target_string)
        data = str.encode(data.decode("utf-8") + "+done")
        sum += 1

        if target_string == "Get item ['cable_red']":
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_0degree)
            time.sleep(0.5)

            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": object_1_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_60degree)
            # time.sleep(2)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": object_1_grasp_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_grasp)
            time.sleep(3.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": object_1_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": transition_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": on_top_of_shelf_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            # wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            # response = start_task(robot, "MoveToJointPose", parameters={"parameters": {"q_g": drop_pose_1.tolist(), "pose": "NoneObject"}})
            # wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_release)
            time.sleep(3.5)

            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": initial_joint_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            # time.sleep(0.5)
            wait_for_task(robot, response["result"]["task_uuid"])

            sent = sock.sendto(data, client_address)
            print('sent {} bytes back to {}'.format(sent, client_address))

        if target_string == "Get item ['cable_grey']":
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_0degree)

            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": object_2_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": object_2_grasp_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_grasp)
            time.sleep(3.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": object_2_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": transition_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": on_top_of_shelf_pose_2.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            # response = start_task(robot, "MoveToJointPose", parameters={"parameters": {"q_g": drop_pose_2.tolist(), "pose": "NoneObject"}})
            # wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_release)
            time.sleep(3.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": initial_joint_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)

            sent = sock.sendto(data, client_address)
            print('sent {} bytes back to {}'.format(sent, client_address))

        if sum == 1:

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_60degree)

            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": clip_1_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": clip_1_grasp_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_grasp)
            time.sleep(3.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": clip_1_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": transition_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": on_top_of_shelf_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            # response = start_task(robot, "MoveToJointPose", parameters={"parameters": {"q_g": drop_pose_2.tolist(), "pose": "NoneObject"}})
            # wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_release)
            time.sleep(3.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": initial_joint_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)

            #second clip
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_60degree)

            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": clip_2_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": clip_2_grasp_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_grasp)
            time.sleep(3.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": clip_2_close_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": transition_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": on_top_of_shelf_pose_2.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)
            # response = start_task(robot, "MoveToJointPose", parameters={"parameters": {"q_g": drop_pose_2.tolist(), "pose": "NoneObject"}})
            # wait_for_task(robot, response["result"]["task_uuid"])
            # time.sleep(0.5)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_release)
            time.sleep(3.5)
            response = start_task(robot, "MoveToJointPose", parameters={
                "parameters": {"q_g": initial_joint_pose.tolist(), "pose": "NoneObject", "speed": 1.5, "acc": 2}})
            wait_for_task(robot, response["result"]["task_uuid"])
            time.sleep(0.5)

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_tilt_target)
            time.sleep(3)

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_pan_target)
            time.sleep(3)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_backward)
            time.sleep(3)
            sent = sock.sendto(data, client_address)
            print('sent {} bytes back to {}'.format(sent, client_address))

        if data:
            sent = sock.sendto(data, client_address)
            print('sent {} bytes back to {}'.format(sent, client_address))