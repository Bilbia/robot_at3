#! /usr/bin/env python
# -*- coding:utf-8 -*-


import rospy
import numpy as np
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
dist = 0

def scaneou(dado):
    global dist
    print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
    print("Leituras:")
    a = np.array(dado.ranges).round(decimals=2)
    print(a[0])
    dist = a[0]
    #print("Intensities")
    #print(np.array(dado.intensities).round(decimals=2))




if __name__=="__main__":

    rospy.init_node("lidar")

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
    v_frente = Twist(Vector3(0.2,0,0), Vector3(0,0,0))
    v_tras = Twist(Vector3(-0.2,0,0), Vector3(0,0,0))
    recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)



    while not rospy.is_shutdown():
        if dist > 1.02:
            velocidade_saida.publish(v_frente)
            rospy.sleep(2)
        elif dist < 1:
            velocidade_saida.publish(v_tras)
            rospy.sleep(2)