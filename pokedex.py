import pypokedex as pokedex
from pokebase import pokemon_species
import pygame
import sys
import requests
import io
import math
import random
import time
pygame.init()

WIN_HEIGHT = 800
WIN_WIDTH = 600

session = requests.Session()

font_title = pygame.font.SysFont('flexo-medium', 60)
font_normal = pygame.font.SysFont('flexo-medium', 40)

arrow_img = pygame.image.load('.\\sprites\\arrow.png')
buttonR_img = pygame.transform.scale(arrow_img, (100,100))
buttonL_img = pygame.transform.flip(buttonR_img, 1, 0)
buttonRandom_img = pygame.image.load('.\\sprites\\dice.png')
buttonRandom_img = pygame.transform.scale(buttonRandom_img, (100, 100))

buttonL_pos = (0, 200)
buttonR_pos = (WIN_WIDTH-100, 200)
buttonRandom_pos = (500, 0)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.NOFRAME)
# uncomment if want frame:
# pygame.display.set_caption('Pokedex - By LegendLeaks')
# window_icon = pygame.image.load('.\\sprites\\logo.png')
# pygame.display.set_icon(window_icon)

# colours: 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def get_pokemon_category(pokemon_id):
    try:
        poke_species = pokemon_species(pokemon_id)
        if poke_species:
            category = poke_species.genera[7].genus  # index 7 = english
            return category
    except Exception as e:
        print("Error fetching category:", e)
        return 'Unknown Pokemon'

def display_pokemon_sprite(pokemon):
    sprite_link = pokemon.sprites.front['default']
    
    response = session.get(sprite_link)
    image = pygame.image.load(io.BytesIO(response.content))
    image = pygame.transform.scale(image, (500, 500)) # aspect ratio for sprites is 1:1

    window.blit(image, (50, -25))

def display_pokemon_name(pokemon):
    label_name = font_title.render(f'{pokemon.name.capitalize()}#{pokemon.dex}', 1, BLACK)
    label_name_rect = label_name.get_rect(center=(WIN_WIDTH/2, 450))
    # above line gets coords to center text
    window.blit(label_name, label_name_rect)

def display_pokemon_type(pokemon):
    if len(pokemon.types) == 1: # pokemon has only 1 type
        type1 = pygame.image.load(f'.\\sprites\\type_{pokemon.types[0]}.png')

        type1_rect = type1.get_rect(center=(WIN_WIDTH/2, 520))
        window.blit(type1, type1_rect)
    else: # pokemon has 2 types
        type1 = pygame.image.load(f'.\\sprites\\type_{pokemon.types[0]}.png')
        type2 = pygame.image.load(f'.\\sprites\\type_{pokemon.types[1]}.png')

        type1_rect = type1.get_rect(center=(WIN_WIDTH/2 - 115, 520))
        type2_rect = type2.get_rect(center=(WIN_WIDTH/2 + 115, 520))

        window.blit(type1, type1_rect)
        window.blit(type2, type2_rect)

def display_pokemon_info(pokemon):
    # blue rectangle for text background:
    blue_bg = pygame.image.load('.\\sprites\\blue_rect.png')
    blue_bg = pygame.transform.scale(blue_bg, (575, 240)) # transform
    blue_bg_rect = blue_bg.get_rect(center=(WIN_WIDTH/2, 675)) # get x/y pos

    window.blit(blue_bg, blue_bg_rect)

    # text:
    #   height:
    label_height = font_normal.render('Height', 1, WHITE)
    height = pokemon.height # in decimeters
    height_feet = math.floor(height/3.048)
    height_inches = math.floor((height/3.048 - height_feet) * 12)
    label_height_value = font_normal.render(f'{height_feet}\' {height_inches:02}\"', 1, BLACK)
    window.blit(label_height, (45, 580))
    window.blit(label_height_value, (45, 620))

    #   category:
    label_category = font_normal.render('Category', 1, WHITE)
    category = get_pokemon_category(pokemon.dex)[:-8]
    label_category_value = font_normal.render(category, 1, BLACK)
    window.blit(label_category, (350, 580))
    window.blit(label_category_value, (350, 620))

    # weight
    label_weight = font_normal.render('Weight', 1, WHITE)
    weight = round(pokemon.weight / 4.536, 1) # converted hectograms to lbs
    label_weight_value = font_normal.render(f'{weight} lbs', 1, BLACK)
    window.blit(label_weight, (45, 700))
    window.blit(label_weight_value, (45, 740))
    
    # ability
    label_ability = font_normal.render('Ability', 1, WHITE)
    label_ability_value = font_normal.render(pokemon.abilities[0].name.capitalize(), 1, BLACK)
    window.blit(label_ability, (350, 700))
    window.blit(label_ability_value, (350, 740))

def display_buttons():
    window.blit(buttonL_img,buttonL_pos)
    window.blit(buttonR_img,buttonR_pos)
    window.blit(buttonRandom_img, buttonRandom_pos)

def display_page(dex):
    window.fill(WHITE)
    pokemon = pokedex.get(dex=dex)

    display_pokemon_sprite(pokemon)
    display_pokemon_name(pokemon)
    display_pokemon_type(pokemon)
    display_pokemon_info(pokemon)
    display_buttons()



def main(): # main pygame loop
    run = True
    clock = pygame.time.Clock()
    r = 1
    clicked = True

    display_page(1)
    pygame.display.update()

    while run:
        pygame.event.pump()
        x, y = pygame.mouse.get_pos()
        L, M, R = pygame.mouse.get_pressed()
        
        
        if (clicked and L and (x <= buttonL_pos[0]+100 and x >= buttonL_pos[0] and y <= buttonL_pos[1]+100 and y >= buttonL_pos[1]) and r > 1):
            r -= 1
            clicked = False
            display_page(r)
            pygame.display.update()
        elif (clicked and L and (x <= buttonR_pos[0]+100 and x >= buttonR_pos[0] and y <= buttonR_pos[1]+100 and y >= buttonR_pos[1]) and r < 1017):
            r += 1
            clicked = False
            display_page(r)
            pygame.display.update()
        elif (clicked and L and (x <= buttonRandom_pos[0]+100 and x >= buttonRandom_pos[0] and y <= buttonRandom_pos[1]+100 and y >= buttonRandom_pos[1])):
            r = random.randint(1,1010)
            clicked = False
            display_page(r)
            pygame.display.update()
        elif (not clicked and not L):
            clicked = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:    #quit window
                pygame.quit()
                sys.exit()
        #clock.tick(60)

main()





def pokemon_lookup():
    print("Enter the name or ID# of any pokemon:")
    p = input()

    try:
        int(p)
        pokemon = pokedex.get(dex=p)
    except:
        pokemon = pokedex.get(name=p)

    print(f"Name: {pokemon.name}")
    print(f"Ability: {pokemon.abilities[0].name}")
    print(f"Type: {', '.join(type for type in pokemon.types)}")
    # print(dir(pokemon))
    # print(pokemon.sprites)
    print(pokemon.get_descriptions(language="en")["red"])