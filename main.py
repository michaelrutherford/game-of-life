# An interactive Python implementation of Conway's Game of Life.
# Copyright (C) 2024 Michael Rutherford

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pygame
import sys
import random

pygame.init() # Initialize Pygame

# Global variables and constants
BACKGROUND_COLOR = (0, 0, 0)
ACTIVE_CELL_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 255, 0)
CELL_BORDER_COLOR = (50, 50, 50)
SPEED = 5
WIDTH, HEIGHT = 960, 720

base_font_size = 15
title_font_size = 25
about_font_size = 14
button_width, button_height, margin = 82, 20, 25

rows, cols = 25, 25
cell_size = 22
grid_width = cols * cell_size
grid_height = rows * cell_size
grid_offset_x = (WIDTH - grid_width) // 2
grid_offset_y = (HEIGHT - grid_height + 15) // 2

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Fonts
font = pygame.font.SysFont("monospace", base_font_size)
title_font = pygame.font.SysFont("monospace", title_font_size)
about_font = pygame.font.SysFont("monospace", about_font_size)

# Game state
grid = [[0 for _ in range(cols)] for _ in range(rows)]
initial_grid = [[0 for _ in range(cols)] for _ in range(rows)]
is_playing = False
clock = pygame.time.Clock()

play_button_text = "Play"
generation_count = 0

about_message = "Conway's Game of Life is a cellular automaton with simple rules that can lead to complex, organic-like patterns."
footer_message = "Version 1.0 - © 2024 Michael Rutherford. Licensed under GNU GPL v3"

# Function to create the initial grid
def create_grid():
    update_initial_grid()

# Function to update the initial grid with current grid values
def update_initial_grid():
    global initial_grid
    initial_grid = [[grid[row][col] for col in range(cols)] for row in range(rows)]

# Function to draw the entire grid on the screen
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            draw_cell(row, col)

# Function to draw a single cell at a specific row and column
def draw_cell(row, col):
    cell_x = grid_offset_x + col * cell_size
    cell_y = grid_offset_y + row * cell_size
    cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
    color = ACTIVE_CELL_COLOR if grid[row][col] else BACKGROUND_COLOR
    pygame.draw.rect(screen, color, cell_rect)
    pygame.draw.rect(screen, CELL_BORDER_COLOR, cell_rect, 1)

