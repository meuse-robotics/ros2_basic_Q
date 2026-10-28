import rclpy 
from rclpy.node import Node 
from std_msgs.msg import Bool 

class MinimalPublisher(Node): 

  def __init__(self):
    super().__init__('minimal_publisher') 
    self.publisher_ = self.create_publisher(Bool, 'led_status', 10)
    timer_period = 0.5 # seconds(点灯0.5秒 + 消灯0.5秒 = 1秒周期で点滅)
    self.timer = self.create_timer(timer_period, self.timer_callback) 
    self.led_state = False 

  def timer_callback(self): 
    self.led_state = not self.led_state # 呼ばれるたびにON/OFFを反転 
    msg = Bool() 
    msg.data = self.led_state 
    self.publisher_.publish(msg) 
    self.get_logger().info('Publishing: "%s"' % msg.data) 

def main(args=None):
  try:
      with rclpy.init(args=args):
          minimal_publisher = MinimalPublisher()
          rclpy.spin(minimal_publisher)
  except (KeyboardInterrupt, ExternalShutdownException):
      pass

if __name__ == '__main__': 
  main()

