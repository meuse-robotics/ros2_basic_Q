#ros
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions

from geometry_msgs.msg import Twist
#pyqtGui
import sys
from .controller import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow,QApplication

STEP = 0.1          # 1回のキー入力で変化する速度の刻み
MAX_LINEAR = 1.0    # 並進速度の上限 [m/s]
MAX_ANGULAR = 1.0   # 角速度の上限 [rad/s]

HELP = 'f:前進  b:後退  l:左旋回  r:右旋回  s:停止  q:終了  (入力後Enter)'

class CommandPublisherGui(QMainWindow):

    def __init__(self, parent=None):
        #GUI
        super(CommandPublisherGui, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #ROS
        rclpy.init()
        self.node = Node('commander')
        self.publisher_ = self.node.create_publisher(Twist, 'cmd_vel', 10)
        self.vel = Twist()
        self.vel.linear.x = 0.0
        self.vel.angular.z = 0.0
        # 浮動小数点の累積誤差を避けるため、速度は「段数(整数)」で保持する
        self.linear_steps = 0
        self.angular_steps = 0
        self.max_linear_steps = round(MAX_LINEAR / STEP)
        self.max_angular_steps = round(MAX_ANGULAR / STEP)

    def fwrd(self):
        self.linear_steps += 1
        self.publish_velocity()
    
    def stop(self):
        self.linear_steps = 0
        self.angular_steps = 0
        self.publish_velocity()
    
    def bwrd(self):
        self.linear_steps -= 1
        self.publish_velocity()
    
    def ltrn(self):
        self.angular_steps += 1
        self.publish_velocity()
    
    def rtrn(self):
        self.angular_steps -= 1
        self.publish_velocity()
    
    def publish_velocity(self):
        # 上限・下限でクランプ
        self.linear_steps = max(-self.max_linear_steps,
                                min(self.max_linear_steps, self.linear_steps))
        self.angular_steps = max(-self.max_angular_steps,
                                 min(self.max_angular_steps, self.angular_steps))
        msg = Twist()
        msg.linear.x = round(self.linear_steps * STEP, 2)
        msg.angular.z = round(self.angular_steps * STEP, 2)
        self.publisher_.publish(msg)
        
    def stop(self):
        """ゼロ速度をpublishする(終了時用)。"""
        self.linear_steps = 0
        self.angular_steps = 0
        self.publish_velocity()

def main(args=None):
    app = QApplication(sys.argv)
    window = CommandPublisherGui()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

