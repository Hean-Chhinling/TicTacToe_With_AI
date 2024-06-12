import pygame
import pickle
from tictactoe import TicTacToe, state_to_str
import time

pygame.init()

WIDTH, HEIGHT = 600, 700
LINE_WIDTH = 10
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
O_RADIUS = SQUARE_SIZE // 3
O_WIDTH = 15
X_WIDTH = 15
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
O_COLOR = (239, 231, 200)
X_COLOR = (84, 84, 84)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (50, 50, 50)
BUTTON_BG_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

with open("tic_tac_toe_agent.pkl", "rb") as f:
    ttt_agent = pickle.load(f)

with open("state_to_id.pkl", "rb") as f:
    state_to_id = pickle.load(f)

tic_tac_toe = TicTacToe()
default_font = pygame.font.Font(None, 36)
large_font = pygame.font.SysFont('Arial', 40)
button_font = pygame.font.Font(None, 50)
result_font = pygame.font.SysFont('Arial', 72, bold=True)

game_started = False
state = None
state_representation = None
is_done = False
result_text = ""


def draw_lines():
    """Draw grid of the Tic Tac Toe Board Game"""
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE),
                         (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0),
                         (row * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)


def draw_figures(game_state):
    """Draw the figure of the player X and O"""
    for row in range(1, BOARD_ROWS + 1):
        for col in range(1, BOARD_COLS + 1):
            if game_state['board'].get((row, col)) == 'X':
                pygame.draw.line(screen, X_COLOR,
                                 ((col - 1) * SQUARE_SIZE + SPACE, (row - 1) * SQUARE_SIZE + SPACE),
                                 ((col - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                                  (row - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 X_WIDTH)
                pygame.draw.line(screen, X_COLOR,
                                 ((col - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE, (row - 1) * SQUARE_SIZE + SPACE),
                                 ((col - 1) * SQUARE_SIZE + SPACE, (row - 1) * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 X_WIDTH)
            elif game_state['board'].get((row, col)) == 'O':
                pygame.draw.circle(screen, O_COLOR,
                                   ((col - 1) * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    (row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   O_RADIUS, O_WIDTH)


def draw_text(text, position, font=default_font, color=TEXT_COLOR):
    """Draw the given text to the screen on the given position"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)


def draw_button(text, position, size):
    """Return the drawing button to the screen"""
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, BUTTON_BG_COLOR, button_rect)
    text_surface = button_font.render(text, True, BUTTON_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect


def draw_bottom_bar():
    """Draw the white bar at the bottom of the scree"""
    pygame.draw.rect(screen, BUTTON_BG_COLOR, (0, HEIGHT - 100, WIDTH, 100))


def restart_game():
    """Reset the game and parameters to initial back"""
    global state, state_representation, is_done, result_text
    state = tic_tac_toe.initial
    state_representation = state_to_str(state)
    if state_representation not in state_to_id:
        state_to_id[state_representation] = len(state_to_id)
    is_done = False
    result_text = ""
    screen.fill(BG_COLOR)
    draw_lines()
    draw_bottom_bar()
    draw_button("Restart", (WIDTH // 2 - 75, HEIGHT - 80), (150, 50))
    pygame.display.update()

    # Agent takes the first turn
    agent_turn()


def agent_turn():
    """Agent take action and updating the game state"""
    global state, state_representation, is_done
    state_representation = state_to_str(state)
    if state_representation not in state_to_id:
        state_to_id[state_representation] = len(state_to_id)

    action = ttt_agent.act(state=state_to_id[state_representation], epsilon=0)
    action_tuple = ((action // 3) + 1, (action % 3) + 1)

    print(f"Agent action: {action}, action_tuple: {action_tuple}")
    if action_tuple in state['steps']:
        state = tic_tac_toe.take_step(action_tuple, state)
        draw_figures(state)
        pygame.display.update()
        print(f"Agent step: {action_tuple}, State after agent move: {state}")

        if tic_tac_toe.is_leaf(state):
            reward = tic_tac_toe.goodness(state, "X")
            is_done = True
            update_result_text(reward, "X")
            print("Game Over. Final Result: ",
                  "Agent win" if reward == 1 else "Agent lose" if reward == -1 else "Draw")
    else:
        print("Agent attempted illegal move, game over.")
        is_done = True

    # Add delay before human turn
    time.sleep(0.5)


def update_result_text(reward, player):
    """Update the result of the game text"""
    global result_text
    if reward == 1:
        result_text = "Agent wins!" if player == "X" else "You win!"
    elif reward == -1:
        result_text = "You win!" if player == "X" else "Agent wins!"
    else:
        result_text = "It's a draw"


def start_screen():
    """The beginning screen of the application"""
    screen.fill(BG_COLOR)
    draw_text("Welcome to TicTacToe Game", (WIDTH // 2, HEIGHT // 4), font=large_font)
    play_button = draw_button("Play", (WIDTH // 2 - 100, HEIGHT // 2 - 25), (200, 50))
    pygame.display.update()
    return play_button


def main():
    """Handling the entire graphical movements of the game in a higher level"""
    global state, state_representation, is_done, result_text, game_started
    state = tic_tac_toe.initial
    state_representation = state_to_str(state)
    if state_representation not in state_to_id:
        state_to_id[state_representation] = len(state_to_id)

    is_done = False
    result_text = ""
    game_started = False

    play_button = start_screen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if not game_started:
                    if play_button.collidepoint(mouse_x, mouse_y):
                        game_started = True
                        restart_game()
                else:
                    restart_button = draw_button("Restart", (WIDTH // 2 - 75, HEIGHT - 80), (150, 50))
                    if restart_button.collidepoint(mouse_x, mouse_y):
                        restart_game()
                    if not is_done:
                        clicked_row = mouse_y // SQUARE_SIZE
                        clicked_col = mouse_x // SQUARE_SIZE
                        human_step = (clicked_row + 1, clicked_col + 1)

                        if human_step in state['steps']:
                            state = tic_tac_toe.take_step(human_step, state)
                            draw_figures(state)
                            pygame.display.update()
                            print(f"Human step: {human_step}, State after human move: {state}")

                            if tic_tac_toe.is_leaf(state):
                                reward = tic_tac_toe.goodness(state, "O")
                                is_done = True
                                print("Game Over. Final Result: ",
                                      "You win" if reward == 1 else "You lose" if reward == -1 else "Draw")
                                update_result_text(reward, "O")
                                continue

                            # Agent's turn
                            time.sleep(0.8)
                            agent_turn()

            if event.type == pygame.KEYDOWN and game_started:
                if event.key == pygame.K_r:
                    restart_game()

        if game_started:
            screen.fill(BG_COLOR)
            draw_lines()
            draw_figures(state)
            draw_bottom_bar()
            draw_button("Restart", (WIDTH // 2 - 75, HEIGHT - 80), (150, 50))
            if is_done:
                draw_text(result_text, (WIDTH // 2, HEIGHT // 2), font=result_font)
        else:
            play_button = start_screen()
        pygame.display.update()


if __name__ == '__main__':
    main()
