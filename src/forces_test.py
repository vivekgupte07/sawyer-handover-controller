#! /usr/bin/env python

import rospy
import math
from intera_core_msgs.msg import EndpointState
def main():
	rospy.init_node('forces_test_py')
	sub = rospy.Subscriber('/robot/limb/right/endpoint_state', EndpointState, force_callback)
	while True:
		try:
			pass
		except rospy.ROSInterruptionException:
			rospy.logerr('Detected keyboard interruption from the user')	
	
		

def force_callback(msg):
	force_x = msg.wrench.force.x
	force_y = msg.wrench.force.y
	force_z = msg.wrench.force.z
	print(math.sqrt(force_x**2+force_y**2+force_z**2))

if __name__ == '__main__':
	main()