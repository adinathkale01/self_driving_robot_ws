#include <rclcpp/rclcpp.hpp>
#include <bumperbot_utils/robot_trajectory_vis.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <nav_msgs/msg/path.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

#include <vector>

using std::placeholders::_1;


RobotPathVis::RobotPathVis(const std::string & name)
     :Node(name)


{
   declare_parameter<std::string>("odom_topic", "bumperbot_controller/odom");
   std::string odom_topic = get_parameter("odom_topic").as_string();

   trajectory_pub_= create_publisher<nav_msgs::msg::Path>("bumperbot_controller/trajectory",10);


   odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(odom_topic,10,
     std::bind(&RobotPathVis::odometryCallback, this,_1));


}

void RobotPathVis::odometryCallback(const nav_msgs::msg::Odometry &msg)

{
    trajectory_.header.frame_id = msg.header.frame_id;
    geometry_msgs::msg::PoseStamped curr_pose;
    curr_pose.header.frame_id = msg.header.frame_id;
    curr_pose.header.stamp = msg.header.stamp;
    curr_pose.pose = msg.pose.pose;
    trajectory_.poses.push_back(curr_pose);

    trajectory_pub_->publish(trajectory_);

    RCLCPP_INFO_STREAM(get_logger(), "Trajectory published ! ");
}


int main(int argc, char* argv[])

{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<RobotPathVis>("robot_trajectory");
    rclcpp::spin(node);

    return 0;
}