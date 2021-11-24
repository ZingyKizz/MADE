import random
import numpy as np
import os
import torch
try:
    from train import Actor
except ModuleNotFoundError:
    from .train import Actor


class Agent:
    def __init__(self):
        self.model = torch.load(__file__[:-8] + "/actor.pkl")

    @torch.no_grad()
    def act(self, state):
        state = torch.tensor(np.array(state)).float()
        action = self.model(state)
        return action.cpu().numpy()

    def reset(self):
        pass