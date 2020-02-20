import pygame
import Connect4Board

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def connect4():
    # setup
    board = Connect4Board.GameBoard()
    winner = 0
    screen = pygame.display.set_mode((700, 600))
    curr_player = 1
    screen.fill(WHITE)
    # The you can draw different shapes and lines or add text to your background stage.
    spaces = []
    for i in range(7):
        for j in range(6):
            spaces.append([15 + i * 100, 15 + j * 100])

    for coords in spaces:
        pygame.draw.ellipse(screen, BLACK, [coords[0], coords[1], 70, 70], 0)

    clock = pygame.time.Clock()
    keep_going = True
    # Loop
    while keep_going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                break
            if event.type == pygame.KEYDOWN:
                col = None
                if event.key == pygame.K_1:
                    col = 0
                elif event.key == pygame.K_2:
                    col = 1
                elif event.key == pygame.K_3:
                    col = 2
                elif event.key == pygame.K_4:
                    col = 3
                elif event.key == pygame.K_5:
                    col = 4
                elif event.key == pygame.K_6:
                    col = 5
                elif event.key == pygame.K_7:
                    col = 6

                if col is not None:
                    valid_move = board.play(curr_player, col)
                    if valid_move:
                        if curr_player == 1:
                            pygame.draw.ellipse(screen, RED, [15 + col * 100, 515 - (board.openRows[col]-1) * 100, 70, 70], 0)
                        else:
                            pygame.draw.ellipse(screen, BLUE, [15 + col * 100, 515 - (board.openRows[col]-1) * 100, 70, 70], 0)

                        curr_player *= -1

        if board.check_win() != 0:
            keep_going = False

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Connect 4")
    connect4()
    pygame.quit()
