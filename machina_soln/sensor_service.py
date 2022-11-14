import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray


class SensorClient(Node):
    def __init__(self):
        self.sub1 = self.create_subscription()
        self.pub1 = self.create_publisher(Float64MultiArray, "sensor1", 10)
        self.pub2 = self.create_publisher(Float64MultiArray, "sensor2", 10)
        self.pub3 = self.create_publisher(Float64MultiArray, "sensor3", 10)
