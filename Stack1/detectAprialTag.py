import pyrealsense2 as rs
import cv2
# import apriltag
import numpy as np
from pupil_apriltags import Detector
import json
import os

# Initialize the RealSense Camera
# Confiure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# Create an AprilTag detector
# The default family is tag25h9 (enodes 25 bits of info, hamming distance is 9)
# The detection will run in a single thread, no decimation is applied
detector = Detector(families='tag25h9', nthreads=1, quad_decimate=1.0)

# Initialize variables to store tag positions
tag_positions = {i: [] for i in range(5)}
tag_pos = {}
tag_pos_aver = {}
frame_count = 0
max_frames = 50
tag_num = 5

# Store the global coordinates of the tag
json_file_path = "/home/fandibi/Desktop/Jingyun/RealSenseCamera/scripts/StackDB.json"

# Load existing data from the JSON file if it exists
with open(json_file_path, 'r') as json_file:
    stack_db = json.load(json_file)

# Initialize the stack_db with empty tag positions
for i in range(tag_num):
    stack_db[str(i)]["pos_cam"] = "None"

# Get positions for all detected tags
for i in range(tag_num):
    tag_pos[i] = [[0, 0, 0]] * max_frames
    tag_pos_aver[i] = [0, 0, 0]


try:
    while frame_count < max_frames:
        # Wait for a new frame from the camera
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert the frame to a numpy array
        color_image = np.asanyarray(color_frame.get_data())
        # Convert the color image to grayscale
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the grayscale image
        tags = detector.detect(gray_image)

        for tag in tags:
            # Get the corners and depth of the tag
            (x_min, x_max, y_min, y_max) = (tag.corners[0][1], tag.corners[0][0], tag.corners[1][1], tag.corners[1][1])
            (w, h) = (x_max - x_min, y_max - y_min)
            z = depth_frame.get_distance(int(tag.center[0]), int(tag.center[1]))

            # Draw the bounding box on the color image
            cv2.rectangle(color_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            
            # transform the apriltag's coordinates to the camera coordinates
            global_coords = np.dot(tag.homography, np.array([tag.center[0], tag.center[1], z]))
            
            if frame_count < max_frames - 1:
                tag_pos[tag.tag_id][frame_count] = global_coords.tolist()
            else:
                tag_pos[tag.tag_id][frame_count] = global_coords.tolist()
                tag_pos_aver[tag.tag_id] = np.mean(tag_pos[tag.tag_id], axis=0).tolist()
                # Update the stack_db with the new tag position
                stack_db[str(tag.tag_id)]["pos_cam"] = tag_pos_aver[tag.tag_id]
            

        # Display the color image with bounding boxes
        cv2.imshow("AprilTag Detection", color_image)
    
        # Increment the frame count
        frame_count += 1

        # press 'q' for 1ms to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline and close all windows
    pipeline.stop()
    cv2.destroyAllWindows()
    
    
    # Save the updated stack_db back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(stack_db, json_file, indent=4)