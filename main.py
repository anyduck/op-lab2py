#!/usr/bin/python
from argparse import ArgumentParser, Namespace
from pathlib import Path
from collections import namedtuple

from csv import multiple_csv2table, table2csv
from student import Student


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


def load_table(folder: Path) -> list[Student]:
    """ Відктриває всі CSV файли в папці як таблицю студентів. """

    files = find_csv(folder)
    table = multiple_csv2table(files)

    return [Student.from_list(row) for row in table]


def find_csv(folder: Path) -> list[Path]:
    """ Повертає список всіх *.csv файлів в теці. """

    return [path for path in folder.iterdir()
            if path.is_file() and path.suffix == '.csv']


def calc_stipend(table: list[Student]) -> list[Student]:
    """ Обчислює список студентів, що отримають спипендію. """

    budget = [student for student in table if not student.is_contractor]

    budget.sort(key=lambda student: student.rating_avg, reverse=True)
    limit = int(len(budget) * 0.4)

    return budget[:limit]


def save_table(table: list[Student], path: Path) -> None:
    """ Зберігає таблицю студентів в CSV. """

    converted = [student.to_rating_list() for student in table]
    table2csv(converted, path)


if __name__ == '__main__':
    main()
