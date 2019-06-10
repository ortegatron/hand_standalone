# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time
import numpy as np
import config

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        # sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there.q This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


params = dict()
params["model_folder"] = config.OPENPOSE_PATH + "/models"
params["hand"] = True
params["hand_detector"] = 2
# params["hand_net_resolution"] = "184x184"
params["body"] = 0

try:
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
except Exception as e:
    # print(e)
    sys.exit(-1)

# Converts a hand bounding box into a OpenPose Rectangle
def box2oprectangle(box):
    left, right, top, bottom = box
    width = np.abs(right - left)
    height = np.abs(top - bottom)
    max_length = int(max(width,height))
    center = (int(left + (width /2 )), int(bottom - (height/2)))
    # Openpose hand detector needs the bounding box to be quite big , so we make it bigger
    # Top point for rectangle
    new_top = (int(center[0] - max_length / 1.3), int(center[1] - max_length /1.3))
    max_length = int(max_length * 1.6)
    hand_rectangle = op.Rectangle(new_top[0],new_top[1],max_length,max_length)
    return hand_rectangle

def detect_keypoints(image, hand_boxes, threshold=0.5):
    # We are considering every seen hand is a left hand
    hands_rectangles = [[box2oprectangle(box),op.Rectangle(0., 0., 0., 0.)] for box in hand_boxes]
    # hands_rectangles.append([hand_rectangle,op.Rectangle(0., 0., 0., 0.)])

    # Create new datum
    datum = op.Datum()
    datum.cvInputData = image
    datum.handRectangles = hands_rectangles
    # Process and display image
    opWrapper.emplaceAndPop([datum])

    if datum.handKeypoints[0].shape == ():
        # if there were no detections
        hand_keypoints = [[],[]]
    else:
        hand_keypoints = datum.handKeypoints
    return hand_keypoints, datum.cvOutputData
