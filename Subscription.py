#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3Stamped
#from hector_uav_msgs.msg import *
import csv

l = csv.writer(open("Location.csv", "wb"))
s = csv.writer(open("Sensor.csv", "wb"))
p = csv.writer(open("PRW.csv", "wb"))
#f = csv.writer(open("Force.csv", "wb"))

def callback(odom):
    (x,y,z,w,a,b,g) = (odom.pose.pose.position.x,odom.pose.pose.position.y,odom.pose.pose.position.z,odom.pose.pose.orientation.x,odom.pose.pose.orientation.y,odom.pose.pose.orientation.z,odom.pose.pose.orientation.w)
    #print x,y,z,w,a,b,g
    t = rospy.get_time()
    l.writerow([x,y,z,w,a,b,g,t])

def call(Imu):    
    (al,be,ga,a1,b1,c1) = (Imu.linear_acceleration.x,Imu.linear_acceleration.y,Imu.linear_acceleration.z,Imu.angular_velocity.x,Imu.angular_velocity.y,Imu.angular_velocity.z)
    ti = rospy.get_time()
    s.writerow([al,be,ga,a1,b1,c1,ti])

def euler(Vector3Stamped):
    (al,be,ga) = Vector3Stamped.vector.x,Vector3Stamped.vector.y,Vector3Stamped.vector.z
    t = rospy.get_time()
    p.writerow([al,be,ga,t])

#def force(WrenchStamped):
#    #print dir(WrenchStamped.wrench)
#    (fx,fy,fz,tx,ty,tz) = #WrenchStamped.wrench.force.x,WrenchStamped.wrench.force.y,WrenchStamped.wrench.force.z,WrenchStamped.wrench.torque.x,WrenchStamped.wrench.torque.y,WrenchStamped.wrench.torque.z
#    t = rospy.get_time()
#    f.writerow([fx,fy,fz,tx,ty,tz,t])

def listener():

    rospy.init_node('location', anonymous=True)

    rospy.Subscriber("ground_truth/state", Odometry, callback, queue_size = 100)
    rospy.Subscriber("raw_imu", Imu, call, queue_size = 100)
    rospy.Subscriber("ground_truth_to_tf/euler", Vector3Stamped,euler,queue_size = 100)
    #rospy.Subscriber("", ,force,queue_size = 100)
    #spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
