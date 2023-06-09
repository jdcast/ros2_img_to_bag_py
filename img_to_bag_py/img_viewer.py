"""
Basic ROS 2 program to subscribe to real-time streaming images

Author:
    - John Dallas Cast, Apr 12, 2023
    - johndallascast.com

Adapted from: https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/ 
"""
  
# Import the necessary libraries
import cv2 # OpenCV library
import rclpy # Python library for ROS 2
import numpy as np

from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images

 
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Image, 
      'image', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving image')
 
    # Convert ROS Image message to OpenCV image
    img = self.br.imgmsg_to_cv2(data)

    print("image shape: {}".format(img.shape))
    print("image max: {}".format(np.max(img)))
    print("image min: {}".format(np.min(img)))
    
    # Display image
    cv2.imshow("image", img)
    
    cv2.waitKey(1)
  
def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the node
    image_subscriber = ImageSubscriber()

    # Spin the node so the callback function is called.
    rclpy.spin(image_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_subscriber.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()
  
if __name__ == '__main__':
  main()
