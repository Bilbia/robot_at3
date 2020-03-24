#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist, Vector3
import numpy as np 

k = 0
if __name__ == "__main__":
	pub = rospy.Publisher("cmd_vel", Twist, queue_size=4)
	rospy.init_node("roda_exemplo")
	v_frente = Twist(Vector3(0.2,0,0), Vector3(0,0,0))
	v_curva = Twist(Vector3(0,0,0), Vector3(0,0,np.pi/6))
	v_parado = Twist(Vector3(0,0,0), Vector3(0,0,0))


	try:
		while not rospy.is_shutdown():
			if k<5:
				pub.publish(v_frente)
				rospy.sleep(5)
				pub.publish(v_parado)
				rospy.sleep(0.5)
				pub.publish(v_curva)
				rospy.sleep(3.095)
				pub.publish(v_parado)
				k+=1
	except rospy.ROSInterruptException:
		print("Ocorreu uma exceção com o rospy")


