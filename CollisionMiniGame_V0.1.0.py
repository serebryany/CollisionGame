import pygame
import sys
import math

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
    def __init__(self, atoms, position, angle=0):
        self.atoms = atoms  # List of (color, offset_x, offset_y)
        self.position = position  # (x, y)
        self.angle = angle  # Rotation angle in radians
        self.selected = False
        self.moving = False

    def draw(self, screen):
        for color, dx, dy in self.atoms:
            x = self.position[0] + dx * math.cos(self.angle) - dy * math.sin(self.angle)
            y = self.position[1] + dx * math.sin(self.angle) + dy * math.cos(self.angle)
            pygame.draw.circle(screen, color, (int(x), int(y)), 20)
        if self.selected:
            pygame.draw.circle(screen, BLUE, (int(self.position[0]), int(self.position[1])), 40, 2)

    def rotate(self, angle):
        self.angle += angle

    def move(self, dx, dy, other_molecule=None):
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Prevent moving off-screen
        if 0 < new_x < WIDTH and 0 < new_y < HEIGHT:
            # Prevent overlapping with other molecule
            if other_molecule:
                if not self.is_colliding(other_molecule, new_x, new_y):
                    self.position = (new_x, new_y)
            else:
                self.position = (new_x, new_y)

    def is_colliding(self, other_molecule, new_x, new_y):
        # Check if two molecules are too close
        for _, dx1, dy1 in self.atoms:
            x1 = new_x + dx1 * math.cos(self.angle) - dy1 * math.sin(self.angle)
            y1 = new_y + dx1 * math.sin(self.angle) + dy1 * math.cos(self.angle)

            for _, dx2, dy2 in other_molecule.atoms:
                x2 = other_molecule.position[0] + dx2 * math.cos(other_molecule.angle) - dy2 * math.sin(other_molecule.angle)
                y2 = other_molecule.position[1] + dx2 * math.sin(other_molecule.angle) + dy2 * math.cos(other_molecule.angle)

                # Check if the distance between the atoms is less than a threshold (collision radius)
                if math.hypot(x1 - x2, y1 - y2) <= 40:  # This threshold can be adjusted
                    return True
        return False

    def is_clicked(self, mouse_pos):
        for _, dx, dy in self.atoms:
            x = self.position[0] + dx * math.cos(self.angle) - dy * math.sin(self.angle)
            y = self.position[1] + dx * math.sin(self.angle) + dy * math.cos(self.angle)
            if math.hypot(mouse_pos[0] - x, mouse_pos[1] - y) <= 20:
                return True
        return False

    def get_atoms_positions(self):
        positions = []
        for color, dx, dy in self.atoms:
            x = self.position[0] + dx * math.cos(self.angle) - dy * math.sin(self.angle)
            y = self.position[1] + dx * math.sin(self.angle) + dy * math.cos(self.angle)
            positions.append((x, y))
        return positions

# Create molecules
co_molecule = Molecule([(GREY, -20, 0), (RED, 20, 0)], (200, 300))
o2_molecule = Molecule([(RED, -20, 0), (RED, 20, 0)], (600, 300))

# Restart button
restart_button = pygame.Rect(WIDTH - 120, 10, 100, 40)

# Main game loop
clock = pygame.time.Clock()
selected_molecule = None
reaction_occurred = False
co2_molecule = None
remaining_o_atom = None

while True:
    screen.fill(WHITE)

    # Draw legend
    font = pygame.font.Font(None, 24)
    screen.blit(font.render("Controls:", True, BLACK), (10, 10))
    screen.blit(font.render("Arrow Keys - Move", True, BLACK), (10, 30))
    screen.blit(font.render("R - Rotate Right", True, BLACK), (10, 50))
    screen.blit(font.render("E - Rotate Left", True, BLACK), (10, 70))
    screen.blit(font.render("Molecules:", True, BLACK), (10, 100))
    pygame.draw.circle(screen, GREY, (20, 123), 7)
    screen.blit(font.render("Carbon (C)", True, BLACK), (40, 115))
    pygame.draw.circle(screen, RED, (20, 143), 7)
    screen.blit(font.render("Oxygen (O)", True, BLACK), (40, 135))

    # Draw restart button
    pygame.draw.rect(screen, GREY, restart_button, border_radius=10)
    text = font.render("Restart", True, BLACK)
    screen.blit(text, (WIDTH - 110, 20))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click to select a molecule or restart
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_pos):
                co_molecule = Molecule([(GREY, -20, 0), (RED, 20, 0)], (200, 300))
                o2_molecule = Molecule([(RED, -20, 0), (RED, 20, 0)], (600, 300))
                co2_molecule = None
                remaining_o_atom = None
                selected_molecule = None
                reaction_occurred = False
            elif not reaction_occurred:
                if co_molecule.is_clicked(mouse_pos):
                    selected_molecule = co_molecule
                    o2_molecule.selected = False
                    co_molecule.selected = True
                elif o2_molecule.is_clicked(mouse_pos):
                    selected_molecule = o2_molecule
                    co_molecule.selected = False
                    o2_molecule.selected = True

        # Rotate selected molecule
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and selected_molecule:
                selected_molecule.rotate(math.radians(10))
            if event.key == pygame.K_e and selected_molecule:
                selected_molecule.rotate(math.radians(-10))

    # Move selected molecule with arrow keys
    keys = pygame.key.get_pressed()
    if selected_molecule:
        if keys[pygame.K_UP]:
            selected_molecule.move(0, -5, o2_molecule if selected_molecule == co_molecule else co_molecule)
        if keys[pygame.K_DOWN]:
            selected_molecule.move(0, 5, o2_molecule if selected_molecule == co_molecule else co_molecule)
        if keys[pygame.K_LEFT]:
            selected_molecule.move(-5, 0, o2_molecule if selected_molecule == co_molecule else co_molecule)
        if keys[pygame.K_RIGHT]:
            selected_molecule.move(5, 0, o2_molecule if selected_molecule == co_molecule else co_molecule)

    # Reaction condition: carbon atom from CO and oxygen atoms from O2 need to align horizontally and be close enough
    co_atoms = co_molecule.get_atoms_positions()
    o2_atoms = o2_molecule.get_atoms_positions()

    # Check if the molecules are aligned horizontally
    for co_x, co_y in co_atoms:
        for o2_x, o2_y in o2_atoms:
            if abs(co_y - o2_y) <= 10 and abs(co_x - o2_x) <= 40:  # Adjust this threshold as needed
                # Trigger the reaction
                if not reaction_occurred:
                    reaction_occurred = True
                    co2_molecule = Molecule([(GREY, 0, 0), (RED, -25, 0), (RED, 25, 0)], ((co_molecule.position[0] + o2_molecule.position[0]) // 2, (co_molecule.position[1] + o2_molecule.position[1]) // 2))
                    remaining_o_atom = (o2_molecule.position[0] + 30, o2_molecule.position[1])

    # Draw molecules
    if not reaction_occurred:
        co_molecule.draw(screen)
        o2_molecule.draw(screen)
    elif co2_molecule:
        co2_molecule.draw(screen)
        pygame.draw.circle(screen, RED, (remaining_o_atom[0], remaining_o_atom[1]), 20)
    
    pygame.display.flip()
    clock.tick(60)
