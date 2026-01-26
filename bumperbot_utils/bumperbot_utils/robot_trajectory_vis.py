#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped


class RobotPathVis(Node):
    def __init__(self):
        super().__init__("robot_trajectory")

        self.declare_parameter("odom_topic", "bumperbot_controller/odom")
        odom_topic = self.get_parameter("odom_topic")
        self.odom_sub_ = self.create_subscription(Odometry, str(odom_topic.value), self.odometryCallback,10)
        self.trajectory_pub_ = self.create_publisher(Path,"bumperbot_controller/trajectory",10)

        self.trajectory_ = Path()
        
      


    def odometryCallback(self,msg: Odometry):
        self.trajectory_.header.frame_id = msg.header.frame_id

        curr_pose = PoseStamped()
        curr_pose.header.frame_id = msg.header.frame_id
        curr_pose.header.stamp = msg.header.stamp
        curr_pose.pose = msg.pose.pose
        self.trajectory_.poses.append(curr_pose)
        self.trajectory_pub_.publish(self.trajectory_)
        
def main():
    rclpy.init()
    robot_path_vis = RobotPathVis()
    rclpy.spin(robot_path_vis)
    robot_path_vis.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()

