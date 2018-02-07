game = {
    'TRAINING': True,

    'WND_WIDTH': 500,
    'WND_HEIGHT': 500,
    'SCOREBAR_HEIGHT': 30,

    # colors
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),

    # game objects
    'BALL_SZ': 9,
    'PAD_H': 45,
    'PAD_W': 15
}

game['BALL_XSPD'] = game['WND_WIDTH'] / 160
game['BALL_XSTR'] = 0.5 * game['WND_WIDTH']
game['BALL_YSTR'] = 0.5 * (game['WND_HEIGHT'] - game['SCOREBAR_HEIGHT']) + SCOREBAR_HEIGHT

game['PAD_SPEED'] = game['WINDOW_HEIGHT'] / 105
game['PAD_START'] = (game['WND_WIDTH'] - game['SCOREBAR_HEIGHT']) / 2

game['AI_PAD_X'] = game['WND_WIDTH'] - game['PADDLE_W'] - 10
game['PLY_PAD_X'] = 10

DQN = {
    'STATE_SIZE': 8,
    'ACT_SIZE': 3
}
