import tensorflow as tf
import numpy as np
import cv2
import random

upper_model_path = ".\models_checkpoints\model_checkpoints\my_checkpoint"
lower_model_path = ".\models_checkpoints\model_checkpoints\my_checkpoint"

IMG_HEIGHT = 256
IMG_WIDTH = 256
IMG_CHANNELS = 3

BATCH_SIZE = 16

AMOUNT_OF_FILTER_POINTS = 5
DISTANCE_THRESHOLD = 20

inputs = tf.keras.layers.Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)

#Contraction path
c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
c1 = tf.keras.layers.Dropout(0.1)(c1)
c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)

c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
c2 = tf.keras.layers.Dropout(0.1)(c2)
c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2)

c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
c3 = tf.keras.layers.Dropout(0.2)(c3)
c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
p3 = tf.keras.layers.MaxPooling2D((2, 2))(c3)

c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
c4 = tf.keras.layers.Dropout(0.2)(c4)
c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
p4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)

c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
c5 = tf.keras.layers.Dropout(0.3)(c5)
c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

#Expansive path
u6 = tf.keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
u6 = tf.keras.layers.concatenate([u6, c4])
c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
c6 = tf.keras.layers.Dropout(0.2)(c6)
c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)

u7 = tf.keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
u7 = tf.keras.layers.concatenate([u7, c3])
c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
c7 = tf.keras.layers.Dropout(0.2)(c7)
c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)

u8 = tf.keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
u8 = tf.keras.layers.concatenate([u8, c2])
c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
c8 = tf.keras.layers.Dropout(0.1)(c8)
c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)

u9 = tf.keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
u9 = tf.keras.layers.concatenate([u9, c1], axis=3)
c9 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
c9 = tf.keras.layers.Dropout(0.1)(c9)
c9 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)

outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)

def apply_mask_to_image(image, mask, x, color):
    color_mask = (cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) * color).astype(np.uint8)

    transfromed_x = int((x / 473) * 256)
    print(transfromed_x)

    start_point = (transfromed_x, 0)    # (x, y) starting point of the line
    end_point = (transfromed_x, image.shape[0])  # (x, y) ending point of the line (height of the image)

    image_with_vertical_line = cv2.line(color_mask, start_point, end_point, (255, 0, 0), 2)
    
    result = cv2.addWeighted(image, 1, image_with_vertical_line, 0.3, 0)

    

    return result

def pick_random_numbers(start, end, x):
    # Create a set to store the picked numbers
    picked_numbers = set()

    # Generate x random numbers
    while len(picked_numbers) < x:
        # Generate a random number between start and end (both included)
        random_number = random.randint(start, end)

        # Add the number to the set
        picked_numbers.add(random_number)

    # Convert the set to a list and return it
    return list(picked_numbers)

def calculate_mean_variance(arr):
    if len(arr) < 2:
        return 0  # If the array has less than 2 elements, there is no variance.

    differences = [abs(arr[i] - arr[i + 1]) for i in range(len(arr) - 1)]
    mean_variance = sum(differences) / len(differences)

    return mean_variance

def get_95_percent_range(numbers_array):
    mean = np.mean(numbers_array)
    std_dev = np.std(numbers_array)

    # Z-score corresponding to the 95th percentile for a normal distribution
    z_score = 1.959963984540054

    lower_bound = mean - z_score * std_dev
    upper_bound = mean + z_score * std_dev

    return lower_bound, upper_bound

def delete_elements_by_index(base_array, indexes_to_delete):
    return [element for i, element in enumerate(base_array) if i not in indexes_to_delete]

def calculate_mean_contiguous_values(arr):
    if not arr:
        return 0

    contiguous_count = 1
    prev_value = arr[0]
    counts = []

    for i in range(1, len(arr)):
        if arr[i] == prev_value:
            contiguous_count += 1
        else:
            if contiguous_count > 1:
                counts.append(contiguous_count)
            contiguous_count = 1

        prev_value = arr[i]

    if contiguous_count > 1:
        counts.append(contiguous_count)

    mean_contiguous = sum(counts) / len(counts) if len(counts) > 0 else 0

    return mean_contiguous

def find_sequence_end_indexes(arr):
    increasing_indexes = []
    decreasing_indexes = []

    if len(arr) == 0:
        return increasing_indexes, decreasing_indexes

    current_sequence = arr[0]
    current_index = 0

    for i in range(1, len(arr)):
        if arr[i] != current_sequence:
            if current_sequence == "increasing":
                increasing_indexes.append(i - 1)
            else:
                decreasing_indexes.append(i - 1)
            current_sequence = arr[i]
            current_index = i

    # Append the last index, as the loop will not include it
    if current_sequence == "increasing":
        increasing_indexes.append(len(arr) - 1)
    else:
        decreasing_indexes.append(len(arr) - 1)

    return increasing_indexes, decreasing_indexes
