import pygame
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


INFO_FONT = pygame.font.SysFont('Future', 25)

pygame.display.set_caption('Number guesser')

CELLS = 28

grid_width = 560
grid_height = 560
screen_width = 760
screen_height = 560

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Number Guesser")


classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class Pixel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        self.neighbors = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.x + self.width, self.y + self.height))

    def get_square(self, grid):
        row = self.y // 20    # row
        col = self.x // 20    # col
        rows = CELLS
        cols = CELLS

        if row < cols - 1:  # Right
            self.neighbors.append(grid.pixels[row + 1][col])
        if col < rows - 1:  # Up
            self.neighbors.append(grid.pixels[row][col + 1])

        if col < rows - 1 and row < cols - 1:  # Bottom Right
            self.neighbors.append(grid.pixels[row + 1][col + 1])


class Grid:
    def __init__(self, row, col, width, height):
        self.rows = row
        self.cols = col
        self.width = width
        self.height = height
        self.pixels = []
        self.pixel_generation()

    def draw(self, surface):
        for row in self.pixels:
            for pixel in row:
                pixel.draw(surface)

    def pixel_generation(self):
        pixel_width = self.width // self.cols
        pixel_height = self.height // self.rows
        self.pixels = []
        for row in range(self.rows):
            self.pixels.append([])
            for col in range(self.cols):
                self.pixels[row].append(Pixel(pixel_width * col, pixel_height * row, pixel_width, pixel_height))

        for row in range(self.rows):
            for col in range(self.cols):
                self.pixels[row][col].get_square(self)

    def clicked(self, pos):
        if self.width > pos[0] and self.height > pos[1]:
            g1 = int(pos[0]) // self.pixels[0][0].width
            g2 = int(pos[1]) // self.pixels[0][0].height

            return self.pixels[g2][g1]
        else:
            pass

    def convert_to_binary(self):
        li = self.pixels

        new_grid = [[] for x in range(len(li))]

        for row in range(len(li)):
            for col in range(len(li[row])):
                if li[row][col].color == WHITE:
                    new_grid[row].append(0)
                else:
                    new_grid[row].append(1)

        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_test = tf.keras.utils.normalize(x_test, axis=1)
        for row in range(CELLS):
            for x in range(CELLS):
                x_test[0][row][x] = new_grid[row][x]

        return x_test[:1]


def guess(li):
    model = tf.keras.models.load_model('handwritten_digits_mnist.model')
    predictions = model.predict(li)
    num = (np.argmax(predictions[0]))
    plt.imshow(li[0], cmap=plt.cm.binary)
    plt.xlabel("I predict {} {:2.0f}%".format(num, 100 * np.max(predictions)))
    plt.show()


def draw_screen():
    g.draw(screen)
    pygame.draw.rect(screen, WHITE, (g.width, 0, screen_width, g.height))
    pygame.draw.line(screen, BLACK, (g.width, 0), (g.width, g.height))

    left_click_text = INFO_FONT.render('Left click for draw', True, BLACK)
    screen.blit(left_click_text, (screen_width-(screen_width-g.width)//2 - left_click_text.get_width()//2, 10))

    right_click_text = INFO_FONT.render('Right click for rubber', True, BLACK)
    screen.blit(right_click_text, (screen_width-(screen_width-g.width)//2 - right_click_text.get_width()//2, 30))

    press_key_text = INFO_FONT.render('Press any key to predict', True, BLACK)
    screen.blit(press_key_text, (screen_width-(screen_width-g.width)//2 - press_key_text.get_width()//2, 50))

    pygame.display.update()


g = Grid(CELLS, CELLS, grid_width, grid_height)


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                li = g.convert_to_binary()
                guess(li)
                g.pixel_generation()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] < g.width and pos[1] < g.height:
                    clicked = g.clicked(pos)
                    clicked.color = BLACK

                    for n in clicked.neighbors:
                        n.color = BLACK

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                clicked = g.clicked(pos)
                clicked.color = WHITE

        draw_screen()
        pygame.display.update()


if __name__ == '__main__':
    main()
