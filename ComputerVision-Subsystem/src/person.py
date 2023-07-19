class PersonObject():
    def __init__(self, coords, id):
        # coords = (x1, y1, x2, y2)
        self.bounding_box = coords
        self.id = id

    def set_bounding_box(self, coords):
        self.bounding_box = coords