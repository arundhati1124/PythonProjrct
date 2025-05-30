from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
import sys

# Game states
STATE_INTRO = 0
STATE_MOUSE_SELECT = 1
STATE_GAME = 2
STATE_GAME_OVER = 3
STATE_LEVEL_COMPLETE = 4

# Maze data
tile_size = 60
wall_thickness = 4
wall_height = 60
angle = 0  # Rotation angle
window_width = 1000
window_height = 800
fovY = 55

# UI Elements
ui_box_width = 600
ui_box_height = 100
ui_box_y_offset = 50  # Distance from top of screen (reduced to be more visible)

# Colors
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)
RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
GRAY = (0.4, 0.4, 0.4)
BROWN = (0.6, 0.3, 0.0)
DARK_GRAY = (0.3, 0.3, 0.3)
BOX_BG = (0.2, 0.2, 0.2)  # Dark gray for the box background

# Game variables
current_state = STATE_INTRO
mouse_type = None
level = 1
score = 0
start_time = 0
treasures_collected = 0
treasures = []
player_pos = [0, 0]  # [x, y]
player_speed = 0.3

# Level configurations
level_configs = {
    1: {"maze_size": 12, "treasures": 10, "speed": 0.3, "time": 60},
    2: {"maze_size": 15, "treasures": 15, "speed": 0.5, "time": 60},
    3: {"maze_size": 18, "treasures": 20, "speed": 0.8, "time": 60}
}

# Generate mazes for each level
# Hardcoded maze data for levels (0 = path, 1 = wall)
maze_level_1 = [
    [1,0,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,1,0,0,0,1],
    [1,1,1,0,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,0,1]
]

maze_level_2 = [
    [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,1,0,0,1],
    [1,0,0,0,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,0,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,0,1,1,0,1,0,1,1,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,0,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
]

maze_level_3 = [
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,1,1,1,0,0,0,1,1,1,0,1,0,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,1,0,0,1,0,0,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1]
]

mazes = {
    1: maze_level_1,
    2: maze_level_2,
    3: maze_level_3
}


# Current maze
maze = mazes[1]
rows = len(maze)
cols = len(maze)
entry_pos = (1, 1)
exit_pos = (rows-2, cols-2)

# Initialize player position at entry
player_pos = [int(player_pos[0]), int(player_pos[1])]

def initialize_level(level_num):
    global maze, rows, cols, entry_pos, exit_pos, player_pos, player_speed
    global treasures, treasures_collected, start_time, level
    
    level = level_num
    config = level_configs[level]
    
    # Set maze
    maze = mazes[level]
    rows = len(maze)
    cols = len(maze)
    
    # Set entry and exit points
    entry_pos = (1, 1)
    exit_pos = (rows-2, cols-2)
    
    # Set player position and speed
    player_pos = [entry_pos[1], entry_pos[0]]
    player_speed = config["speed"]
    
    # Generate treasures
    treasures = []
    treasures_collected = 0
    
    # Find empty cells
    empty_cells = []
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 0 and (i, j) != entry_pos and (i, j) != exit_pos:
                empty_cells.append((i, j))
    
    # Place treasures
    treasure_count = min(config["treasures"], len(empty_cells))
    treasure_positions = random.sample(empty_cells, treasure_count)
    
    for pos in treasure_positions:
        treasures.append(pos)
    
    # Reset timer
    start_time = time.time()

def draw_maze():
    global maze, rows, cols
    
    # Draw solid floor
    glColor3f(*GRAY)
    glBegin(GL_QUADS)
    glVertex3f(-cols * tile_size / 2, -rows * tile_size / 2, 0)
    glVertex3f(cols * tile_size / 2, -rows * tile_size / 2, 0)
    glVertex3f(cols * tile_size / 2, rows * tile_size / 2, 0)
    glVertex3f(-cols * tile_size / 2, rows * tile_size / 2, 0)
    glEnd()

    # Draw solid walls
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                x = j * tile_size - (cols * tile_size) / 2 + tile_size / 2
         
                y = i * tile_size - (rows * tile_size) / 2 + tile_size / 2
                glColor3f(0.4, 0.3, 0.2)  # Brown wall color
                glPushMatrix()
                glTranslatef(x, y, wall_height / 2)
                glScalef(tile_size - wall_thickness, tile_size - wall_thickness, wall_height)
                glutSolidCube(1)
                glColor3f(0, 0, 0)  # Border
                glutWireCube(1.01)
                glPopMatrix()

