from eye import Eye

class Default(Eye.State):
    pass


class Blinking(Eye.State):
    def __init__(self, value: int):
        self.value = value