import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist

from arduino.app_utils import *

class CommandSubscriberAction(Node):
    target_speed_R = 0.0
    target_speed_L = 0.0
    def __init__(self):
        super().__init__('command_subscriber_action')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
                        
    def listener_callback(self, Twist):
        self.get_logger().info(f'並進速度={Twist.linear.x}角速度={Twist.angular.z}')
        self.target_speed_R = Twist.linear.x + Twist.angular.z
        self.target_speed_L = Twist.linear.x - Twist.angular.z
        Bridge.call("set_target_speed", self.target_speed_R, self.target_speed_L)
        
def main(args=None):
    try:
        with rclpy.init(args=args):
            command_subscriber_action = CommandSubscriberAction()
            rclpy.spin(command_subscriber_action)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

if __name__ == '__main__':
    main()