def draw_entry_exit():
    global entry_pos, exit_pos, rows, cols
    
    # Entry (green)
    i, j = entry_pos
    x = j * tile_size - (cols * tile_size) / 2 + tile_size / 2
    y = i * tile_size - (rows * tile_size) / 2 + tile_size / 2
    glColor3f(*GREEN)
    glPushMatrix()
    glTranslatef(x, y, 10)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()
    draw_text(x - 20, y - 10, 30, "ENTRY", GREEN)
    
    # Exit (red)
    i, j = exit_pos
    x = j * tile_size - (cols * tile_size) / 2 + tile_size / 2
    y = i * tile_size - (rows * tile_size) / 2 + tile_size / 2
    glColor3f(*RED)
    glPushMatrix()
    glTranslatef(x, y, 15)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()
    draw_text(x - 5, y - 20, 30, "EXIT", RED)
    

def draw_treasures():
    global treasures, rows, cols
    
    for treasure_pos in treasures:
        i, j = treasure_pos
        x = j * tile_size - (cols * tile_size) / 2 + tile_size / 2
        y = i * tile_size - (rows * tile_size) / 2 + tile_size / 2
        
        # Draw cheese (yellow triangle prism)
        glColor3f(*YELLOW)
        glPushMatrix()
        glTranslatef(x, y, 20)
        
        # Base of the cheese (triangle)
        glBegin(GL_TRIANGLES)
        glVertex3f(-15, -15, 0)
        glVertex3f(15, -15, 0)
        glVertex3f(0, 15, 0)
        glEnd()
        
        # Top of the cheese (triangle)
        glBegin(GL_TRIANGLES)
        glVertex3f(-15, -15, 10)
        glVertex3f(15, -15, 10)
        glVertex3f(0, 15, 10)
        glEnd()
        
        # Sides of the cheese (quads)
        glBegin(GL_QUADS)
        # Side 1
        glVertex3f(-15, -15, 0)
        glVertex3f(15, -15, 0)
        glVertex3f(15, -15, 10)
        glVertex3f(-15, -15, 10)
        
        # Side 2
        glVertex3f(15, -15, 0)
        glVertex3f(0, 15, 0)
        glVertex3f(0, 15, 10)
        glVertex3f(15, -15, 10)
        
        # Side 3
        glVertex3f(0, 15, 0)
        glVertex3f(-15, -15, 0)
        glVertex3f(-15, -15, 10)
        glVertex3f(0, 15, 10)
        glEnd()
        
        # Draw holes in cheese (black circles)
        glColor3f(*BLACK)
        glPushMatrix()
        glTranslatef(-5, -5, 10)
        glutSolidSphere(3, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(5, 0, 10)
        glutSolidSphere(3, 8, 8)
        glPopMatrix()
        
        glPopMatrix()

def draw_player():
    global player_pos, rows, cols, mouse_type
    
    j, i = player_pos  # x, y coordinates in the maze
    x = j * tile_size - (cols * tile_size) / 2 + tile_size / 2
    y = i * tile_size - (rows * tile_size) / 2 + tile_size / 2
    
    # Choose mouse color based on type
    if mouse_type == "brown":
        color = BROWN
    else:  # Default to gray
        color = DARK_GRAY
    
    glPushMatrix()
    glTranslatef(x, y, 15)
    
    # Body (big oval)
    glColor3f(*color)
    glPushMatrix()
    glScalef(1.0, 0.7, 0.5)
    glutSolidSphere(15, 20, 20)
    glPopMatrix()
    
    # Head (small oval)
    glPushMatrix()
    glTranslatef(15, 0, 0)
    glScalef(0.8, 0.6, 0.5)
    glutSolidSphere(12, 15, 15)
    glPopMatrix()
    
    # Ears (cones)
    glPushMatrix()
    glTranslatef(18, 10, 5)
    glRotatef(-30, 1, 0, 0)
    glutSolidCone(5, 10, 8, 8)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(18, -10, 5)
    glRotatef(30, 1, 0, 0)
    glutSolidCone(5, 10, 8, 8)
    glPopMatrix()
    
    # Tail (cylinder)
    glPushMatrix()
    glTranslatef(-15, 0, 0)
    glRotatef(90, 0, 1, 0)
    glScalef(0.5, 0.5, 1.0)
    gluCylinder(gluNewQuadric(), 3, 1, 20, 8, 2)
    glPopMatrix()
    
    # Eyes (small black spheres)
    glColor3f(*BLACK)
    glPushMatrix()
    glTranslatef(22, 5, 5)
    glutSolidSphere(3, 8, 8)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(22, -5, 5)
    glutSolidSphere(3, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_ui_text(x, y, text, color=(1, 1, 1)):
    # Fixed text drawing function
    glDisable(GL_DEPTH_TEST)  # Disable depth testing for text
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glEnable(GL_DEPTH_TEST)  # Re-enable depth testing

def draw_ui_box():
    # Save the current matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Disable depth testing for UI elements
    glDisable(GL_DEPTH_TEST)
    
    # Draw the UI box at the top middle of the screen
    box_left = (window_width - ui_box_width) // 2
    box_bottom = window_height - ui_box_height - ui_box_y_offset
    
    # Draw background box
    glColor4f(*BOX_BG, 0.8)  # Dark gray with transparency
    glBegin(GL_QUADS)
    glVertex2f(box_left, box_bottom)
    glVertex2f(box_left + ui_box_width, box_bottom)
    glVertex2f(box_left + ui_box_width, box_bottom + ui_box_height)
    glVertex2f(box_left, box_bottom + ui_box_height)
    glEnd()
    
    # Draw border
    glLineWidth(2.0)  # Make border more visible
    glColor3f(*WHITE)
    glBegin(GL_LINE_LOOP)
    glVertex2f(box_left, box_bottom)
    glVertex2f(box_left + ui_box_width, box_bottom)
    glVertex2f(box_left + ui_box_width, box_bottom + ui_box_height)
    glVertex2f(box_left, box_bottom + ui_box_height)
    glEnd()
    
    # Display text based on game state
    text_x = box_left + 20
    text_y = box_bottom + ui_box_height - 30
    
    if current_state == STATE_INTRO:
        draw_ui_text(text_x, text_y, "TREASURE HUNT", WHITE)
        draw_ui_text(text_x, text_y - 25, "Find all the cheese before time runs out!", WHITE)
        draw_ui_text(text_x, text_y - 50, "Press SPACE to start", WHITE)
    
    elif current_state == STATE_MOUSE_SELECT:
        draw_ui_text(text_x, text_y, "SELECT YOUR MOUSE", WHITE)
        draw_ui_text(text_x, text_y - 25, "Press 1 for Gray Mouse or 2 for Brown Mouse", WHITE)
    
    elif current_state == STATE_GAME:
        # Calculate remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, level_configs[level]["time"] - elapsed_time)
        
        draw_ui_text(text_x, text_y, f"Level: {level}   Score: {score}   Cheese: {treasures_collected}/{level_configs[level]['treasures']}   Time: {int(remaining_time)}s", WHITE)
        draw_ui_text(text_x, text_y - 25, "Use arrow keys to move. Press ESC to end game.", WHITE)
    
    elif current_state == STATE_LEVEL_COMPLETE:
        draw_ui_text(text_x, text_y, "LEVEL COMPLETE!", GREEN)
        draw_ui_text(text_x, text_y - 25, f"Moving to Level {level}", WHITE)
        draw_ui_text(text_x, text_y - 50, "Press SPACE to continue", WHITE)
    
    elif current_state == STATE_GAME_OVER:
        draw_ui_text(text_x, text_y, "GAME OVER", RED)
        draw_ui_text(text_x, text_y - 25, f"Final Score: {score}", WHITE)
        draw_ui_text(text_x, text_y - 50, "Press R to restart or Q to quit", WHITE)
    
    # Re-enable depth testing
    glEnable(GL_DEPTH_TEST)
    
    # Restore matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def draw_text(x, y, z, text, color=(1, 1, 1)):
    # Keep this for backward compatibility
    glColor3f(*color)
    glRasterPos3f(x, y, z)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, window_width / window_height, 0.1, 2000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Bird's-eye view from top, rotating
    radius = 1000
    x = radius * math.cos(math.radians(angle))
    y = radius * math.sin(math.radians(angle))
    gluLookAt(x, y, 1200, 0, 0, 0, 0, 0, 1)

def update_game():
    global current_state, treasures, treasures_collected, score, level

    if current_state == STATE_GAME:
        # Check for treasure collection
        player_i, player_j = int(player_pos[1]), int(player_pos[0])
        
        for treasure_pos in treasures[:]:
            treasure_i, treasure_j = treasure_pos
            if player_i == treasure_i and player_j == treasure_j:
                treasures.remove(treasure_pos)
                treasures_collected += 1
                score += 1
        
        # Check if all treasures are collected
        if len(treasures) == 0:
            if level < 3:
                level += 1
                current_state = STATE_LEVEL_COMPLETE
            else:
                current_state = STATE_GAME_OVER
        
        # Check time limit
        elapsed_time = time.time() - start_time
        if elapsed_time > level_configs[level]["time"]:
            current_state = STATE_GAME_OVER
        
        # Check if player reached exit
        if player_pos[1] == exit_pos[0] and player_pos[0] == exit_pos[1]:
            if level < 3:
                level += 1
                current_state = STATE_LEVEL_COMPLETE
            else:
                current_state = STATE_GAME_OVER

def key_pressed(key, x, y):
    global angle, current_state, mouse_type, level, player_pos, player_speed, score

    # Rotating the view (available in any state)
    if key == b'a':
        angle += 5
    elif key == b'd':
        angle -= 5
    
    # State-specific key handling
    if current_state == STATE_INTRO:
        if key == b' ':  # Space
            current_state = STATE_MOUSE_SELECT
    
    elif current_state == STATE_MOUSE_SELECT:
        if key == b'1':
            mouse_type = "gray"
            current_state = STATE_GAME
            initialize_level(1)
        elif key == b'2':
            mouse_type = "brown"
            current_state = STATE_GAME
            initialize_level(1)
    
    elif current_state == STATE_GAME:
        new_pos = player_pos.copy()
        
        if key == b'\x1b':  # ESC
            current_state = STATE_GAME_OVER
        
        #if key == b'w':
         #  new_pos[1] -= 1
        #elif key == b's':
        #   new_pos[1] += 1
       # elif key == b'a':
       #    new_pos[0] -= 1
      #  elif key == b'd':
        #    new_pos[0] += 1

        # Check if the new position is valid (not a wall)
       # new_i, new_j = int(new_pos[1]), int(new_pos[0])
        #if 0 <= new_i < rows and 0 <= new_j < cols and maze[new_i][new_j] == 0:
         #   player_pos = new_pos
    
    elif current_state == STATE_LEVEL_COMPLETE:
        if key == b' ':  # Space
            initialize_level(level)
            current_state = STATE_GAME
    
    elif current_state == STATE_GAME_OVER:
        if key == b'r':  # Restart
            current_state = STATE_INTRO
            level = 1
            score = 0
        elif key == b'q':  # Quit
            sys.exit(0)
    
    glutPostRedisplay()
    
    
def special_key_pressed(key, x, y):
    global player_pos, player_speed

    if current_state == STATE_GAME:
        new_pos = player_pos.copy()

        if key == GLUT_KEY_UP:
            new_pos[1] -= 1  # Move up (row - 1)
        elif key == GLUT_KEY_DOWN:
            new_pos[1] += 1  # Move down (row + 1)
        elif key == GLUT_KEY_LEFT:
            new_pos[0] += 1  # Move left (col - 1)
        elif key == GLUT_KEY_RIGHT:
            new_pos[0] -= 1  # Move right (col + 1)

        new_i, new_j = int(new_pos[1]), int(new_pos[0])

        # Check bounds and wall collision
        if 0 <= new_i < rows and 0 <= new_j < cols and maze[new_i][new_j] == 0:
            player_pos = new_pos

    glutPostRedisplay()


def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, window_width, window_height)
    
    # Draw 3D maze scene first
    setup_camera()
    
    # Draw game elements only in certain states
    if current_state != STATE_INTRO and current_state != STATE_MOUSE_SELECT:
        update_game()
        draw_maze()
        draw_entry_exit()
        draw_treasures()
        draw_player()
    
    # Draw the fixed UI box overlay after 3D elements
    draw_ui_box()
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Treasure Hunt Game")
    
    # Setup OpenGL state
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glutDisplayFunc(show_screen)
    glutIdleFunc(show_screen)
    glutKeyboardFunc(key_pressed)
    glutSpecialFunc(special_key_pressed)
    
    glutMainLoop()

if __name__ == "__main__":
    main()