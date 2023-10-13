import RPi.GPIO as GPIO
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SensorPublisherRight(Node):

        def __init__(self):
                super().__init__('ultrson_sens_publisher_right')
                self.publisher_right_ = self.create_publisher(String, '/obstacle_avoidance_right', 10)
                timer_period_right = 0.12  # seconds
                self.timer_right = self.create_timer(timer_period_right, self.obstacle_avoidance_callback_right)
                self.iterator_right = 0

                trigger_r = 16
                echo_r = 12

                GPIO.setmode(GPIO.BCM)

                #Ultrasonic sensor
 
                GPIO.setup(trigger_r, GPIO.OUT)
                GPIO.setup(echo_r, GPIO.OUT)

                self.tr = trigger_r
                self.er = echo_r


        def obstacle_avoidance_callback_right(self):
                msg_right = String()
                distance_right = self.check_distance_right(self.tr, self.er)
                if distance_right > 10:
                        msg_right.data = "All good"
                else:
                        msg_right.data = "Too close"
                self.publisher_right_.publish(msg_right)
        

        def check_distance_right(self, sensor_t, sensor_e):
                #print("Calculating distance")
                new_reading = False
                counter = 0
                GPIO.output(sensor_t, GPIO.HIGH)
                
                time.sleep(0.00001)

                GPIO.output(sensor_t, GPIO.LOW)
                pulse_start_time_right = 0
                pulse_end_time_right = 0
                while GPIO.input(sensor_e)==0:
                        pass
                        counter += 1
                        if counter == 5000:
                                new_reading = True
                                break
                pulse_start_time_right = time.time()
                while GPIO.input(sensor_e)==1:
                        pass
                pulse_end_time_right = time.time()

                pulse_duration_right = pulse_end_time_right - pulse_start_time_right
                distance_right = round(pulse_duration_right * 17150, 2)
                
                return distance_right
               

def main(args=None):
        rclpy.init(args=args)

        ultrson_sens_publisher_right = SensorPublisherRight()

        rclpy.spin(ultrson_sens_publisher_right)

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        ultrson_sens_publisher_right.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
        main()