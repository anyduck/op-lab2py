from pathlib import Path


def csv2table(path: Path) -> list[list[str]]:
    """ Конвертує вміст csv в двовимірний список. """

    result = []
    with open(path, 'r') as csv:
        for row in csv.readlines()[1:]:  # Пропускаємо перший рядок
            result.append(row.rstrip('\n').split(','))
    return result


def multiple_csv2table(files: list[Path]) -> list[list[str]]:
    """ Об'єднує декілька csv в двовимірний список. """

    result = []
    for file in files:
        result += csv2table(file)
    return result


def table2csv(table: list[list[str]], path: Path) -> None:
    """ Зберігає двовимірний список в csv. """

    with open(path, 'w') as csv:
        for row in table:
            csv.write(','.join(row) + '\n')
