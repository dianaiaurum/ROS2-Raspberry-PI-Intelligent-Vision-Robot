import RPi.GPIO as GPIO
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SensorPublisher(Node):

        def __init__(self):
                super().__init__('ultrson_sens_publisher')
                self.publisher_ = self.create_publisher(String, '/obstacle_avoidance_front', 10)
                timer_period = 0.1  # seconds
                self.timer = self.create_timer(timer_period, self.obstacle_avoidance_callback)
                self.iterator = 0

                trigger_f = 26
                echo_f = 19

                GPIO.setmode(GPIO.BCM)

                #Ultrasonic sensor

                GPIO.setup(trigger_f, GPIO.OUT)
                GPIO.setup(echo_f, GPIO.IN)

                self.tf = trigger_f
                self.ef = echo_f


        def obstacle_avoidance_callback(self):
                msg = String()
                distance = self.check_distance(self.tf, self.ef)
                if distance > 10:
                        msg.data = "All good"
                else:
                        msg.data = "Too close"
                print(distance)
                self.publisher_.publish(msg)
        

        def check_distance(self, sensor_t, sensor_e):
                #print("I am calculating distance")
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
                if new_reading:
                        return False
                while GPIO.input(sensor_e)==1:
                        pass
                pulse_end_time = time.time()
                print("2")

                pulse_duration = pulse_end_time - pulse_start_time
                distance = round(pulse_duration * 17150, 2)
                #print(distance)
                return distance
               

def main(args=None):
        rclpy.init(args=args)

        ultrson_sens_publisher = SensorPublisher()

        rclpy.spin(ultrson_sens_publisher)

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        ultrson_sens_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
        main()