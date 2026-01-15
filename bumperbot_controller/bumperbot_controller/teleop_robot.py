#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import sys, select, termios, tty

# Key mapping
move_bindings = {
    '\x1b[A': (1.0, 0.0),   # Up arrow -> forward
    '\x1b[B': (-1.0, 0.0),  # Down arrow -> backward
    '\x1b[C': (0.0, -1.0),  # Right arrow -> turn right
    '\x1b[D': (0.0, 1.0),   # Left arrow -> turn left
}

# Velocities
LINEAR_SPEED = 0.2  # m/s
ANGULAR_SPEED = 0.5 # rad/s

def get_key():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    key = ''
    if rlist:
        key = sys.stdin.read(3)  # arrow keys are 3 chars: \x1b[A etc.
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        self.pub = self.create_publisher(
            TwistStamped, '/bumperbot_controller/cmd_vel', 10
        )
        self.get_logger().info("Keyboard Teleop Started. Use arrow keys to move.")

        # Timer to continuously publish zero velocity if no key is pressed
        self.timer = self.create_timer(0.1, self.publish_zero)
        self.current_key = None

    def publish_zero(self):
        if self.current_key is None:
            msg = TwistStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.0
            self.pub.publish(msg)

    def run(self):
        global settings
        settings = termios.tcgetattr(sys.stdin)
        try:
            while rclpy.ok():
                key = get_key()
                self.current_key = key
                if key in move_bindings:
                    linear, angular = move_bindings[key]
                    msg = TwistStamped()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.twist.linear.x = linear * LINEAR_SPEED
                    msg.twist.angular.z = angular * ANGULAR_SPEED
                    self.pub.publish(msg)
                    self.get_logger().info(f"Linear: {msg.twist.linear.x:.2f}, Angular: {msg.twist.angular.z:.2f}")
                elif key == '\x03':  # Ctrl-C
                    break
                else:
                    self.current_key = None
        except Exception as e:
            print(e)
        finally:
            # Stop robot on exit
            msg = TwistStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.0
            self.pub.publish(msg)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
