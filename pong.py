import gym
import numpy as np
import pygame as pg
import datetime, time
import sys, random, math
from . import common
from pygame.locals import *

class Pong(object):
    def __init__(self):
        for key, value in common.GAME:
            self.game[key] = value
        for key, value in common.DQN:
            self.dqn[key] = value

        self.playerScore = 0
        self.aiScore = 0

    def run(self):
        pass

    def angleCalc(paddle_y, ball_y):
        y =  5 * ((ball_y - (paddle_y + (PADDLE_H / 2 ))) / PADDLE_H*.5 )
        return y




# initialise the pygame module
pg.init()

# setting windows detail







# set up display size
windowDisplay = pg.display.set_mode((game['WINDOW_WIDTH', game['WINDOW_HEIGHT'), HWSURFACE | DOUBLEBUF | RESIZABLE)

# title
pg.display.set_caption("PongHackMT")

clock = pg.time.Clock()

ball_img = pg.image.load('ball.png')
paddle1_img = pg.image.load('paddle.png')
paddle2_img = pg.image.load('paddle.png')

def paddle1(paddleP_x,paddleP_y):
        windowDisplay.blit(paddle1_img, (paddleP_x, paddleP_y))

def paddle2(paddleC_x,paddleC_y):
        windowDisplay.blit(paddle2_img, (paddleC_x, paddleC_y))

def ball(ball_x,ball_y):
        windowDisplay.blit(ball_img, (ball_x,ball_y))



## hard exits the game
def quit(agent):
    # save the model
    fn = 'weights/pong_weights-' + str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M")) \
         + '.h5'
    agent.save(fn)
    print('Saved pong weights as',fn)
    print('Exiting..')
    pg.quit()
    sys.exit()

paddleC_x = game['WINDOW_WIDTH'] - game['PADDLE_W' - 10
paddleP_x = 10
paddleP_y = (0.5*(WINDOW_HEIGHT-SCORE_BAR_HEIGHT))+SCORE_BAR_HEIGHT
paddleC_y = paddleP_y
paddleP_change = 0
paddleC_change = 0
ball_x = 0.5 * WINDOW_WIDTH
ball_y = (0.5 * (WINDOW_HEIGHT-SCORE_BAR_HEIGHT))+SCORE_BAR_HEIGHT
ball_xspeed = WINDOW_WIDTH/160
ball_yspeed = random.uniform(-3,3)*WINDOW_HEIGHT/210

paddle_shift=0
paddle_shift_rate=0.6


myFont = pg.font.SysFont("Courier New", 20, bold=True)


# instantiate the Deep Q Neural Agent

agent = DQNAgent(state_size, action_size)

# kinda large
batch_size = 1000

# total rewards throughout the lifetime of the game
total_reward = 0

# how many clocks until exit
epoch = 0
TOTAL_TICKS = 300000

# flag for training mode
TRAINING = False

# deque for the mean of the rewards measured in the matches
mean = deque(maxlen=10000)

print('hackmt pong ai: Training Mode', TRAINING)

# game loop
while epoch < TOTAL_TICKS:

    # current reward for the match
    curr_reward = 0

    if epoch != 0 and epoch % 1000 == 0:
       print ('epoch:', epoch, 'mean: ', np.mean(mean),'e:', agent.epsilon)

    if not TRAINING:
        scoresLine = pg.draw.rect(windowDisplay, WHITE, (0, SCORE_BAR_HEIGHT-1, WINDOW_WIDTH, 2), 0)

    while ball_yspeed == 0:
            ball_yspeed = random.uniform(-3,3)


    state = np.array([paddleP_y,paddleP_change, paddleC_y, paddleC_change,
                        ball_x, ball_y, ball_xspeed, ball_yspeed])
    state = np.reshape(state, [1, state_size])
    action = agent.act(state)

    if action == 0:
        paddleC_change = - (paddle_speed)
    # down
    if action == 2:
        paddleC_change = (paddle_speed)

    done = ball_x<0
    if done:
        print('computer scored')


    #Paddle Movement
    for event in pg.event.get():
        if event.type == QUIT:
            quit(agent)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit(agent)
            if event.key == pg.K_UP:
                paddleP_change = - (paddle_speed)
            if event.key == pg.K_DOWN:
                paddleP_change = (paddle_speed)
            if event.key == pg.K_w:
                paddleC_change = - (paddle_speed)
            if event.key == pg.K_s:
                paddleC_change = (paddle_speed)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                paddleP_change = 0
            if event.key == pg.K_w or event.key == pg.K_s:
                paddleC_change = 0

    #randomize left side level
    if paddle_shift_rate >= 1:
        paddle_shift_rate -= 0.7
    if paddle_shift > PADDLE_H:
        paddle_shift_rate -= PADDLE_H

    if paddleP_y + paddle_shift > ball_y + 0.5 * BALL_SIZE:
        paddleP_change = -paddle_shift_rate * (paddle_speed)
    else:
        paddleP_change = paddle_shift_rate * (paddle_speed)


    # bounding box for the paddles
    if paddleP_y + (paddleP_change+PADDLE_H) >= game['WINDOW_HEIGHT'] +paddle_speed or paddleP_y + (paddleP_change) <= SCORE_BAR_HEIGHT:
        paddleP_change = 0
    if paddleC_y + (paddleC_change+PADDLE_H) >= WINDOW_HEIGHT+paddle_speed or paddleC_y + (paddleC_change) <= SCORE_BAR_HEIGHT:
        paddleC_change = 0
    #END Paddle Movement


    #Ball Movement
    paddleP_y += paddleP_change
    paddleC_y += paddleC_change
    ball_x += ball_xspeed

    if not TRAINING:
        pg.display.update()
        windowDisplay.fill(BLACK)

    paddle1(paddleP_x,paddleP_y)
    paddle2(paddleC_x,paddleC_y)
    #END Ball Movement


    # Ball/Paddle Collision
    #Player Paddle
    if ball_x + ball_xspeed <= paddleP_x + PADDLE_W - 1 and ball_x + BALL_SIZE - 1 + ball_xspeed >= paddleP_x:
        if ball_y + ball_yspeed <= paddleP_y + PADDLE_H - 1 and ball_y + BALL_SIZE - 1 + ball_yspeed >= paddleP_y:
            ball_x +=1
            ball_xspeed *= -1
            angle = angleCalc(paddleP_y, ball_y)
            ball_yspeed = ball_xspeed * math.sin(angle)*2
            player_hit = 1

            if TRAINING:
                paddle_shift += 3
                paddle_shift_rate += 0.08

    # CPU paddle
    if BALL_X + ball_xspeed <= paddleC_x + PADDLE_W - 1 and ball_x + BALL_SIZE - 1 + ball_xspeed >= paddleC_x:
        if ball_y + ball_yspeed <= paddleC_y + PADDLE_H - 1 and ball_y + BALL_SIZE - 1 + ball_yspeed >= paddleC_y:
            ball_x -= 1
            ball_xspeed *= -1
            angle = angleCalc(paddleC_y, ball_y)
            ball_yspeed = ball_xspeed * math.sin(angle) *-2
            computer_hit = 1

            # advance the current reward to 1
            #curr_reward = 1
    # END Ball/Paddle Collision


    # Ball Out of Bounds
    # If Player Loses
    if (ball_x<0):

        # reset the position of the player paddle
        ball_x = 0.5 * WINDOW_WIDTH
        ball_y = (0.5 * (WINDOW_HEIGHT-SCORE_BAR_HEIGHT))+SCORE_BAR_HEIGHT
        ball_yspeed = random.uniform(-3,3)
        cpuScore += 1   # increase the scoreboard

    # If CPU Loses
    if (ball_x>WINDOW_WIDTH):

        # reset the position of the cpu paddle
        ball_x = 0.5 * WINDOW_WIDTH
        ball_y = (0.5 * (WINDOW_HEIGHT-SCORE_BAR_HEIGHT))+SCORE_BAR_HEIGHT
        ball_yspeed = random.uniform(-3,3)
        playerScore += 1    # increase the scoreboard

    # exit the match
    #if not TRAINING and playerScore == 20:
    #    pg.quit()
    #    sys.exit()
    # END Ball Out of Bounds



    # Ball Vertical Limit
    if ball_y  + ball_yspeed <= SCORE_BAR_HEIGHT - 1:
        ball_y += (SCORE_BAR_HEIGHT-ball_y)-ball_yspeed
        ball_yspeed = -1* ball_yspeed
    elif ball_y + (BALL_SIZE-1) +ball_yspeed >= WINDOW_HEIGHT:
        ball_y += (WINDOW_HEIGHT-(ball_y+BALL_SIZE-1))-ball_yspeed
        ball_yspeed = -1* ball_yspeed
    else:
        ball_y += ball_yspeed
    #END Ball Vertical Limit

    # set the coordinated of the ball
    ball(ball_x,ball_y)

    # Update and Display Score
    if not game[]:
        cpuScoreDisplay = myFont.render(str(cpuScore), 1, WHITE)
        playerScoreDisplay = myFont.render(str(playerScore), 1, WHITE)
        windowDisplay.blit(cpuScoreDisplay, (WINDOW_WIDTH*3/4, SCORE_BAR_HEIGHT/2 - 10))
        windowDisplay.blit(playerScoreDisplay, (WINDOW_WIDTH/4, SCORE_BAR_HEIGHT/2 - 10))
    # END Update and Display Score

    if not TRAINING:
        clock.tick(30)

    if (np.abs(ball_y - paddleC_y) > 25):
        curr_reward = -1

    next_state = np.array([paddleP_y,paddleP_change, paddleC_y, paddleC_change,
                        ball_x, ball_y, ball_xspeed, ball_yspeed])
    next_state = np.reshape(state, [1, state_size])
    agent.remember(state, action, curr_reward, next_state, done)

    if len(agent.memory) > batch_size:
        agent.replay(batch_size)

    # append the current reward value to the mean deque
    mean.append(curr_reward)
    epoch+=1     # reduce the game ticker down one

quit(agent)
