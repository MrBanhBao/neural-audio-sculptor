import torch


def create_direction_vector(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Checks if vector 'a' has passed vector 'b' using the dot product method.

    Args:
    - a (torch.Tensor): The first vector.
    - b (torch.Tensor): The second vector, must have the same shape as 'a'.

    Returns:
    - torch.Tensor: normalized direction vector with a length of 1 (unit vector).
    """
    d = b - a

    # normalize direction vector
    return d / torch.norm(d)


def has_passed(a: torch.Tensor, b: torch.Tensor, d: torch.Tensor) -> bool:
    """
    Checks if vector 'a' has passed vector 'b' using the dot product method.

    Args:
    - a (torch.Tensor): The first vector.
    - b (torch.Tensor): The second vector, must have the same shape as 'a'.
    - d (torch.Tensor): The direction vector from 'a' to 'b', must have the same shape as 'a'.

    Returns:
    - bool: True if 'a' has passed 'b', False otherwise.
    """
    # Compute the dot product between (b - a) and (d - a)
    dot_product = torch.sum((b - a) * d)

    # Return True if dot product is non-negative, indicating 'a' has passed 'b'
    return dot_product < 0