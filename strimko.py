import pygame
import sys
from constraint import Problem, AllDifferentConstraint, InSetConstraint

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

CRIMSON = (220, 20, 60)
DODGERBLUE = (30, 144, 255)
YELLOW = (255, 255, 0)
TURQUOISE = (64, 224, 208)
HOTPINK = (255, 105, 180)
LAWNGREEN = (124, 252, 0)
ORANGE_RED = (255, 69, 0)

colorDict = {
    0: CRIMSON,
    1: DODGERBLUE,
    2: YELLOW,
    3: TURQUOISE,
    4: HOTPINK,
    5: LAWNGREEN,
    6: ORANGE_RED
}

WINDOW_HEIGHT = 400
MENU_WIDTH = 200
WINDOW_WIDTH = 400


class Square:
    rectangle = pygame.Rect
    border = pygame.Rect
    route = 0
    value = 0
    color = WHITE
    border_color = BLACK

    def __init__(self, r, v):
        self.route = r
        self.value = v

    def __init__(self, rec, color, border):
        self.rectangle = rec
        self.color = color
        self.border = border


size = int(input('podaj wielkosc lamiglowki: '))

global SCREEN
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH + MENU_WIDTH, WINDOW_HEIGHT))
SCREEN.fill(BLACK)

# menu
font = pygame.font.SysFont('Corbel', 35)

gap = 50
buttonSize = 150
print(font.get_height())

# rendering a text written in
# this font
reset_text = font.render('RESET', True, WHITE)
reset = pygame.Rect(WINDOW_WIDTH + gap, WINDOW_HEIGHT - font.get_height(), buttonSize, font.get_height())

check_text = font.render('CHECK', True, WHITE)
check = pygame.Rect(WINDOW_WIDTH + gap, WINDOW_HEIGHT - 400, buttonSize, font.get_height())


def drawMenu():
    pygame.draw.rect(SCREEN, WHITE, reset, 1)
    SCREEN.blit(reset_text, reset)

    pygame.draw.rect(SCREEN, WHITE, check, 1)
    SCREEN.blit(check_text, check)


blockSize = int(WINDOW_WIDTH / size)  # Set the size of the grid block

numberFont = pygame.font.SysFont('Corbel', blockSize - 20)

fields = [[0 for x in range(size)] for y in range(size)]

for x in range(0, size):
    for y in range(0, size):
        rect = pygame.Rect(y * blockSize + 5, x * blockSize + 5, blockSize - 5, blockSize - 5)
        bor = pygame.Rect(y * blockSize, x * blockSize, blockSize, blockSize)
        # print(x * blockSize, y * blockSize)
        fields[x][y] = Square(rect, WHITE, bor)

print(fields[0][0].rectangle)
print(fields[0][1].rectangle)
print(fields[0][2].rectangle)
print(fields[0][3].rectangle)

def drawGrid():
    for x in range(0, size):
        for y in range(0, size):
            pygame.draw.rect(SCREEN, fields[x][y].color, fields[x][y].rectangle)
            pygame.draw.rect(SCREEN, fields[x][y].border_color, fields[x][y].border, 5)
            if fields[x][y].value != 0:
                num_text = numberFont.render(str(fields[x][y].value), True, BLACK)
                SCREEN.blit(num_text, fields[x][y].rectangle)


def resetGrid():
    for x in range(0, size):
        for y in range(0, size):
            fields[x][y].color = WHITE
            fields[x][y].value = 0
            fields[x][y].route = 0


def solveStrimko(routes, values):
    res = [["." for i in range(size)] for j in range(size)]

    for r in res:
        for c in r:
            print(c, end=" ")
        print()

    S = len(res)
    problem = Problem()
    for route in routes:
        problem.addConstraint(AllDifferentConstraint(), route)
        print(route)

    for x in values:
        res[int(x[0])][int(x[1])] = str(x[2])

    cellnames = [(i, j) for j, row in enumerate(res) for i, val in enumerate(row)]
    lookup = {(i, j): res[i][j] for i, j in cellnames}
    problem.addVariables(cellnames, [str(j) for j in range(1, size + 1)])

    for j in range(size):
        # Columns in grid
        problem.addConstraint(AllDifferentConstraint(), [(i, j) for i in range(size)])
        # Rows in grid
        problem.addConstraint(AllDifferentConstraint(), [(j, i) for i in range(size)])

    for cell, value in lookup.items():
        if value != ".":
            problem.addConstraint(InSetConstraint([str(value)]), [cell])
            print("check")
    print("\n".join(" ".join(lookup[(i, j)] for j in range(size)) for i in range(size)))

    for solution in problem.getSolutions():
        for i in range(0, size):
            for j in range(0, size):
                fields[i][j].value = solution[(i, j)]


