def check_nim(nim_list: list, target: str):
    if target in nim_list:
        return f"{target} sudah terdaftar di sistem", True
    return "", False


def total_average(models, Avg):
    return models.aggregate(Avg('score'))
