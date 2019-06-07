import pygame
import random

block = 30
size = 1000, 700

SNAKE_COLOR = (0, 0, 0)
APPLE_COLOR = (100, 255, 80)
INITIAL_SNAKE_SIZE = 7


class Snake(list):
    def next_snake(self, direction, apples):
        tail = self[-1]
        head = self[0]
        next_head = (
            (head[0] + direction[0]) % (size[0] // block),
            (head[1] + direction[1]) % (size[1] // block),
        )

        if next_head in self:
            print("collision dead")
            pygame.quit()
            exit()

        if next_head in apples:
            apples.remove(next_head)
            print(len(self))
            return Snake([next_head] + self)
        return Snake([next_head] + self[:-1])

    def draw(self, surface):
        for s in self:
            pygame.draw.rect(
                surface, SNAKE_COLOR, (s[0] * block, s[1] * block, block, block)
            )


class Apples(list):
    def draw(self, surface):
        for apple in self:
            pygame.draw.rect(
                surface, APPLE_COLOR, (apple[0] * block, apple[1] * block, block, block)
            )

    def generate(self):
        if len(self) >= 4:
            return
        if random.random() > 0.1:
            return
        x = random.randint(1, (size[0] - block) // block)
        y = random.randint(1, (size[1] - block) // block)
        self.append((x, y))

    def degenerate(self):
        if len(self) <= 3:
            return
        if random.random() < 0.01:
            self.remove(self[0])


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


def main():
    global SNAKE_COLOR

    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont("DejaVu", 42)
    pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    srfc = pygame.display.get_surface()

    snake = Snake([(i, 17) for i in range(10, 10 - INITIAL_SNAKE_SIZE, -1)])
    direction = (1, 0)
    apples = Apples([(5, 5)])

    scores = {
        score: myfont.render(f"Score: {score-INITIAL_SNAKE_SIZE}", False, (255, 255, 0))
        for score in range(50)
    }

    while True:
        apples.generate()
        apples.degenerate()

        srfc.fill((0, 0, 0))

        apples.draw(srfc)

        for event in list(pygame.event.get()):
            nd = handle_event(event, direction)
            if nd:
                direction = nd
            break
        snake = snake.next_snake(direction, apples)
        snake.draw(srfc)

        score = scores[len(snake)]
        srfc.blit(score, (800, 20))
        clock.tick(min(len(snake), 30))
        r = min(255, 100 + len(snake) * 5)
        SNAKE_COLOR = r, 255 - r, 255 - r
        pygame.display.flip()


if __name__ == "__main__":
    main()
