import sys

import cv2
import rclpy
import message_filters
from rclpy.node import Node

import zerorpc

import numpy as np

from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String


class CosyposeRosBridge(Node):

    def __init__(self, cams):
        super().__init__('cosypose_ros_bridge')
        print(f"Selected topics: {cams}")
        self.c = zerorpc.Client(timeout=5)
        print("Connecting to Cosypose...")
        self.c.connect("tcp://127.0.0.1:4242")
        self.publisher = self.create_publisher(String, 'cosypose/pose', 10)
        cams = [message_filters.Subscriber(self, CompressedImage, cam) for cam in cams]
        ts = message_filters.ApproximateTimeSynchronizer(cams, 1, 1)
        ts.registerCallback(self.listener_callback)

    def listener_callback(self, *msgs):
        try:
            result = self.c.solve([np.array(msg.data).tolist() for msg in msgs])
            msg = String()
            msg.data = str(result)
            self.publisher.publish(msg)
            print(result)
        except:
            print("Cosypose not running!")


def main(args=None):
    rclpy.init(args=args)
    cams = sys.argv[1:]

    cosypose_ros_bridge = CosyposeRosBridge(cams)

    rclpy.spin(cosypose_ros_bridge)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    cosypose_ros_bridge.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
