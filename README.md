# Live Stream Motion Detection

A real-time webcam streaming application with motion detection capabilities built with FastAPI and OpenCV.

## Features

- 📹 **Live Video Streaming**: High-quality webcam feed at 1280x720 resolution, 30 FPS
- 🎯 **Motion Detection**: Automatically detects and highlights movement with bounding boxes
- ⚡ **Fast API Backend**: Built with FastAPI for high performance
- 🎨 **Enhanced Video Quality**: Automatic brightness and contrast adjustment
- 🔄 **Real-time Processing**: Low-latency video streaming with motion tracking

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **OpenCV (cv2)**: Computer vision library for video capture and processing
- **Uvicorn**: ASGI server for running the application
- **NumPy**: Numerical computing for image processing

## Requirements

- Python 3.8+
- Webcam/Camera device
- Dependencies listed in requirements (if available)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd live_steam_project
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# or
source .venv/bin/activate    # Linux/Mac
```

3. Install dependencies:
```bash
pip install fastapi uvicorn opencv-python numpy
```

## Usage

### Running the Application

Start the server using either method:

**Method 1: Direct Python execution**
```bash
python main.py
```

**Method 2: Using Uvicorn**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

### API Endpoints

#### `GET /video_feed`
Streams live video feed with motion detection overlay.

**Response**: Multipart stream of JPEG frames
**Content-Type**: `multipart/x-mixed-replace; boundary=frame`

### Testing

Use the included `test_main.http` file to test the endpoints with REST Client or similar tools.

## How It Works

1. **Video Capture**: Captures frames from the default webcam at 1280x720 resolution
2. **Motion Detection**: 
   - Converts frames to grayscale
   - Applies Gaussian blur to reduce noise
   - Compares consecutive frames to detect changes
   - Identifies contours of moving objects
   - Draws bounding boxes around detected motion
3. **Enhancement**: Applies brightness and contrast adjustments for better visibility
4. **Streaming**: Encodes frames as JPEG (90% quality) and streams to clients

## Configuration

The application uses the following default settings:

- **Resolution**: 1280x720 pixels
- **Frame Rate**: 30 FPS
- **JPEG Quality**: 90%
- **Motion Threshold**: 25 (pixel difference)
- **Minimum Contour Area**: 100 pixels
- **Server Port**: 8000

You can modify these values in `main.py` to suit your needs.

## Camera Settings

The application configures the camera with:
- `CAP_PROP_FRAME_WIDTH`: 1280
- `CAP_PROP_FRAME_HEIGHT`: 720
- `CAP_PROP_FPS`: 30

## Cleanup

The application automatically releases the camera when shut down (CTRL+C).

## Project Structure

```
live_steam_project/
│
├── main.py              # Main application code
├── test_main.http       # HTTP endpoints for testing
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Troubleshooting

**Camera not detected:**
- Ensure your webcam is connected and not in use by another application
- Check camera permissions on your system

**Poor video quality:**
- Adjust the `alpha` and `beta` values in `cv2.convertScaleAbs()` for brightness/contrast
- Modify the JPEG quality setting in `cv2.imencode()`

**High CPU usage:**
- Reduce the frame resolution
- Lower the FPS setting
- Increase the motion detection threshold

## Future Enhancements

- [ ] Add recording functionality
- [ ] Support multiple camera sources
- [ ] Add web interface for viewing the stream
- [ ] Implement motion detection alerts/notifications
- [ ] Add configuration file for easy customization

## License

This project is open source and available for educational purposes.

## Author

Created as part of a live streaming motion detection project.
