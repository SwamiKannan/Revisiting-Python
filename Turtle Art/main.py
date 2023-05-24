import turtle
from turtle import Screen
import random


def create_turt():
    tim1 = turtle.Turtle()
    # sc = Screen()
    # sc.exitonclick()
    TOTAL_ANGLE = 360
    screen = Screen()
    screen.colormode(255)

    tim1.speed('fastest')
    dict_name = {}
    return tim1, screen
    
def randomcolor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    
def random_walk():
    tim,screen=create_turt()
    for _ in range(200):
        tim.color((randomcolor()))
        tim.pensize(10)
        tim.forward(30)
        tim.speed(10.5)
        angle = random.choice((90, 180, 270, 360))
        tim.right(angle)
    return screen


def damien_hirst(interval, dot_size):
    tim,screen=create_turt()
    ht = screen.canvheight
    wt = screen.canvwidth
    for i in range(-ht, ht + interval, interval):
        for j in range(-wt, wt + interval, interval):
            tim.penup()
            tim.setposition(j, i)
            tim.pendown()
            tim.dot(dot_size, randomcolor())
    return screen


def spirograph(gap):
    tim,screen=create_turt()
    for _ in range(int(360 / gap)):
        tim.color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        tim.pendown()
        tim.circle(100)
        tim.penup()
        tim.setheading(tim.heading() + gap)
    return screen

for e, a in enumerate('abcdefghijklmnopqrstuvwxyz'):
    dict_name = {a: e}
prompt = input('Enter your name?\n')
sum = 0
for alphabet in prompt.lower():
    if alphabet in dict_name:
        sum += dict_name[alphabet] + 1
random.seed(sum)

type_of_art = input('What type of art would you like? Random_walk, Spirograph or damien_hirst?').lower()
if type_of_art == 'random_walk':
    screen=random_walk()
elif type_of_art == 'spirograph':
    space = int(input('How much space would you like between the circles?'))
    screen=spirograph(space)
elif type_of_art == 'damien_hirst':
    size = input('What size dots would you like?')
    screen=damien_hirst(50, int(size))
else:
    screen = Screen()
    print('Incorrect option')

screen.exitonclick()









