import cv2

# draw the detected bounding boxes on the images
def draw_box_on_image(boxes, image_np):
    for box in boxes:
        (left, right, top, bottom) = box
        p1 = (int(left), int(top))
        p2 = (int(right), int(bottom))
        cv2.rectangle(image_np, p1, p2, (77, 255, 9), 3, 1)

# Show fps value on image.
def draw_fps_on_image(fps, image_np):
    cv2.putText(image_np, fps, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (77, 255, 9), 2)

# Draws the fingers keypoints and them
def draw_hand_keypoints(keypoints, image_np):
    for hand_list in keypoints:
        for hand in hand_list:
            for i in range(0,len(HAND_PAIRS),2):
                i0,i1  = HAND_PAIRS[i], HAND_PAIRS[i+1]
                p0,p1 = tuple(hand[i0,:2].astype(int)), tuple(hand[i1,:2].astype(int))
                color = tuple(HAND_COLORS[int(i/2)*3:(int(i/2)*3) + 3])
                cv2.line(image_np,p0,p1,color,thickness=5,lineType=8)

# Extracted from openpose rendering
HAND_PAIRS  =  [0,1,  1,2,  2,3,  3,4,  0,5,  5,6,  6,7,  7,8,  0,9,  9,10,  10,11,  11,12,  0,13,  13,14,  14,15,  15,16,  0,17,  17,18,  18,19,  19,20]
HAND_COLORS =  [
    100,  100,  100, \
    100,    0,    0, \
    150,    0,    0, \
    200,    0,    0, \
    255,    0,    0, \
    100,  100,    0, \
    150,  150,    0, \
    200,  200,    0, \
    255,  255,    0, \
      0,  100,   50, \
      0,  150,   75, \
      0,  200,  100, \
      0,  255,  125, \
      0,   50,  100, \
      0,   75,  150, \
      0,  100,  200, \
      0,  125,  255, \
    100,    0,  100, \
    150,    0,  150, \
    200,    0,  200, \
    255,    0,  255 ]
