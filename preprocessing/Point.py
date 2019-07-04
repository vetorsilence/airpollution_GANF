from pyproj import Proj, transform

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def convertToCoord(self):
        in_proj = Proj(init='epsg:3857')
        out_proj = Proj(init='epsg:4326')
        lat, long = transform(in_proj, out_proj, self.x, self.y)
        return lat, long

    def isWithinBB(self, bb):
        isWithin = False
        if (self.x >= bb.left_top.x and self.y <= bb.left_top.y):
            if (self.x <= bb.right_bottom.x and self.y >= bb.right_bottom.y):
                isWithin = True
        return isWithin