#!/usr/bin/env python3

import rospy
from morai_msgs.msg import GPSMessage
import os
import csv
from math import sqrt

class GPS:
    def __init__(self):
        rospy.init_node("gps_node")
        self.gps_sub = rospy.Subscriber("/gps", GPSMessage, self.gps_CB)
        self.previous_location = None
        self.csv_file = None
        file = open("gps_coordinates.txt", 'w')
        self.csv_file = csv.writer(file)

    def gps_CB(self, msg):
        gps_msg = msg

        os.system("clear")
        print("------------------------------")
        print(f"latitude : {gps_msg.latitude}")
        print(f"longitude : {gps_msg.longitude}")
        print(f"altitude : {gps_msg.altitude}")
        print("------------------------------")

        coord = (gps_msg.latitude, gps_msg.longitude)
        x = coord[0]
        y = coord[1]

        if self.previous_location is not None:
            distance = sqrt((x - self.previous_location[0])**2 + (y - self.previous_location[1])**2)

            if distance >= 0.5:
                data = [x, y]
                self.csv_file.writerow(data)
                print(f"location : {data}")
                self.previous_location = [x, y]
            else:
                print(f"location not moved enough to record: {data}")
        else:
            data = [x, y]
            self.csv_file.writerow(data)
            print(f"initial location : {data}")
            self.previous_location = [x, y]

if __name__ == "__main__":
    try:
        gps = GPS()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
