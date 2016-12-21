#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy
from rover_msgs.msg import CameraMotion

PI = 3.14159
motion_value = [True, True, True, True]

##  To control yaw pitch motion of camera
# 	@joy_sub- joy node subscriber
#	@data - is the array of the joystick values

class CameraControl:
    def __init__(self):
	self.left_value=0
        self.right_value=0
        self.up_value=0
        self.down_value=0
        rospy.init_node('CameraControl', anonymous = True)
        self.topic= rospy.get_param('~camear_topic','rover1/camera_dir')
        self.joy_sub = rospy.Subscriber('joy', Joy, self.joyCallback)

    ## @joyCallback callback function for joy subscriber
    #    left_value = data.buttons[2]
    #    right_value = data.buttons[1]
    #    up_value = data.buttons[3]
    #    down_value = data.buttons[0]

 
    def joyCallback(self, data):
        motion_value[0] = data.buttons[2]
        motion_value[1] = data.buttons[1]
        motion_value[2] = data.buttons[3]
        motion_value[3] = data.buttons[0]
        rospy.loginfo("Left %s\t" % data.buttons[2] +"Rigth %s \t" % data.buttons[1] + "Up %s\t" % data.buttons[3] + "Down %s" % data.buttons[0])



    ##  @start starts to publish the values to 'rover1/camera_dir' topic
    #	    @cam_pub- is   publisher variable
    #	    @rate- publishing rate in Hz      

    def start(self):
        self.cam_pub = rospy.Publisher(self.topic, CameraMotion, queue_size = 10)
        self.rate = rospy.Rate(10)

        CameraMotion.X_button = self.left_value
        CameraMotion.B_button = self.right_value
        CameraMotion.Y_button = self.up_value
        CameraMotion.A_button = self.down_value

        while not rospy.is_shutdown():
            self.cam_pub.publish(CameraMotion)
            self.rate.sleep()
        cam_pub = rospy.Publisher('rover1/camera_dir', CameraMotion, queue_size = 10)
        joy_sub = rospy.Subscriber('joy', Joy, self.joyCallback)
        rate = rospy.Rate(10)
        print value
        while not rospy.is_shutdown():
            rospy.loginfo("camera motion values publishing %s" % get_time())
            cam_pub.publish( motion_value[0], motion_value[1], motion_value[2], motion_value[3])
            rate.sleep()

if __name__ == '__main__':
    try:
        camControl = CameraControl()
        camControl.start()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