route_counter = 0
tile_counter = 0
val = 0

route = []
routes = []
values = []

while True:
    drawGrid()
    drawMenu()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        x = int(pos[1] / blockSize)
        y = int(pos[0] / blockSize)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(x, pos[1])  # oś x
            # print(y, pos[0])  # oś y

            if route_counter < size:
                if tile_counter == size:
                    routes.append(route)
                    print('rc', route_counter)
                    route_counter += 1
                    route = []
                    tile_counter = 0
                if y < size:
                    # if tile_counter == size:

                    if x <= WINDOW_WIDTH and y <= WINDOW_HEIGHT and route_counter < size:
                        # print(tile_counter)
                        fields[x][y].color = colorDict[route_counter]
                        fields[x][y].route = route_counter
                        route.append((x, y))
                        # print(route, route_counter)
                        tile_counter += 1
                    print(tile_counter, size)
            # reset
            if pos[0] >= WINDOW_WIDTH + gap and pos[1] >= WINDOW_HEIGHT - buttonSize:
                resetGrid()
                route_counter = 0
                tile_counter = 0
                routes = []
                values = []
                val = 0
            # check
            if pos[0] >= WINDOW_WIDTH + gap and pos[1] <= buttonSize:
                print('solving')
                for r in routes:
                    print(r)
                solveStrimko(routes, values)

        if event.type == pygame.KEYDOWN:
            if 49 <= event.key <= 55:
                val = event.key - 48
            if val != 0:
                fields[x][y].value = val
                values.append((x, y, val))


        pygame.display.update()

# res = [["." for i in range(size)] for j in range(size)]
#
# for r in res:
#     for c in r:
#         print(c, end=" ")
#     print()
#
# S = len(res)
# problem = Problem()
#
# for j in range(size):
#     array: List[Tuple[Any, Any]] = []
#     x = []
#     route = input('podaj sciezke nr ' + str(j) + ' [rzad, kolumna]: \n')
#     x = re.findall("[0-9]+", route)
#     print(x)
#     for i in range(0, len(x), 2):
#         print(i)
#         array.append((int(x[i]), int(x[i + 1])))
#         print(array)
#     problem.addConstraint(AllDifferentConstraint(), array)
#
# for i in range(size - 1):
#     values = input('uzupelnij wybrane miejsce: \n')
#     x = re.findall("[0-9]+", values)
#     res[int(x[0])][int(x[1])] = x[2]
#
# cellnames = [(i, j) for j, row in enumerate(res) for i, val in enumerate(row)]
# lookup = {(i, j): res[i][j] for i, j in cellnames}
# problem.addVariables(cellnames, [str(j) for j in range(1, size + 1)])
#
# # streams in grid
# # [row,column]
# # problem.addConstraint(AllDifferentConstraint(), [(0, 0), (1, 1), (2, 2), (3, 3)])
# # problem.addConstraint(AllDifferentConstraint(), [(1, 0), (0, 1), (0, 2), (1, 3)])
# # problem.addConstraint(AllDifferentConstraint(), [(2, 0), (3, 1), (3, 2), (2, 3)])
# # problem.addConstraint(AllDifferentConstraint(), [(3, 0), (2, 1), (1, 2), (0, 3)])
#
# for j in range(size):
#     # Columns in grid
#     problem.addConstraint(AllDifferentConstraint(), [(i, j) for i in range(size)])
#     # Rows in grid
#     problem.addConstraint(AllDifferentConstraint(), [(j, i) for i in range(size)])
#
# for cell, value in lookup.items():
#     if value != ".":
#         problem.addConstraint(InSetConstraint([str(value)]), [cell])
#         print("check")
# print("\n".join(" ".join(lookup[(i, j)] for j in range(size)) for i in range(size)))
#
# for solution in problem.getSolutions():
#     print("\n".join(" ".join(solution[(i, j)] for j in range(size)) for i in range(size)))
#     print()
