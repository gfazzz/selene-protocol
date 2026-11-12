"""toolkit/scan.py — поиск нарушений в потоке показаний. Эталон s01e03."""


def first_out_of_range(values, low, high):
    for index, value in enumerate(values):
        if not low <= value <= high:
            return index
    return None


def count_out_of_range(values, low, high):
    count = 0
    for value in values:
        if value < low or value > high:
            count += 1
    return count


def first_gap(numbers):
    position = 1
    while position < len(numbers):
        expected = numbers[position - 1] + 1
        if numbers[position] != expected:
            return expected
        position += 1
    return None
