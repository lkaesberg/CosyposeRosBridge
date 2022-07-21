import sys

import cv2
import rclpy
import message_filters
from rclpy.node import Node

import zerorpc

import numpy as np

from sensor_msgs.msg import CompressedImage


class CosyposeServ(Node):

    def __init__(self, cams):
        super().__init__('cosypose_serv')
        print(cams)
        self.c = zerorpc.Client(timeout=5)
        print("Connecting to Cosypose...")
        self.c.connect("tcp://127.0.0.1:4242")
        cams = [message_filters.Subscriber(self, CompressedImage, cam) for cam in cams]
        ts = message_filters.ApproximateTimeSynchronizer(cams, 1, 1)
        ts.registerCallback(self.listener_callback)

    def listener_callback(self, *msgs):
        img = cv2.imdecode(np.array(msgs[0].data), cv2.IMREAD_ANYCOLOR)

        cv2.imshow("test", img)
        print(img)
        # try:
        #    result = self.c.solve([np.array(msg.data).tolist() for msg in msgs])
        #    print(result)
        # except:
        #    print("Cosypose not running!")


def main(args=None):
    rclpy.init(args=args)
    cams = sys.argv[1:]

    cosypose_serv = CosyposeServ(cams)

    rclpy.spin(cosypose_serv)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    cosypose_serv.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
