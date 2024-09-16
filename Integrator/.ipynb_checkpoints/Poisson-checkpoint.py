# Integrator/Poisson.py

import torch
import torch.nn as nn
import numpy as np
from Differentiator.FiniteDifference import FiniteDifference  # Absolute import from Differentiator package

class Poisson(nn.Module):
    """
    Computes Poisson terms based on the vector field using finite difference filters.
    
    Args:
        channel_size (int): Number of input channels for each vector component.
        cd_filter_1d (np.array): 1D filter for finite difference (e.g., np.array([-1.0, 1.0])).
        padding (str): Padding mode. "SYMMETRIC" in TensorFlow corresponds to "reflect" in PyTorch.
    """
    def __init__(self, channel_size=1, cd_filter_1d=np.array([-1.0, 1.0]), padding_mode="SYMMETRIC"):
        super(Poisson, self).__init__()
        self.cdiff = FiniteDifference(channel_size, cd_filter_1d, padding_mode)

    def forward(self, vector_field):
        """
        Forward pass to compute Poisson terms from the vector field.
        
        Args:
            vector_field (list or tuple of torch.Tensor): 
                - vector_field[0]: Tensor of shape [N, C, H, W] representing the first component (e.g., y-component).
                - vector_field[1]: Tensor of shape [N, C, H, W] representing the second component (e.g., x-component).
        
        Returns:
            ux2 (torch.Tensor): Element-wise square of the x-derivative of the first component, shape [N, C, H-1, W-1]
            vy2 (torch.Tensor): Element-wise square of the y-derivative of the second component, shape [N, C, H-1, W-1]
            uyvx (torch.Tensor): Element-wise product of the y-derivative of the first component and the x-derivative of the second component, shape [N, C, H-1, W-1]
        """
        # Compute derivatives for the first component
        uy, ux = self.cdiff(vector_field[0])  # uy: d/dy of first component, ux: d/dx of first component
        
        # Compute derivatives for the second component
        vy, vx = self.cdiff(vector_field[1])  # vy: d/dy of second component, vx: d/dx of second component
        
        # Compute Poisson terms
        ux2 = ux * ux       # Element-wise square of ux
        vy2 = vy * vy       # Element-wise square of vy
        uyvx = uy * vx      # Element-wise product of uy and vx
        
        return ux2, vy2, uyvx