import pygame
import math
pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Planet Sim")

# COLORS & FONT
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 30, 250)
RED = (240, 25, 10)
DARK_GREY = (200, 200, 200)
BROWN = (139, 125, 130)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Courier", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU # 1AU = 100px
    TIMESTEP = 3600 * 24 # 1 day


    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.dist_to_sun = 0

        self.vel_x = 0
        self.vel_y = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        updated_points = []
        if len(self.orbit) > 2:
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            dist_text = FONT.render(f"{round(self.dist_to_sun/1000)}Km", 1, WHITE)
            win.blit(dist_text, (x - dist_text.get_width() / 2, y - dist_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        dist_x = other_x - self.x
        dist_y = other_y - self.y
        dist = math.sqrt(dist_x**2 + dist_y**2)
        
        if other.sun:
            self.dist_to_sun = dist
        force = self.G * self.mass * other.mass / dist**2
        theta = math.atan2(dist_y, dist_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)

        return force_x, force_y
    
    def update_pos(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.vel_x += total_fx / self.mass * self.TIMESTEP
        self.vel_y += total_fy / self.mass * self.TIMESTEP

        self.x += self.vel_x * self.TIMESTEP
        self.y += self.vel_y * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.988892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.vel_y = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, 0, 14, BROWN, 4.8685 * 10**24)
    venus.vel_y = -35.02 * 1000
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.vel_y = 29.783 * 1000 
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.vel_y = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(70)
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_pos(planets)
            planet.draw(WIN)
        
        pygame.display.update()


    pygame.quit()


main()
