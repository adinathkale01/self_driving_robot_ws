#ifndef ROBOT_TRAJECTORY_VIS_HPP
#define ROBOT_TRAJECTORY_VIS_HPP


#include <rclcpp/rclcpp.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <nav_msgs/msg/path.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

#include <string>
#include <memory>
#include <vector>

class RobotPathVis : public rclcpp::Node

{
public:

    RobotPathVis(const std::string & name);

private:
    
   void odometryCallback(const nav_msgs::msg::Odometry & msg);

   rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
   rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr trajectory_pub_;


   nav_msgs::msg::Path trajectory_;

};

#endif