import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time

from geometry_msgs.msg import Twist


class VelocitySubscriber(Node):

    def __init__(self):
        super().__init__('cmd_vel_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_to_pwm_callback,
            10)
        self.subscription  # prevent unused variable warning

        right_motor_s = 17
        right_motor_d = 27

        left_motor_s = 6
        left_motor_d = 13

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(right_motor_d, GPIO.OUT)
        GPIO.setup(right_motor_s, GPIO.OUT)

        GPIO.setup(left_motor_d, GPIO.OUT)
        GPIO.setup(left_motor_s, GPIO.OUT)

        self.pwm_r = GPIO.PWM(right_motor_s, 1000)
        self.pwm_l = GPIO.PWM(left_motor_s, 1000)

        self.pwm_r.start(25)  #max speed 100
        self.pwm_l.start(50)

        self.mr = right_motor_d
        self.ml = left_motor_d


    def cmd_to_pwm_callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.data)
        
        right_wheel_vel = (msg.linear.x + msg.angular.z) / 2
        left_wheel_vel = (msg.linear.x - msg.angular.z) / 2

        print(right_wheel_vel, " / ", left_wheel_vel)



def main(args=None):
    rclpy.init(args=args)

    velocity_subscriber = VelocitySubscriber()

    rclpy.spin(velocity_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    velocity_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()