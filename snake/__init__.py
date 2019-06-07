import pygame
import random

block = 30
size = 1000, 700

SNAKE_COLOR = (0, 0, 0)
APPLE_COLOR = (100, 255, 80)
INITIAL_SNAKE_SIZE = 7


def next_snake(snake, direction, apples):
    tail = snake[-1]
    head = snake[0]
    next_head = (
        (head[0] + direction[0]) % (size[0] // block),
        (head[1] + direction[1]) % (size[1] // block),
    )

    if next_head in snake:
        score = len(snake) - INITIAL_SNAKE_SIZE
        print("You eat yourself.\nScore: {}".format(score))
        pygame.quit()
        exit()

    if next_head in apples:
        apples.remove(next_head)
        return [next_head] + snake
    return [next_head] + snake[:-1]


def draw_snake(snake, surface):
    for s in snake:
        pygame.draw.rect(
            surface, SNAKE_COLOR, (s[0] * block, s[1] * block, block, block)
        )


def draw_apples(apples, surface):
    for apple in apples:
        pygame.draw.rect(
            surface, APPLE_COLOR, (apple[0] * block, apple[1] * block, block, block)
        )


def generate(apples):
    if len(apples) >= 4:
        return
    if random.random() > 0.1:
        return
    x = random.randint(1, (size[0] - block) // block)
    y = random.randint(1, (size[1] - block) // block)
    apples.append((x, y))


def degenerate(apples):
    if len(apples) <= 3:
        return
    if random.random() < 0.01:
        apples.remove(apples[0])


def get_dir(key, direction):
    if key in (pygame.K_w, pygame.K_UP):
        if direction == (0, 1):
            return
        return (0, -1)
    if key in (pygame.K_a, pygame.K_LEFT):
        if direction == (1, 0):
            return
        return (-1, 0)
    if key in (pygame.K_s, pygame.K_DOWN):
        if direction == (0, -1):
            return
        return (0, 1)
    if key in (pygame.K_d, pygame.K_RIGHT):
        if key == (-1, 0):
            return
        return (1, 0)


def handle_event(event, direction):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit(0)
    if event.type == pygame.KEYDOWN:
        key = event.key
        if key in (pygame.K_q, pygame.K_ESCAPE):
            pygame.quit()
            exit(0)
        else:
            d = get_dir(key, direction)
            if d:
                return d


def game_loop(snake, apples, srfc, clock):
    global SNAKE_COLOR
    direction = (1, 0)
    myfont = pygame.font.SysFont("DejaVu", 42)
    scores = {
        score: myfont.render(
            "Score: {}".format(score - INITIAL_SNAKE_SIZE), False, (255, 255, 0)
        )
        for score in range(50)
    }
    while True:
        generate(apples)
        degenerate(apples)

        srfc.fill((0, 0, 0))

        draw_apples(apples, srfc)

        for event in list(pygame.event.get()):
            nd = handle_event(event, direction)
            if nd:
                direction = nd
            break
        snake = next_snake(snake, direction, apples)
        draw_snake(snake, srfc)

        score = scores[len(snake)]
        srfc.blit(score, (800, 20))
        clock.tick(min(len(snake), 30))
        r = min(255, 100 + len(snake) * 5)
        SNAKE_COLOR = r, 255 - r, 255 - r
        pygame.display.flip()


def main():
    pygame.init()
    pygame.font.init()

    pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    srfc = pygame.display.get_surface()

    snake = [(i, 17) for i in range(10, 10 - INITIAL_SNAKE_SIZE, -1)]
    apples = [(5, 5)]

    game_loop(snake, apples, srfc, clock)


if __name__ == "__main__":
    main()
