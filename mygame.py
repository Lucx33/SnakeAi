import pygame
import random
import numpy as np

SPEED = 500
STUCK = 300

compass = ['UP', 'RIGHT', 'DOWN', 'LEFT']

# reset
# reward
# play (action) -> direction
# game_iteration
# is_collision

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = [random.randrange(1, (self.width//10)) * 10, random.randrange(1, (self.height//10)) * 10]
        self.food_spawn = True

        self.record = 0

        self.direction = compass[1] # RIGHT
        self.change_to = self.direction
        self.score = 0

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.frame_iteration = 0
        self.movestoapple = 0

    def play_step(self, action):
        reward = 0
        self.frame_iteration += 1
        self.movestoapple += 1
        # Collecting user input or AI action
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.change_to = 'RIGHT'
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.change_to = 'DOWN'
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        facing = compass.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            self.change_to = self.direction
        elif np.array_equal(action, [0, 1, 0]):
            self.change_to = compass[(facing + 1) % 4]
        elif np.array_equal(action, [0, 0, 1]):
            self.change_to = compass[(facing - 1) % 4]



        # Making sure the snake cannot move in the opposite direction instantaneously
        self.direction = self.change_to

        # Move the snake
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10
        elif self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif self.direction == 'UP':
            self.snake_pos[1] -= 10
        elif self.direction == 'DOWN':
            self.snake_pos[1] += 10

        # Snake body mechanics
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.score += 1
            if self.score > self.record:
                self.record = self.score
                reward = 10
            else:
                reward = 5
            if(self.movestoapple < 5000):
                reward += 5
            self.food_spawn = False
            self.movestoapple = 0
        else:
            self.snake_body.pop()

        # Food spawn
        if not self.food_spawn:
            while True:
                self.food_pos = [random.randrange(1, (self.width // 10)) * 10, random.randrange(1, (self.height // 10)) * 10]
                if self.food_pos not in self.snake_body[1:]:
                    break
            self.food_spawn = True

        # Game over conditions
        if ((self.snake_pos[0] >= self.width or self.snake_pos[0] < 0 or
                self.snake_pos[1] >= self.height or self.snake_pos[1] < 0 or
                self.snake_pos in self.snake_body[1:])):
            reward = -5
            return reward, True, self.score
        elif self.movestoapple > (STUCK * len(self.snake_pos)):
            reward = -10
            return reward, True, self.score

        # Drawing everything on the screen
        self.screen.fill((0, 0, 0))
        for pos in self.snake_body:
            pygame.draw.rect(self.screen, (34,139,34), pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 7, 7))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))


        moves_text = self.font.render(f'Moves: {self.frame_iteration}', True, (255, 255, 255))
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(moves_text, [0, 0])
        self.screen.blit(score_text, [0, 20])
        pygame.display.flip()
        self.clock.tick(SPEED)
        return reward, False, self.score

    def reset(self):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = [random.randrange(1, (self.width//10)) * 10, random.randrange(1, (self.height//10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.frame_iteration = 0
        self.movestoapple = 0

        return self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake_pos
        # Wall collision
        if pt[0] >= self.width or pt[0] < 0 or pt[1] >= self.height or pt[1] < 0:
            return True
        # Self collision
        elif pt in self.snake_body[1:]:
            return True
        return False

if __name__ == '__main__':
    game = SnakeGame()
    action = 1
    # Game loop
    while True:
        Reward, game_over, score = game.play_step(action)
        if game_over:
            Reward = -10
            game.reset()

    print('Final Score:', score)
    pygame.quit()
