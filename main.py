import pygame
import random
import time
from sprite import * # import all
from settings import * # import all


class Game:
    def __init__(self):
        pygame.init() # Initialize pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Set width and height of screen
        pygame.display.set_caption(title) # Set window name
        self.clock = pygame.time.Clock() # Set clock
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        """
        Making this grid:

        [1  2  3]
        [4  5  6]
        [7  8   ]

        """
        grid = []
        number = 1
        for x in range(GAME_SIZE):
            grid.append([])
            for y in range(GAME_SIZE):
                grid[x].append(number)
                number += 1
        grid[-1][-1] = 0 # Set last number to 0 (empty tile)
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []
        # Take the index of every element inside of the list
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            # Enumerating every element in the self.tiles_grid list
            for col, tile in enumerate(x):
                # If tile isn't 0, make a tile
                if tile != 0:
                    # Append a tile
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game() # return the grid
        self.tiles_grid_completed = self.create_game() # If completed grid is the same as first grid, then game is finished
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "Shuffle", LIGHTBROWN, YELLOW_BROWN))
        self.buttons_list.append(Button(500, 170, 200, 50, "Reset", LIGHTBROWN, YELLOW_BROWN))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw_grid(self): # Making the grid
        # Iterates through the rows of the grid
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
        # Draw the line based on: screen where grid is drawn, line color for grid, starting point of line for current row, end point of line for current row.
            pygame.draw.line(self.screen, DARKERBROWN, (row, 0), (row, GAME_SIZE * TILESIZE))
        
        # Iterates through the columns of the grid
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
        # Draw the line based on: screen where grid is drawn, line color for grid, starting point of line for current column, end point of line for current column.
            pygame.draw.line(self.screen, DARKERBROWN, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR) # Set the background color
        self.all_sprites.draw(self.screen) # Draw the sprites
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(430, 300, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        pygame.display.flip() # Update the entire screen

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if X button is pressed
                pygame.quit() # If pressed, quit the game
                quit(0)

            # If mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos() # Return a tuple and set it to var mouse_x and mouse_y
                # Loop through every single tile
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y): # If click the tile, going to check every tile agaisnt the mouse coordinates and return the tile that's being clicked
                            # If there's a tile on the right tile that we clicked and if there is, also check if it's a 0, if it is, swap them
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                            # Swap the variables
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            # Everything is the same
                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()

# Initialize game
game = Game() # Start file, create instance of game
while True:
    game.new() # Create new game
    game.run() # Run the game
