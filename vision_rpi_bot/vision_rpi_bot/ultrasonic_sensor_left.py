import RPi.GPIO as GPIO
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SensorPublisherLeft(Node):

        def __init__(self):
                super().__init__('ultrson_sens_publisher_left')
                self.publisher_ = self.create_publisher(String, '/obstacle_avoidance_left', 10)
                timer_period = 0.16  # seconds
                self.timer = self.create_timer(timer_period, self.obstacle_avoidance_callback_left)
                self.iterator = 0

                trigger_l = 23
                echo_l = 24

                GPIO.setmode(GPIO.BCM)

                #Ultrasonic sensor
                GPIO.setup(trigger_l, GPIO.OUT)
                GPIO.setup(echo_l, GPIO.IN)

                self.tl = trigger_l
                self.el = echo_l


        def obstacle_avoidance_callback_left(self):
                msg = String()
                distance = self.check_distance(self.tl, self.el)
                if distance > 10:
                        msg.data = "All good"
                else:
                        msg.data = "Too close"
                self.publisher_.publish(msg)
        

        def check_distance(self, sensor_t, sensor_e):
                #print("Calculating distance")
                new_reading = False
                counter = 0
                GPIO.output(sensor_t, GPIO.HIGH)

                time.sleep(0.00001)

                GPIO.output(sensor_t, GPIO.LOW)
                pulse_start_time = 0
                pulse_end_time = 0
                while GPIO.input(sensor_e)==0:
                        pass
                        counter += 1
                        if counter == 5000:
                                new_reading = True
                                break
                pulse_start_time = time.time()
                while GPIO.input(sensor_e)==1:
                        pass
                pulse_end_time = time.time()

                pulse_duration = pulse_end_time - pulse_start_time
                
                distance = round(pulse_duration * 17150, 2)
                print(distance)
                return distance
               

def main(args=None):
        rclpy.init(args=args)

        ultrson_sens_publisher_left = SensorPublisherLeft()

        rclpy.spin(ultrson_sens_publisher_left)

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        ultrson_sens_publisher_left.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
        main()