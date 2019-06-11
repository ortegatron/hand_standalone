import numpy as np
import sys
import os
import detection_keypoints
import detection_rectangles
from utils import draw_util
import cv2
import argparse
import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-sth',
        '--scorethreshold',
        dest='score_thresh',
        type=float,
        default=0.2,
        help='Score threshold for displaying bounding boxes')
    parser.add_argument(
        '-src',
        '--source',
        dest='video_source',
        default=0,
        help='Device index of the camera.')
    parser.add_argument(
        '-wd',
        '--width',
        dest='width',
        type=int,
        default=640,
        help='Width of the frames in the video stream.')
    parser.add_argument(
        '-ht',
        '--height',
        dest='height',
        type=int,
        default=360,
        help='Height of the frames in the video stream.')
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    im_width, im_height = (cap.get(3), cap.get(4))

    start_time = datetime.datetime.now()
    num_frames = 0

    detection_graph, sess = detection_rectangles.load_inference_graph()
    while True:
        ret, image_np = cap.read()
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        # 1 - Get bounding boxes for seen hands
        relative_boxes, scores, classes = detection_rectangles.detect_objects(image_np, detection_graph, sess)
        box_relative2absolute = lambda box: (box[1] * im_width, box[3] * im_width, box[0] * im_height, box[2] * im_height)
        hand_boxes = [ box_relative2absolute(box)  for box,score in zip(relative_boxes,scores) if score > args.score_thresh]

        # 2 - Detect keypoints for those bounding boxes
        keypoints, _ = detection_keypoints.detect_keypoints(image_np, hand_boxes)

        # 3 - Draw!
        # Draw bounding boxes
        draw_util.draw_box_on_image(hand_boxes,  image_np)
        # Draw hand keypoints
        draw_util.draw_hand_keypoints(keypoints, image_np)

        # Calculate & Draw Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time
        draw_util.draw_fps_on_image("FPS : " + str(int(fps)), image_np)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
