import gym
import sys
import time
import math
import random
import datetime
import numpy as np
import pygame as pg
from pygame.locals import *
from . import globals


class Pong(object):

    def run(self):
        pass

    def __init__(self):
        for key, value in globals.game:
            self.pong[key] = value
        for key, value in globals.DQN:
            self.dqn[key] = value

        self.playerScore = 0
        self.aiScore = 0

        self.ball['x'] = self.pong['BALL_XSTR']
        self.ball['y'] = self.pong['BALL_YSTR']
        self.ball['x_spd'] = self.pong['BALL_XSPD']
        self.ball['y_spd'] = random.uniform(-3, 3) * self.pong['WND_HEIGHT'] / 210

        self.ply_paddle = self.pong['PAD_START']
        self.ai_paddle = self.pong['PAD_START']

    def collision(self):
        angle = float(0)
        collision = False

        if ply_collision(ball=self.ball):
            angle = angle(self.ply_paddle, self.ball['y'])
            self.ball['y_spd'] = self.ball['x_spd'] * math.sin(angle) * 2
            collision = True
            player_hit = 1

            """
            if TRAINING:
                paddle_shift += 3
                paddle_shift_rate += 0.08
            """
        if ai_collision(ball=self.ball):
            angle = angle(self.ai_paddle, self.ball['y'])
            self.ball['y_spd'] = self.ball['x_spd'] * math.sin(angle) * -2
            collision = True
            computer_hit = 1

        if collision:
            self.ball['x_spd'] *= -1
            self.ball['x'] += 1

    def bounds(self, ball):
        if ball['y'] + ball['y_spd'] <= self.pong['SCOREBAR_HEIGHT'] - 1:
            ball['y'] += self.pong['SCOREBAR_HEIGHT'] - ball['y'] - ball['y_spd']
            ball['y_spd'] *= -1
        elif ball['y'] + (self.pong['BALL_SZ'] - 1) + ball['y_spd'] >= pong['WND_HEIGHT']:
            ball['y'] += (pong['WND_HEIGHT'] - (ball['y'] + self.pong['BALL_SZ'] - 1)) - ball['y_spd']
            ball['y_spd'] *= -1
        else:
            ball['y'] += ball['y_spd']

        if ball['x'] > self.pong['WND_WIDTH'] or ball['x'] < 0:
            ball_x = 0.5 * self.pong['WND_WIDTH']
            ball_y = (0.5 * (WND_HEIGHT - SCOREBAR_HEIGHT)) + SCOREBAR_HEIGHT
            ball_yspeed = random.uniform(-3,3)
        else:
            return

        if ball['x'] < 0:
            cpuScore += 1

        if (ball['x'] > self.pong['WND_WIDTH']):
            playerScore += 1

        ball(ball['x'],ball['y'])

    def quit(agent):
        # save the model
        filename = 'weights/pong_weights-' + \
            str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M")) \
            + '.h5'

        agent.save(filename)
        print('Saved pong weights as', filename)
        print('Exiting...')
        pg.quit()
        sys.exit()

    def angle(paddle_y, ball_y):
        y = 5 * ((ball_y - (paddle_y + (PADDLE_H / 2))) / PADDLE_H * .5)
        return y

    def ply_collion(ball):
        if ball['x'] + ball['x_spd'] > self.pong['PAD_W'] + self.pong['PLY_PAD_X'] - 1:
            return False
        if ball['y'] + ball['y_spd'] > self.pong['PAD_H'] + self.ply_paddle - 1:
            return False
        if ball['x'] + ball['x_spd'] + self.pong['BALL_SZ'] - 1 < self.pong['PLY_PAD_X']:
            return False
        if ball['y'] + ball['y_spd'] + self.pong['BALL_SZ'] - 1 < self.ply_paddle:
            return False
        return True

    def ai_collision(ball):
        if ball['x'] + ball['x_spd'] > self.pong['PAD_W'] + self.pong['AI_PAD_X'] - 1:
            return False
        if ball['y'] + ball['y_spd'] < self.pong['PAD_H'] + self.ai_paddle - 1:
            return False
        if ball['x'] + ball['x_spd'] + self.pong['BALL_SZ'] - 1 < self.pong['AI_PAD_X']:
            return False
        if ball['y'] + ball['y_spd'] + self.pong['BALL_SZ'] - 1 < self.ai_paddle:
            return False
        return True

# initialise the pygame module
pg.init()

# setting windows detail







# set up display size

# title
pg.display.set_caption("PongHackMT")
windowDisplay = pg.display.set_mode(pong['WND_WIDTH'], pong['WND_HEIGHT'], HWSURFACE | DOUBLEBUF | RESIZABLE)
clock = pg.time.Clock()

# Update and Display Score
if not True:
    cpuScoreDisplay = font.render(str(cpuScore), 1, WHITE)
    playerScoreDisplay = font.render(str(playerScore), 1, WHITE)
    windowDisplay.blit(cpuScoreDisplay, (WND_WIDTH*3/4, SCOREBAR_HEIGHT/2 - 10))
    windowDisplay.blit(playerScoreDisplay, (WND_WIDTH/4, SCOREBAR_HEIGHT/2 - 10))
# END Update and Display Score


paddleP_change = 0
paddleC_change = 0

paddle_shift=0
paddle_shift_rate=0.6


font = pg.font.SysFont("Courier New", 20, bold=True)


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

# game loop
while epoch < TOTAL_TICKS:

    # current reward for the match
    curr_reward = 0

    if epoch != 0 and epoch % 1000 == 0:
       print ('epoch:', epoch, 'mean: ', np.mean(mean),'e:', agent.epsilon)

    if not TRAINING:
        scoresLine = pg.draw.rect(windowDisplay, WHITE, (0, SCOREBAR_HEIGHT-1, WND_WIDTH, 2), 0)

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
    if paddleP_y + (paddleP_change+PADDLE_H) >= pong['WND_HEIGHT'] +paddle_speed or paddleP_y + (paddleP_change) <= SCOREBAR_HEIGHT:
        paddleP_change = 0
    if paddleC_y + (paddleC_change+PADDLE_H) >= WND_HEIGHT+paddle_speed or paddleC_y + (paddleC_change) <= SCOREBAR_HEIGHT:
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
