import tensorflow as tf

import numpy as np
import cv2

import math

from . utils import *

class Model:
    def __init__(self, id, path, batch_size):
        self.id = id

        self.model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model.load_weights(path)
        self.batch_size = batch_size

        self.results = None
        

    def preprocess_images(self, images):
        self.results = np.zeros((len(images), 3))
        preprocessed_images = np.zeros((len(images), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        print("images", len(images))

        for i, image in enumerate(images):
            # Apply filters
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            equalized = cv2.equalizeHist(gray)
            filtered = cv2.bilateralFilter(equalized, 9, 75, 75)
            color = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)

            # Resize image
            # Calculate the new aspect ratio
            h, w = image.shape[:2]
            aspect_ratio = w / h
            new_height = int(IMG_WIDTH / aspect_ratio)
            resized_image = cv2.resize(color, (IMG_WIDTH, new_height))
            # print(img_x.shape)

            # Pad the image to the desired height
            pad_top = int((IMG_HEIGHT - new_height) / 2)
            pad_bottom = IMG_HEIGHT - new_height - pad_top
            resized_image = cv2.copyMakeBorder(resized_image, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

            preprocessed_images[i] = resized_image

        # cv2.imshow('example', preprocessed_images[0])

        return preprocessed_images
    
    def redimension_images(self, images):
        redimensioned_images = []

        for resized_image in images:
            original_height, original_width = [300, 473]
            image = resized_image = cv2.resize(resized_image, (473, 473))

            image= image[86: image.shape[1] - 87]

            redimensioned_images.append(image)
        
        return redimensioned_images

    
    def generate_batches(self, images):
        batches = []
        amount_of_batches = math.ceil(len(images) / BATCH_SIZE)
        
        # print(len(images))
        # print(amount_of_batches)

        # Initialize the batches list with empty lists
        for _ in range(amount_of_batches):
            batches.append([])

        for i, image in enumerate(images):
            batches[int(i / BATCH_SIZE)].append(image)

        batches = np.array(batches)

        return batches
    
    def perform_inference(self, batch):
        batch = np.array(batch)

        # print('batch dims 2:', np.shape(batch))
        # image = batch[0]
        # batch = np.expand_dims(batch, axis=0)
        # print(batch.shape)
        predictions = self.model.predict(batch, verbose=0) #

        # print(np.unique(predictions))

        predictions = (predictions > 0.5).astype(np.uint8)

        # print(np.unique(predictions))

        print('predictions dims:', np.shape(predictions))

        # predictions = self.model.predict(batch)

        return predictions
    
    def analyze_predictions(self, predictions, x_coordinate):
        results = []
        largest_contours = []
        predictions = np.squeeze(predictions, axis = -1) * 255
        predictions = np.array(self.redimension_images(predictions))

        for prediction in predictions:
            contours, _ = cv2.findContours(prediction, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            canvas = np.zeros_like(prediction)
            if len(contours) > 0:
                largest_contour = max(contours, key=cv2.contourArea)
                cv2.drawContours(canvas, [largest_contour], -1, 255, 2)
            
            largest_contours.append(canvas)
            # cv2.line(canvas, (x_coordinate, 0), (x_coordinate, canvas.shape[0]), 255, 2)
            # cv2.imshow('canvas', canvas)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()




        if x_coordinate is not None:
            topmost_point = None
            lowermost_point = None
            for canvas in largest_contours:
                white_indices = np.where(canvas[:, x_coordinate] == 255)[0]

                if len(white_indices) > 0:
                    topmost_point = white_indices[0]
                    lowermost_point = white_indices[-1]
                
                results.append([lowermost_point, topmost_point])

        else: 
            results = None 

        results = np.array(results)

        return results
