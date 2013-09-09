def has_type_handler(obj, handlers):
    return isinstance(obj, tuple(handlers.keys()))


def get_type_handler(obj, handlers):
    for type_, handler in handlers.items():
        if isinstance(obj, type_):
            return handler
