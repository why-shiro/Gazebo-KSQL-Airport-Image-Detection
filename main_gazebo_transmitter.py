#
# This code captures a video stream using GStreamer from a PX4 drone, displays it with OpenCV, 
# and sends the compressed video frames over UDP. The GStreamer pipeline receives the video
# from port 5600, decodes the stream, and processes the frames in real-time. The frames are 
# compressed to JPEG format to reduce their size, and then sent to the target IP and port using 
# a UDP socket in small chunks to ensure safe transmission.
#

import cv2
import socket
import numpy as np

# GStreamer pipeline definition (receiving video stream from port 5600)
gst_pipeline = (
    "udpsrc port=5600 ! "
    "application/x-rtp, payload=96 ! "
    "rtph264depay ! h264parse ! "
    "avdec_h264 ! videoconvert ! "
    "appsink"
)

# Configuration
TARGET_IP = '192.168.1.59'
PORT = 9999
MAX_DGRAM = 65000  # Ensures the packet size stays within safe limits

# OpenCV to capture video stream using GStreamer
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("GStreamer pipeline couldn't be opened")
    exit()

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (TARGET_IP, PORT)  # Target IP and port

while True:
    # Read frame from GStreamer pipeline
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame")
        break

    # Display the frame
    cv2.imshow('GStreamer Video', frame)

    # Compress the frame to JPEG format with reduced quality
    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

    buffer_data = buffer.tobytes()

    for i in range(0, len(buffer_data), MAX_DGRAM):
        sock.sendto(buffer_data[i:i + MAX_DGRAM], server_address)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
sock.close()
cv2.destroyAllWindows()
