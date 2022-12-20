#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped, Pose
from std_msgs.msg import Bool
import move_base_msgs.msg
import actionlib

rospy.init_node("go_node")
pub = rospy.Publisher("/arrive", Pose, queue_size=10)
pub2 = rospy.Publisher("/go_pose", PoseStamped, queue_size=10)

get_prev_pose = False
prev_pose = Pose()

def cb(data):
    global get_prev_pose, prev_pose
    if get_prev_pose == False:
            get_prev_pose = True
            prev_pose = data.base_position.pose

def go_pose(data):
    global pub, prev_pose, get_prev_pose
    client = actionlib.SimpleActionClient('move_base', move_base_msgs.msg.MoveBaseAction)
    
    client.wait_for_server()
    
    desiredPose = PoseStamped()

    desiredPose.header.frame_id = "map"

    goal = move_base_msgs.msg.MoveBaseGoal(data)
    print(goal)
    
    client.send_goal(goal, feedback_cb=cb)
    client.wait_for_result()
    pub.publish(prev_pose)
    prev_pose = Pose()
    get_prev_pose = False
    
    
rospy.Subscriber("/go_pose", PoseStamped, go_pose)

if __name__ == "__main__":
    while True:
        pass