import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from cv_bridge import CvBridge

class RGBDetectionNode(Node):
    def __init__(self):
        super().__init__('rgb_detection_node')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # Adjust the topic name as per your configuration
            self.listener_callback,
            10
        )
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def listener_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # Detect RGB boxes
        blue_box = self.detect_color(cv_image, "blue")
        red_box = self.detect_color(cv_image, "red")
        green_box = self.detect_color(cv_image, "green")

        if blue_box:
            self.get_logger().info("Blue box detected! Moving to it.")
            self.move_to_box(blue_box)
        else:
            self.get_logger().info("No blue box detected, performing motion planning.")
            self.perform_motion_planning()

    def detect_color(self, image, color):
        # Convert the image to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if color == "blue":
            lower = np.array([100, 150, 0])
            upper = np.array([140, 255, 255])
        elif color == "red":
            lower = np.array([0, 120, 70])
            upper = np.array([10, 255, 255])
        elif color == "green":
            lower = np.array([35, 100, 100])
            upper = np.array([85, 255, 255])

        # Create a mask for the color
        mask = cv2.inRange(hsv, lower, upper)

        # Find contours of the detected colored objects
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Get the largest contour (the detected box)
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 1000:  # Adjust area threshold as needed
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw the bounding box
                return (x + w // 2, y + h // 2)  # Return the center of the box
        return None

    def move_to_box(self, box_center):
        # Move the robot to the detected box
        move_cmd = Twist()

        # For now, make a simple movement strategy to stop at the detected box
        # You can refine this later based on the robot's position and box center
        move_cmd.linear.x = 0.1  # Move forward at a constant speed
        move_cmd.angular.z = 0.0  # No rotation
        self.publisher.publish(move_cmd)

    def perform_motion_planning(self):
        # Implement your motion planning here
        # Example: Move to a random position or explore the map
        move_cmd = Twist()
        move_cmd.linear.x = 0.1
        move_cmd.angular.z = 0.5  # Rotate to explore
        self.publisher.publish(move_cmd)

def main(args=None):
    rclpy.init(args=args)
    rgb_detection_node = RGBDetectionNode()
    rclpy.spin(rgb_detection_node)

    # Destroy the node after spinning
    rgb_detection_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
