# Standalone hand detector python wrapper for OpenPose

The content in folder lib is a modification for the OpenPose python wrapper to support Standalone hand keypoint detection.
Copy the content in lib to your OpenPose folder, replacing the existing files. Then sudo make install OpenPose again, and executing test.py should show you the detected hand.

The detector needs as a parameter the bounding box for the hands. 
