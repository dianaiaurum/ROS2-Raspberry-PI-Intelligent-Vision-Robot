import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import time

class video_publisher(Node):

    def __init__(self):
        super().__init__('rpi_video_publisher')
        self.publisher_ = self.create_publisher(Image, '/rpi_video_feed', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.camera_callback)
        self.cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        time.sleep(0.5)
        self.bridge = CvBridge()

    def camera_callback(self):
        ret, frame = self.cap.read()
        
        while True:
            ret, frame = self.cap.read()
            
            while ret == False:
                print("Can't receive frame. Retrying ...")
                self.cap.release()
                self.cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
                ret, frame = self.cap.read()
            
            #print("Frame received")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = self.bridge.cv2_to_imgmsg(frame, 'mono8', None)
            self.publisher_.publish(frame)
            
        

def main(args=None):
    
    rclpy.init(args=args)

    publisher = video_publisher()
    print("Video Node Started")
    rclpy.spin(publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    video_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()