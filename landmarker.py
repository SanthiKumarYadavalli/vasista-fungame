import time
import mediapipe as mp
    
class FaceLandmarkDetector:
    def __init__(self):
        self.result = mp.tasks.vision.FaceLandmarkerResult
        self.landmarker = mp.tasks.vision.FaceLandmarker
        self.create_landmarker()
        
    def create_landmarker(self):
        # callback function that runs every time we detect
        def update_result(result, mp_image, timestamp_ms):
            self.result = result

        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path="./face_landmarker.task"),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=update_result
        )
        self.landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(options)
    
    def detect(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.landmarker.detect_async(mp_image, int(time.time() * 1000))
    