import os

import cv2

import numpy as np

from . utils import *

import matplotlib.pyplot as plt

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

    def locate_image_rectangle(self, num_frames=10, threshold_value=10):

        min_xs = []
        max_xs = []
        min_ys = []
        max_ys = []
        nearest_points = []
        last_consecutive_points = []
        first_white_points = []

        video = cv2.VideoCapture(self.path)

        for counter in range(num_frames):
            # Read the current frame
            ret, frame = video.read()

            # Break the loop if the video has ended
            if not ret:
                break

            # Convert the frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply binary thresholding
            max_value = 255  # Maximum value for thresholding
            _, binary_image = cv2.threshold(gray_frame, threshold_value, max_value, cv2.THRESH_BINARY)

            # cv2_imshow(binary_image)

            # Find contours
            contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)

            frame_copy = frame.copy()
            cv2.drawContours(frame_copy, [largest_contour], -1, (0, 255, 0), 2)
            # cv2_imshow(frame_copy)

            # Obtain the highest and lowest coordinates
            x_values = largest_contour[:, :, 0]
            y_values = largest_contour[:, :, 1]
            min_x = np.min(x_values)
            max_x = np.max(x_values)
            min_y = np.min(y_values)
            max_y = np.max(y_values)

            min_xs.append(min_x)
            max_xs.append(max_x)
            min_ys.append(min_y)
            max_ys.append(max_y)

            # Define the given point
            point = (max_x, min_y)  # Example coordinates, replace with your own

            # Find the nearest white point to the right of the given point
            nearest_point = None
            nearest_distance = float("inf")

            height, width = binary_image.shape[:2]

            for y in range(point[1], height):
                for x in range(point[0] + 1, width):
                    if binary_image[y, x] == 255:
                        distance = np.sqrt((x - point[0])**2 + (y - point[1])**2)
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_point = (x, y)

            # Find the last right consecutive white point from the nearest point
            last_consecutive_point = nearest_point

            for x in range(nearest_point[0] + 1, width):
                if binary_image[nearest_point[1], x] == 255:
                    last_consecutive_point = (x, nearest_point[1])
                else:
                    break

            # Find the first white point below the last consecutive point
            first_white_point = None

            for y in range(last_consecutive_point[1] + 1, height):
                if binary_image[y, last_consecutive_point[0]] == 255:
                    first_white_point = (last_consecutive_point[0], y)
                    break

            if last_consecutive_point is not None and first_white_point is not None:
                nearest_points.append(nearest_point)
                last_consecutive_points.append(last_consecutive_point)
                first_white_points.append(first_white_point)

        # Release the video object and close the window
        video.release()
        # cv2.destroyAllWindows()

        vertices = [min_xs, max_xs, min_ys, max_ys]
        distances = [nearest_points, last_consecutive_points, first_white_points]

        return vertices, distances
    
    def obtain_extreme_points(self):
        found = False
        counter = 0
        patience = 10
        x_target_difference = 400
        y_target_difference = 300


        while not found and counter < patience:
            vertices, distances = self.locate_image_rectangle(threshold_value=patience - counter)

            min_xs, max_xs, min_ys, max_ys = vertices

            ordered_min_xs = ordered_by_frequency(min_xs)
            ordered_max_xs = ordered_by_frequency(max_xs)
            ordered_min_ys = ordered_by_frequency(min_ys)
            ordered_max_ys = ordered_by_frequency(max_ys)

            indexes_x, difference_x = find_indexes_with_difference(ordered_min_xs, ordered_max_xs, target_difference = x_target_difference)
            indexes_y, difference_y = find_indexes_with_difference(ordered_min_ys, ordered_max_ys, target_difference = y_target_difference)

            print(difference_x, difference_y)

            if abs(x_target_difference - difference_x) < 15 and abs(y_target_difference - difference_y) < 15:
                found = True

            print(ordered_min_xs)
            print(ordered_max_xs)
            print(ordered_min_ys)
            print(ordered_max_ys)

        if not found:
            raise ValueError("Image is not suitable to be processed")

        min_x = ordered_min_xs[indexes_x[0]]
        max_x = ordered_max_xs[indexes_x[1]]
        min_y = ordered_min_ys[indexes_y[0]]
        max_y = ordered_max_ys[indexes_y[1]]

        # top_left_corner = [ordered_min_xs[indexes_x[0]], ordered_min_ys[indexes_y[0]]]
        # bottom_left_corner = [ordered_min_xs[indexes_x[0]], ordered_max_ys[indexes_y[1]]]
        # top_right_corner = [ordered_max_xs[indexes_x[1]], ordered_min_ys[indexes_y[0]]]
        # bottom_right_corner = [ordered_max_xs[indexes_x[1]], ordered_max_ys[indexes_y[1]]]

        # corners = [top_left_corner, bottom_left_corner, top_right_corner, bottom_right_corner]

        # print(max_y)
        return [min_y, max_y, min_x, max_x]
    
    def process_video_and_concatenate_columns(self, extreme_points):
        cap = cv2.VideoCapture(self.path)

        # Check if the video file was successfully opened
        if not cap.isOpened():
            print("Error opening video file")
            return None

        counter = 0
        columns = []

        # Read and process frames
        while True:
            counter += 1
            # Read the next frame
            ret, frame = cap.read()

            # Break the loop if the video has ended
            if not ret:
                break

            cropped_frame = frame[extreme_points[0]:extreme_points[1], extreme_points[2]:extreme_points[3]]

            # Extract the desired column for each offset
            column = cropped_frame[:, self.point.x()]

            # Create a vertical image from the column
            column_image = np.expand_dims(column, axis=1)

            columns.append(column_image)

        # Concatenate the column images horizontally
        concatenated_image = np.concatenate(columns, axis=1)

        # Release the video object and close the window
        cap.release()
        # cv2.destroyAllWindows()

        return concatenated_image
    
    def resize_image(self, image, desired_height=300):
        # Get the current height and width of the image
        height, width, _ = image.shape

        # Calculate the aspect ratio
        aspect_ratio = desired_height / height

        # Calculate the new width based on the aspect ratio
        new_width = int(width * aspect_ratio)

        # Resize the image
        resized_image = cv2.resize(image, (new_width, desired_height))

        return resized_image

    def generate_sub_images(self, image, stride = 100):
        # Open the image using OpenCV
        height, width, _ = image.shape

        # Calculate the number of square images and the remaining width
        num_images = (width - 300) // stride + 1
        remaining_width = (width - 300) % stride

        # Create a list to store the cropped square images
        cropped_images = []

        # Crop the image horizontally into squares
        for i in range(num_images):
            left = i * stride
            right = left + 300
            box = (left, 0, right, height)
            cropped_img = image[0:height, left:right]
            cropped_images.append({"image": cropped_img, "stride": left})
            print(left)

        # Crop the last image if there's any remaining width
        if remaining_width > 0:
            left = width - 300
            right = width
            box = (left, 0, right, height)
            cropped_img = image[0:height, left:right]
            cropped_images.append(cropped_img)
            print(left)

        return cropped_images

    def preprocess_video(self):
        print("I never reach this")
        extreme_points = self.obtain_extreme_points()
        print("X coordinate is", self.point.x())
        concatenated_image = self.process_video_and_concatenate_columns(extreme_points)

        if concatenated_image.shape[0] != 300:
            concatenated_image = self.resize_image(self, concatenated_image, desired_height=300)

        concatenated_images = self.generate_sub_images(concatenated_image)

        # # Define the filename for the saved image
        # output_filename = 'output_image.jpg'

        # # Save the image in the current path
        # cv2.imwrite(output_filename, concatenated_image)

        # # Get the absolute path of the saved image
        # saved_image_path = os.path.abspath(output_filename)

        # # Print the path
        # print("Image saved at:", saved_image_path)

        return None


