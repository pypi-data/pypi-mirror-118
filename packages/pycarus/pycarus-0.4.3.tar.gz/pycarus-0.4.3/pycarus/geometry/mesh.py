from typing import Tuple

import numpy as np
import torch
from skimage.measure import marching_cubes  # type: ignore
from torch import nn


@torch.no_grad()  # type: ignore
def sdf_to_mesh(
    mlp: nn.Module,
    grid_size: int = 256,
    max_batch: int = 100_000,
) -> Tuple[np.ndarray, np.ndarray]:
    """Obtain the mesh corresponding to the 3D shape whose SDF
    is contained in the input MLP.

    Args:
        mlp: The MLP representing the 3D shape SDF.
        grid_size: The SDF sampling resolution. Defaults to 256.
        max_batch: The max batch size used to query the input MLP. Defaults to 100_000.

    Returns:
        - The vertices of the computed mesh as numpy array.
        - The faces of the computed mesh as numpy array.
    """
    voxel_origin = [-1, -1, -1]
    voxel_size = 2.0 / (grid_size - 1)

    overall_index = torch.arange(0, grid_size ** 3, 1)
    coords = torch.zeros(grid_size ** 3, 4)

    coords[:, 2] = overall_index % grid_size
    coords[:, 1] = (overall_index.long() / grid_size) % grid_size
    coords[:, 0] = ((overall_index.long() / grid_size) / grid_size) % grid_size

    coords[:, 0] = (coords[:, 0] * voxel_size) + voxel_origin[2]
    coords[:, 1] = (coords[:, 1] * voxel_size) + voxel_origin[1]
    coords[:, 2] = (coords[:, 2] * voxel_size) + voxel_origin[0]

    num_samples = grid_size ** 3
    start = 0

    while start < num_samples:
        end = min(start + max_batch, num_samples)
        coords_subset = coords[start:end, :3].cuda()
        sdf = mlp(coords_subset).cpu()
        coords[start:end, 3] = sdf
        start += max_batch

    sdf = coords[:, 3].reshape(grid_size, grid_size, grid_size)

    verts, faces, _, _ = marching_cubes(sdf.numpy(), level=0.0, spacing=[voxel_size] * 3)

    return verts, faces
