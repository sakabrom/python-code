import random
import curses
import time

# Taille de la carte
MAP_WIDTH = 20
MAP_HEIGHT = 10

# Variables du joueur
player_pos = [MAP_HEIGHT // 2, MAP_WIDTH // 2]  # Position initiale du joueur
player_symbol = "O"

# Variables des monstres
monster_symbol = "X"
monsters = []

# Murs de la carte
walls = [(x, y) for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT) if
         x == 0 or x == MAP_WIDTH - 1 or y == 0 or y == MAP_HEIGHT - 1]


# Fonction pour afficher la carte
def print_map(stdscr):
    stdscr.clear()  # Clear the screen

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if (x, y) in walls:
                stdscr.addstr(y, x * 2, "#")  # Afficher les murs
            elif [y, x] == player_pos:
                stdscr.addstr(y, x * 2, player_symbol)  # Afficher le joueur
            elif any(monster[0] == y and monster[1] == x for monster in monsters):
                stdscr.addstr(y, x * 2, monster_symbol)  # Afficher les monstres
            else:
                stdscr.addstr(y, x * 2, " ")  # Case vide

    stdscr.refresh()


# Fonction pour déplacer le joueur
def move_player(direction):
    global player_pos
    new_pos = player_pos[:]

    if direction == 'z':  # Haut
        new_pos[0] -= 1
    elif direction == 's':  # Bas
        new_pos[0] += 1
    elif direction == 'q':  # Gauche
        new_pos[1] -= 1
    elif direction == 'd':  # Droite
        new_pos[1] += 1

    # Vérifier que le nouveau déplacement ne sort pas de la carte ou ne touche pas un mur
    if (new_pos[0], new_pos[1]) not in walls:
        player_pos = new_pos


# Fonction pour spawn des monstres
def spawn_monsters():
    while len(monsters) < 5:  # Limiter le nombre de monstres à 5
        monster_pos = [random.randint(1, MAP_HEIGHT - 2), random.randint(1, MAP_WIDTH - 2)]
        if monster_pos not in walls and monster_pos not in monsters:
            monsters.append(monster_pos)


# Main game loop
def game(stdscr):
    spawn_monsters()  # Spawn initial des monstres

    # Désactiver le curseur pour éviter qu'il clignote
    curses.curs_set(0)

    while True:
        print_map(stdscr)
        move = stdscr.getkey()  # Obtenir une touche du joueur

        if move in ['z', 's', 'q', 'd']:
            move_player(move)

        spawn_monsters()  # Faire apparaître des monstres à chaque tour

        time.sleep(0.1)  # Petit délai pour ne pas trop solliciter le terminal


if __name__ == "__main__":
    curses.wrapper(game)

