class VideoErrorException(Exception):
    def __init__(self, video_name):
        super().__init__(f"Video couldn't be proccesed: {video_name}")
        self.video_name = video_name