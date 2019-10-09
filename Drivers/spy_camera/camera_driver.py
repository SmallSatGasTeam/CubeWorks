from Drivers.Driver import Driver


class SpyCamera(Driver):
    def __init__(self):
        super().__init__("Camera")
        self.latest_picture = "/path/to/file"

    def read(self):
        return self.latest_picture

    def take_picture(self):
        # TODO: Code to operate the PiCamera to take a picture
        self.latest_picture = "/path/to/new/picture"
