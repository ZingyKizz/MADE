from gym import make
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import Adam
import random


INITIAL_STEPS = 1024
TRANSITIONS = 500000
STEPS_PER_UPDATE = 4
STEPS_PER_TARGET_UPDATE = STEPS_PER_UPDATE * 1000


class DeepQNetwork(nn.Module):
    HIDDEN_LAYER_SIZE = 64
    LEARNING_RATE = 5e-4

    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.fc1 = nn.Linear(state_dim, self.HIDDEN_LAYER_SIZE)
        self.fc2 = nn.Linear(self.HIDDEN_LAYER_SIZE, self.HIDDEN_LAYER_SIZE)
        self.fc3 = nn.Linear(self.HIDDEN_LAYER_SIZE, action_dim)
        self.optimizer = Adam(self.parameters(), lr=self.LEARNING_RATE)
        self.loss = nn.MSELoss()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def forward(self, states):
        x = self.fc1(states)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        actions = self.fc3(x)
        return actions


class DQN:
    BUFFER_MAXSIZE = 10 ** 5
    BATCH_SIZE = 128
    GAMMA = 0.99

    def __init__(self, state_dim, action_dim):
        self.steps = 0  # Do not change
        self.model = DeepQNetwork(state_dim, action_dim)

        self.state_buffer = np.zeros(
            (self.BUFFER_MAXSIZE, self.model.state_dim), dtype=np.float32
        )
        self.action_buffer = np.zeros(self.BUFFER_MAXSIZE, dtype=np.int32)
        self.next_state_buffer = np.zeros(
            (self.BUFFER_MAXSIZE, self.model.state_dim), dtype=np.float32
        )
        self.reward_buffer = np.zeros(self.BUFFER_MAXSIZE, dtype=np.float32)
        self.terminal_buffer = np.zeros(self.BUFFER_MAXSIZE, dtype=np.bool)
        self.buffer_size = 0

    def update_buffer_size(self):
        self.buffer_size += 1

    def consume_transition(self, transition):
        # Add transition to a replay buffer.
        # Hint: use deque with specified maxlen. It will remove old experience automatically.
        state, action, next_state, reward, done = transition
        idx = self.buffer_size % self.BUFFER_MAXSIZE
        self.state_buffer[idx] = state
        self.action_buffer[idx] = action
        self.next_state_buffer[idx] = next_state
        self.reward_buffer[idx] = reward
        self.terminal_buffer[idx] = done
        self.update_buffer_size()

    def sample_batch(self):
        # Sample batch from a replay buffer.
        # Hints:
        # 1. Use random.randint
        # 2. Turn your batch into a numpy.array before turning it to a Tensor. It will work faster
        if self.buffer_size < self.BATCH_SIZE:
            return
        idxs = np.random.choice(
            np.arange(min(self.buffer_size, self.BUFFER_MAXSIZE)),
            size=self.BATCH_SIZE,
            replace=False,
        )

        state_batch = torch.Tensor(self.state_buffer[idxs]).to(self.model.device)
        action_batch = self.action_buffer[idxs]
        next_state_batch = torch.Tensor(self.next_state_buffer[idxs]).to(
            self.model.device
        )
        reward_batch = torch.Tensor(self.reward_buffer[idxs]).to(self.model.device)
        terminal_batch = torch.BoolTensor(self.terminal_buffer[idxs]).to(
            self.model.device
        )

        return state_batch, action_batch, next_state_batch, reward_batch, terminal_batch

    def train_step(self, batch):
        # Use batch to update DQN's network.
        (
            state_batch,
            action_batch,
            next_state_batch,
            reward_batch,
            terminal_batch,
        ) = batch
        batch_idx = np.arange(self.BATCH_SIZE)

        self.model.optimizer.zero_grad()

        q_eval = self.model(state_batch)[batch_idx, action_batch]
        q_next = self.model(next_state_batch)
        q_next[terminal_batch] = 0.0
        q_target = reward_batch + self.GAMMA * torch.max(q_next, dim=1).values

        loss = self.model.loss(q_target, q_eval).to(self.model.device)
        loss.backward()
        self.model.optimizer.step()

    def update_target_network(self):
        # Update weights of a target Q-network here. You may use copy.deepcopy to do this or
        # assign a values of network parameters via PyTorch methods.
        pass

    @torch.no_grad()
    def act(self, state, target=False):
        # Compute an action. Do not forget to turn state to a Tensor and then turn an action to a numpy array.
        state = torch.Tensor([state]).to(self.model.device)
        actions = self.model(state)
        action = torch.argmax(actions).item()
        return action

    def update(self, transition):
        # You don't need to change this
        self.consume_transition(transition)
        if self.steps % STEPS_PER_UPDATE == 0:
            batch = self.sample_batch()
            self.train_step(batch)
        if self.steps % STEPS_PER_TARGET_UPDATE == 0:
            self.update_target_network()
        self.steps += 1

    def save(self):
        torch.save(self.model.state_dict(), "model.pt")


def evaluate_policy(agent, episodes=5):
    env = make("LunarLander-v2")
    returns = []
    for _ in range(episodes):
        done = False
        state = env.reset()
        total_reward = 0.0

        while not done:
            state, reward, done, _ = env.step(agent.act(state))
            total_reward += reward
        returns.append(total_reward)
    return returns


def main():
    env = make("LunarLander-v2")
    dqn = DQN(state_dim=env.observation_space.shape[0], action_dim=env.action_space.n)
    eps = 0.1
    state = env.reset()
    for _ in range(INITIAL_STEPS):
        action = env.action_space.sample()

        next_state, reward, done, _ = env.step(action)
        dqn.consume_transition((state, action, next_state, reward, done))

        state = next_state if not done else env.reset()
    max_reward = -np.inf
    for i in range(TRANSITIONS):
        # Epsilon-greedy policy
        if random.random() < eps:
            action = env.action_space.sample()
        else:
            action = dqn.act(state)

        next_state, reward, done, _ = env.step(action)
        dqn.update((state, action, next_state, reward, done))

        state = next_state if not done else env.reset()

        if (i + 1) % (TRANSITIONS // 100) == 0:
            rewards = evaluate_policy(dqn, 5)
            mean_reward = np.mean(rewards)
            print(
                f"Step: {i + 1}, Reward mean: {mean_reward}, Reward std: {np.std(rewards)}"
            )
            if mean_reward > max_reward:
                dqn.save()
                max_reward = mean_reward


if __name__ == "__main__":
    main()
