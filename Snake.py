from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 10
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FFC0CB"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, i*SPACE_SIZE])

        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

        print(f"original coordinates: {self.coordinates}")

class Food:
    def __init__(self):
        self.x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        self.y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE

        canvas.create_oval(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def next_turn(snake, food):
    global direction_changed_flag
    x, y = snake.coordinates[-1]

    if direction_changed_flag == True: verify_change_direction()

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # START drawing the new squares of the snake with new direction coordinates
    snake.coordinates.append([x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.append(square)
    # END drawing the new squares

    # START check for collision with food
    if x == food.x and y == food.y:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()

    else:

        # START deleting the last square of the snake
        del snake.coordinates[0]
        canvas.delete(snake.squares[0])
        del snake.squares[0]
        print(f"new coordinates: {snake.coordinates}")
        # END deleting the last quare of the snake
    # END check for collision with food

    if check_collision(snake):
        game_over()
    
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(user_input):
    global direction_changed_flag
    direction_changed_flag = True

    global new_direction
    new_direction = user_input

def verify_change_direction():
    global direction
    global direction_changed_flag
    
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

    direction_changed_flag = False

# Note: the x,y coordinates are of the top-left corner of the snake squares.
#       Therefor when the snake is travelling to the right or down, one
#       square of the snake will go off screen, allowing it to travel off
#       screen from the bottom and right sides of the window.
#       To prevent this we need to check the collision from the
#       x,y coordinates of the right corner or bottom corner of the square.
#       To do this we simply add SPACE_SIZE to the x and y coordintes respectively.
def check_collision(snake):
    x, y = snake.coordinates[-1]

    # START check for collision with the window
    if direction == "left" and x < 0:
        return True
    elif direction == "right" and x + SPACE_SIZE > GAME_WIDTH:
        return True
    elif direction == "up" and y < 0:
        return True
    elif direction == "down" and y + SPACE_SIZE > GAME_HEIGHT:
        return True
    # END check for collision with the window
    
    # START check for collision with itself
    for i, j in snake.coordinates[0:-1]:
        if x == i and y == j:
            return True
    # END check for collision with itself

def game_over():
    print("Game over :(")


window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = "down"
new_direction = "down"
direction_changed_flag = False

label = Label(window, text="Score: {}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# BEGIN reposition window to the center of the monitor
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
# END reposition window

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

snake = Snake()
food = Food()

# START defining the controls of the game
window.bind("<Left>", lambda event : change_direction("left"))
window.bind("<Right>", lambda event : change_direction("right"))
window.bind("<Up>", lambda event : change_direction("up"))
window.bind("<Down>", lambda event : change_direction("down"))
# END defining the controls

window.after(SPEED, next_turn, snake, food)

window.mainloop()