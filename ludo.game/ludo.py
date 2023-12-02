import pygame
import random
import math
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600 # 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ludo game")

display_font = pygame.font.SysFont("comicsans", 16)
winner_font = pygame.font.SysFont("comicsans", 40)

HOUSE_WIDTH = 230 # 250
HOUSE_HEIGHT = 230 # 250
COLOR_VALUE = {"red": 5, "blue": 6, "yellow": 8, "green": 9}
HOME_VALUE = {"red": 1, "blue": 2, "yellow": 3, "green": 4}
excluded_tile_pos = {"red": (6, 0), "blue": (0, 2), "yellow": (14, 0), "green": (8, 14)}

BOX_WIDTH = 60
BOX_HEIGHT = 44
BOX_WIDTH2 = 40 # 46
BOX_HEIGHT2 = 40 # 46

ROWS = 3
COLS = 15

DICE_WIDTH = 36
DICE_HEIGHT = 36
SEED_RADIUS = 14
PLACEMENT_RADIUS = 18

LOGO_WIDTH = BOX_WIDTH2 * 3 + 40
LOGO_HEIGHT = BOX_HEIGHT2 * 3 + 40

seed_capture = pygame.USEREVENT + 1
seed_capture_sound = pygame.mixer.Sound(os.path.join("Assets", "mixkit-arcade-game-jump-coin-216.wav"))

seed_movement = pygame.USEREVENT + 2
seed_movement_sound = pygame.mixer.Sound(os.path.join("Assets", "mixkit-game-coin-touch-3217.wav"))

die_roll = pygame.USEREVENT + 3
die_roll_sound = pygame.mixer.Sound(os.path.join("Assets", "gamemisc_dice-roll-on-wood_jaku5-37414.mp3"))

FPS = 60

NUM_OF_PLAYERS = 4
MAX_NUM_OF_PLAYERS = 4

assets_dir = os.path.abspath("Assets")

red_image  = pygame.image.load(os.path.join(assets_dir, "red.png"))
blue_image  = pygame.image.load(os.path.join(assets_dir, "blue.png"))
green_image  = pygame.image.load(os.path.join(assets_dir, "green.png"))
yellow_image  = pygame.image.load(os.path.join(assets_dir, "yellow.png"))
logo_image = pygame.image.load(os.path.join(assets_dir, "logo.png"))


red_house = pygame.transform.scale(red_image, (HOUSE_WIDTH, HOUSE_HEIGHT))
blue_house = pygame.transform.scale(blue_image, (HOUSE_WIDTH, HOUSE_HEIGHT))
green_house = pygame.transform.scale(green_image, (HOUSE_WIDTH, HOUSE_HEIGHT))
yellow_house = pygame.transform.scale(yellow_image, (HOUSE_WIDTH, HOUSE_HEIGHT))
logo = pygame.transform.scale(logo_image, (LOGO_WIDTH, LOGO_HEIGHT))


