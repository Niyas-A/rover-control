#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy
from rover_msgs.msg import CameraMotion

PI = 3.14159

##  To control yaw pitch motion of camera
# 	@joy_sub- joy node subscriber
	

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
    #      @x_axis_value- x axis position of joystick controller
    #	   @y_axis_value- y axis position of joystick controller
    #	   @scale- magnitude of a vector, lies between (0, 5)
    #	   @angle- horizontal plane angle made by controller

 
    def joyCallback(self, data):
        self.left_value = data.buttons[2]
        self.right_value = data.buttons[1]
        self.up_value = data.buttons[3]
        self.down_value = data.buttons[0]
        rospy.loginfo("Left %s\t" % self.left_value +"Rigth %s \t" % self.right_value + "Up %s\t" % self.up_value + "Down %s" % self.down_value)



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

if __name__ == '__main__':
    try:
        camControl = CameraControl()
        camControl.start()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
