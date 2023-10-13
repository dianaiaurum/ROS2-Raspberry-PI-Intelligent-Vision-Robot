import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2

class camera_sub(Node):

    def __init__(self):
        super().__init__('camera_feed_node')
        self.camera_sub = self.create_subscription(Image, '/rpi_video_feed', self.camera_cb, 10)
        self.bridge = CvBridge()

    def camera_cb(self, data):
        frame = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)

    sensor_sub = camera_sub()

    rclpy.spin(sensor_sub)
    sensor_sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()