import pygame

pygame.init()

def get_font_size(font_name, given_height):
    test_size = 100
    test_font = pygame.font.SysFont(font_name, test_size)
    t_test_font = test_font.render("test", True, (255, 255, 255))
    font_height = t_test_font.get_height()
    height_per_size = font_height/test_size
    font_size = int(round(given_height / height_per_size, 0))

    return font_size