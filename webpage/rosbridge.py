import rclpy
from rclpy.node import Node
from rosbridge_library.protocol import RosbridgeProtocol
from geometry_msgs.msg import Twist

class RosbridgeServer(Node):
    def __init__(self):
        super().__init__('rosbridge_server')

        # Create a RosbridgeProtocol instance
        self.bridge = RosbridgeProtocol()

        # Subscribe to ROS topics
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.topic_callback,
            10
        )

        # Advertise ROS topics
        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

        self.bridge.register_publisher('cmd_vel', self.publisher)
        self.bridge.start()

    def topic_callback(self, msg):
        self.bridge.publish_message('cmd_vel', msg)

    def shutdown(self):
        self.bridge.unregister()
        self.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    server = RosbridgeServer()
    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    server.shutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
