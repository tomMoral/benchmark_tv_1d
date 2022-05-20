from benchopt import BaseDataset
from benchopt import safe_import_context

with safe_import_context() as import_ctx:
    import numpy as np


class Dataset(BaseDataset):

    name = "Simulated sinusoidal"

    # List of parameters to generate the datasets. The benchmark will consider
    # the cross product for each key in the dictionary.
    # cos + bruit ~ N(mu, sigma)
    parameters = {
        'sigma': [0.1],
        'mu': [0],
        'K': [500],
        'len_output': [400],
        'type_A': ['identity', 'random_square', 'random_nonsquare']}

    def __init__(self, mu=0, sigma=0.3, K=10, len_output=5,
                 type_A='identity', random_state=27):
        # Store the parameters of the dataset
        self.mu = mu
        self.sigma = sigma
        self.K, self.len_output = K, len_output
        self.type_A = type_A
        self.random_state = random_state

    def set_A(self, rng):
        if self.type_A == 'random_square':
            A = rng.randn(self.K, self.K)
        elif self.type_A == 'random_nonsquare':
            A = rng.randn(self.K, self.len_output)
        else:
            A = np.identity(self.K)
        return A

    def get_data(self):
        t = np.arange(self.K)
        rng = np.random.RandomState(47)
        w = np.cos(np.pi*t/self.K*10)
        y = self.A @ w + rng.normal(self.mu, self.sigma, self.K)
        data = dict(A=self.set_A(rng), y=y)

        return data
