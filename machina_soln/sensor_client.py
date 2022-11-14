import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from machina_interfaces import RequestSensorData

class SensorClient(Node):
    def __init__(self):

        self.cli = self.create_client()

        self.sub1 = self.create_subscription()
        self.pub1 = self.create_publisher(Float64MultiArray, "sensor1", 10)
        self.pub2 = self.create_publisher(Float64MultiArray, "sensor2", 10)
        self.pub3 = self.create_publisher(Float64MultiArray, "sensor3", 10)

        self.req = RequestSensorData.Request()
        self.response = RequestSensorData

    def request_data(self, sensor_id, data_size):
        """
        return a np array containing all the data
        """
        self.req.sensor_id = sensor_id
        self.req.data_size = data_size
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def timer_callback(self):
        """
        how the sensor publishers publish the message
        """
        #ROS messages
        msg1 = Float64MultiArray()
        msg2 = Float64MultiArray()
        msg3 = Float64MultiArray()

        #send the socket request message
        byte_data1 = self.sock1.recv(10000)
        byte_data2 = self.sock2.recv(10000)
        byte_data3 = self.sock3.recv(10000)

        data1 = np.frombuffer(byte_data1)
        data2 = np.frombuffer(byte_data2)
        data3 = np.frombuffer(byte_data3)

        msg1.data = data1.tolist()
        msg2.data = data2.tolist()
        msg3.data = data3.tolist()