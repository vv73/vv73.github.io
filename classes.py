import pygame
import random
import colors
import sys
from abc import ABC, abstractmethod
from utils import draw_text
from enum import auto, Enum

PICTURES = "static"
HIT_DELAY = 200


class PokemonStates(Enum):
    CAUGHT = auto()
    WILD = auto()


class TrainerStates(Enum):
    IDLE = auto()
    FIGHTING = auto()


class BattleStates(Enum):
    NOT_STARTED = -1
    STARTED = 0


class Pokemon(pygame.sprite.Sprite, ABC):
    def __init__(self, name, atk, df, x, y, pic):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = random.randint(1, 5)
        self.vy = random.randint(1, 5)
        self._picture = pygame.image.load(f"{PICTURES}/{pic}").convert_alpha()
        self._picture = pygame.transform.scale(self._picture, (150, 150))
        size = self._picture.get_size()
        self.image = pygame.Surface((size[0], size[1] + 40), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.state = PokemonStates.WILD
        self.name = name
        self.hp = 100
        self.atk = atk
        self.df = df

    def update(self):
        if self.state == PokemonStates.WILD:
            # передвижение
            self.y += self.vy
            self.x -= self.vx

        elif self.state == PokemonStates.CAUGHT:
            # сидит около тренера
            pass
        self.image.fill((255, 255, 255, 0))
        self.rect.center = (self.x, self.y)
        size = self._picture.get_size()
        self.image.blit(self._picture, (0, 0))
        draw_text(
            self.image, colors.WHITE, f"Atk {self.atk} Df {self.df} HP {self.hp}", where=(0, size[1] - 10), font_size=18
        )

    @abstractmethod
    def attack(self, other, damage=None):
        if other.hp <= 0:
            other.hp = 0
            return
        if self.hp <= 0:
            self._hp = 0
            return
        if damage is None:
            damage = self.atk - other.df
        if damage >= 0:
            other.hp -= damage
        else:
            other.hp -= 1

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        if self._hp <= 0:
            self._hp = 0
        return self._hp

    @property
    def atk(self):
        return self._atk

    @property
    def df(self):
        return self._df

    @name.setter
    def name(self, value):
        self._name = value

    @hp.setter
    def hp(self, value):
        self._hp = value

    @atk.setter
    def atk(self, value):
        self._atk = value

    @df.setter
    def df(self, value):
        self._df = value


class WaterPokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super(WaterPokemon, self).__init__(name, atk, df, x, y, "squirtle.png")

    def attack(self, other, **kwargs):
        if isinstance(other, FirePokemon):
            super().attack(other, self.atk * 3 - other.df)
        else:
            super().attack(other)


class FirePokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super().__init__(name, atk, df, x, y, "charmander.png")

    def attack(self, other, **kwargs):
        super().attack(other)


class GrassPokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super().__init__(name, atk, df, x, y, "bulbasaur.png")

    def attack(self, other, **kwargs):
        if isinstance(other, FirePokemon):
            super().attack(other, self.atk - (other.df // 2))
        else:
            super().attack(other)


class ElectricPokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super().__init__(name, atk, df, x, y, "ampharos.png")

    def attack(self, other, **kwargs):
        if isinstance(other, WaterPokemon):
            super().attack(other, self.atk)
        else:
            super().attack(other)


class Trainer(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, pic, scale, fix=0):
        super().__init__()
        self.x = x
        self.y = y
        self._picture = pygame.image.load(f"{PICTURES}/{pic}").convert_alpha()
        self._picture = pygame.transform.scale(self._picture, scale)
        size = self._picture.get_size()
        self.image = pygame.Surface((size[0] + fix, size[1] + 40), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.box = []
        self.wins = 0
        self.state = TrainerStates.IDLE

    def add_pokemon(self, p):
        self.box.append(p)

    @abstractmethod
    def best_team(self, **kwargs):
        pass

    def update(self):
        if self.state == TrainerStates.IDLE:
            # TODO
            pass

        elif self.state == TrainerStates.FIGHTING:
            # TODO
            pass
        self.image.fill((255, 255, 255, 0))
        self.rect.center = (self.x, self.y)
        size = self._picture.get_size()
        self.image.blit(self._picture, (0, 0))
        draw_text(
            self.image, colors.WHITE, f"Wins {self.wins} Poks {len(self.box)}", where=(0, size[1] - 3), font_size=18
        )


class DullTrainer(Trainer):
    def __init__(self, x, y):
        super().__init__(x, y, "trainer.png", (180, 200))

    def best_team(self, n):
        return self.box[:n]


class SmartTrainer(Trainer):
    def __init__(self, x, y):
        super().__init__(x, y, "smart_trainer.png", (100, 200), 25)

    def best_team(self, n):
        # TODO
        pass


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill((255, 255, 0))


class World:
    MAX_POKEMON_ATK = 5
    MAX_POKEMON_DF = 5

    def __init__(self, n_pok, x1, y1, x2, y2):
        self.n_pok = n_pok
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.horBorders = pygame.sprite.Group()
        self.vertBorders = pygame.sprite.Group()
        self.vertBorders.add(Border(x1, y1, x1, y2))
        self.vertBorders.add(Border(x2, y1, x2, y2))
        self.horBorders.add(Border(x1, y1, x2, y1))
        self.horBorders.add(Border(x1, y2, x2, y2))
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        size = self.rect.size
        self.pokemons = pygame.sprite.Group()
        self.trainers = pygame.sprite.Group()
        self.dull_trainer = DullTrainer(size[0] - 100, size[1] - 100)
        self.smart_trainer = SmartTrainer(100, size[1] - 100)
        self._generate_pokemons()
        self._generate_trainers()

    def _generate_trainers(self):
        self.trainers.add(self.dull_trainer)
        self.trainers.add(self.smart_trainer)

    def _generate_pokemons(self):
        for _ in range(self.n_pok):
            pok_pick = random.randint(1, 4)
            if pok_pick == 1:
                self.pokemons.add(WaterPokemon(
                    "wp", random.randint(1, World.MAX_POKEMON_ATK),
                    random.randint(1, World.MAX_POKEMON_DF),
                    random.randint(100, self.rect.right - 100), random.randint(100, self.rect.bottom - 100))
                )
            elif pok_pick == 2:
                self.pokemons.add(
                    FirePokemon(
                        "fp", random.randint(1, World.MAX_POKEMON_ATK),
                        random.randint(1, World.MAX_POKEMON_DF),
                        random.randint(100, self.rect.right - 100), random.randint(100, self.rect.bottom - 100))
                )
            elif pok_pick == 3:
                self.pokemons.add(GrassPokemon(
                    "gp", random.randint(1, World.MAX_POKEMON_ATK),
                    random.randint(1, World.MAX_POKEMON_DF),
                    random.randint(100, self.rect.right - 100), random.randint(100, self.rect.bottom - 100))
                )
            else:
                self.pokemons.add(ElectricPokemon(
                    "ep", random.randint(1, World.MAX_POKEMON_ATK),
                    random.randint(1, World.MAX_POKEMON_DF),
                    self.rect.center[0], self.rect.center[1])
                )

    def draw(self, surface):
        self.horBorders.draw(surface)
        self.vertBorders.draw(surface)
        surface.set_clip(self.rect)
        self.pokemons.draw(surface)
        self.trainers.draw(surface)
        surface.set_clip(None)

    def update(self):
        hor_collision = pygame.sprite.groupcollide(self.pokemons, self.horBorders, False, False)
        for p in hor_collision:
            p.vy = -p.vy
        vert_collision = pygame.sprite.groupcollide(self.pokemons, self.vertBorders, False, False)
        for p in vert_collision:
            p.vx = -p.vx
        self.pokemons.update()
        self.trainers.update()

    def events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                left, mid, right = pygame.mouse.get_pressed(3)
                if mid:
                    break
                caught_pokemon = self._catch_pokemon(pygame.mouse.get_pos())
                if caught_pokemon is not None:
                    if left:
                        self.smart_trainer.add_pokemon(caught_pokemon)
                    else:
                        self.dull_trainer.add_pokemon(caught_pokemon)

    def _catch_pokemon(self, pos):
        for pokemon in self.pokemons:
            if pokemon.rect.collidepoint(pos[0], pos[1]):
                self.pokemons.remove(pokemon)
                return pokemon


class Battle:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y
        self.turn = 1
        self.state = BattleStates.NOT_STARTED

    def draw(self, surface):
        if self.state == BattleStates.NOT_STARTED:
            return
        self.team1.draw(surface)
        self.team2.draw(surface)
        if len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
            pygame.draw.line(surface, (255, 0, 0), self.team1.sprites()[0].rect.midright,
                             self.team2.sprites()[0].rect.midleft, 3)

            hit_circle = pygame.Surface((self.team1.sprites()[0].rect.width, self.team1.sprites()[0].rect.height),
                                        pygame.SRCALPHA)
            pygame.draw.circle(hit_circle, (255, 0, 0, 100), hit_circle.get_rect().center,
                               hit_circle.get_rect().width // 2 - 5, 0)

            if self.turn == 1:
                surface.blit(hit_circle, self.team2.sprites()[0].rect.topleft)
            else:
                surface.blit(hit_circle, self.team1.sprites()[0].rect.topleft)

    def start(self, trainer1, trainer2):
        if self.state == BattleStates.NOT_STARTED:
            self.trainer1 = trainer1
            self.trainer2 = trainer2
            self.team1 = pygame.sprite.Group()
            self.team1.add(trainer1.best_team(self.n))
            self.team2 = pygame.sprite.Group()
            self.team2.add(trainer2.best_team(self.n))
            if len(self.team1) < self.n or len(self.team2) < self.n:
                return

            y = self.y
            for pokemon in self.team1:
                pokemon.rect.topleft = (self.x, y)
                y += pokemon.rect.height + 10
                pokemon.vx = pokemon.vy = 0
            y = self.y
            for pokemon in self.team2:
                pokemon.rect.topleft = (self.x + 280, y)
                y += pokemon.rect.height + 10
                pokemon.vx = pokemon.vy = 0
            self.state = BattleStates.STARTED
            self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.state == BattleStates.STARTED:
            now_time = pygame.time.get_ticks()
            if now_time - self.last_update > HIT_DELAY:
                self.last_update = now_time
            else:
                return
            if self.turn == 1 and len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
                self.team1.sprites()[0].attack(self.team2.sprites()[0])
                if self.team2.sprites()[0].hp <= 0:
                    self.team2.remove(self.team2.sprites()[0])
                if len(self.team2.sprites()) == 0:
                    return self.finish(1)
            elif self.turn == 2 and len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
                self.team2.sprites()[0].attack(self.team1.sprites()[0])
                if self.team1.sprites()[0].hp <= 0:
                    self.team1.remove(self.team1.sprites()[0])
                if len(self.team1.sprites()) == 0:
                    return self.finish(2)
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
            self.team1.update()
            self.team2.update()

    def finish(self, result):
        self.state = BattleStates.NOT_STARTED
        for p in self.team1:
            self.trainer1.add(p)
        for p in self.team2:
            self.trainer2.add(p)
        if result == 1:
            self.trainer1.wins += 1
        else:
            self.trainer2.wins += 1

    def started(self):
        return True if self.state == BattleStates.STARTED else False
