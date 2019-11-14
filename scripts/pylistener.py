#!/usr/bin/env python
#coding=utf-8
import rospy
import math
#导入mgs到pkg中
from sensor_msgs.msg import LaserScan

#回调函数输入的应该是msg
def callback(LaserScan):
    rospy.loginfo(LaserScan)

def listener():
    rospy.init_node('scan_listener', anonymous=True)
    #Subscriber函数第一个参数是topic的名称，第二个参数是接受的数据类型 第三个参数是回调函数的名称
    rospy.Subscriber('/tb3_1/scan', LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

