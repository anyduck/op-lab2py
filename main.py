#!/usr/bin/python
from pathlib import Path
from collections import namedtuple


InputLine = namedtuple('InputLine', ['surname', 'rating', 'is_contractor'])
OutputLine = namedtuple('OutputLine', ['surname', 'rating_avg'])


def list2input_line(line: list) -> InputLine:
    """ Конвертує список вхідних даних в InputLine. """

    def flag2bool(flag: str) -> bool:
        """ Перетворює текстовий флаг в булеву змінну. """

        if flag.lower() in ('true', 'yes'):
            return True
        if flag.lower() in ('false', 'no'):
            return False
        raise ValueError(f'Невідомий флаг {flag}')

    surname: str = line[0]
    rating: tuple = tuple(int(r) for r in line[1:5])
    is_contractor: bool = flag2bool(line[6])

    return InputLine(surname, rating, is_contractor)


def find_csv(folder: Path) -> list[Path]:
    """ Повертає список всіх *.csv файлів в теці. """

    return [path for path in folder.iterdir()
            if path.is_file() and path.suffix == '.csv']


def csv2list(path: Path) -> list[InputLine]:
    """ Конвертує вміст csv в список InputLine-ів. """

    result = []
    with open(path, 'r') as csv:
        for line in csv.readlines()[1:]:  # Пропускаємо перший рядок
            result.append(list2input_line(line.rstrip('\n').split(',')))
    return result


def multiple_csv2list(files: list[Path]) -> list[InputLine]:
    """ Об'єднує декілька csv в список InputLine-ів. """

    result = []

    for file in files:
        result += csv2list(file)
    return result


def calc_scholarship_average_rating(table: list[InputLine]) -> list[OutputLine]:
    """ Обчислює середній бал студентів б'юджетників. """

    def average(rating):
        return round(sum(rating) / len(rating), 3)

    return [OutputLine(student.surname, average(student.rating))
            for student in table if not student.is_contractor]


def calc_stipend(table: list[OutputLine]) -> list[OutputLine]:
    table = sorted(table, key=lambda x: x.rating_avg, reverse=True)
    limit = int(len(table) * 0.4)
    return table[:limit]


def main(folder: Path, output: Path) -> None:
    files = find_csv(folder)
    table = multiple_csv2list(files)
    scholarship_table = calc_scholarship_average_rating(table)
    stipend_table = calc_stipend(scholarship_table)
    print(f'Мінімальний рейтинг для стипендії становить: {stipend_table[-1].rating_avg}')
    print(stipend_table)


if __name__ == '__main__':
    folder = Path(input('Введіть теку з фалами: '))
    main(folder, output=Path('rating.csv'))
