import pygame
import sys
import math

"""
move these init variables to a function called main
"""
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Theory Mini-Game")

# Colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Molecule properties
class Molecule:
    def __init__(self, atoms:list[tuple], position:tuple, angle=0):
        self.atoms = atoms  # List of (color, offset_x, offset_y)
        self.position = position  # (x, y)
        self.angle = angle  # Rotation angle in radians
        self.selected = False
        self.exists = True  # Used to check if the molecule should still be displayed

    def draw(self, screen:pygame.display):
        if self.exists:
            for color, dx, dy in self.atoms:
                x = self.position[0] + dx * math.cos(self.angle) - dy * math.sin(self.angle)
                y = self.position[1] + dx * math.sin(self.angle) + dy * math.cos(self.angle)
                pygame.draw.circle(screen, color, (int(x), int(y)), 20)
            if self.selected:
                pygame.draw.circle(screen, BLUE, (int(self.position[0]), int(self.position[1])), 30, 3)
    
    def rotate(self, angle):
        self.angle += angle

    def move(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def is_clicked(self, mouse_pos):
        for _, dx, dy in self.atoms:
            x = self.position[0] + dx * math.cos(self.angle) - dy * math.sin(self.angle)
            y = self.position[1] + dx * math.sin(self.angle) + dy * math.cos(self.angle)
            if math.hypot(mouse_pos[0] - x, mouse_pos[1] - y) <= 20:
                return True
        return False

# Create molecules
"""these also all go to main"""
co_molecule = Molecule([(GREY, -20, 0), (RED, 20, 0)], (200, 300))
o2_molecule = Molecule([(RED, -20, 0), (RED, 20, 0)], (600, 300))
co2_molecule = None
extra_o_atom = None

# Main game loop
"""and this"""
clock = pygame.time.Clock()
selected_molecule = None
reaction_occurred = False

"""this loop can be its own function"""
while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click to select a molecule
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if co_molecule.exists and co_molecule.is_clicked(mouse_pos):
                selected_molecule = co_molecule
                o2_molecule.selected = False #not 
                co_molecule.selected = True
            elif o2_molecule.exists and o2_molecule.is_clicked(mouse_pos):
                selected_molecule = o2_molecule
                co_molecule.selected = False
                o2_molecule.selected = True

        # Rotate selected molecule
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and selected_molecule:
                selected_molecule.rotate(math.radians(10))  # Rotate right
            if event.key == pygame.K_l and selected_molecule:
                selected_molecule.rotate(math.radians(-10))  # Rotate left

    # Move selected molecule with arrow keys
    keys = pygame.key.get_pressed()
    if selected_molecule:
        if keys[pygame.K_UP]:
            selected_molecule.move(0, -5)
        if keys[pygame.K_DOWN]:
            selected_molecule.move(0, 5)
        if keys[pygame.K_LEFT]:
            selected_molecule.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            selected_molecule.move(5, 0)

    # Draw molecules
    co_molecule.draw(screen)
    o2_molecule.draw(screen)
    if co2_molecule:
        co2_molecule.draw(screen)
    if extra_o_atom:
        extra_o_atom.draw(screen)

    # Check for reaction (CO:O2 configuration)
    if co_molecule.exists and o2_molecule.exists:
        co_atoms = [(co_molecule.position[0] + dx * math.cos(co_molecule.angle) - dy * math.sin(co_molecule.angle),
                     co_molecule.position[1] + dx * math.sin(co_molecule.angle) + dy * math.cos(co_molecule.angle))
                    for _, dx, dy in co_molecule.atoms]
        o2_atoms = [(o2_molecule.position[0] + dx * math.cos(o2_molecule.angle) - dy * math.sin(o2_molecule.angle),
                     o2_molecule.position[1] + dx * math.sin(o2_molecule.angle) + dy * math.cos(o2_molecule.angle))
                    for _, dx, dy in o2_molecule.atoms]
        
        if math.hypot(co_atoms[1][0] - o2_atoms[0][0], co_atoms[1][1] - o2_atoms[0][1]) < 40:
            font = pygame.font.Font(None, 74)
            text = font.render("CO2 Formed!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
            co_molecule.exists = False
            o2_molecule.exists = False
            co2_molecule = Molecule([(RED, -20, 0), (GREY, 0, 0), (RED, 20, 0)], (400, 300))
            extra_o_atom = Molecule([(RED, 0, 0)], (500, 300))

    # Display key instructions
    font = pygame.font.Font(None, 24)
    instructions = ["Arrow Keys: Move", "R: Rotate Right", "L: Rotate Left", "Click: Select Molecule"]
    color_info = ["Grey: Carbon (C)", "Red: Oxygen (O)"]
    y_offset = 10
    for line in instructions + color_info:
        text = font.render(line, True, BLACK)
        screen.blit(text, (10, y_offset))
        y_offset += 20

    # Update display
    pygame.display.flip()
    clock.tick(60)
