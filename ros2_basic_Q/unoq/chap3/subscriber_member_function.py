# ROS 2のPythonクライアントライブラリをインポート
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Bool

# MCUとの通信に使う
import arduino.app_utils as app_utils

# Subscriberノードを定義するクラス
class MinimalSubscriber(Node):

    def __init__(self):
        # 親クラスNodeを初期化し、ノード名を'minimal_subscriber'に設定
        super().__init__('minimal_subscriber')
        # サブスクリプション（購読）を作成
        # - Bool型のメッセージを
        # - 'led_status'という名前のトピックから
        # - self.listener_callback というコールバック関数で受け取る
        # - キューサイズは10
        self.subscription = self.create_subscription(
            Bool,
            'led_status',
            self.listener_callback,
            10)

    # メッセージ受信時に呼び出されるコールバック関数
    def listener_callback(self, msg):
		    self.get_logger().info(f'Setting LED to: {msg.data}') 
        app_utils.Bridge.call("set_led_state", msg.data)

# メイン関数
def main(args=None):
	  # rclpyの初期化。終了時には自動でシャットダウンするようにwith文を使用
    with rclpy.init(args=args):
    # MinimalSubscriberインスタンスを生成
    minimal_subscriber = MinimalSubscriber()

    try:
        # ノードをスピンさせ、メッセージ受信を待つ
        rclpy.spin(minimal_subscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        # Ctrl+Cなどによる終了要求を捕捉して終了
        pass
	  finally:
		    minimal_subscriber.destroy_node()
		    rclpy.try_shutdown()

# スクリプトが直接実行されたときにmain()を呼び出す
if __name__ == '__main__':
    main()
