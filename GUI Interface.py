import pygame
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

def create_pixel_array(row, col, width, height):
    pixel_array = []
    x_px = width // col
    y_px = height // row
    for r in range(row):
        pixel_array.append([])
        for c in range(col):
            pixel_array[r].append([white, x_px * c, y_px * r, x_px, y_px])
    return pixel_array


def update_pixel_array(pos, pixel_array):
    x_pos = pos[0]
    y_pos = pos[1]
    j = x_pos // 20
    i = y_pos // 20
    try:
        pixel_array[i][j][0] = black
        # Updating neighboring pixels horizontally and vertically
        if i < columns - 1:  # Right
            pixel_array[i + 1][j][0] = black
        if i > 0:  # Left
            pixel_array[i - 1][j][0] = black
        if j > 0:  # Up
            pixel_array[i][j - 1][0] = black
        if j < rows - 1:  # Down
            pixel_array[i][j + 1][0] = black
        # Updating neighboring pixels diagonally
        if i < columns - 1 and j > 0:  # Top Right
            pixel_array[i + 1][j - 1][0] = black
        if i > 0 and j > 0:  # Top Left
            pixel_array[i - 1][j - 1][0] = black
        if i < columns - 1 and j < rows - 1:  # Bottom Right
            pixel_array[i + 1][j + 1][0] = black
        if i > 0 and j < rows - 1:  # Bottom Left
            pixel_array[i - 1][j + 1][0] = black
    except:
        pass
    return pixel_array


def draw_gui(surface, pixel_array):
    for r in range(rows):
        for c in range(columns):
            pygame.draw.rect(surface, pixel_array[r][c][0], (pixel_array[r][c][1], pixel_array[r][c][2],
                                                             pixel_array[r][c][3], pixel_array[r][c][4]))

def binary_conversion(pixel_array):
    binary = []
    for r in range(rows):
        binary.append([])
        for c in range(columns):
            if pixel_array[r][c][0] == (0, 0, 0):
                binary[r].append(1)
            else:
                binary[r].append(0)
    return binary

def prediction(array):
    model = load_model('digit_reader.model')
    predict = model.predict(array)
    return np.argmax(predict[0])

def print_Text(output, font_size=14):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(output, True, black)
    text_rect = text.get_rect()
    text_rect.center = (280, 600)
    win.blit(text, text_rect)

if __name__ == '__main__':
    white = (255, 255, 255)
    black = (0, 0, 0)
    pygame.init()
    width = height = 560
    rows, columns = 28, 28

    # window
    pygame.display.set_caption('Digit Recognition')
    win = pygame.display.set_mode((width, 650))
    win.fill((43, 192, 180))

    # button
    button_color = (234, 216, 91)
    pygame.draw.rect(win, button_color, (230, 575, 100, 50))
    print_Text('OUTPUT')

    array = create_pixel_array(rows, columns, width, height)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_BACKSPACE:
                    array = create_pixel_array(28, 28, width, height)
                    pygame.draw.rect(win, button_color, (230, 575, 100, 50))
                    print_Text('OUTPUT')

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                array = update_pixel_array(pos, array)
                if 230 < pos[0] < 330 and 575 < pos[1] < 625:
                    array_binary = binary_conversion(array)
                    np_array_binary = np.array(array_binary)
                    np_array_binary = np_array_binary.reshape(-1, 28, 28, 1)
                    output = prediction(np_array_binary)
                    pygame.draw.rect(win, button_color, (230, 575, 100, 50))
                    print_Text(str(output), 20)

        draw_gui(win, array)
        pygame.display.update()
    pygame.quit()
