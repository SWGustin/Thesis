import turtle
import os
import json

# disp = turtle.Screen()
# disp.title("ArPEl")
# disp.bgcolor("white")
# disp.setup(width = 800, height= 600)
# disp.tracer(0)

class ArPEl():
    def __init__(self, file_name):
        path = os.getcwd() +'\\software\\MVC\\Model\\'+file_name
        with open(path, 'r') as f:
            geometry = json.loads(f.read())
        

test = ArPEl("Planar_geometry.json")




# #paddle a
# paddle_a = turtle.Turtle()
# paddle_a.speed(0)
# paddle_a.shape("square")
# paddle_a.color("white")
# paddle_a.shapesize(4,1)
# paddle_a.penup()
# paddle_a.goto(-350,0)

# #paddle b
# paddle_b = turtle.Turtle()
# paddle_b.speed(0)
# paddle_b.shape("square")
# paddle_b.color("white")
# paddle_b.shapesize(4,1)
# paddle_b.penup()
# paddle_b.goto(350,0)

# #ball
# ball = turtle.Turtle()
# ball.speed(0)
# ball.shape("square")
# ball.color("white")
# ball.penup()
# ball.goto(0,0)
# ball.dx = 1
# ball.dy = 1


# #score
# score_A = 0
# score_B = 0

# pen = turtle.Turtle()
# pen.speed(0)
# pen.color('white')
# pen.penup()
# pen.hideturtle()
# pen.goto(0,260)

# def paddle_up_a():
#     _y = paddle_a.ycor()
#     _y += 40
#     paddle_a.sety(_y)

# def paddle_dwn_a():
#     _y = paddle_a.ycor()
#     _y -= 40
#     paddle_a.sety(_y)

# def paddle_up_b():
#     _y = paddle_b.ycor()
#     _y += 40
#     paddle_b.sety(_y)

# def paddle_dwn_b(): 
#     _y = paddle_b.ycor()
#     _y -= 40
#     paddle_b.sety(_y)

# #keyboard binding

# wn.listen()
# wn.onkeypress(paddle_up_a, "w")
# wn.onkeypress(paddle_dwn_a, "s")
# wn.onkeypress(paddle_up_b,'Up')
# wn.onkeypress(paddle_dwn_b, "Down")
#main game loop

# while True:
#     disp.update()   
#     # ball.setx(ball.xcor()+ball.dx)
    # ball.sety(ball.ycor()+ball.dy)

    #border checking
    # if ball.ycor() >290 or ball.ycor() < -290 :
    #     ball.dy *= -1

    # if (ball.xcor() == paddle_a.xcor()+10 and abs(ball.ycor()-paddle_a.ycor())<=40) or \
    #     (ball.xcor() == paddle_b.xcor()-10 and abs(ball.ycor()-paddle_b.ycor())<=40):
    #     ball.dx *= -1

    # if ball.xcor() > paddle_b.xcor():
    #     pen.clear()
    #     pen.write(f"player A: {score_A}  player B: {score_B}", align= 'center', font = ('courier', 24, 'bold') )    
    #     score_A +=1
    #     ball.setx(0)
    #     ball.sety(0)

    # if ball.xcor() < paddle_a.xcor():
    #     score_B +=1
    #     pen.clear()
    #     pen.write(f"player A: {score_A}  player B: {score_B}", align= 'center', font = ('courier', 24, 'bold') )
    #     ball.setx(0)
    #     ball.sety(0)    