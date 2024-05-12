import math

import torch
import torch.nn.functional as F

import core.transformations.py3d_tools as p3d

device = 'cpu'
if torch.cuda.is_available():
    device = torch.device('cuda')
print(f'GeoMetrixTransform; Torch is running with: {device}.')


def transform_2D(tensor: torch.Tensor, rotate_angle: float = 0, translate_x: float = 0, translate_y: float = 0,
                 scale_x: float = 1,
                 scale_y: float = 1, padding_mode: str = "zeros") -> torch.Tensor:
    tensor.to(device)
    angle = torch.tensor(rotate_angle)
    # in pixels
    # tx = 2 * (translate_x / width)
    # ty = 2 * (translate_y / height)

    theta = torch.deg2rad(angle)  # Rotation angle in radians
    sx = torch.tensor(scale_x)  # Scaling factor along x-axis
    sy = torch.tensor(scale_y)  # Scaling factor along y-axis
    dx = torch.tensor(translate_x)  # Translation along x-axis
    dy = torch.tensor(translate_y)  # Translation along y-axis

    # Define affine matrix
    affine_matrix = torch.tensor([
        [sx * torch.cos(theta), -torch.sin(theta), dx],
        [torch.sin(theta), sy * torch.cos(theta), dy]], device=device)

    # Generate grid
    grid = F.affine_grid(affine_matrix.unsqueeze(0), tensor.size(), align_corners=True)
    # Apply affine transformation using grid_sample with border control
    tensor = F.grid_sample(tensor, grid, padding_mode=padding_mode)  # "border", "reflection", "zeros"
    return tensor


def transform_3D(tensor: torch.Tensor, rotate_x: float = 0, rotate_y: float = 0, rotate_z: float = 0,
                 translate_x: float = 0, translate_y: float = 0,
                 translate_z: float = 0, padding_mode: str = "zeros") -> torch.Tensor:
    ASPECT_RATIO = 1
    NEAR = 1
    FAR = -1
    FOV = 2

    batch, channel, height, width = tensor.size()
    depth = height

    # rotation values
    rotate_xyz = [
        math.radians(rotate_y),
        math.radians(rotate_x),
        math.radians(rotate_z)
    ]
    # rotation matrix
    rot_mat = p3d.euler_angles_to_matrix(torch.tensor(rotate_xyz, device=device), "XYZ").unsqueeze(0)

    # translation values
    TRANSLATION_SCALE_X = 1.0 / (height / 10)
    TRANSLATION_SCALE_Y = 1.0 / (width / 10)
    TRANSLATION_SCALE = 1.0 / (depth / 10)
    translate = [
        -translate_x * TRANSLATION_SCALE_X,
        translate_y * TRANSLATION_SCALE_Y,
        -translate_z * TRANSLATION_SCALE
    ]

    cam_old = p3d.FoVPerspectiveCameras(NEAR, FAR, ASPECT_RATIO, fov=FOV, degrees=True, device=device)
    cam_new = p3d.FoVPerspectiveCameras(NEAR, FAR, ASPECT_RATIO, fov=FOV, degrees=True, R=rot_mat,
                                        T=torch.tensor([translate]), device=device)

    y, x = torch.meshgrid(torch.linspace(-1., 1., height, device=device),
                          torch.linspace(-1., 1., width, device=device))
    z = torch.ones_like(x)

    xyz_world_points = torch.stack((x.flatten(), y.flatten(), z.flatten()), dim=1)

    xyz_old_cam_points = cam_old.get_full_projection_transform().transform_points(xyz_world_points)
    xyz_new_cam_points = cam_new.get_full_projection_transform().transform_points(xyz_world_points)

    xy_old_cam_points = xyz_old_cam_points[:, 0:2]
    xy_new_cam_points = xyz_new_cam_points[:, 0:2]
    xy_offset_points = xy_new_cam_points - xy_old_cam_points

    # affine_grid theta param expects a batch of 2D mats. Each is 2x3 to do rotation+translation.
    identity_2d_batch = torch.tensor([[1., 0., 0.],
                                      [0., 1., 0.]], device=device).unsqueeze(0)

    coords_2d = F.affine_grid(identity_2d_batch, [batch, channel, height, width], align_corners=False)
    offset_coords_2d = coords_2d - torch.reshape(xy_offset_points, (height, width, 2)).unsqueeze(0)

    tensor = F.grid_sample(tensor, offset_coords_2d, padding_mode=padding_mode)  # "border", "reflection", "zeros"

    return tensor
