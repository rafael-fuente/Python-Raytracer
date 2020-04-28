class PointLight:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        
        
class DirectionalLight:
    def __init__(self, Ldir, color):
        self.Ldir = Ldir
        self.color = color
