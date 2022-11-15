import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from machina_interfaces import RequestSensorData

class SensorClientPub(Node):
    """
    it's a client and a publisher
    """
    def __init__(self):

        self.cli = self.create_client(RequestSensorData, 'sensor_data_request')

        self.sub1 = self.create_subscription()
        self.pub1 = self.create_publisher(Float64MultiArray, "sensor1", 10)
        self.pub2 = self.create_publisher(Float64MultiArray, "sensor2", 10)
        self.pub3 = self.create_publisher(Float64MultiArray, "sensor3", 10)

        self.req = RequestSensorData.Request()

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

        response1 = self.request_data(self, 1, 500)
        response2 = self.request_data(self, 2, 500)
        response3 = self.request_data(self, 3, 500)

        msg1.data = response1.data
        msg2.data = response2.data
        msg3.data = response3.data

        self.pub1.publish(msg1)
        self.pub2.publish(msg2)
        self.pub3.publish(msg3)

def main(args=None):
    rclpy.init(args=args)

    client_pub = SensorClientPub()
    rclpy.spin(client_pub)

    client_pub.destrroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
