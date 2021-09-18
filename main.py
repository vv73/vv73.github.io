from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import colors
import sys

from classes import (
    World
)

FPS = 60
SIZE = (1200, 1000)
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.mixer.init()
pygame.display.set_caption("Pokemons by arsikurin")
clock = pygame.time.Clock()
world = World(20, 0, 0, 1199, 799)

try:
    while True:
        world.events_handler()
        screen.fill(colors.BLACK)
        world.draw(screen)
        world.update()
        pygame.display.flip()
        clock.tick(FPS)
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()

# Сражаются команды по N покемонов
battle = Battle(5, 10, 120)

# Цикл игры
running = True
ntrainer = 0
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if len(world.pokemons) == 0 and not battle.started():
                world.generate_pokemones()
            else:
                pokemon = world.catch_pokemon(e.pos)
                if pokemon is not None:
                    trainers[ntrainer].add(pokemon)
                    ntrainer += 1
                    ntrainer %= len(trainers)
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                pass

    # Рендеринг
    screen.fill((0, 0, 0))
    world.draw(screen)
    trainers_g.draw(screen)
    battle.draw(screen)

    # После отрисовки всего, переворачиваем экран

    pygame.display.flip()
    clock.tick(FPS)

    # Обновление
    world.update()
    battle.update()
    trainers_g.update()

    if len(world.pokemons) == 0:
        battle.start(trainers[0], trainers[1])

pygame.quit()
