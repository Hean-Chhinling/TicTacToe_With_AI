import pygame
import pickle
from tictactoe import TicTacToe, state_to_str
import time

pygame.init()

WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

with open("tic_tac_toe_agent.pkl", "rb") as f:
    ttt_agent = pickle.load(f)

with open("state_to_id.pkl", "rb") as f:
    state_to_id = pickle.load(f)

tic_tac_toe = TicTacToe()


def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures(state):
    for row in range(1, BOARD_ROWS + 1):
        for col in range(1, BOARD_COLS + 1):
            if state['board'].get((row, col)) == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 ((col - 1) * SQUARE_SIZE + SPACE, (row - 1) * SQUARE_SIZE + SPACE),
                                 ((col - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE, (row - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 ((col - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE, (row - 1) * SQUARE_SIZE + SPACE),
                                 ((col - 1) * SQUARE_SIZE + SPACE, (row - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
            elif state['board'].get((row, col)) == '0':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   ((col - 1) * SQUARE_SIZE + SQUARE_SIZE // 2, (row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)


def restart_game():
    global state, state_representation, is_done
    state = tic_tac_toe.initial
    state_representation = state_to_str(state)
    if state_representation not in state_to_id:
        state_to_id[state_representation] = len(state_to_id)
    is_done = False
    screen.fill(BG_COLOR)
    draw_lines()
    pygame.display.update()

    # Agent takes the first turn
    agent_turn()


def agent_turn():
    global state, state_representation, is_done
    state_representation = state_to_str(state)
    if state_representation not in state_to_id:
        state_to_id[state_representation] = len(state_to_id)

    action = ttt_agent.act(state=state_to_id[state_representation], epsilon=0)
    action_tuple = ((action // 3) + 1, (action % 3) + 1)

    # Debugging: Print action and check if it's legal
    print(f"Agent action: {action}, action_tuple: {action_tuple}")
    if action_tuple in state['steps']:
        state = tic_tac_toe.take_step(action_tuple, state)
        draw_figures(state)
        pygame.display.update()
        print(f"Agent step: {action_tuple}, State after agent move: {state}")

        if tic_tac_toe.is_leaf(state):
            reward = tic_tac_toe.goodness(state, "X")
            is_done = True
            print("Game Over. Final Result: ",
                  "Agent win" if reward == 1 else "Agent lose" if reward == -1 else "Draw")
    else:
        print("Agent attempted illegal move, game over.")
        is_done = True

    # Add delay before human turn
    time.sleep(0.5)


def main():
    global state, state_representation, is_done
    state = tic_tac_toe.initial
    state_representation = state_to_str(state)
    if state_representation not in state_to_id:
        state_to_id[state_representation] = len(state_to_id)

    is_done = False
    screen.fill(BG_COLOR)
    draw_lines()

    # Agent takes the first turn
    agent_turn()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not is_done:
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // SQUARE_SIZE
                clicked_col = mouse_x // SQUARE_SIZE
                human_step = (clicked_row + 1, clicked_col + 1)

                if human_step in state['steps']:
                    state = tic_tac_toe.take_step(human_step, state)
                    draw_figures(state)
                    pygame.display.update()
                    print(f"Human step: {human_step}, State after human move: {state}")

                    if tic_tac_toe.is_leaf(state):
                        reward = tic_tac_toe.goodness(state, "0")
                        is_done = True
                        print("Game Over. Final Result: ",
                              "You win" if reward == 1 else "You lose" if reward == -1 else "Draw")
                        continue

                    # Agent's turn
                    agent_turn()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()

        pygame.display.update()


if __name__ == '__main__':
    main()
