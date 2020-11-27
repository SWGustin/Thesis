import math 

class ArPEl:
    def __init__(self):
        self._base_chord = 0
        self._tip_chord = 0
        self._span = 0
        self._leading_angle = 0
        self._pel_spacing = float('inf')
        self._geometry = []
        self._pels = [[]]

    @property
    def geometry(self):
        return self._geometry

    # @geometry.setter
    # def geometry(self,points):
    #     self._geometry = [[(x,y) for x,y in point ]for point in points]
        
    @geometry.setter
    def geometry(self, values):
        try:
            base_chord, tip_chord, span, leading_angle = values
        except ValueError:
            raise ValueError("Pass all required values")
        self._geometry = [(0,0)]
        self._geometry.append((span, span*math.tan(math.radians(leading_angle))))
        self._geometry.append((span,self._geometry[1][1]+tip_chord))
        self._geometry.append((0,base_chord))

    #TODO: add unadded setters and calculate array of pels
