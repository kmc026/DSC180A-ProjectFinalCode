#!/usr/bin/env python

import roslib
import sys
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String

import lane_utils
from ackermann_msgs.msg import AckermannDriveStamped

from datetime import datetime

class follow_centroid(object):
    def __init__(self):
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.camera_callback)
        self.drivecar_object = drive_car()
        self.temp_time = datetime.now()

    def camera_callback(self, data):
        start = datetime.now()
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            
        h = cv_image.shape[0]
        w = cv_image.shape[1]

        cropped_bgr_img = cv_image[int(h*0.5):, int(w*0.2):int(w*0.8)]
        lane_img = lane_utils.find_yellow_lanes(cropped_bgr_img)
        centroid_img, (cX, cY) = lane_utils.find_n_largest_contours(lane_img)
        cv2.imshow("Image", cropped_bgr_img)
        cv2.imshow("Centroid", centroid_img)
        cv2.waitKey(1)
        
        h = cropped_bgr_img.shape[0]
        w = cropped_bgr_img.shape[1]

        # if cX > h*0.6:
        #     my_steering_angle = -np.arctan(cY-w/0.3)
        #     temp_percent = cX/h
        # elif cX > h*0.45:
        #     my_steering_angle = -np.arctan((cY-w/2)/2)

        if cX > w/2:
            my_steering_angle = -0.7#-np.arctan((cY-w/2) / (h-cX+1e-20))
        else:
            my_steering_angle = 0.7

        acker_object = AckermannDriveStamped()
        acker_object.drive.steering_angle = my_steering_angle
        print(cY, w/2)
        acker_object.drive.steering_angle_velocity = my_steering_angle/200
        acker_object.drive.speed = 0.5


        self.drivecar_object.move_robot(acker_object)


class drive_car(object):
    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher('/vesc/low_level/ackermann_cmd_mux/output', AckermannDriveStamped, queue_size=1)
        self.last_cmdvel_command = AckermannDriveStamped()

    def move_robot(self, acker_object):
        self.cmd_vel_pub.publish(acker_object)
    
    def reset_robot(self):
        return


def main():
    line_follower_object = follow_centroid()
    rospy.init_node("line_following_node")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()