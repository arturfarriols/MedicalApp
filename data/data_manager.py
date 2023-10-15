import sys
import csv
import pandas as pd
import openpyxl
from enum import EnumType  
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

from qt_core import *

# from models import health_indicators_utils as HIUtils

from .export_formats_enum import ExportFormats
from models.video.video_formats_enum import VideoFormats

from exceptions.exceptions_core import *

class DataManager:
    def __init__(self):
        pass

    def export_data(self, data):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            # self,
            QWidget(),
            "Export Data",
            "",
            "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)",
            options=options,
        )

        if file_name:
            # data = [["Name", "Age", "City"], ["Alice", "25", "New York"], ["Bob", "30", "Los Angeles"]]
            file_format = ExportFormats.CSV if file_name.endswith(".csv") else ExportFormats.EXCEL

            if file_format == ExportFormats.CSV:
                # Open a CSV file for writing
                with open(file_name, mode="w", newline="") as file:
                    writer = csv.writer(file)

                    # Get the header from the keys of the dictionary
                    header = ["Video name"] + list(data[0][0].keys())
                    
                    # Write the header to the CSV file
                    writer.writerow(header)
                    
                    # Write the data rows to the CSV file
                    for item in data:
                        row = [str(item[1].get_file_name())] + [item[0][key] for key in header[1:]] # Adding the video.path
                        writer.writerow(row)

            elif file_format == ExportFormats.EXCEL:
                self._generate_excel_from_dict(data, file_name)
                # df = pd.DataFrame()

                # # Iterate through each element in the data_structure
                # for item in data:
                #     # Convert the dictionary (item[0]) to a DataFrame
                #     item_df = pd.DataFrame(item[0])
                #     # Add a 'Video name' column containing the video path
                #     item_df['Video name'] = item[1].get_file_name()
                #     # Append this DataFrame as a new row in the main DataFrame
                #     df = pd.concat([df, item_df], ignore_index=True)

                # # Reorder the columns to have 'Video name' as the first column
                # df = df[['Video name'] + list(df.columns[:-1])]

                # # Save the DataFrame to an Excel file
                # df.to_excel(file_name, index=False)     

    def import_video(self):
        options = QFileDialog.Options()
        video_path, _ = QFileDialog.getOpenFileName(QWidget(), "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        print("VIDEO PATH", video_path)
        video_extension = video_path.split('.')[-1].lower()
        is_valid = self._check_valid_format(video_extension, VideoFormats)

        if not is_valid and video_path != "":
            video_formats = [member.value for member in VideoFormats]
            video_formats = ", ".join(video_formats)
            raise InvalidDataException(RT.VIDEO.value, video_formats)

        return video_path


    def _check_valid_format(self, data, valid_formats):
        is_valid = False
        print("DATA", data)

        for member in valid_formats:
            print(member.value)
        print(type(valid_formats))
        print(isinstance(valid_formats, EnumType))

        if isinstance(valid_formats, EnumType):
            is_valid = any(member.value == data for member in valid_formats)
            print("is_valid Enum Format", is_valid)
        elif isinstance(valid_formats, list):
            is_valid = data in valid_formats
            print("is_valid List Format", is_valid)

        return is_valid

    # Function to generate an Excel file from a dictionary
    def _generate_excel_from_dict(self, data, file_name):
        # Create a new Excel workbook
        workbook = openpyxl.Workbook()
        
        # Create a new Excel sheet
        sheet = workbook.active
        sheet.title = "Data"
        
        # Get the header from the keys of the dictionary
        header = ["Video name"] + list(data[0][0].keys())
        
        # Write the header to the Excel sheet
        sheet.append(header)
        
        # Write the data rows to the Excel sheet
        for item in data:
            row = [str(item[1].get_file_name())] + [item[0][key] for key in header[1:]]  # Adding the video.path
            sheet.append(row)

        # Save the Excel workbook to a file
        workbook.save(file_name)