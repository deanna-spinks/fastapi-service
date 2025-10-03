_next_id = 1


def get_next_id() -> int:
    global _next_id
    _next_id += 1
    return _next_id - 1
