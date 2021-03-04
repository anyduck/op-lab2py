#!/usr/bin/python
from argparse import ArgumentParser, Namespace
from pathlib import Path
from collections import namedtuple

from csv import multiple_csv2table, table2csv


InputLine = namedtuple('InputLine', ['surname', 'rating', 'is_contractor'])
OutputLine = namedtuple('OutputLine', ['surname', 'rating_avg'])


def main():
    args = parse_args()
    table = load_table(args.folder)

    stipend_table = calc_stipend(table)
    print(f'Мінімальний рейтинг для стипендії становить: {stipend_table[-1].rating_avg}')

    save_table(stipend_table, args.output)


def parse_args() -> Namespace:
    parser = ArgumentParser(description='Process rating csv files')
    parser.add_argument('folder', type=Path,
                        help='folder with csv files')
    parser.add_argument('-o', '--output', type=Path,
                        default=Path('rating.csv'),
                        help='path to the final csv file')

    return parser.parse_args()


def load_table(folder: Path) -> list[InputLine]:
    files = find_csv(folder)
    table = multiple_csv2table(files)

    return [list2input_line(row) for row in table]


def find_csv(folder: Path) -> list[Path]:
    """ Повертає список всіх *.csv файлів в теці. """

    return [path for path in folder.iterdir()
            if path.is_file() and path.suffix == '.csv']


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
    rating: tuple = tuple(int(r) for r in line[1:6])
    is_contractor: bool = flag2bool(line[6])

    return InputLine(surname, rating, is_contractor)


def calc_stipend(table: list[InputLine]) -> list[OutputLine]:
    """ Обчислює список студентів, що отримають спипендію. """

    def average(rating):
        return round(sum(rating) / len(rating), 3)

    table = [OutputLine(student.surname, average(student.rating))
             for student in table if not student.is_contractor]

    table = sorted(table, key=lambda x: x.rating_avg, reverse=True)
    limit = int(len(table) * 0.4)

    return table[:limit]


def save_table(table: list[OutputLine], path: Path) -> None:
    converted = [output_line2list(row) for row in table]
    table2csv(converted, path)


def output_line2list(line: OutputLine) -> list[str]:
    """ Конвертує кінцевий OuptupLine в список. """

    return [str(x) for x in line]


if __name__ == '__main__':
    main()
