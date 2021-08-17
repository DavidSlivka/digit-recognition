import pygame
import numpy as np
import tensorflow as tf

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.display.set_caption('Number guesser')


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
        i = self.y // 20    # row
        j = self.x // 20    # col
        rows = 28
        cols = 28

        if i < cols - 1:  # Right
            self.neighbors.append(grid.pixels[i + 1][j])
        if j < rows - 1:  # Up
            self.neighbors.append(grid.pixels[i][j + 1])

        if j < rows - 1 and i < cols - 1:  # Bottom Right
            self.neighbors.append(grid.pixels[i + 1][j + 1])


class Grid:
    def __init__(self, row, col, width, height):
        self.rows = row
        self.cols = col
        self.width = width
        self.height = height
        self.pixels = []
        self.generatePixels()

    def draw(self, surface):
        for row in self.pixels:
            for col in row:
                col.draw(surface)

    def generatePixels(self):
        x_gap = self.width // self.cols
        y_gap = self.height // self.rows
        self.pixels = []
        for r in range(self.rows):
            self.pixels.append([])
            for c in range(self.cols):
                self.pixels[r].append(Pixel(x_gap * c, y_gap * r, x_gap, y_gap))

        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c].get_square(self)

    def clicked(self, pos): #Return the position in the grid that user clicked on
        try:
            t = pos[0]
            w = pos[1]
            g1 = int(t) // self.pixels[0][0].width
            g2 = int(w) // self.pixels[0][0].height

            return self.pixels[g2][g1]
        except:
            pass

    def convert_binary(self):
        li = self.pixels

        new_grid = [[] for x in range(len(li))]

        for i in range(len(li)):
            for j in range(len(li[i])):
                if li[i][j].color == (255,255,255):
                    new_grid[i].append(0)
                else:
                    new_grid[i].append(1)

        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_test = tf.keras.utils.normalize(x_test, axis=1)
        for row in range(28):
            for x in range(28):
                x_test[0][row][x] = new_grid[row][x]

        return x_test[:1]


def guess(li):
    model = tf.keras.models.load_model('handwritten_digits_mnist.model')
    predictions = model.predict(li)
    t = (np.argmax(predictions[0]))
    print("I predict this number is a:", t)


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                li = g.convert_binary()
                guess(li)
                g.generatePixels()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                clicked = g.clicked(pos)
                clicked.color = BLACK

                for n in clicked.neighbors:
                    n.color = BLACK

        g.draw(window)
        pygame.display.update()


width, height = 560, 560
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Number Guesser")
g = Grid(28, 28, width, height)

if __name__ == '__main__':
    main()