# Function to count the number of live neighbors for a specific cell
def count_neighbors(row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r = (row + i) % rows
            c = (col + j) % cols
            count += grid[r][c]
    return count

# Function to update the grid based on the game's rules
def update_grid():
    global grid, generation_count, is_playing, play_button_text
    if generation_count < 99999:
        new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
        for row in range(rows):
            for col in range(cols):
                neighbors = count_neighbors(row, col)
                if grid[row][col] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[row][col] = 0
                    else:
                        new_grid[row][col] = 1
                else:
                    if neighbors == 3:
                        new_grid[row][col] = 1
        grid = new_grid
        generation_count += 1
    else:
        is_playing = False
        play_button_text = "Play"

# Function to clear or reset the grid based on the reset variable
def clear_or_reset_grid(reset=False):
    global grid, is_playing, play_button_text, generation_count
    for row in range(rows):
        for col in range(cols):
            grid[row][col] = initial_grid[row][col] if reset else 0
    is_playing = False
    play_button_text = "Play"
    generation_count = 0

# Function to clear the grid
def clear_grid():
    clear_or_reset_grid(reset=False)

# Function to reset the grid
def reset_grid():
    clear_or_reset_grid(reset=True)

# Function to randomize the grid with live and dead cells
def randomize_grid():
    global grid
    for row in range(rows):
        for col in range(cols):
            grid[row][col] = random.choice([0, 1])

# Function to increase the game speed
def handle_toggle_speed_increase():
    global SPEED
    SPEED = min(SPEED+ 1, 100)

# Function to decrease the game speed
def handle_toggle_speed_decrease():
    global SPEED
    SPEED = max(SPEED- 1, 1)

# Function to draw buttons on the screen with given texts
def draw_buttons(button_texts, x_start, y_pos):
    button_rects = []
    for i, text in enumerate(button_texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        button_rect = pygame.Rect(x_start + i * (button_width + margin), y_pos, button_width, button_height)
        pygame.draw.rect(screen, BACKGROUND_COLOR, button_rect)
        screen.blit(text_surface, (button_rect.centerx - text_rect.width // 2, button_rect.centery - text_rect.height // 2))
        pygame.draw.line(screen, CELL_BORDER_COLOR, (button_rect.left, button_rect.bottom), (button_rect.right, button_rect.bottom), 1)
        button_rects.append(button_rect)
    return button_rects

# Function to draw the main buttons (Play, Clear, Reset, Randomize)
def draw_main_buttons():
    button_texts = [play_button_text, "Clear", "Reset", "Randomize"]
    x_start = (WIDTH - (len(button_texts) * button_width + (len(button_texts) - 1) * margin)) // 2
    return draw_buttons(button_texts, x_start, 50)

# Function to draw the speed buttons (Faster, Slower)
def draw_speed_buttons():
    button_texts = ["Faster", "Slower"]
    info_x = grid_offset_x - 150
    info_y_start = grid_offset_y + 3 * (base_font_size + 10) + 20
    button_rects = []
    for i, text in enumerate(button_texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        button_rect = pygame.Rect(info_x, info_y_start + i * (button_height + margin), button_width, button_height)
        pygame.draw.rect(screen, BACKGROUND_COLOR, button_rect)
        screen.blit(text_surface, (button_rect.centerx - text_rect.width // 2, button_rect.centery - text_rect.height // 2))
        pygame.draw.line(screen, CELL_BORDER_COLOR, (button_rect.left, button_rect.bottom), (button_rect.right, button_rect.bottom), 1)
        button_rects.append(button_rect)
    return button_rects

# Function to draw the title on the screen
def draw_title():
    title_text = "Conway's Game of Life"
    text_surface = title_font.render(title_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 20))
    screen.blit(text_surface, text_rect)

# Function to draw the footer message on the screen
def draw_footer():
    text_surface = about_font.render(footer_message, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(midbottom=(WIDTH // 2, HEIGHT - 5))
    screen.blit(text_surface, text_rect)

# Function to draw the about panel with game information
def draw_about_panel():
    about_message = (
        "Conway's Game of Life is a cellular automaton with simple rules that can lead to complex, organic-like patterns.\n\n"
        "The game takes place on a 2-D grid of cells that are either alive or dead and evolve based on the game's rules.\n\n"
        "These are the 4 rules:\n"
        "\nUnderpopulation: Any live cell with fewer than two live neighbors dies.\n"
        "\nStability: Any live cell with two or three live neighbors lives on to the next generation.\n"
        "\nOverpopulation: Any live cell with more than three live neighbors dies.\n"
        "\nReproduction: Any dead cell with exactly three live neighbors becomes a live cell."
    )
    lines = about_message.splitlines()
    max_width = WIDTH - (grid_offset_x + grid_width + 20)
    wrapped_lines = []
    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if about_font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word + " "
        wrapped_lines.append(current_line)
    line_spacing = 1.1
    text_surface_height = len(wrapped_lines) * about_font.get_linesize() * line_spacing
    text_surface = pygame.Surface((max_width, int(text_surface_height)), pygame.SRCALPHA)
    text_surface.fill((0, 0, 0, 0))
    for idx, line in enumerate(wrapped_lines):
        text = about_font.render(line, True, TEXT_COLOR)
        text_surface.blit(text, (0, idx * about_font.get_linesize() * line_spacing))
    text_rect = text_surface.get_rect(topleft=(grid_offset_x + grid_width + 10, grid_offset_y))
    screen.blit(text_surface, text_rect)

# Function to draw the information panel with game statistics
def draw_info_panel(generation_count, live_cells, SPEED):
    info_x = grid_offset_x - 160
    info_y_start = grid_offset_y
    info_texts = [
        f"Generation: {generation_count}",
        f"Live Cells: {live_cells}",
        f"Speed: {SPEED}"
    ]
    for i, text in enumerate(info_texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(topleft=(info_x, info_y_start + i * (base_font_size + 10)))
        screen.blit(text_surface, text_rect)

# Function to handle mouse click events on the grid and buttons
def handle_mouse_click(x, y, button_rects1, speed_button_rects):
    if grid_offset_x <= x < grid_offset_x + grid_width and grid_offset_y <= y < grid_offset_y + grid_height:
        col = (x - grid_offset_x) // cell_size
        row = (y - grid_offset_y) // cell_size
        grid[row][col] = 1 if grid[row][col] == 0 else 0
        update_initial_grid()
    else:
        handle_button_click(x, y, button_rects1, speed_button_rects)

# Function to handle button click events
def handle_button_click(x, y, button_rects1, speed_button_rects):
    for i, rect in enumerate(button_rects1):
        if rect.collidepoint((x, y)):
            if i == 0:
                toggle_play()
            elif i == 1:
                clear_grid()
            elif i == 2:
                reset_grid()
            elif i == 3:
                randomize_grid()
    for i, rect in enumerate(speed_button_rects):
        if rect.collidepoint((x, y)):
            if i == 0:
                handle_toggle_speed_increase()
            elif i == 1:
                handle_toggle_speed_decrease()

# Function to toggle the play and pause state of the game
def toggle_play():
    global is_playing, play_button_text
    is_playing = not is_playing
    play_button_text = "Pause" if is_playing else "Play"

create_grid() # Set up initial grid

# Main loop
while True:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_title()
    button_rects = draw_main_buttons()
    live_cells = sum(sum(row) for row in grid) # Count the number of live cells on the grid
    draw_info_panel(generation_count, live_cells, SPEED)
    speed_button_rects = draw_speed_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event.pos[0], event.pos[1], button_rects, speed_button_rects)
    
    if is_playing:
        update_grid()

    draw_about_panel()
    draw_footer()
    pygame.display.flip() # Updates the full display to the screen
    clock.tick(SPEED)