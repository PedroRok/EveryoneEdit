from enum import Enum
import os

import pygame.image
from pygame import Surface


def find_elements():
    found_elements = []

    for current_folder, sub_folder, files in os.walk("resources"):
        for file in files:
            file_path = os.path.join(current_folder, file)
            file_path = file_path.removeprefix("resources\\")
            found_elements.append(file_path)

    return found_elements


class Texture:
    def __init__(self, label, file: Surface, category):
        self.label = label
        self.file = file
        self.category = category


class Textures:

    def __init__(self):
        self.texture_list = []
        elements = find_elements()
        for element in elements:
            split = element.split("\\")
            label = split[len(split) - 1].removesuffix(".png")
            category = split[len(split) - 2]
            texture = Texture(label, pygame.image.load(f"resources/{element}"), category)
            self.texture_list.append(texture)
        pass

    def get_texture_by_label(self, label) -> Surface:
        for texture in self.texture_list:
            if texture.label == label:
                return texture.file.copy()
    def get_elements_by_category(self, category):
        elements = []
        for element in self.texture_list:
            if element.category == category:
                elements.append(element)
        return elements


textures = Textures()

def get():
    return textures
