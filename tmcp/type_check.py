from typing import get_type_hints


def type_check(func):
    hints = get_type_hints(func)
    args_names = func.__code__.co_varnames[:func.__code__.co_argcount]

    def type_checked_func(*args, **kwargs):
        for arg, hint in hints.items():
            # We don't care about the type of the return value.
            if arg == "return":
                continue
            # Get the value of the argument.
            try:
                x = kwargs.get(arg, None)
                if not x:   
                    x = args[args_names.index(arg)]
            except IndexError:
                continue
            # Check if type matches the hint.
            if not isinstance(x, hint):
                raise TypeError(f"{arg} is {type(x)} but expected {hint}")
            
        return func(*args, **kwargs)

    return type_checked_func
