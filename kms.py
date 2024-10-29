import cv2
import torch
from ultralytics import YOLO

# YOLO modelini yükleme
model = YOLO('best.pt')

# GStreamer pipeline tanımlama (UDP portu 5600 üzerinden H.264 video)
gst_pipeline = (
    "udpsrc port=5600 ! "
    "application/x-rtp, payload=96 ! "
    "rtph264depay ! h264parse ! "
    "avdec_h264 ! videoconvert ! "
    "appsink"
)

# OpenCV ile VideoCapture kullanarak GStreamer pipeline'ını açın
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("GStreamer pipeline açılmadı.")
    exit()

# Video akışını okuyup nesne tespiti
while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame alınamadı.")
        break

    # YOLO modelini kullanarak nesne tespiti
    results = model(frame)

    # Tespit edilen nesnelerin etrafına kare çizimi
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[box.cls[0].item()]
            conf = box.conf[0].item()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("GStreamer YOLO Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
