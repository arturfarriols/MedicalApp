import torch
from torchvision import transforms

from torch.utils.data import DataLoader
from torch.utils.data import Dataset as BaseDataset
import torch.optim as optim
import albumentations as albu
from torchvision.transforms import ToTensor

import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger

import os
import inspect
import distutils

import torch.nn.functional as F
import segmentation_models_pytorch as smp

from PIL import Image
import numpy as np
import cv2

from . model_pytorch import Model



# model_path = ".\models_checkpoints\model_checkpoints\version_576\checkpoints\epoch=5-step=521.ckpt"
model_path = "version_576\checkpoints\epoch=5-step=521.ckpt"

loss = smp.losses.DiceLoss(smp.losses.constants.MULTICLASS_MODE)
optimizer = optim.Adam
selected_parameters = {'model': 'unetplusplus',
                'encoder_name': 'efficientnet-b2',
                'in_channels': 3, 'classes': 3,
                'encoder_weights': 'imagenet',
                'loss': loss,
                'optimizer': optimizer,
                'learning_rate': 0.0008000076640604941,
                'minimum_learning_rate': 5e-06,
                'scheduler_used': False,
                'decoder_attention_type': None}

class SegmentationModel:
    
    def __init__(self, id):
        self.id = id

        app_folder = os.environ.get("MY_APP_FOLDER")

        # Split the app_folder path into its components
        folders = app_folder.split(os.path.sep)

        # Remove the last folder
        if len(folders) > 0:
            folders.pop()

        # Join the modified app_folder with the checkpoint_path
        final_path = os.path.join(os.path.sep.join(folders), model_path)

        print("Final path:", final_path)


        self.model = self.generate_model(info=False, **selected_parameters)
        checkpoint = torch.load(final_path, map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint['state_dict'])
        self.preprocess_transform = self.get_single_image_preprocessing()


    def generate_model(self, info = True, **kwargs):
        arch = kwargs['model']
        encoder_name = kwargs['encoder_name']
        in_channels = kwargs['in_channels']
        classes = kwargs['classes']
        loss = kwargs['loss']
        optimizer = kwargs['optimizer']
        learning_rate = kwargs['learning_rate']
        minimum_learning_rate = kwargs['minimum_learning_rate']
        scheduler_used = kwargs['scheduler_used']

        if info:
            for key, value in kwargs.items():
                print(f"{key}: {value}")

        kwargs = {key: value for key, value in kwargs.items() if value is not None and key != 'model' and key != 'encoder_name' and key != 'in_channels' and key != 'classes'
                and key != 'loss' and key != 'optimizer' and key != 'learning_rate' and key != 'minimum_learning_rate' and key != 'scheduler_used'}

        model = Model(arch, encoder_name, in_channels, classes, loss, optimizer, learning_rate, minimum_learning_rate, scheduler_used, **kwargs)
        # print(model)
        return model

    def to_tensor(self, x, **kwargs):
        return x.astype('float32')

    def get_single_image_preprocessing(self):
        """Construct preprocessing transform

        Args:
            preprocessing_fn (callable): data normalization function
                (can be specific for each pretrained neural network)
        Return:
            transform: albumentations.Compose
        """
        _transform = [
            albu.Lambda(image=self.to_tensor),
        ]
        return albu.Compose(_transform)
    
    # def perform_inference(self, image_path):
    #     image = Image.open(image_path)

    #     target_size = (256, 256)
    #     image = image.resize(target_size, Image.LANCZOS)

    #     # Convert the PIL image to a NumPy array
    #     image_np = np.array(image)

    #     # Apply the preprocessing transform to the NumPy array
    #     preprocessed_image = self.preprocess_transform(image=image_np)["image"]

    #     # Convert the preprocessed image to a PyTorch tensor using torchvision's ToTensor()
    #     input_tensor = ToTensor()(preprocessed_image)

    #     # Ensure the shape is 3x256x256
    #     input_tensor = input_tensor.unsqueeze(0)  # Add a batch dimension
    #     print(input_tensor.shape)  # Output: torch.Size([1, 3, 256, 256])

    #     with torch.no_grad():
    #         self.model.eval()
    #         logits = self.model(input_tensor)
    #     pr_masks = logits.softmax(dim=1)

    #     _, pr_masks = torch.max(pr_masks, dim=1)

    #     # Map the predicted labels to the desired class values
    #     pr_masks = pr_masks.to(torch.float32)  # Convert to float for consistency
    #     pr_masks = pr_masks * 2 / (3 - 1)  # Scale the values to range [0, 2]
    #     # print(torch.unique(predicted_labels))
    #     pr_masks = pr_masks.unsqueeze(dim=1)

    #     print(np.unique(pr_masks))

    #     return pr_masks

    def perform_inference(self, image):
        # image = Image.open(image_path)

        target_size = (256, 256)
        print("TYPE", type(image))
        print("SHAPE", np.shape(image))
        image = cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)

        # Convert the PIL image to a NumPy array
        # image_np = np.array(image)

        # preprocess_transform = get_single_image_preprocessing()

        # Apply the preprocessing transform to the NumPy array
        preprocessed_image = self.preprocess_transform(image=image)["image"]

        # Convert the preprocessed image to a PyTorch tensor using torchvision's ToTensor()
        input_tensor = ToTensor()(preprocessed_image)

        # Ensure the shape is 3x256x256
        input_tensor = input_tensor.unsqueeze(0)  # Add a batch dimension
        print(input_tensor.shape)  # Output: torch.Size([1, 3, 256, 256])

        with torch.no_grad():
            self.model.eval()
            logits = self.model(input_tensor)
        pr_masks = logits.softmax(dim=1)

        _, pr_masks = torch.max(pr_masks, dim=1)

        # Map the predicted labels to the desired class values
        pr_masks = pr_masks.to(torch.float32)  # Convert to float for consistency
        pr_masks = pr_masks * 2 / (3 - 1)  # Scale the values to range [0, 2]
        # print(torch.unique(predicted_labels))
        pr_masks = pr_masks.unsqueeze(dim=1)

        print(np.unique(pr_masks))

        return pr_masks
    
    def divide_predicted_values(self, masks, display=False):
        # Load the gray image (replace 'path_to_image' with the actual path to your image)
        image = masks.numpy().squeeze()

        # Define the values you want to extract (1 for the first image, 2 for the second image)
        value_to_extract_1 = 1
        value_to_extract_2 = 2

        # Create masks for extracting pixels with value 1 and value 2
        mask_1 = (image == value_to_extract_1)
        mask_2 = (image == value_to_extract_2)

        # Generate two images based on the masks
        image_with_value_1 = np.zeros_like(image)
        image_with_value_1[mask_1] = value_to_extract_1

        image_with_value_2 = np.zeros_like(image)
        image_with_value_2[mask_2] = value_to_extract_2

        # Display or save the generated images as needed
        if display:
            cv2.imwrite("upper_mask.jpg", image_with_value_1 * 255)
            print()
            cv2.imwrite("lower_mask.jpg", image_with_value_2 * 255)

        return image_with_value_1, image_with_value_2
    
    def filter_and_resize_predictions(self, image, new_size=300):
        # Load the original image (replace 'path_to_image' with the actual path to your image)
        # image = image_with_value_2

        # Apply binary thresholding to the image
        _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
        binary_image = np.uint8(binary_image)

        # cv2_imshow(binary_image)

        # Find contours in the binary image
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        threshold_area = 100

        # Filter contours by area
        filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > threshold_area]

        # Find the center of the biggest contour
        if filtered_contours:
            biggest_contour = max(filtered_contours, key=cv2.contourArea)
            M = cv2.moments(biggest_contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Set the threshold for y coordinate difference from the biggest contour's center
            threshold_y = 30

            # Filter out contours whose center coordinate y is not within the threshold
            final_contours = [contour for contour in filtered_contours if abs(cy - cv2.minEnclosingCircle(contour)[0][1]) <= threshold_y]

            # Create a canvas image with the same shape as the original image
            canvas = np.zeros_like(image)

            # Draw white filled polygons (interior of the contours) on the canvas
            cv2.drawContours(canvas, final_contours, -1, 255, thickness=cv2.FILLED)

            # Resize the canvas image to 300x300 using the nearest-neighbor interpolation to maintain original values
            resized_canvas = cv2.resize(canvas, (new_size, new_size), interpolation=cv2.INTER_NEAREST)

            return resized_canvas
        return None
    
    def get_extreme_pixels(self, image, store_uppermost=True):
        import cv2
        import numpy as np

        # Load the grayscale image
        # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Check if the image was successfully loaded
        if image is None:
            print("Error: Unable to read the image from the specified path.")
        else:
            # Get the height and width of the image
            height, width = image.shape

            # Initialize a list to store the extreme pixels position for each column
            extreme_pixels = []

            # Loop through each column
            for col in range(width):
                # Initialize the row index based on whether we are looking for uppermost or lowermost pixels
                if store_uppermost:
                    row = 0
                else:
                    row = height - 1

                # Scan the column from top to bottom or from bottom to top
                while 0 <= row < height:
                    # Check if the pixel is white (pixel value = 255)
                    if image[row, col] == 255:
                        # Store the position of the extreme pixel for this column
                        extreme_pixels.append((row, col))
                        break

                    # Move to the next row (up or down depending on the mode)
                    if store_uppermost:
                        row += 1
                    else:
                        row -= 1

            # Now, 'extreme_pixels' contains the position of the extreme pixel for each column.
            return extreme_pixels
        
    def create_subarrays(self, input_array):
        result = []
        current_subarray = []
        last_value = None

        for item in input_array:
            if last_value is None:
                # For the first item, initialize the current_subarray and last_value
                current_subarray.append(item)
                last_value = item[1]
            elif item[1] == last_value + 1:
                # If the current item's second value is contiguous to the last value,
                # add it to the current_subarray
                current_subarray.append(item)
                last_value = item[1]
            else:
                # If there is a gap, add the current_subarray to the result and start a new one
                result.append(current_subarray)
                current_subarray = [item]
                last_value = item[1]

        # Add the last current_subarray to the result
        if current_subarray:
            result.append(current_subarray)

        return result

    def find_local_extrema(self, sequence):
        n = len(sequence)
        extrema = []
        extrema_info = []
        first = True

        for i in range(n):
            current_value = sequence[i][0]
            is_maximum = True
            is_minimum = True

            for j in range(1, 6):  # Check the next 5 elements
                if i + j < n and sequence[i + j][0] > current_value:
                    is_maximum = False
                if i + j < n and sequence[i + j][0] < current_value:
                    is_minimum = False

            for j in range(1, 6):  # Check the previous 5 elements
                if i - j >= 0 and sequence[i - j][0] > current_value:
                    is_maximum = False
                if i - j >= 0 and sequence[i - j][0] < current_value:
                    is_minimum = False

            if is_maximum:
                    extrema_information = list(sequence[i])
                    extrema_information.append("maximum")
                    extrema.append(extrema_information)
                    # print("maximum", extrema_information)
            elif is_minimum:
                    extrema_information = list(sequence[i])
                    extrema_information.append("minimum")
                    extrema.append(extrema_information)
                    # print("minimum", extrema_information)


        return extrema
    
    def find_middle_numbers(self, sequence):
        result = []
        i = 0
        n = len(sequence)

        while i < n:
            start = i
            while i < n - 1 and sequence[i][0] == sequence[i + 1][0]:
                i += 1
            end = i

            # Determine the middle index
            middle_index = (start + end) // 2

            # Append the middle tuple to the result
            result.append(sequence[middle_index])

            i += 1

        return result
    
    def process_sequences(self, data):
        result = []
        previous_label = None
        previous_value = None

        for item in data:
            value, _, label = item

            if previous_label is None or label != previous_label:
                result.append(item)
                previous_label = label
                previous_value = value
            else:
                if (label == 'maximum' and value > previous_value) or (label == 'minimum' and value < previous_value):
                    result[-1] = item
                    previous_value = value

        return result
    
    def local_extrema_filtering(self, local_extrema):
        filtered_sequence = self.find_middle_numbers(local_extrema)
        processed_sequence = self.process_sequences(filtered_sequence)

        return processed_sequence
    
    def split_maximum_minimum(self, data):
        maximum_values = []
        minimum_values = []

        for item in data:
            _, middle, label = item
            if label == 'maximum':
                maximum_values.append(item)
            elif label == 'minimum':
                minimum_values.append(item)

        return maximum_values, minimum_values

    def merge_maximum_minimum(self, maximum_data, minimum_data):
        merged_data = []
        max_idx = 0
        min_idx = 0

        while max_idx < len(maximum_data) and min_idx < len(minimum_data):
            max_middle = maximum_data[max_idx][1]
            min_middle = minimum_data[min_idx][1]

            if max_middle < min_middle:
                merged_data.append(maximum_data[max_idx])
                max_idx += 1
            else:
                merged_data.append(minimum_data[min_idx])
                min_idx += 1

        # Append any remaining elements from maximum_data and minimum_data
        while max_idx < len(maximum_data):
            merged_data.append(maximum_data[max_idx])
            max_idx += 1

        while min_idx < len(minimum_data):
            merged_data.append(minimum_data[min_idx])
            min_idx += 1

        return merged_data
    
    def enough_elements(self, split, threshold = 4):
        if len(split) < threshold: return False
        return True
    
    def remove_sequence_outliers(self, data, min_difference = 5):
        # Extract the first elements of the tuples for analysis
        first_elements = [item[0] for item in data]

        # Calculate the IQR (Interquartile Range)
        q1 = np.percentile(first_elements, 25)
        q3 = np.percentile(first_elements, 75)
        iqr = q3 - q1

        # # Ensure the minimum difference between upper and lower bounds is 5
        # min_iqr = max(iqr, 5)

        # Define the lower and upper bounds for outliers
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        difference = abs(upper_bound - lower_bound)
        if difference < min_difference:
            remaining = (min_difference - difference) / 2
            # print(remaining)
            upper_bound += remaining
            lower_bound -= remaining

        print(lower_bound, upper_bound)

        # Filter out elements that are outside the bounds
        filtered_data = [item for item in data if lower_bound <= item[0] <= upper_bound]

        return filtered_data
    
    def compare_sequences(self, upper_sequence, lower_sequence, threshold = 8):
        filtered_upper_sequence = [item for item in upper_sequence if any(abs(item[1] - x[1]) < threshold for x in lower_sequence)]
        filtered_lower_sequence = [item for item in lower_sequence if any(abs(item[1] - x[1]) < threshold for x in upper_sequence)]
        return filtered_upper_sequence, filtered_lower_sequence
    
    def generate_comparisson_dict(self, shorter_sequence, longer_sequence, threshold=8):
        result = {}

        for i, shorter_item in enumerate(shorter_sequence):
            result[i] = []
            for j, longer_item in enumerate(longer_sequence):
                if abs(shorter_item[1] - longer_item[1]) < threshold:
                    result[i].append(j)

        return result

    def compare_sequences_2(self, upper_sequence, lower_sequence, threshold=8):
        upper_size = len(upper_sequence)
        lower_size = len(lower_sequence)

        print(upper_size, lower_size)

        if upper_size <= lower_size:
            comparisson_dict = self.generate_comparisson_dict(upper_sequence, lower_sequence)
            is_upper = True
        else:
            comparisson_dict = self.generate_comparisson_dict(lower_sequence, upper_sequence)
            is_upper = False

        print(comparisson_dict)

        return comparisson_dict, is_upper
    
    def filter_and_remove_keys(self, dictionary, upper_sequence, lower_sequence, analyzing_maximums=True, is_upper=True):
        # Initialize a new dictionary to store the filtered results
        filtered_dict = {}

        func = min if analyzing_maximums else max

        # Iterate through the dictionary
        for key, value_list in dictionary.items():
            if len(value_list) > 1:
                # Find the index with the largest difference in the first value
                if len(upper_sequence) >= len(lower_sequence):#if is_upper:
                    print("dictionary", dictionary)
                    print("lower_sequence", lower_sequence)
                    print("upper_sequence", upper_sequence)
                    diff_index = func(value_list, key=lambda index: abs(upper_sequence[index][0] - lower_sequence[key][0]))
                else:
                    print("dictionary", dictionary)
                    print("lower_sequence", lower_sequence)
                    print("upper_sequence", upper_sequence)
                    diff_index = func(value_list, key=lambda index: abs(lower_sequence[index][0] - upper_sequence[key][0]))
                filtered_dict[key] = diff_index
            else:
                filtered_dict[key] = value_list[0]


        # Updated dictionaries

        # Iterate through the dictionary to find and remove keys
        keys_to_remove = set()  # Store keys to remove in a set to avoid modifying the dictionary while iterating

        for key1, value1 in filtered_dict.items():
            for key2, value2 in filtered_dict.items():
                if key1 != key2 and value1 == value2:
                    # Compare the first elements of tuples
                    if is_upper:
                        diff1 = abs(lower_sequence[key1][0] - upper_sequence[value1][0])
                        diff2 = abs(lower_sequence[key2][0] - upper_sequence[value2][0])
                    else:
                        diff1 = abs(lower_sequence[key1][0] - upper_sequence[value1][0])
                        diff2 = abs(lower_sequence[key2][0] - upper_sequence[value2][0])
                    # If the first element of key1 is closer to its value, mark key1 for removal
                    if diff1 < diff2:
                        keys_to_remove.add(key1)
                    # If the first element of key2 is closer to its value, mark key2 for removal
                    elif diff2 <= diff1:
                        keys_to_remove.add(key2)

        # Remove keys from the dictionary
        for key in keys_to_remove:
            del filtered_dict[key]

        return filtered_dict
    
    def calculate_mean_central_difference(self, arr1, arr2, index_dict):
        differences = []

        for key, value in index_dict.items():
            if key < len(arr1) and value < len(arr2):
                diff = abs(arr1[key][0] - arr2[value][0])
                differences.append(diff)

        if differences:
            mean_difference = sum(differences) / len(differences)
            return mean_difference
        else:
            return None
        
    def filter_elements_by_indexes(self, elements, indexes):
        filtered_elements = [elements[i] for i in indexes if i < len(elements)]
        return filtered_elements
    
    def calculate_upper_and_lower_distances(self, array1, array2, array3):
        finished = False
        i = 0
        min_difference = 0
        max_difference = 0
        min_matches = 0
        max_matches = 0

        while not finished and i < len(array3):
            # print(array3[i][1])
            if len(array1) > 0 and array3[i][1] == array1[0][1]:
                min_difference += abs(array1[0][0] - array3[i][0])
                min_matches += 1
                array1.pop(0)

                # print("min_array", array1)

            if len(array2) > 0 and array3[i][1] == array2[0][1]:
                max_difference += abs(array2[0][0] - array3[i][0])
                max_matches += 1
                array2.pop(0)

                # print("max_array", array2)

            if len(array1) <= 0 and len(array2) <= 0:
                finished = True

            i += 1

        mean_min_difference = min_difference / min_matches if min_matches != 0 else 0
        mean_max_difference = max_difference / max_matches if max_matches != 0 else 0

        return mean_min_difference, mean_max_difference
    
    def calculate_mean_distance_extremes(self, sequence):
        # Initialize a variable to store the sum of distances for the first value
        sum_distance_first = 0

        # Iterate through the sequence
        for i in range(len(sequence) - 1):
            current_item = sequence[i]
            next_item = sequence[i + 1]

            # Calculate the absolute difference for the first value
            diff_first = abs(current_item[1] - next_item[1])

            # Add the difference to the sum
            sum_distance_first += diff_first

        # Calculate the mean distance for the first element
        mean_distance_first = sum_distance_first / (len(sequence) - 1)

        return mean_distance_first

    def process_results(self, mask):
        image_1, image_2 = self.divide_predicted_values(mask, display=False)

        processed_image_1 = self.filter_and_resize_predictions(image_1)
        processed_image_2 = self.filter_and_resize_predictions(image_2)

        extreme_points_1_up = self.get_extreme_pixels(processed_image_1.copy(), store_uppermost=True)
        extreme_points_1_down = self.get_extreme_pixels(processed_image_1.copy(), store_uppermost=False)

        extreme_points_2_up = self.get_extreme_pixels(processed_image_2.copy(), store_uppermost=True)
        extreme_points_2_down = self.get_extreme_pixels(processed_image_2.copy(), store_uppermost=False)

        lower_subarrays = self.create_subarrays(extreme_points_1_down)
        upper_subarrays = self.create_subarrays(extreme_points_2_up)
        lower_and_upper_subarrays = [lower_subarrays, upper_subarrays]
        lower_and_upper_sequences = []
        min_sequences = []
        max_sequences = []

        for subarrays in lower_and_upper_subarrays:
            # print("NEW SUBARRAYS")
            max_subarrays = []
            min_subarrays = []
            for subarray in subarrays:
                # print("New subarray")
                local_extrema = self.find_local_extrema(subarray)
                filtered_sequence = self.local_extrema_filtering(local_extrema)
                # print("filtered_sequence", filtered_sequence)
                split = self.split_maximum_minimum(filtered_sequence)
                long_sequence = self.enough_elements(split[0]) and self.enough_elements(split[1])

                if long_sequence:
                    max_sequence_no_outliers = self.remove_sequence_outliers(split[0])
                    min_sequence_no_outliers = self.remove_sequence_outliers(split[1])
                    max_subarrays.extend(max_sequence_no_outliers)
                    min_subarrays.extend(min_sequence_no_outliers)

            # lower_and_upper_sequences.append([min_subarrays, max_subarrays])
            min_sequences.append(min_subarrays)
            max_sequences.append(max_subarrays)

        min_sequences[0], max_sequences[1] = self.compare_sequences(min_sequences[0], max_sequences[1])
        max_sequences[0], min_sequences[1] = self.compare_sequences(max_sequences[0], min_sequences[1])

        # print()
        # print("lower_and_upper_sequences", min_sequences)
        # print("lower_and_upper_sequences", max_sequences)

        min_comparisson_dict, min_is_upper = self.compare_sequences_2(min_sequences[0], max_sequences[1], threshold=8)
        max_comparisson_dict, max_is_upper = self.compare_sequences_2(max_sequences[0], min_sequences[1], threshold=8)

        min_comparisson_dict = self.filter_and_remove_keys(min_comparisson_dict, min_sequences[0], max_sequences[1], analyzing_maximums=False, is_upper=min_is_upper)
        max_comparisson_dict = self.filter_and_remove_keys(max_comparisson_dict, max_sequences[0], min_sequences[1], analyzing_maximums=True, is_upper=max_is_upper)

        # print()
        # print("min_comparisson_dict", min_comparisson_dict)
        # print("max_comparisson_dict", max_comparisson_dict)

        if min_is_upper:
            min_central_difference = self.calculate_mean_central_difference(min_sequences[0], max_sequences[1], min_comparisson_dict)
            min_sequences[0] = self.filter_elements_by_indexes(min_sequences[0], min_comparisson_dict)
            max_sequences[1] = self.filter_elements_by_indexes(max_sequences[1], min_comparisson_dict)
        else:
            min_central_difference = self.calculate_mean_central_difference(max_sequences[1], min_sequences[0], min_comparisson_dict)
            max_sequences[1] = self.filter_elements_by_indexes(max_sequences[1], min_comparisson_dict)
            min_sequences[0] = self.filter_elements_by_indexes(min_sequences[0], min_comparisson_dict)

        if max_is_upper:
            max_central_difference = self.calculate_mean_central_difference(max_sequences[0], min_sequences[1], min_comparisson_dict)
            max_sequences[0] = self.filter_elements_by_indexes(max_sequences[0], min_comparisson_dict)
            min_sequences[1] = self.filter_elements_by_indexes(min_sequences[1], min_comparisson_dict)
        else:
            max_central_difference = self.calculate_mean_central_difference( min_sequences[1], max_sequences[0], min_comparisson_dict)
            min_sequences[1] = self.filter_elements_by_indexes(min_sequences[1], min_comparisson_dict)
            max_sequences[0] = self.filter_elements_by_indexes(max_sequences[0], min_comparisson_dict)

        upper_min_difference, upper_max_difference = self.calculate_upper_and_lower_distances(min_sequences[0].copy(), max_sequences[0].copy(), extreme_points_1_up)
        lower_min_difference, lower_max_difference = self.calculate_upper_and_lower_distances(max_sequences[1].copy(), min_sequences[1].copy(), extreme_points_2_down)

        merged_upper_sequence = self.process_sequences(self.merge_maximum_minimum(min_sequences[0], max_sequences[0]))
        merged_lower_sequence = self.process_sequences(self.merge_maximum_minimum(min_sequences[1], max_sequences[1]))

        upper_mean_distance = self.calculate_mean_distance_extremes(merged_upper_sequence) * 2
        lower_mean_distance = self.calculate_mean_distance_extremes(merged_lower_sequence) * 2

        results = {"upper_min_difference": upper_min_difference, "upper_max_difference": upper_max_difference, "min_central_difference":min_central_difference,
                "max_central_difference":max_central_difference, "lower_min_difference":lower_min_difference, "lower_max_difference":lower_max_difference,
                "upper_mean_distance": upper_mean_distance, "lower_mean_distance": lower_mean_distance}

        return results