class Tiles:
    def __init__(self, value, x, y, width, height, grid_pos):
        self.rect = pygame.Rect(x, y, width, height) #dimensions for the rectangle
        self.grid_position = i, j = grid_pos
        self.selected = False
        self.value = value
        self.special = False
        self.highlight = False
        self.color = "white"
        self.special_tile_color = None
        self.special_tile_circle_color = "white"
        self.highlight_color = "brown"

    def draw(self, win):
        '''Draws a tile on the board'''
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, "black", (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2) 
    
    def draw_special_tiles(self, win):
        '''Draws a tile on the board'''
        # pygame.draw.circle(win, "brown", (self.rect.x + (self.rect.width//2) - 5, self.rect.y - (self.rect.height//2) + 5))
        pygame.draw.rect(win, self.special_tile_color, self.rect)
        pygame.draw.rect(win, "black", (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        pygame.draw.circle(win, self.special_tile_circle_color, (self.rect.x + (self.rect.width//2), self.rect.y + (self.rect.height//2)), 16)

    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos): #checks if a point is inside a rect
            self.selected = True
        return self.selected
    
    def toggle_tile_highlight(self):
        if not self.highlight:

            if not self.special:
                self.color = self.highlight_color

            self.highlight = not self.highlight
            return

        if self.highlight:

            if not self.special:
                self.color = "white"
             
            self.highlight = not self.highlight
        
    def is_special_tiles_hor(self):
        i, j = self.grid_position
        if (i == 7 and 1 <= j <= 5) and not self.highlight:
            self.special = True
            self.special_tile_color = "red"
        
        elif (i == 7 and 14 > j > 8) and not self.highlight:
            self.special = True
            self.special_tile_color = "green"
        
        elif self.highlight:
            self.special_tile_color = self.highlight_color
    
        return self.special
    
    def is_special_tiles_ver(self):
        i, j = self.grid_position
        if (j == 1 and 1 <= i <= 5) and not self.highlight:
            self.special = True
            self.special_tile_color = "blue"

        elif (j == 1 and 14 > i > 8) and not self.highlight:
            self.special = True
            self.special_tile_color = "yellow"
            
        elif self.highlight:
            self.special_tile_color = self.highlight_color

        return self.special
        

class House:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self,  win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Seed:

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.out = False
        self.current_pos = None
        self.visited = set()
        self.clicked = False
        self.player = None
        self.lst_visited = list(self.visited)
        self.valid_grid_nums = {-1, 5, 6, 8, 9}

        self.visited.add(excluded_tile_pos[self.color])


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        # pygame.draw.circle(win, self.house_pos_color, (self.x, self.y), self.radius, 7)
    
    def set_seed_position(self, x, y):
        self.x = x
        self.y = y
    
    def is_clicked(self, pos_x, pos_y):
        distance = math.sqrt((pos_x - self.x)**2 + (pos_y - self.y)**2)

        if distance <= self.radius:
            self.clicked = True
        
        return self.clicked
    
    def __str__(self):
        return f"{self.color}: {self.clicked}"
        

class SeedPlacement:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = "white"
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Dice:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = "grey"
        self.moves = [0, 0]
    
    def roll_dice(self):
        first_move = random.randint(1, 6)
        second_move = random.randint(1, 6)
        self.moves = [first_move, second_move]
        return self.moves
    
    def draw(self, win):
        num1 = display_font.render(str(self.moves[0]), 1, "black")
        num2 = display_font.render(str(self.moves[1]), 1, "black")
        second_dice = pygame.Rect(self.x + self.width + 2, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, self.color, second_dice)

        win.blit(num1, (self.x + (self.width//2) - num1.get_width(), self.y - (self.height//2)  + num1.get_height()))
        win.blit(num2, (second_dice.x + (self.width//2) - num1.get_width(), self.y - (self.height//2) + num1.get_height()))


class Player:
    def __init__(self, id,  seeds):
        self.name = f"Player {id}"
        self.seeds = seeds
        self.score = 2
        self.num_of_seeds = 4 if len(seeds) == 1 else 8
        self.num_of_active_seeds = 0
        self.seed_grid_value = set()
        self.seeds_at_goal_area = []
        self.seed_at_risk = []

        for seed_group in self.seeds:

            # self.seed_grid_value.add(COLOR_VALUE[seed_group])

            for seed in self.seeds[seed_group]:
                    
                    if COLOR_VALUE[seed.color] not in self.seed_grid_value:
                        # self.seed_grid_value.add(HOME_VALUE[seed.color])
                        self.seed_grid_value.add(COLOR_VALUE[seed.color])

                    seed.player = self

    def check_seed_home_or_goal(self, box_grid):
        for seed_group in self.seeds:
            for seed in self.seeds[seed_group]:

                if seed.out:
                    i, j = seed.current_pos

                    
                    if box_grid[i][j] == HOME_VALUE[seed.color]:
                        self.seeds_at_goal_area.append(seed)


    def simulate_attack(self, box_grid):
        enemy_pos = []
        for seed_group in self.seeds:
            for seed in self.seeds[seed_group]:
                if seed.out:
                    enemy_pos = self.dfs_seed(seed, box_grid)


        return enemy_pos
    
    def predict_seed_capture(self, box_grid):
        for seed_group in self.seeds:
            for seed in self.seeds[seed_group]:
                if seed.out:
                    for i, j, n in enumerate(seed.lst_visited[::-1]):
                        if box_grid[i][j] not in self.seed_grid_value:
                            self.seed_at_risk.append(seed)
                        
                        elif not(box_grid[i][j] not in self.seed_grid_value) and seed in self.seed_at_risk:
                            self.seed_at_risk.remove(seed)

    def dfs_seed(self, seed, box_grid):
        enemy_pos = []
        end_positions = {"red": (6, 0), "blue": (0, 2), "green": (8, 14), "yellow": (14, 0)}

        start_pos = seed.current_pos
        total_sum = 12
    
        x = 0
        stack = [(start_pos)]
        visited = set()

        while x < total_sum and len(stack):
            row, col = stack.pop()
            
            if box_grid[row][col] not in seed.valid_grid_nums:
                continue


            if (row, col) in seed.visited or (row, col) in visited:
                continue

            if box_grid[row][col] not in self.seed_grid_value:
                enemy_pos.append([(row, col), x])
            
            visited.add((row, col))

            if box_grid[row][col] == 7 and HOME_VALUE[seed.color] in seed.valid_grid_nums:
                break

            x += 1

            neighbours = find_neighbours(box_grid, row, col)

            if len(seed.visited) > 30 and end_positions[seed.color] in neighbours:
                seed.valid_grid_nums.add(HOME_VALUE[seed.color])
                seed.valid_grid_nums.add(7)
                
            for neighbour in neighbours:
                stack.append(neighbour)

        return enemy_pos


    def current_player_at_goal_area(self):
        pass

    def __str__(self):
        return self.name
    

def create_grid():
    
    box_grid2 = [[-1, -1, -1], 
                [-1, 2, -1], 
                [-1, 2, -1], 
                [-1, 2, -1], 
                [-1, 2, -1], 
                [-1, 2, -1], 
                [-1, -1, -1, -1, -1, -1, 7, 7, 7, -1, -1, -1, -1, -1, -1], 
                [-1, 1, 1, 1, 1, 1, 7, 7, 7, 4, 4, 4, 4, 4, -1], 
                [-1, -1, -1, -1, -1, -1, 7, 7, 7, -1, -1, -1, -1, -1, -1], 
                [-1, 3, -1], 
                [-1, 3, -1], 
                [-1, 3, -1], 
                [-1, 3, -1], 
                [-1, 3, -1], 
                [-1, -1, -1]]
   
    box_positon = {}
    lst_of_boxes = []
   
    for i in range(len((box_grid2))):
        y = (i * BOX_HEIGHT2) + 4.5 # 10
            
        for j in range(len(box_grid2[i])):
            if 6 <= i <= 8:
                 y = BOX_HEIGHT2 - 36 + i * BOX_HEIGHT2 # 36
                 x = (j * BOX_WIDTH2) + 1.0 # 4  
            else:
                x = (WIDTH//2 - BOX_WIDTH2 - 20) + 2.5 + j * BOX_WIDTH2 # 2.5, 25

            pos = i, j
            box = Tiles(box_grid2[i][j], x, y, BOX_WIDTH2, BOX_HEIGHT2, (i, j))
            box_positon[pos] = box
            lst_of_boxes.append(box)

    # print(len(box_positon))
    # print(len(lst_of_boxes))
    return box_grid2, lst_of_boxes, box_positon


def handle_seed_movement(seeds_to_move, box_positons, event, mouse_pos, box_grid, seed_groups, seed_placement, unused_move, current_player):
    moved = False
    seed_moved = None
    for seed in seeds_to_move:
        for idx, move in enumerate(seeds_to_move[seed]):
            i, j = move
            tile = box_positons[move] 

            # if tile.highlight:
            if event.button == 1 and tile.clicked(mouse_pos) and tile.highlight and box_grid[i][j] not in current_player.seed_grid_value: 
            
                new_pos_x = tile.rect.x + (tile.rect.width//2)
                new_pos_y = tile.rect.y + (tile.rect.height//2)
                seed.set_seed_position(new_pos_x, new_pos_y)
                pygame.event.post(pygame.event.Event(seed_movement))
    
                if seed.out:
                    r, c = seed.current_pos
                    if box_grid[r][c] not in [HOME_VALUE[seed.color], 7]:
                        box_grid[r][c] = -1

                    if sum(unused_move) == idx:
                        unused_move.clear()
                    
                    elif idx in unused_move:
                        unused_move.remove(idx)

                if not seed.out:
                    unused_move.remove(6)
                    if len(unused_move):
                        if unused_move[0] == idx:
                            unused_move.clear()

                    seed.out = True
                    current_player.num_of_active_seeds += 1
                    
                seed.current_pos = move

                if box_grid[i][j] != HOME_VALUE[seed.color] and box_grid[i][j] != 7:
                    box_grid[i][j] = COLOR_VALUE[seed.color]

                else:
                    current_player.num_of_active_seeds -= 1

                skipped_pos = seeds_to_move[seed][:idx]

                if len(seeds_to_move[seed]) > 1:
                    for pos in skipped_pos:
                        seed.visited.add(pos)
                
                moved = True
                seed_moved = seed
                seed.clicked = False
                tile.selected = False

                if handle_enemy_capture(seed_groups, seed_placement, move, seed, current_player, box_grid, unused_move):
                    if box_grid[i][j] != 7:
                        box_grid[i][j] = -1


    if moved:
        for tile_pos in seeds_to_move[seed]:
            if box_positons[tile_pos].highlight:
                box_positons[tile_pos].toggle_tile_highlight()

    return moved, seed_moved


def handle_enemy_capture(seed_groups, seed_placement, move, current_seed, current_player, box_grid, unused_move):
    capture = False
    a, b  = move

    for seed_color in seed_groups:

        if seed_color in current_player.seeds:
            continue

        for i, seed in enumerate(seed_groups[seed_color]):
            if seed == current_seed:
                continue

            if seed.current_pos == move:
                placement = seed_placement[seed.color][i]
                seed.set_seed_position(placement.x, placement.y)
                seed.current_pos = None
                seed.out = False
                seed.visited = {excluded_tile_pos[seed.color]}
                opponet = seed.player
                opponet.num_of_active_seeds -= 1
                opponet.score -= 1
                capture = True
                pygame.event.post(pygame.event.Event(seed_capture))

                break

    if capture:
        seed_groups[current_seed.color].remove(current_seed)
        current_player.num_of_active_seeds -= 1
        current_player.num_of_seeds -= 1
        current_player.score += 1
    
    elif box_grid[a][b] == 7:
        seed_groups[current_seed.color].remove(current_seed)
        current_player.num_of_active_seeds -= 1
        current_player.num_of_seeds -= 1
        current_player.score += 1
        unused_move.clear()
        pygame.event.post(pygame.event.Event(seed_capture))


    return capture


def dfs_movement(box_grid, dice_roll, seed, opening_moves, pair_nums):
    second_value = pair_nums[0]
    valid_tiles = []
    end_positions = {"red": (6, 0), "blue": (0, 2), "green": (8, 14), "yellow": (14, 0)}

    if seed.current_pos == None:
        total_sum = second_value + 1
        start_pos = opening_moves[seed.color][0]

    else:
        total_sum = sum(dice_roll) + 1
        start_pos = seed.current_pos
    
    x = 0
    stack = [(start_pos)]
    visited = set()

    while x < total_sum and len(stack):
        row, col = stack.pop()
        
        if box_grid[row][col] not in seed.valid_grid_nums:
            continue


        if (row, col) in seed.visited or (row, col) in visited:
            continue
        
        visited.add((row, col))

        valid_tiles.append((row, col))

        if box_grid[row][col] == 7 and HOME_VALUE[seed.color] in seed.valid_grid_nums:
            break

        x += 1

        neighbours = find_neighbours(box_grid, row, col)

        if len(seed.visited) > 30 and end_positions[seed.color] in neighbours:
            seed.valid_grid_nums.add(HOME_VALUE[seed.color])
            seed.valid_grid_nums.add(7)
            
        for neighbour in neighbours:
            stack.append(neighbour)

    return valid_tiles


def find_neighbours(box_grid, row, col):
    neighbours = []
    up_limit = 9
    down_limit = 5
    left_limit = 9
    right_limit = 5

    if row > 0 : # up
        if len(box_grid[row]) == len(box_grid[row - 1]):
            neighbours.append((row - 1, col)) 

    if row > 0 and row == up_limit: # up diagonal
        if  not(len(box_grid[row]) == len(box_grid[row - 1])):
            neighbours.append((row - 1, col + 5))
    
    if row < len(box_grid) - 1: # down
        if len(box_grid[row]) == len(box_grid[row + 1]):
            neighbours.append((row + 1, col))

    if row < len(box_grid) - 1 and row == down_limit and col != 0: # down diagonal
        if not(len(box_grid[row]) == len(box_grid[row + 1])):
            neighbours.append((row + 1, up_limit))
    
    if col > 0: # left
        neighbours.append((row, col - 1))
    
    if col == left_limit: # left diagonal
        if len(box_grid[row]) != len(box_grid[row + 1]):
            neighbours.append((row + 1, col - 7))
    
    if col < len(box_grid[row]) - 1: # right
        neighbours.append((row, col + 1))
    
    if col == right_limit: # right diagonal
        if len(box_grid[row]) != len(box_grid[row - 1]):
            neighbours.append((row - 1, col - col))
    
    return neighbours


def handle_current_player_seeds(current_player, num_movement, box_positions, box_grid, unused_moves, seeds_to_move):
    pos_x, pos_y = pygame.mouse.get_pos()

    for seed_color in current_player.seeds:
        for seed in current_player.seeds[seed_color]:

            if seed.is_clicked(pos_x, pos_y):
                moves_to_make = show_valid_moves(num_movement, box_positions, seed, box_grid, unused_moves, current_player)
                # seed.clicked = False

                if seed in seeds_to_move:
                    seed.clicked = False
                    del seeds_to_move[seed]

                elif not(seed in seeds_to_move) and len(moves_to_make) and len(unused_moves):    
                    seeds_to_move[seed] = moves_to_make


def handle_current_player_and_opponent(current_player, unused_moves, players, lucky, opponents, current_player_idx):
    if current_player.num_of_active_seeds >= 1 and not(len(unused_moves)) or current_player.num_of_active_seeds < 1 and 6 not in unused_moves:
        current_player_idx = handle_player_turn(players, current_player_idx, lucky)
        lucky = False
        
        current_player = players[current_player_idx]
        

        opponents = []
        for player in players:
            if player != current_player:
                opponents.append(player)

    return lucky, current_player_idx



def show_valid_moves(dice_roll, box_positions, seed, box_grid, unused_moves, current_player):
    first_value, second_value = dice_roll
    pair_nums = [first_value, second_value]
    start_value = 6
    opening_moves = {"red": [(6, 1), "right"], "blue": [(1, 2), "down"], "green": [(8, 13), "left"], "yellow": [(13, 0), "up"]}
    contains_6 = False
    valid_moves = []

    if not seed.out:
        for num in pair_nums:

            if num == start_value:
                contains_6 = True
                pair_nums.remove(num)
                break

    if contains_6 and len(unused_moves) or seed.out:
        valid_moves = dfs_movement(box_grid, dice_roll, seed, opening_moves, pair_nums)
        
        if not seed.out:
                if start_value in unused_moves and current_player.num_of_active_seeds >= 1:
                    box_positions[valid_moves[0]].toggle_tile_highlight()

                if  pair_nums[0] in unused_moves and start_value in unused_moves and len(unused_moves) == 2:
                    box_positions[valid_moves[pair_nums[0]]].toggle_tile_highlight()
            
        elif seed.out and pair_nums[0] == pair_nums[1]:
                total = sum(pair_nums)
                if pair_nums[0] in unused_moves and current_player.num_of_active_seeds > 1:
                        box_positions[valid_moves[pair_nums[0]]].toggle_tile_highlight()
                        # box_positions[valid_moves[-1]].toggle_tile_highlight()

                if len(unused_moves) == len(pair_nums):
                    if total == len(valid_moves) - 1:
                        box_positions[valid_moves[total]].toggle_tile_highlight() 

                    else:
                     box_positions[valid_moves[-1]].toggle_tile_highlight()

        else:
            total = sum(pair_nums)

            if len(unused_moves) == len(pair_nums):
                if total == len(valid_moves) - 1:
                    box_positions[valid_moves[total]].toggle_tile_highlight()
                
                else:
                     box_positions[valid_moves[-1]].toggle_tile_highlight()

            for num in unused_moves: 
                    if len(unused_moves) == 1 or current_player.num_of_active_seeds > 1:
                            box_positions[valid_moves[num]].toggle_tile_highlight()


    if not(len(unused_moves)) or not(contains_6 and len(unused_moves) or seed.out):
        seed.clicked = False
    
    return valid_moves


def handle_player_turn(players, current_player_index, lucky):
    if current_player_index != len(players) - 1: 
        current_player_index += 1

    elif not lucky:
        current_player_index = 0

    return current_player_index


def loop(current_player, box_grid, num_movement, players):
    current_player.check_seed_home_or_goal(box_grid)
    enemy_pos = current_player.simulate_attack(box_grid)
    current_player.predict_seed_capture(box_grid)




def draw(win, lst_of_houses, lst_of_ver_boxes, dice, seed_groups, seed_placement, current_player):
    gap = 5
    # backgrd = pygame.Rect(WIDTH // 2 + BOX_HEIGHT2 * 3 - 208, HEIGHT // 2 - BOX_WIDTH2 * 3 + 75, BOX_HEIGHT2 * 3, BOX_WIDTH2 * 3)
    player = display_font.render(str(current_player), 1, "black")
    win.fill("white")
   
    for house in lst_of_houses.values():
        house.draw(win)
    
    win.blit(red_house, (gap, 20))
    win.blit(blue_house, (WIDTH - HOUSE_WIDTH - gap, 20))
    win.blit(green_house, (WIDTH - HOUSE_WIDTH - gap, HEIGHT - HOUSE_HEIGHT - gap)) 
    win.blit(yellow_house, (gap, HEIGHT - HOUSE_HEIGHT - gap))
    
    for box in lst_of_ver_boxes:
            if box.is_special_tiles_ver() or box.is_special_tiles_hor():
                box.draw_special_tiles(win)
            
            else:
                box.draw(win)
    
    # pygame.draw.rect(win, "white", backgrd)

    win.blit(logo, (WIDTH//2 - LOGO_WIDTH + 90, HEIGHT//2 - LOGO_HEIGHT + 80))
    win.blit(player, (WIDTH // 2 - player.get_width() + 30, -2)) # 10, 30


    for group in seed_placement:
        for seed_pos in seed_placement[group]:
            seed_pos.draw(win)

    for group in seed_groups:
        for seed in seed_groups[group]:
            seed.draw(win)

    dice.draw(win)

    pygame.display.update()


 
def draw_winner_text(winner):
    text = f"{winner} WINS"
    winner_text = winner_font.render(text, 1, "black")
    WIN.blit(winner_text, ((WIDTH // 2) - winner_text.get_width() // 2, (HEIGHT // 2) - winner_text.get_height() // 2))
    pygame.display.update()



class LudoGame:
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.window = window
        self.opponets = []
        self.current_player = None


    def main(self):
        run = True
        gap = 5
        clock = pygame.time.Clock()
        lst_of_houses = {"red": House(gap, 20, HOUSE_WIDTH, HOUSE_HEIGHT, "red"),# top left
                        "blue": House(WIDTH - HOUSE_WIDTH - gap, 20, HOUSE_WIDTH, HOUSE_HEIGHT, "blue"), # top right
                        "yellow": House(gap, HEIGHT - HOUSE_HEIGHT - gap, HOUSE_WIDTH, HOUSE_HEIGHT, "yellow"),#bottom left
                        "green": House(WIDTH - HOUSE_WIDTH - gap, HEIGHT - HOUSE_HEIGHT - gap, HOUSE_WIDTH, HOUSE_HEIGHT, "green")# bottom right
        }
        
        lucky_roll = [6, 6]
        lucky = False
        square_size = 50
        seeds_to_move = {}
        winner = None 

        num_movement = [0, 0]
        unused_moves = []
        box_grid, lst_of_ver_boxes, box_positions = create_grid() 
        dice = Dice((WIDTH//2) - DICE_WIDTH, (HEIGHT//2) - DICE_HEIGHT, DICE_WIDTH, DICE_HEIGHT)
        seed_groups = {"red": [], "blue": [], "yellow": [], "green": []}
        seed_placement = {"red": [], "blue": [], "yellow": [], "green": []}
        colors  = ["red", "blue", "green", "yellow"] 
        

        
        for house in lst_of_houses.values():
            seeds = [Seed(house.x + (house.width//2) - square_size // 2 , house.y + house.height//2 - square_size // 2, SEED_RADIUS, house.color),
                Seed(house.x + (house.width//2) + square_size // 2 , house.y + house.height//2 - square_size // 2, SEED_RADIUS, house.color),
                Seed(house.x + (house.width//2) - square_size // 2 , house.y + house.height//2 + square_size // 2, SEED_RADIUS, house.color),
                Seed(house.x + (house.width//2) + square_size // 2 , house.y + house.height//2 + square_size // 2, SEED_RADIUS, house.color)]
            
            placement = [SeedPlacement(house.x + (house.width//2) - square_size // 2 , house.y + house.height//2 - square_size // 2, PLACEMENT_RADIUS),
                SeedPlacement(house.x + (house.width//2) + square_size // 2 , house.y + house.height//2 - square_size // 2, PLACEMENT_RADIUS),
                SeedPlacement(house.x + (house.width//2) - square_size // 2 , house.y + house.height//2 + square_size // 2, PLACEMENT_RADIUS),
                SeedPlacement(house.x + (house.width//2) + square_size // 2 , house.y + house.height//2 + square_size // 2, PLACEMENT_RADIUS)]
            
            seed_placement[house.color].extend(placement)     
            seed_groups[house.color].extend(seeds)
        
        players = []
        num_of_players = 4
        max_num_of_players = 4
        current_player_idx = -1

        for i in range(num_of_players):
            groups = {}
            for color in colors[:]:

                if color in colors:
                    groups[color] = seed_groups[color]
                    colors.remove(color)
                
                if num_of_players == max_num_of_players:
                    break

                if len(groups) == 2:
                    break

            player = Player(i+1, groups)
            players.append(player)

        current_player = players[current_player_idx]   

        
        while run: 
            clock.tick(FPS)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and not(len(unused_moves)) or current_player.num_of_active_seeds == 0 and 6 not in num_movement:
                        if num_movement == lucky_roll:
                            lucky = True

                        num_movement = dice.roll_dice()
                        pygame.event.post(pygame.event.Event(die_roll))

                        # lucky, current_player_idx = handle_current_player_and_opponent(current_player, unused_moves, players, lucky, self.opponets, current_player_idx)

                        if current_player.num_of_active_seeds >= 1 and not(len(unused_moves)) or current_player.num_of_active_seeds < 1 and 6 not in unused_moves:
                                current_player_idx = handle_player_turn(players, current_player_idx, lucky)
                                lucky = False
                                
                                current_player = players[current_player_idx]

                    
                                self.opponets = []
                                for player in players:
                                    if player != current_player:
                                        self.opponets.append(player)

                               
                        unused_moves = num_movement[:]

                if event.type == seed_capture:
                    seed_capture_sound.play()
                
                elif event.type == seed_movement:
                    seed_movement_sound.play()

                if event.type == die_roll:
                    die_roll_sound.play()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        handle_current_player_seeds(current_player, num_movement, box_positions, box_grid, unused_moves, seeds_to_move)
            
                    mouse_pos = pygame.mouse.get_pos()
                    moved, seed = handle_seed_movement(seeds_to_move, box_positions, event, mouse_pos, box_grid, seed_groups, seed_placement, unused_moves, current_player) 
                    
                    if moved:
                        del seeds_to_move[seed]
                    

            if winner:
                draw_winner_text(winner)
                pygame.time.delay(5000)       
                break

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_SPACE]:
                current_player.num_of_seeds = 0          
            
            for player in players:
                if player.num_of_seeds == 0:
                    winner = player

            draw(WIN, lst_of_houses, lst_of_ver_boxes, dice, seed_groups, seed_placement, current_player) 
            

        self.main()


if __name__ == "__main__":
    ludo = LudoGame(WIDTH, HEIGHT, WIN)
    ludo.main()