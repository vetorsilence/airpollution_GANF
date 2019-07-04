from pyproj import Proj, transform

class Coord():
    def __init__(self,lat,long):
        self.lat = lat
        self.long = long

    def convertToPoint(self):
        in_proj = Proj(init='epsg:4326')
        out_proj = Proj(init='epsg:3857')
        x, y = transform(in_proj, out_proj, self.lat, self.long)
        return x, y