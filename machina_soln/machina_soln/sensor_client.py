import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from machina_interfaces.srv import RequestSensorData

class SensorClientPub(Node):
    """
    it's a client and a publisher
    """
    def __init__(self):
        super().__init__('sensor_client')
        self.cli = self.create_client(RequestSensorData, 'request_sensor_data')
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        self.pub1 = self.create_publisher(Float64MultiArray, "sensor1", 10)
        self.pub2 = self.create_publisher(Float64MultiArray, "sensor2", 10)

        self.req = RequestSensorData.Request()

        self.timer = self.create_timer(0.002, self.timer_callback)

    def request_data(self, sensor_id, data_size):
        """
        return a np array containing all the data
        """
        self.req.sensor_id = sensor_id
        self.req.data_size = data_size
        
        ##synchronous call
        #return self.cli.call(self.req)

        ## async call
        self.future = self.cli.call_async(self.req)
        print("client sent request ", self.req.sensor_id)
        rclpy.spin_until_future_complete(self, self.future)
        print("request completed")
        return self.future.result()

    def timer_callback(self):
        """
        how the sensor publishers publish the message
        """
        #ROS messages
        msg1 = Float64MultiArray()
        msg2 = Float64MultiArray()

        response1 = self.request_data(1, 10)
        print("here's data: ", response1)
        response2 = self.request_data(2, 10)

        msg1.data = response1.data
        msg2.data = response2.data

        self.pub1.publish(msg1)
        self.pub2.publish(msg2)

def main(args=None):
    rclpy.init(args=args)

    client_pub = SensorClientPub()
    rclpy.spin(client_pub)

    client_pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
