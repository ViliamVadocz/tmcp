from typing import List, Any


def try_convert_direction(direction: Any) -> List[float]:
    """
    Attempts to convert any type into a list of 3 floats.
    Will raise a TypeError if the type is not something it can convert.
    It expects two or three coordinates (it will take z to be 0.0 if not specified).
    """
    # Convert from objects that store their coordinates in a data attribute.
    if hasattr(direction, "data"):
        direction = direction.data

    # Convert any indexable into a list, so that length can be changed if needed.
    if hasattr(direction, "__getitem__"):
        direction = list(direction)

    # Convert from objects with have x, y, z attributes.
    elif hasattr(direction, "x") and hasattr(direction, "y"):
        new_dir = [direction.x, direction.y]
        if hasattr(direction, "z"):
            new_dir.append(direction.z)
        direction = new_dir

    if isinstance(direction, list):
        if len(direction) == 2:
            direction.append(0.0)
        if len(direction) == 3:
            # Convert all to floats.
            for index, axis in enumerate(direction):
                direction[index] = float(axis)
            return direction

    raise TypeError("Could not convert direction")
