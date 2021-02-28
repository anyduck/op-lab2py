#!/usr/bin/python
from pathlib import Path
from collections import namedtuple

from csv import multiple_csv2table, table2csv


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


def output_line2list(line: OutputLine) -> list[str]:
    """ Конвертує кінцевий OuptupLine в список. """

    return [str(x) for x in line]


def find_csv(folder: Path) -> list[Path]:
    """ Повертає список всіх *.csv файлів в теці. """

    return [path for path in folder.iterdir()
            if path.is_file() and path.suffix == '.csv']


def load_table(folder: Path) -> list[InputLine]:
    files = find_csv(folder)
    table = multiple_csv2table(files)

    return [list2input_line(row) for row in table]


def calc_scholarship_average_rating(table: list[InputLine]) -> list[OutputLine]:
    """ Обчислює середній бал студентів б'юджетників. """

    def average(rating):
        return round(sum(rating) / len(rating), 3)

    return [OutputLine(student.surname, average(student.rating))
            for student in table if not student.is_contractor]


def calc_stipend(table: list[OutputLine]) -> list[OutputLine]:
    """ Обчислює список студентів, що отримають спипендію. """

    table = sorted(table, key=lambda x: x.rating_avg, reverse=True)
    limit = int(len(table) * 0.4)

    return table[:limit]


def save_table(table: list[OutputLine], path: Path) -> None:
    converted = [output_line2list(row) for row in table]
    table2csv(converted, path)


def main(folder: Path, output: Path) -> None:
    table = load_table(folder)
    scholarship_table = calc_scholarship_average_rating(table)
    stipend_table = calc_stipend(scholarship_table)
    print(f'Мінімальний рейтинг для стипендії становить: {stipend_table[-1].rating_avg}')
    save_table(stipend_table, output)


if __name__ == '__main__':
    folder = Path(input('Введіть теку з фалами: '))
    main(folder, output=Path('rating.csv'))
