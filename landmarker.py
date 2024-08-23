import time
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

    
class FaceDetector:
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
        
    
def draw_landmarks_on_image(rgb_image, detection_result):
    try:
        face_landmarks_list = detection_result.face_landmarks
        annotated_image = np.copy(rgb_image)

        # Loop through the detected faces to visualize.
        for idx in range(len(face_landmarks_list)):
            face_landmarks = face_landmarks_list[idx]

            # Draw the face landmarks.
            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
            ])

            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_tesselation_style())
            # solutions.drawing_utils.draw_landmarks(
            #     image=annotated_image,
            #     landmark_list=face_landmarks_proto,
            #     connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mp.solutions.drawing_styles
            #     .get_default_face_mesh_contours_style())
            # solutions.drawing_utils.draw_landmarks(
            #     image=annotated_image,
            #     landmark_list=face_landmarks_proto,
            #     connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mp.solutions.drawing_styles
            #     .get_default_face_mesh_iris_connections_style())
        return annotated_image
    except:
        return rgb_image
    
    
