from typing import Iterable

import numpy as np
import torch

from cca_zoo.deepmodels import objectives
from cca_zoo.deepmodels.dcca import DCCA
from cca_zoo.models import MCCA


class DCCA_NOI(DCCA):
    """
    A class used to fit a DCCA model by non-linear orthogonal iterations

    """

    def __init__(self, latent_dims: int, N: int,
                 encoders=None,
                 r: float = 0, rho: float = 0.2, eps: float = 1e-3, shared_target: bool = False):
        """
        Constructor class for DCCA

        :param latent_dims: # latent dimensions
        :param N: # samples used to estimate covariance
        :param encoders: list of encoder networks
        :param r: regularisation parameter of tracenorm CCA like ridge CCA
        :param rho: covariance memory like DCCA non-linear orthogonal iterations paper
        :param eps: epsilon used throughout
        :param shared_target: not used
        """
        super().__init__(latent_dims=latent_dims, encoders=encoders,
                         r=r, eps=eps)
        self.N = N
        self.covs = None
        if rho < 0 or rho > 1:
            raise ValueError(f"rho should be between 0 and 1. rho={rho}")
        self.eps = eps
        self.rho = rho
        self.shared_target = shared_target
        self.mse = torch.nn.MSELoss()

    def forward(self, *args):
        z = self.encode(*args)
        return z

    def encode(self, *args):
        z = []
        for i, encoder in enumerate(self.encoders):
            z.append(encoder(args[i]))
        return tuple(z)

    def loss(self, *args):
        z = self(*args)
        self.update_covariances(*z)
        covariance_inv = [objectives._compute_matrix_power(objectives._minimal_regularisation(cov, self.eps), -0.5) for
                          cov in self.covs]
        preds = [torch.matmul(z, covariance_inv[i]).detach() for i, z in enumerate(z)]
        loss = self.mse(z[0], preds[1]) + self.mse(z[1], preds[0])
        return loss

    def update_covariances(self, *args):
        b = args[0].shape[0]
        batch_covs = [self.N * z_i.T @ z_i / b for i, z_i in enumerate(args)]
        if self.covs is not None:
            self.covs = [(self.rho * self.covs[i]).detach() + (1 - self.rho) * batch_cov for i, batch_cov
                         in
                         enumerate(batch_covs)]
        else:
            self.covs = batch_covs

    def post_transform(self, *z_list, train=False) -> Iterable[np.ndarray]:
        if train:
            self.cca = MCCA(latent_dims=self.latent_dims)
            self.cca.fit(*z_list)
            z_list = self.cca.transform(*z_list)
        else:
            z_list = self.cca.transform(*z_list)
        return z_list
