import pyproj as Proj, transform

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def convertToCoord(self):
        in_proj = Proj(init='epsg:3857')
        out_proj = Proj(init='epsg:4326')
        lat, long = transform(in_proj, out_proj, self.x, self.y)
        return lat, long


class Coord():
    def __init__(self,lat,long):
        self.lat = lat
        self.long = long

    def convertToPoint(self):
        in_proj = Proj(init='epsg:4326')
        out_proj = Proj(init='epsg:3857')
        x, y = transform(in_proj, out_proj, self.lat, self.long)
        return x, y

class Bounding_box():
    def __init__(self,id,dim,left_top,right_bottom):
        self.id = id
        self.dim = dim
        self.left_top = left_top
        self.right_bottom = right_bottom

class station():
    def __init__(self, id, type, location):
        self.id = id
        self.type = type
        self.location = location
    def isWithinBB(self, left_top,right_bottom):
        isWithin = False
        if(self.location.x > left_top.x and self.location.y < left_top.y):
            if(self.x < right_bottom.x and self.y > right_bottom.y):
                isWithin = True
        return isWithin




