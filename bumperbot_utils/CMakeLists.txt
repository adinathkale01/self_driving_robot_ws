cmake_minimum_required(VERSION 3.8)
project(bumperbot_utils)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(twist_mux_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

add_executable(robot_trajectory_vis src/robot_trajectory_vis.cpp)
target_include_directories(robot_trajectory_vis PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(robot_trajectory_vis rclcpp geometry_msgs nav_msgs)


add_executable(safety_stop src/safety_stop.cpp)
target_include_directories(safety_stop PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(safety_stop rclcpp rclcpp_action sensor_msgs std_msgs twist_mux_msgs visualization_msgs )

ament_python_install_package(${PROJECT_NAME})


install(TARGETS
   robot_trajectory_vis
   DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS
   safety_stop
   DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS 
  ${PROJECT_NAME}/robot_trajectory_vis.py
  DESTINATION lib/${PROJECT_NAME})

install(PROGRAMS 
  ${PROJECT_NAME}/safety_stop.py
  DESTINATION lib/${PROJECT_NAME})


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
 
  set(ament_cmake_copyright_FOUND TRUE)
 
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
