import turtle
import viewer_config as config

#paddle a
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("black")
paddle_a.shapesize(4,1)
paddle_a.penup()
paddle_a.goto(-350,0)


pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0,260)


#keyboard binding

class Display:(turtle)
    def __init__(self):
        self._arrowLength = config.maxArrowLength
        self._arrowWidth = config.arrowWidth
        self._onColour = config.onColour
        self._offColour = config.offColour 
        
        self.wn = turtle.Screen()
        self.wn.title(config.displayTitle)
        self.wn.bgcolor(config.bgColour)
        self.wn.setup(*config.screenSize)
        self.wn.tracer(0)


    def update(self):
        self.wn.update()


disp = Display()
while True:
    disp.update()
    