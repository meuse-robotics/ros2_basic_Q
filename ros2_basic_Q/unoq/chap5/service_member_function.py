from robot_interfaces.srv import RobotCommand

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from arduino.app_utils import *

class RobotService(Node):
    target_speed_R = 0.0
    target_speed_L = 0.0
    def __init__(self):
        super().__init__('robot_service')
        self.srv = self.create_service(RobotCommand, 'robot_command', self.robot_command_callback)

    def robot_command_callback(self, request, response):
        response.done = False
        # 走行開始
        self.target_speed_R = 0.3
        self.target_speed_L = 0.3
        Bridge.call("set_target_speed", self.target_speed_R, self.target_speed_L)
        # 距離到達を待つ
        while count_R < request.dist:
            pass
        # 停止
        self.target_speed_R = 0.0
        self.target_speed_L = 0.0
        Bridge.call("set_target_speed", self.target_speed_R, self.target_speed_L)
        response.done = True
        return response

def main(args=None):
    try:
        with rclpy.init(args=args):
            robot_service = RobotService()
            rclpy.spin(robot_service)
            
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

if __name__ == '__main__':
    main()
