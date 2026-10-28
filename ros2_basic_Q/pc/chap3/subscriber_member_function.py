import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Bool

import arduino.app_utils as app_utils

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Bool,
            'led_status',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
		self.get_logger().info(f'Setting LED to: {msg.data}') 
        app_utils.Bridge.call("set_led_state", msg.data)

def main(args=None):

    try:
		with rclpy.init(args=args):
			minimal_subscriber = MinimalSubscriber()
        	rclpy.spin(minimal_subscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
	
if __name__ == '__main__':
    main()
