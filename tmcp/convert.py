from typing import List, Any


def try_convert_direction(direction: Any) -> List[float]:
    """Attempts to convert any type into a list of 3 floats."""
    # Convert from objects that store their coordinates in a data attribute.
    if hasattr(direction, "data"):
        direction = direction.data

    # Convert any indexable into a list, so that length can be changed if needed.
    if hasattr(direction, "__getitem__"):
        direction = list(direction)

    # Convert from objects with have x, y, z attributes.
    elif hasattr(direction, "x"):
        new_dir = [direction.x]
        if hasattr(direction, "y"):
            new_dir.append(direction.y)
            if hasattr(direction, "z"):
                new_dir.append(direction.z)
        direction = new_dir

    if isinstance(direction, list):
        l = len(direction)
        # Pad with zeroes.
        if l < 3:
            direction.extend([0.0] * (3 - l))
        # Take the first three numbers.
        elif l > 3:
            direction = direction[:3]

        # Try converting all to floats.
        for index, axis in enumerate(direction):
            try:
                direction[index] = float(axis)
            except:
                direction[index] = 0.0
    else:
        direction = [0.0, 0.0, 0.0]

    return direction
