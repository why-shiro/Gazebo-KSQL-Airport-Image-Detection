#
# This code listens for incoming video frames over UDP, decodes the frames, processes them using
# a YOLOv8 model for object detection, and then displays the processed frames. The video is 
# received as compressed JPEG data through UDP, decoded into frames, and analyzed in real-time 
# with the YOLO model. Detected objects are highlighted with bounding boxes and labels. The 
# processed frames are then displayed on the screen.
#

import socket
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Load YOLO model
model = YOLO('best.pt')  # An example pre-trained model for ksql_airport buildings

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999)) 

while True:
    data, _ = sock.recvfrom(65535)  # Maximum UDP packet size

    # Convert data to numpy array
    frame = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Skip processing if an invalid frame is received
    if frame is None:
        print("Invalid frame received, skipping...")
        continue

    # Perform object detection with YOLO
    results = model(frame)

    # Draw bounding boxes around detected objects
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[box.cls[0].item()]
            conf = box.conf[0].item()

            # Add bounding box and label to the image
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the image
    cv2.imshow('Received UDP Video Processed with YOLO', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sock.close()
cv2.destroyAllWindows()
