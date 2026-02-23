import cv2
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import uvicorn
import numpy as np

app = FastAPI()

# Start webcam and set quality
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Higher width
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Higher height
camera.set(cv2.CAP_PROP_FPS, 30)  # Smoother video
if not camera.isOpened():
    raise RuntimeError("Could not start camera.")

previous_frame = None

def generate_frames():
    global previous_frame
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Resize for motion detection only
        small_frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if previous_frame is None:
            previous_frame = gray
            continue

        frame_delta = cv2.absdiff(previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 100:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            scale_x = frame.shape[1] / small_frame.shape[1]
            scale_y = frame.shape[0] / small_frame.shape[0]
            x, y, w, h = int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Motion Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        previous_frame = gray

        # Boost brightness and contrast
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)

        # Encode with high quality
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.on_event("shutdown")
def cleanup():
    print("cleanup: releasing camera")
    camera.release()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)