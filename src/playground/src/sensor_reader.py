#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import cv2
import numpy as np

class SensorReader:
    def __init__(self):
        rospy.init_node('sensor_reader', anonymous=True)
        
        # Initialize CV Bridge for camera images
        self.bridge = CvBridge()
        
        # Storage for sensor data
        self.laser_data = None
        self.camera_image = None
        self.odom_data = None
        
        # Subscribers
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        self.camera_sub = rospy.Subscriber('/camera/image_raw', Image, self.camera_callback)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
        rospy.loginfo("Sensor Reader Node Started!")
        rospy.loginfo("Listening to: /scan, /camera/image_raw, /odom")
    
    def laser_callback(self, msg):
        """Callback function for laser scanner data"""
        self.laser_data = msg
        
        # Get important information
        ranges = np.array(msg.ranges)
        valid_ranges = ranges[np.isfinite(ranges)]
        
        if len(valid_ranges) > 0:
            min_distance = np.min(valid_ranges)
            max_distance = np.max(valid_ranges)
            avg_distance = np.mean(valid_ranges)
            
            rospy.loginfo_throttle(2, 
                f"LASER - Min: {min_distance:.2f}m, Max: {max_distance:.2f}m, Avg: {avg_distance:.2f}m")
            
            # Check for obstacles
            front_ranges = ranges[len(ranges)//2 - 30:len(ranges)//2 + 30]
            front_ranges = front_ranges[np.isfinite(front_ranges)]
            
            if len(front_ranges) > 0 and np.min(front_ranges) < 0.5:
                rospy.logwarn(f"⚠️  Obstacle detected at {np.min(front_ranges):.2f}m ahead!")
    
    def camera_callback(self, msg):
        """Callback function for camera images"""
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.camera_image = cv_image
            
            # Get image dimensions
            height, width, channels = cv_image.shape
            
            rospy.loginfo_throttle(5, 
                f"CAMERA - Image size: {width}x{height}, Channels: {channels}")
            
            # Optional: Display image (comment out if running headless)
            # cv2.imshow("Robot Camera", cv_image)
            # cv2.waitKey(1)
            
        except Exception as e:
            rospy.logerr(f"Error processing camera image: {e}")
    
    def odom_callback(self, msg):
        """Callback function for odometry data"""
        self.odom_data = msg
        
        # Extract position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        
        # Extract orientation (quaternion)
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        
        # Convert quaternion to yaw angle
        yaw = np.arctan2(2.0 * (qw * qz + qx * qy), 
                         1.0 - 2.0 * (qy * qy + qz * qz))
        
        # Extract velocities
        linear_vel = msg.twist.twist.linear.x
        angular_vel = msg.twist.twist.angular.z
        
        rospy.loginfo_throttle(2, 
            f"ODOM - Pos: ({x:.2f}, {y:.2f}), Yaw: {np.degrees(yaw):.1f}°, "
            f"Vel: {linear_vel:.2f}m/s, AngVel: {angular_vel:.2f}rad/s")
    
    def get_sensor_summary(self):
        """Print a summary of all sensor data"""
        rospy.loginfo("=" * 60)
        rospy.loginfo("SENSOR DATA SUMMARY")
        rospy.loginfo("=" * 60)
        
        if self.laser_data:
            ranges = np.array(self.laser_data.ranges)
            valid_ranges = ranges[np.isfinite(ranges)]
            rospy.loginfo(f"Laser: {len(valid_ranges)} valid readings")
            rospy.loginfo(f"  Range: {self.laser_data.range_min:.2f}m to {self.laser_data.range_max:.2f}m")
            rospy.loginfo(f"  Angle: {np.degrees(self.laser_data.angle_min):.1f}° to {np.degrees(self.laser_data.angle_max):.1f}°")
        else:
            rospy.loginfo("Laser: No data received")
        
        if self.camera_image is not None:
            h, w, c = self.camera_image.shape
            rospy.loginfo(f"Camera: {w}x{h} image with {c} channels")
        else:
            rospy.loginfo("Camera: No image received")
        
        if self.odom_data:
            x = self.odom_data.pose.pose.position.x
            y = self.odom_data.pose.pose.position.y
            rospy.loginfo(f"Odometry: Position ({x:.2f}, {y:.2f})")
        else:
            rospy.loginfo("Odometry: No data received")
        
        rospy.loginfo("=" * 60)
    
    def run(self):
        """Main loop"""
        rate = rospy.Rate(1)  # 1 Hz for summary
        
        while not rospy.is_shutdown():
            self.get_sensor_summary()
            rate.sleep()

if __name__ == '__main__':
    try:
        reader = SensorReader()
        reader.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()
        