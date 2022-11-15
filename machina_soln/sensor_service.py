import socket
import sys
import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

from machina_interfaces.srv import RequestSensorData

class SensorService(Node):
    def __init__(self):
        super().__init__('sensor_data_server')
        self.srv = self.create_service(RequestSensorData, 'request_sensor_data', self.service_callback)
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        ## these connections could potentially be taken in as parameters if these were real sensors
        self.sock1.connect(('127.0.0.3', 10000)) 
        self.sock2.connect(('127.0.0.3', 10001))
        print('connected to ports')

        self.number_of_samples = 10

        message_string = str(self.number_of_samples)
        self.message = message_string.encode()

    def service_callback(self, request, response):
        if request.sensor_id == 1:
            self.sock1.sendall(self.message)
            byte_data1 = self.sock1.recv(10000)
            data = np.frombuffer(byte_data1)
            response.data = data.tolist()

        elif request.sensor_id == 2:
            print("service if id 2")
            self.sock2.sendall(self.message)
            byte_data2 = self.sock2.recv(10000)
            data = np.frombuffer(byte_data2)
            response.data = data.tolist()

        else:
            self.get_logger().error("sensor_id not found. please check again")
        print("before response")
        return response

    def close(self):
        self.sock1.close()
        self.sock2.close()
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    sensor_service = SensorService()
    
    rclpy.spin(sensor_service)
    sensor_service.close()
    rclpy.shutdown()

if __name__ == "__main__":
    main()