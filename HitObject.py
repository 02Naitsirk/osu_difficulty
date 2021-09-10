class HitObject:
    def __init__(self, x: int, y: int, time: int, object_type: int, is_slider: bool):
        self.x = x
        self.y = y
        self.time = time
        self.object_type = object_type
        self.is_slider = is_slider
