from os import walk
from typing import List, Tuple

import pygame

from src.utils.colors import colors


def format_text(line: str) -> List[Tuple[str, Tuple[int, int, int]]]:
    """Format text with color codes.

    Args:
        line (str): The input text line.

    Returns:
        List[Tuple[str, Tuple[int, int, int]]]: A list of tuples containing formatted text and corresponding color tuples.
    """
    formatted_lines = []  # List to store formatted text lines
    current_color = (255, 255, 255)  # Default color (white)
    current_text = ""  # Current text being processed
    index = 0  # Index for iterating through the input line
    line_length = len(line)  # Precompute the length of the input line

    # TODO: Split this function into smaller pieces (and avoid bow shapes >-)
    while index < line_length:
        # TODO: Add an escape char (as does the \ most of programming languages)
        # For example you can say that if there is two &, then the text isn't colored and only one is shown
        if line[index] == "&" and index + 1 < line_length and line[index + 1] in "0123456789ABCDEFabcdef":
            # Check if the character is a color code
            color_char = line[index + 1]  # Extract color character
            try:
                color_index = int(color_char, 16)  # Convert color character to integer
                if 0 <= color_index < len(colors):  # Check if color index is within range
                    if current_text:
                        formatted_lines.append((current_text, current_color))  # Append current text with its color
                        current_text = ""  # Reset current text
                    current_color = colors[color_char]  # Update current color
                index += 2  # Move index forward by 2 to skip the color code
            except ValueError:
                current_text += line[index]  # Append character to current text
                index += 1  # Move index forward by 1
        else:
            current_text += line[index]  # Append character to current text
            index += 1  # Move index forward by 1

    if current_text:
        formatted_lines.append((current_text, current_color))  # Append remaining text with its color

    return formatted_lines  # Return the list of formatted lines


def draw_formatted_message(font, surface, formatted_message, pos):
    x, y = pos
    for text, color in formatted_message:
        font.render_to(surface, (x, y), text, color)
        x += font.get_rect(text)[2] + 5


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
