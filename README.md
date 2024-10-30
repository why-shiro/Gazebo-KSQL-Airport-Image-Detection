# OpenCV YOLO Project

## An Object Detection Project using OpenCV and YOLO

This project demonstrates how to build OpenCV from source with GStreamer support, how to use it for real-time object detection using the YOLO model (`best.pt`), and how to transmit the video stream over a local area network (LAN) using sockets.

## Requirements
- OpenCV with GStreamer support
- YOLOv11 or another compatible YOLO model
- GStreamer and its necessary plugins
- Python libraries: `socket`, `opencv-python`, `numpy`, `torch`, and `ultralytics`

## Features
- GStreamer integration with OpenCV for high-performance video processing
- Real-time object detection using the YOLO model
- Video transmission over LAN using UDP sockets
- Python-based implementation for ease of use and customization
- Dockerized environment for easy deployment across different systems

## Installation

Follow the steps below to build OpenCV with GStreamer support, set up the YOLO model for object detection, and enable LAN-based video transmission.

### Step 1: Install Dependencies
First, ensure that all necessary dependencies are installed on your system:

```sh
sudo apt update
sudo apt install -y build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev

```

## Step 2: Clone the OpenCV Repository
Next, clone the OpenCV and OpenCV contrib repositories from GitHub:

```sh
cd ~
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

```

## Step 3: Build OpenCV with GStreamer support
Now, let's build OpenCV from source:


```sh
cd ~/opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
      -D WITH_GSTREAMER=ON \
      -D WITH_TBB=ON \
      -D BUILD_EXAMPLES=ON ..

make -j$(nproc)  # Parallel build using the number of available cores
sudo make install
sudo ldconfig  # Update shared library cache
```

## Step 4: Verify the installation

```sh
python3 -c "import cv2; print(cv2.getBuildInformation())"
```

Look for a line that says GStreamer: `YES`. If it says `NO`, go back and check if the correct GStreamer libraries were installed.

## YOLO Model Setup

This project uses the YOLO model for object detection. You can download the pre-trained weights or train your own model.


To use YOLO, first install the `ultralytics` package:

```sh
pip install torch torchvision ultralytics
```

Then, make sure you have your `best.pt` model file ready.

## Docker

To easily deploy this project using Docker, you can create a Dockerfile as follows:

```
FROM ubuntu:20.04

# Install OpenCV dependencies
RUN apt update && apt install -y build-essential cmake git pkg-config \
    libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev \
    libtiff-dev gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev

# Install Python dependencies
RUN pip install torch torchvision ultralytics

# Copy project files
COPY . /usr/src/app
WORKDIR /usr/src/app

CMD ["python3", "your_script.py"]
```
To build and run the Docker container:

```sh
docker build -t my-opencv-yolo .
docker run -it --rm my-opencv-yolo
```

## License
MIT


