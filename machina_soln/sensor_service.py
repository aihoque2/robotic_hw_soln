import socket
import sys
import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

from srv import RequestSensorData

class SensorPublisher(Node):
    def __int__(self):
        super().__init__("sensor publishers")
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ## these connections could potentially be taken in as parameters if these were real sensors
        self.sock1.connect(('127.0.0.3', 10000)) 
        self.sock2.connect(('127.0.0.3', 10001))
        self.sock3.connect(('127.0.0.3', 10002))
        
        self.number_of_samples = 10

        self.pub1 = self.create_publisher(Float64MultiArray, "sensor1", 10)
        self.pub2 = self.create_publisher(Float64MultiArray, "sensor2", 10)
        self.pub3 = self.create_publisher(Float64MultiArray, "sensor3", 10)

        self.timer = self.create_timer()


    def close(self):
        self.sock1.close()
        self.sock2.close()
        self.sock3.close()
        self.destroy_node()

    def timer_callback(self):
        """
        how the sensor publishers publish the message
        """
        #ROS messages
        msg1 = Float64MultiArray()
        msg2 = Float64MultiArray()
        msg3 = Float64MultiArray()

        #send the socket request message
        message_string = str(self.number_of_samples)
        message = message_string.encode()
        self.sock1.sendall(message)
        self.sock2.sendall(message)
        self.sock3.sendall(message)

        byte_data1 = self.sock1.recv(10000)
        byte_data2 = self.sock2.recv(10000)
        byte_data3 = self.sock3.recv(10000)

        data1 = np.frombuffer(byte_data1)
        data2 = np.frombuffer(byte_data2)
        data3 = np.frombuffer(byte_data3)

        msg1.data = data1.tolist()
        msg2.data = data2.tolist()
        msg3.data = data3.tolist()


def main(args=None):
    rclpy.init(args=args)
    sensor_publisher = SensorPublisher()
    
    rclpy.spin(sensor_publisher)
    sensor_publisher.close()
    rclpy.shutdown()

if __name__ == "__main__":
    main()