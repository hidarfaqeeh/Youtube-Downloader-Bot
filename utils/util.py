def humanbytes(size):
    # يحول البايتات لوحدة أسهل للقراءة (KB, MB, GB)
    if not size:
        return ""
    power = 2**10
    n = 0
    labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {labels[n]}"
