# pip install gymnasium matplotlib

import gymnasium as gym, numpy as np, matplotlib.pyplot as plt

class QLearningAgent:
    def __init__(self, state_size, action_size, n_bins=8):
        self.n_bins = n_bins
        self.bins   = [
            np.linspace(-4.8,  4.8,  n_bins),
            np.linspace(-4.0,  4.0,  n_bins),
            np.linspace(-0.42, 0.42, n_bins),
            np.linspace(-4.0,  4.0,  n_bins),
        ]
        self.q_table  = np.zeros([n_bins]*state_size + [action_size])
        self.alpha    = 0.1
        self.gamma    = 0.99
        self.epsilon  = 1.0
        self.eps_min  = 0.01
        self.eps_decay= 0.995

    def discretize(self, state):
        idx = [np.digitize(state[i], self.bins[i]) - 1 for i in range(len(state))]
        return tuple(max(0, min(self.n_bins-1, i)) for i in idx)

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(2)
        return np.argmax(self.q_table[self.discretize(state)])

    def learn(self, state, action, reward, next_state, done):
        s, s_ = self.discretize(state), self.discretize(next_state)
        q_cur = self.q_table[s][action]
        q_tgt = reward if done else reward + self.gamma * np.max(self.q_table[s_])
        self.q_table[s][action] += self.alpha * (q_tgt - q_cur)

    def decay_epsilon(self):
        self.epsilon = max(self.eps_min, self.epsilon * self.eps_decay)


env     = gym.make("CartPole-v1")
agent   = QLearningAgent(state_size=4, action_size=2, n_bins=8)
rewards = []

for episode in range(500):
    state, _ = env.reset()
    total    = 0
    for step in range(500):
        action = agent.choose_action(state)
        next_state, reward, done, truncated, _ = env.step(action)
        if done: reward = -10
        agent.learn(state, action, reward, next_state, done)
        state = next_state
        total += 1
        if done or truncated: break
    agent.decay_epsilon()
    rewards.append(total)
    if episode % 50 == 0:
        avg = np.mean(rewards[-50:])
        print(f"에피소드 {episode:4d}  avg={avg:.1f}  ε={agent.epsilon:.3f}")

env.close()
