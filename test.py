import numpy as np
import cv2
import sys
import os

# Load openpose.
sys.path.append('/usr/local/python')
from openpose import *

params = dict()
params["logging_level"] = 3
params["output_resolution"] = "-1x-1"
params["net_resolution"] = "-1x368"
params["model_pose"] = "BODY_25"
params["alpha_pose"] = 0.6
params["scale_gap"] = 0.3
params["scale_number"] = 1
params["render_threshold"] = 0.05
params["num_gpu_start"] = 0
params["disable_blending"] = False
params["default_model_folder"] = "/home/marcelo/openpose/models/"

openpose = OpenPose(params)

frame = cv2.imread("../h5.jpg")

# one person, only one left hand
hands_rectangles = [[[200, 150, 428, 390], [0, 0, 0, 0]]]

for box in hands_rectangles[0]:
    cv2.rectangle(frame, (box[0],box[1]), (box[2],box[3]), (77, 255, 9), 3, 1)


left_hands, right_hands,frame = openpose.forward_hands(frame, hands_rectangles, True)
print "left hands:"
print left_hands

print "right hands:"
print right_hands

    # for hand in left_hands:
    #     for point in hand:
    #         if point[0] != 0:
    #             print point
    #         # print "vaaa"
    #         cv2.circle(frame, (point[0], point[1]), 3, (255,0,0), thickness = -1)
    # for hand in right_hands:
    #     for point in hand:
    #         if point[0] != 0:
    #             print point
    #         cv2.circle(frame, (point[0], point[1]), 3, (0,255,0), thickness = -1)
    # Display the resulting frame
while 1:
    cv2.imshow("output", frame)
    cv2.waitKey(15)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
