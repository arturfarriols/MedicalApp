import os

import cv2

class Video:
    def __init__(self, video_id, path):
        self.id = video_id
        self.path = path
        self.is_automatic = None
        self.point = None

    def set_point(self, is_automatic, point):
        self.is_automatic = is_automatic
        self.point = point

    def does_path_exist(self):
        if os.path.exists(self.path):
            return True
        else:
            return False


    def get_first_frame(self):
        status = "Video does not exist"
        frame = None
        if self.does_path_exist():
            # Open the video file
            video_capture = cv2.VideoCapture(self.path)
            status = "Ok"

            # Check if the video file was successfully opened
            if not video_capture.isOpened():
                print("Error opening video file:", self.path)
                status = "Can't load the video"

            # Read the first frame from the video
            else:
                ret, frame = video_capture.read()

                # Check if a frame was successfully read
                if not ret:
                    print("Error reading video frame.")
                    status = "Can't load the frame"

                # Release the video capture object
                video_capture.release()

        return status, frame

        
    def get_number_of_frames(self):
        status = "Video does not exist"
        frame_count = None

        if self.does_path_exist():
            video_capture = cv2.VideoCapture(self.path)
            status = "Ok"
            if not video_capture.isOpened():
                print("Error opening video file:", self.path)
                status = "Can't load the video"
            else:
                frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
                video_capture.release()

        return status, frame_count
    
    def get_cropped_frames(self):
        status = "Video does not exist"
        cropped_frames = []

        if self.does_path_exist():
            status = "Ok"
            # Open the video file
            video = cv2.VideoCapture(self.path)


            # Read the first frame
            success, frame = video.read()

            # Loop through all frames in the video
            while success:
                x, y, crop_w, crop_h = 52, 62, 525, 362
                # Crop the frame using the provided crop area coordinates
                cropped_frame = frame[62:362, 52:525]

                # Append the cropped frame to the list
                cropped_frames.append(cropped_frame)

                # Read the next frame
                success, frame = video.read()

            # Release the video file
            video.release()

        print(type(cropped_frames))
        print(type(cropped_frames[0]))

        return status, cropped_frames

        
