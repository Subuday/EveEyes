from main import Eye

class Blinking(Eye.State):
    def __init__(self, value: int):
        self.value = value