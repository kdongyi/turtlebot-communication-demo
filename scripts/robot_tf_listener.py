#!/usr/bin/env python
#coding=utf-8

import rospy

import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('item')

    listener = tf.TransformListener() #TransformListener创建后就开始接受tf广播信息，最多可以缓存10s

    '''
    #设置robot2的初始坐标
    rospy.wait_for_service('spawn') #等待spawn的service出现 阻塞  spawn是sim提供的一个服务
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn) #建立client，向spawn请求turtlesim.srv.Spawn类型的数据
    spawner(4, 2, 0, 'robot2') #发起请求 将请求的参数传入  robot2的初始位置
                                #    float32 x      参数传入 初始的坐标x
                                #    float32 y      参数传入 初始的坐标y
                                #    float32 theta  参数传入 初始的角度theta
                                #    string name    参数传入
                                #    ---
                                #    string name
    '''

    #Publisher 函数第一个参数是话题名称，第二个参数 数据类型，现在就是我们定义的msg 最后一个是缓冲区的大小
    turtle_vel = rospy.Publisher('robot2/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            #得到以robot2为坐标原点的robot1的姿态信息(平移和旋转)
            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time()) #查看相对的tf,返回平移和旋转  turtle2跟着turtle1变换
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        angular = math.atan2(trans[1], trans[0]) #角度变换 计算出前往robot1的角速度
        linear = math.sqrt(trans[0] ** 2 + trans[1] ** 2) #平移变换 计算出前往robot1的线速度
        msg = geometry_msgs.msg.Twist()
        #msg.linear.x = linear   #平移变换
        #msg.angular.z = angular #角度变换
        rospy.loginfo('linear=%f, angular=%f', linear, angular)
        
        if linear>0.008: #如果robot1不动，但是数值有轻微漂移 就不让robot2动
            msg.linear.x = linear #*0.2    #平移变换
            msg.angular.z = angular #*0.1  #角度变换
        else:
            msg.linear.x = 0
            msg.angular.z = 0
        
        turtle_vel.publish(msg) #向/robot2/cmd_vel话题发布新坐标  (即robot2根据/robot2/cmd_vel的数据来控制robot2移动)
        rate.sleep()
        