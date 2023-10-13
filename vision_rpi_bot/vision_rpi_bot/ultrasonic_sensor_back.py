import RPi.GPIO as GPIO
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SensorPublisherBack(Node):

        def __init__(self):
                super().__init__('ultrson_sens_publisher_back')
                self.publisher_ = self.create_publisher(String, '/obstacle_avoidance_back', 10)
                timer_period = 0.14  # seconds
                self.timer = self.create_timer(timer_period, self.obstacle_avoidance_callback_back)
                self.iterator = 0
               
                trigger_b = 20
                echo_b = 21

                GPIO.setmode(GPIO.BCM)

                #Ultrasonic sensor

                GPIO.setup(trigger_b, GPIO.OUT)
                GPIO.setup(echo_b, GPIO.OUT)

                self.tb = trigger_b
                self.eb = echo_b


        def obstacle_avoidance_callback_back(self):
                msg = String()
                distance = self.check_distance(self.tb, self.eb)
                if distance > 10:
                        msg.data = "All good"
                else:
                        msg.data = "Too close"
                self.publisher_.publish(msg)
        

        def check_distance(self, sensor_t, sensor_e):
                #print("Calculating distance")

                GPIO.output(sensor_t, GPIO.HIGH)
                new_reading = False
                counter = 0
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
                
                return distance
               

def main(args=None):
        rclpy.init(args=args)

        ultrson_sens_publisher_back = SensorPublisherBack()

        rclpy.spin(ultrson_sens_publisher_back)

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        ultrson_sens_publisher_back.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
        main()