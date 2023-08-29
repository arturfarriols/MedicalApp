from . segmentation_model import *
from . model_pytorch import *
from . segmentation_model_pytorch import *
from . video import *
from . utils import *
from . qt_thread import *

from . import calculate_health_indicators as CHI

# Backend controller class
class ModelController:
    def __init__(self, window):
        self.processing_videos = False
        self.thread = None
        self.upper_segmentation_model = None #Model(upper_model_path)
        self.lower_segmentation_model = None #Model(lower_model_path)
        self.window = window
        # self.initiate_models()

    def initiate_models(self):
        self.upper_segmentation_model = Model("upper", upper_model_path, BATCH_SIZE)
        self.lower_segmentation_model = Model("lower", lower_model_path, BATCH_SIZE)

    def initialize_thread_processing(self, videos):
        if not self.processing_videos:
            self.processing_videos = True
            self.thread = FunctionThread(self, videos)
            self.thread.status_changed.connect(self.handle_status_changed)
            self.thread.start()

    def handle_status_changed(self, status):
        # Handle the status value here
        print("Received status:", status)

    def final_process_videos(self, videos):
        amount_of_videos = len(videos)
        status = "Ok"

        for video in videos:
            res = self.final_process_video(video)

    def final_process_video(self, video):
        preprocessed_images = video.preprocess_video()

    def process_videos(self, videos):
        amount_of_frames_processed = 0
        amount_of_frames = 0
        status = "Ok"

        for video in videos:
            status, frames = video.get_number_of_frames()
            amount_of_frames += frames
            if status != "Ok":
                break
        
        if status == "Ok":

            for video in videos:
                previous_amount_of_frames_processed = amount_of_frames_processed
                amount_of_frames_processed = self.process_video(video, amount_of_frames_processed, amount_of_frames)

                if amount_of_frames_processed == -1:
                    status = f"Can't process video + {video.path}"
                    break
                elif amount_of_frames_processed == -2:
                    status = f"Execution interrupted"
                    break

            self.window.actualize_percentage(100)

        self.processing_videos = False
        
        return status

    def process_video(self, video, amount_of_frames_processed, total_amount_of_frames):
        status, frames = video.get_cropped_frames()
        is_automatic = video.is_automatic

        if is_automatic == False:
            x = video.point.x()
        else:
            x = None
        print("X is: ", x)

        if status == "Ok":
            preprocessed_images = self.lower_segmentation_model.preprocess_images(frames)
            batches = self.lower_segmentation_model.generate_batches(preprocessed_images)
            batch_size = len(batches[0])

            results = np.zeros((len(frames), 6))

            # auxiliar_results = []
            
            lower_points = []
            upper_points = []

            for i, batch in enumerate(batches):
                if self.thread._stop_execution:
                    return -2
                # print('batch dims:', np.shape(batch))
                print(i)
                lower_masks = self.lower_segmentation_model.perform_inference(batch)
                upper_masks = self.upper_segmentation_model.perform_inference(batch)
                # auxiliar_results.append(lower_masks)

                batch_lower_points = self.lower_segmentation_model.analyze_predictions(lower_masks, x)
                batch_upper_points = self.upper_segmentation_model.analyze_predictions(upper_masks, x)

                batch_lower_points = batch_lower_points.reshape(-1, 2)
                batch_upper_points = batch_upper_points.reshape(-1, 2)

                print(np.shape(batch_lower_points))
                # print(batch_lower_points)

                if i == 0:
                    lower_points = batch_lower_points
                    upper_points = batch_upper_points
                else:
                    lower_points = np.concatenate((lower_points, batch_lower_points), axis=0)
                    upper_points = np.concatenate((upper_points, batch_upper_points), axis=0)


                current_percentage = int(((i * batch_size + amount_of_frames_processed) / total_amount_of_frames) * 100)
                self.window.actualize_percentage(current_percentage)
                # for i in range(len(lower_masks)):
                #     img = apply_mask_to_image(batch[i], np.squeeze(lower_masks[i]), x, (255, 255, 0))
                #     print(batch_lower_points[i])
                #     cv2.imshow('result', img)
                #     cv2.waitKey(0)
                #     cv2.destroyAllWindows()

            amount_of_frames_processed = batch_size * len(batches)

            print(len(lower_points))
            print(len(upper_points))
            print("SHAPE", np.shape(np.array(lower_points)))

            self.process_points(lower_points, upper_points, amount_of_frames_processed)


            processed_results = results

            # self.window.actualize_results_table(processed_results, video)
            
            return amount_of_frames_processed
        
        return -1 
    

    def process_points(self, lower_points, upper_points, amount_of_frames_processed):
        points = self.delete_outlayers(lower_points, upper_points)
        # print("POINTS", points)
        lower = [subarray[0][1] for subarray in points]
        # upper = [subarray[1][0] for subarray in points]

        cycle = self.analyze_cardiac_cycle(lower)
        mean_contioguous_values = calculate_mean_contiguous_values(cycle)
        bpm = int((amount_of_frames_processed / (mean_contioguous_values * 2)) * 12)
        print("mean_contioguous_values", mean_contioguous_values)
        print("bpm", bpm)

        increasing_indexes, decreasing_indexes = find_sequence_end_indexes(cycle)

        self.get_indexes(points, increasing_indexes, decreasing_indexes, bpm)

        # for i in increasing_indexes:
        #     print(cycle[i])
        # print("")
        # for i in decreasing_indexes:
        #     print(cycle[i])

        # for i, p in enumerate(points):
        #     print(p, cycle[i])

    def delete_outlayers(self, lower_points, upper_points):
        filtered_points = []
        size = len(lower_points)

        # print(lower_points)

        for i in range(size):
            lower_point = lower_points[i]
            upper_point = upper_points[i]

            if np.isnan(lower_point).any() or np.isnan(upper_point).any():
                continue

            filtered_points.append([lower_point, lower_point, i])

        lower = [subarray[0][1] for subarray in filtered_points]
        upper = [subarray[1][0] for subarray in filtered_points]

        # print(lower)
        lower_threshold = round(calculate_mean_variance(lower)) + DISTANCE_THRESHOLD
        upper_threshold = round(calculate_mean_variance(upper)) + DISTANCE_THRESHOLD
        lower_lower_bound, lower_upper_bound = get_95_percent_range(lower)
        upper_lower_bound, upper_upper_bound = get_95_percent_range(upper)

        print(lower_lower_bound, lower_upper_bound)
        print(upper_lower_bound, upper_upper_bound)
        indexes_to_exclude = []
        previous_was_deleted = False

        for i in range(1, len(lower)):
            if not previous_was_deleted:
                if abs(lower[i] - lower[i - 1]) > lower_threshold or abs(upper[i] - upper[i - 1]) > upper_threshold:
                    indexes_to_exclude.append(i)
                    previous_was_deleted = True
                else:
                    previous_was_deleted = False
            else:
                if lower_lower_bound < lower[i] < lower_upper_bound and upper_lower_bound < upper[i] < upper_upper_bound:
                    previous_was_deleted = False
                else:
                   indexes_to_exclude.append(i) 

        # print("filtered_points", len(filtered_points))
        # print("indexes_to_exclude", len(indexes_to_exclude))
        for i in range(len(indexes_to_exclude)):
            print(lower[indexes_to_exclude[i]])
        # filtered_points = delete_elements_by_index(filtered_points, indexes_to_exclude)
        # print("filtered_points", len(filtered_points))

        # print("calculate_mean_variance", calculate_mean_variance(lower))

        return filtered_points
    
    def get_means(self, points, increasing_indexes, decreasing_indexes):
        lower_increasing_distances = []
        upper_increasing_distances = []
        medium_increasing_distances = []

        lower_decreasing_distances = []
        upper_decreasing_distances = []
        medium_decreasing_distances = []

        for index in increasing_indexes:
            print("point", points[index])
            lower_distance = abs(points[index][0][0] - points[index][0][1])
            upper_distance = abs(points[index][1][0] - points[index][1][1])
            medium_distance = abs(points[index][0][1] - points[index][1][0])

            lower_increasing_distances.append(lower_distance)
            upper_increasing_distances.append(upper_distance)
            medium_increasing_distances.append(medium_distance)
            print("lower_distance", lower_distance)

        print("")
        lower_increasing_mean = np.mean(np.array(lower_increasing_distances))
        upper_increasing_mean = np.mean(np.array(upper_increasing_distances))
        medium_increasing_mean = np.mean(np.array(medium_increasing_distances))

        for index in decreasing_indexes:
            print("point", points[index])
            lower_distance = abs(points[index][0][0] - points[index][0][1])
            upper_distance = abs(points[index][1][0] - points[index][1][1])
            medium_distance = abs(points[index][0][1] - points[index][1][0])

            lower_decreasing_distances.append(lower_distance)
            upper_decreasing_distances.append(upper_distance)
            medium_decreasing_distances.append(medium_distance)
            print("lower_distance", lower_distance)

        lower_decreasing_mean = np.mean(np.array(lower_decreasing_distances))
        upper_decreasing_mean = np.mean(np.array(upper_decreasing_distances))
        medium_decreasing_mean = np.mean(np.array(medium_decreasing_distances))

        print("increasing mean", np.mean(np.array(lower_increasing_distances)))
        print("decreasing mean", np.mean(np.array(lower_decreasing_distances)))

        means = [lower_increasing_mean, upper_increasing_mean, medium_increasing_mean, lower_decreasing_mean, upper_decreasing_mean, medium_decreasing_mean]

        print("means shape", np.shape(means))

        return means
    
    def get_indexes(self, points, increasing_indexes, decreasing_indexes, bpm):
        means = self.get_means(points, increasing_indexes, decreasing_indexes)
        # means *= 0.03 

        health_indicators = CHI.calculateAll(means[1], means[4], means[2], means[5], means[0], means[3], bpm)

        
    def filter_first_points(lower_points, upper_points):
        results = []

        distance1 = abs(lower_points[0][0] - lower_points[1][0])
        distance2 = abs(lower_points[0][0] - lower_points[2][0])
        distance3 = abs(lower_points[0][1] - lower_points[1][1])
        distance4 = abs(lower_points[0][1] - lower_points[2][1])

        if distance1 < DISTANCE_THRESHOLD and distance2 < DISTANCE_THRESHOLD and distance3 < DISTANCE_THRESHOLD and distance4  < DISTANCE_THRESHOLD:
            included = [0, 1, 2]
        elif distance1 >= DISTANCE_THRESHOLD or distance3 >= DISTANCE_THRESHOLD and (distance2 < DISTANCE_THRESHOLD and distance4  < DISTANCE_THRESHOLD) and (abs(distance1 - distance2) > DISTANCE_THRESHOLD / 2 and abs(distance3 - distance4) / 2 > DISTANCE_THRESHOLD):
            included = [0, 2]
        elif distance2 >= DISTANCE_THRESHOLD or distance4 >= DISTANCE_THRESHOLD and (distance1 < DISTANCE_THRESHOLD and distance3  < DISTANCE_THRESHOLD) and (abs(distance1 - distance2) > DISTANCE_THRESHOLD / 2 and abs(distance3 - distance4) / 2 > DISTANCE_THRESHOLD):
            included = [0, 1]
        elif abs(distance1 - distance2) < DISTANCE_THRESHOLD and abs(distance3 - distance4) < DISTANCE_THRESHOLD:
                included = [1, 2]
        else:
            return []
        
        distance1 = abs(upper_points[0][0] - upper_points[1][0])
        distance2 = abs(upper_points[0][0] - upper_points[2][0])
        distance3 = abs(upper_points[0][1] - upper_points[1][1])
        distance4 = abs(upper_points[0][1] - upper_points[2][1])

        print(abs(distance1 - distance2))
        print(abs(distance1 - distance2) > DISTANCE_THRESHOLD / 2)

        if distance1 < DISTANCE_THRESHOLD and distance2 < DISTANCE_THRESHOLD and distance3 < DISTANCE_THRESHOLD and distance4  < DISTANCE_THRESHOLD:
            included = included
        elif (distance1 >= DISTANCE_THRESHOLD or distance3 >= DISTANCE_THRESHOLD) and (distance2 < DISTANCE_THRESHOLD and distance4  < DISTANCE_THRESHOLD) and (abs(distance1 - distance2) > DISTANCE_THRESHOLD / 2 and abs(distance3 - distance4) / 2 > DISTANCE_THRESHOLD):
            included = [element for element in included if element != 1]
        elif (distance2 >= DISTANCE_THRESHOLD or distance4 >= DISTANCE_THRESHOLD) and (distance1 < DISTANCE_THRESHOLD and distance3  < DISTANCE_THRESHOLD) and (abs(distance1 - distance2) > DISTANCE_THRESHOLD / 2 and abs(distance3 - distance4) / 2 > DISTANCE_THRESHOLD):
            print('babazinga')        
            included = [element for element in included if element != 2]
        elif abs(distance1 - distance2) < DISTANCE_THRESHOLD and abs(distance3 - distance4) < DISTANCE_THRESHOLD:
                print(distance2)
                print(distance2 >= DISTANCE_THRESHOLD or distance4 >= DISTANCE_THRESHOLD)
                print('babazinga')
                included = [element for element in included if element != 0]
        else:
            return []  
        
        if len(included) == 1:
            included = []

        for i in included:
            results.append([lower_points[i], upper_points[i]])

        return results


    def analyze_cardiac_cycle(self, array):
        result = []
        for i in range(len(array)):
            if i == 0:
                if array[i] > array[i + 1]:
                    result.append("decreasing")
                else:
                    result.append("increasing")
            elif array[i] > array[i - 1]:
                result.append("increasing")
            elif array[i] < array[i - 1]:
                result.append("decreasing")
            else:
                result.append(result[i - 1])
        return result




    def button1_function(self):
        if not self.processing_videos:
            self.processing_videos = True
            self.thread = None #Expensive function
            self.thread.start()

    def button2_function(self):
        self.processing_videos = False
        if self.thread is not None:
            self.thread.stop_execution()