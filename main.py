import colors
import pygame
import sys

from utils import draw_text
from classes import (
    World,
    PICTURES,
    Battle,
    SIZE
)

FPS = 60
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.mixer.music.load(f"{PICTURES}/105-recruiting.ogg")
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pokemons by arsikurin [RECRUITING]")
clock = pygame.time.Clock()
world = World(20, 0, 0, SIZE[0] - 1, SIZE[1] - 201)
battle = Battle(4, 10, 120)
try:
    while True:
        screen.fill(colors.BLACK)
        world.draw(screen)
        battle.draw(screen)
        world.update()
        battle.update()
        if not battle.is_started() and not battle.is_finished():
            draw_text(
                screen, colors.YELLOW, "Press B key to start the battle!", where=(SIZE[0] // 3, SIZE[1] - 150), font_size=26
            )
        world.events_handler(screen, battle, world)
        pygame.display.flip()
        clock.tick(FPS)
        if len(world.pokemons) == 0:
            battle.start(world)
        if battle.is_finished():
            break
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()

pygame.mixer.music.load(f"{PICTURES}/116-victory.ogg")
pygame.mixer.music.play(-1)
pygame.display.set_caption("Pokemons by arsikurin [FINISHED]")
screen.fill(colors.BLACK)
if battle.smart_trainer.wins:
    draw_text(screen, colors.GREEN, "Smart trainer won!", where=(SIZE[0] // 2 - 150, SIZE[1] // 2), font_size=40)
else:
    draw_text(screen, colors.GREEN, "Dull trainer won!", where=(SIZE[0] // 2 - 150, SIZE[1] // 2), font_size=40)
pygame.display.flip()

while True:
    world.events_handler(screen, battle, world)
