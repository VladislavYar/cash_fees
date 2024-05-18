
def max_len_status(statuses):
    """Определяет максимальную длину статуса."""
    max_len = 0
    for status in statuses:
        len_status = len(status[0])
        if len_status > max_len:
            max_len = len_status
    return max_len
