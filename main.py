#!/usr/bin/python3

# TODO: handler does not seem to execute properly
import asyncio
import os
import signal
import sys

from viam.components.generic import Generic
from viam.logging import getLogger
from viam.module.module import Module
from components import RosTopicPublisher
from utils import RclpyNodeManager

logger = getLogger(__name__)

rclpy_mgr = None
viam_node = None


def sigterm_handler(_signo, _stack_frame):
    logger.info('attempting rclpy shutdown')
    sys.exit(0)

    
async def main(addr: str) -> None:
    try:
        global rclpy_mgr
        global viam_node
        logger.info('starting ros2 module server')

        # setup viam ros node & do we need to do work in finally
        rclpy_mgr = RclpyNodeManager.get_instance()
        viam_node = ViamRosNode.get_viam_ros_node()
        rclpy_mgr.spin_and_add_node(viam_node)

        m = Module(addr)
        m.add_model_from_registry(Generic.SUBTYPE, RosTopicPublisher.MODEL)
        await m.start()
    finally:
        rclpy_mgr.shutdown()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('need socket path as cmd line arg')
    signal.signal(signal.SIGTERM, sigterm_handler)
    asyncio.run(main(sys.argv[1]))
