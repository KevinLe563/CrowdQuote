class PersonObject():
    def __init__(self, id, centroid):
        # coords = (x1, y1, x2, y2)
        self.objectID = id
        self.centroids = [centroid]
        self.is_counted = False