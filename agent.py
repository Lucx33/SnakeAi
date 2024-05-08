import torch
import random
import numpy as np
from collections import deque
from mygame import SnakeGame
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
N_GAMES = 2000
MODEL_NAME = 'test'

LR = 0.001

Load = True



class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.initial_epsilon = float(60)
        self.min_epsilon = 0
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(14, 256, 3)
        if Load:
            model_path = './model/'+MODEL_NAME+'.pth'
            try:
                self.model.load_state_dict(torch.load(model_path))
                print("Loaded model from", model_path)
            except FileNotFoundError:
                print("Saved model not found. Starting with a fresh model.")
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake_pos
        point_l10 = [head[0] - 10, head[1]]
        point_r10 = [head[0] + 10, head[1]]
        point_u10 = [head[0], head[1] - 10]
        point_d10 = [head[1], head[1] + 10]

        point_l01 = [head[0] - 1, head[1]]
        point_r01 = [head[0] + 1, head[1]]
        point_u01 = [head[1], head[1] - 1]
        point_d01 = [head[1], head[1] + 1]

        dir_l = game.direction == 'LEFT'
        dir_r = game.direction == 'RIGHT'
        dir_u = game.direction == 'UP'
        dir_d = game.direction == 'DOWN'

        state = [
            # Danger straight in 10 units
            (dir_r and game.is_collision(point_r10)) or
            (dir_l and game.is_collision(point_l10)) or
            (dir_u and game.is_collision(point_u10)) or
            (dir_d and game.is_collision(point_d10)),

            # Danger right in 10 units
            (dir_u and game.is_collision(point_r10)) or
            (dir_d and game.is_collision(point_l10)) or
            (dir_l and game.is_collision(point_u10)) or
            (dir_r and game.is_collision(point_d10)),

            # Danger left in 10 units
            (dir_d and game.is_collision(point_r10)) or
            (dir_u and game.is_collision(point_l10)) or
            (dir_r and game.is_collision(point_u10)) or
            (dir_l and game.is_collision(point_d10)),

            # Perigo imediato à frente
            (dir_r and game.is_collision(point_r01)) or
            (dir_l and game.is_collision(point_l01)) or
            (dir_u and game.is_collision(point_u01)) or
            (dir_d and game.is_collision(point_d01)),

            # Perigo imediato à direita
            (dir_u and game.is_collision(point_r01)) or
            (dir_d and game.is_collision(point_l01)) or
            (dir_l and game.is_collision(point_u01)) or
            (dir_r and game.is_collision(point_d01)),

            # Perigo imediato à esquerda
            (dir_d and game.is_collision(point_r01)) or
            (dir_u and game.is_collision(point_l01)) or
            (dir_r and game.is_collision(point_u01)) or
            (dir_l and game.is_collision(point_d01)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food_pos[0] < game.snake_pos[0],  # food left
            game.food_pos[0] > game.snake_pos[0],  # food right
            game.food_pos[1] < game.snake_pos[1],  # food up
            game.food_pos[1] > game.snake_pos[1]  # food down
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        for state, action, reward, next_state, done in mini_sample:
            self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = max(float(self.min_epsilon), self.initial_epsilon * (0.96 ** self.n_games) - 0.5)
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
    def train(self):
        plot_scores = []
        plot_mean_scores = []
        plot_avg_moves_to_apple = []
        plot_mean_avg_moves_to_apple = []
        total_score = 0
        record = 0
        moves = 0
        agent = Agent()
        game = SnakeGame()
        while True:
            moves += 1
            # get old state
            state_old = agent.get_state(game)

            # get move
            final_move = agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = game.play_step(final_move)
            state_new = agent.get_state(game)

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            agent.remember(state_old, final_move, reward, state_new, done)

            # train long memory, plot result
            if done:
                game.reset()
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                if score > 0:
                    avg_moves_to_apple = moves / score
                    moves = 0
                else:
                    avg_moves_to_apple = 0
                plot_avg_moves_to_apple.append(avg_moves_to_apple)
                plot_mean_avg_moves_to_apple.append(sum(plot_avg_moves_to_apple)/agent.n_games)
                plot(plot_scores, plot_mean_scores, plot_avg_moves_to_apple, plot_mean_avg_moves_to_apple, MODEL_NAME)

                if agent.n_games == N_GAMES:
                    break


if __name__ == '__main__':
    agent = Agent()  # Create an instance of Agent
    agent.train()
